from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import math
from collections import defaultdict, Counter
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
CORS(app)

# Initialize text processing
nltk.download('wordnet', quiet=True)
word_lemmatizer = WordNetLemmatizer()

# Global variables for indexes
inverted_index = defaultdict(lambda: {'document_frequency': 0, 'document_postings': defaultdict(int)})
forward_index = defaultdict(lambda: {'term_frequencies': Counter(), 'normalization_value': 0.0})
stopwords = set()
documents_directory = 'uploads'
os.makedirs(documents_directory, exist_ok=True)


# Read stopwords from a file into a set
def load_stopwords(stopword_file_path):
    with open(stopword_file_path, 'r') as file:
        return {line.strip() for line in file}


# Read text from file using multiple encoding attempts
def read_file_with_encoding_fallback(file_path):
    supported_encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    for encoding in supported_encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    return None

# Convert text to lowercase word tokens
def generate_word_tokens(input_text):
    return re.findall(r'\w+', input_text.lower())


# Clean and lemmatize tokens
def process_and_lemmatize_tokens(word_tokens, stopwords):
    filtered_tokens = []
    for token in word_tokens:
        if token not in stopwords:
            filtered_tokens.append(word_lemmatizer.lemmatize(token))
    return filtered_tokens

# Construct search indices from document collection
def build_indices():
    global inverted_index, forward_index
    inverted_index = defaultdict(lambda: {'document_frequency': 0, 'document_postings': defaultdict(int)})
    forward_index = defaultdict(lambda: {'term_frequencies': Counter(), 'normalization_value': 0.0})
    total_documents = 0

    for filename in os.listdir(documents_directory):
        if not filename.endswith('.txt'):
            continue

        document_id = os.path.splitext(filename)[0]
        full_file_path = os.path.join(documents_directory, filename)

        file_content = read_file_with_encoding_fallback(full_file_path)
        if file_content is None:
            print(f"Skipping unreadable file: {filename}")
            continue

        # Process document content
        raw_tokens = generate_word_tokens(file_content)
        processed_terms = process_and_lemmatize_tokens(raw_tokens, stopwords)
        term_frequency_counter = Counter(processed_terms)

        # Update forward index
        forward_index[document_id]['term_frequencies'] = term_frequency_counter

        # Update inverted index
        encountered_terms = set()
        for term, frequency in term_frequency_counter.items():
            inverted_index[term]['document_postings'][document_id] = frequency
            if term not in encountered_terms:
                inverted_index[term]['document_frequency'] += 1
                encountered_terms.add(term)

        total_documents += 1

    # Calculate inverse document frequencies
    for term in inverted_index:
        document_frequency = inverted_index[term]['document_frequency']
        inverted_index[term]['idf'] = math.log(total_documents / document_frequency) if document_frequency else 0

    # Calculate document normalization values
    for document_id in forward_index:
        squared_weight_sum = 0.0
        for term, frequency in forward_index[document_id]['term_frequencies'].items():
            term_idf = inverted_index[term]['idf']
            squared_weight_sum += (frequency * term_idf) ** 2
        forward_index[document_id]['normalization_value'] = math.sqrt(squared_weight_sum)

    return {
        'message': f'Index built with {total_documents} documents',
        'document_count': total_documents,
        'unique_terms': len(inverted_index)
    }

# Search Stopwords Endpoint
@app.route('/upload-stopwords', methods=['POST'])
def upload_stopwords():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file or not file.filename.endswith('.txt'):
        return jsonify({'error': 'Invalid file format'}), 400

    try:
        global stopwords
        content = file.read().decode('utf-8', errors='ignore')
        stopwords = {line.strip() for line in content.splitlines() if line.strip()}
        return jsonify({
            'message': 'Stopwords uploaded successfully',
            'count': len(stopwords)
        })
    except Exception as error:
        return jsonify({'error': f'Error processing stopwords: {str(error)}'}), 500

# Upload Documents Endpoint
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'}), 400

    uploaded_files = request.files.getlist('files[]')
    if not uploaded_files:
        return jsonify({'error': 'No files selected'}), 400

    results = []
    errors = []

    for file in uploaded_files:
        if file and file.filename.endswith('.txt'):
            try:
                filename = os.path.join(documents_directory, file.filename)
                file.save(filename)
                results.append({
                    'name': file.filename,
                    'doc_id': os.path.splitext(file.filename)[0]
                })
            except Exception as error:
                errors.append(f"Error saving {file.filename}: {str(error)}")
        else:
            if file.filename:
                errors.append(f"Invalid file type: {file.filename}")

    # Rebuild indices after upload
    build_result = build_indices()

    return jsonify({
        'message': 'Files uploaded successfully',
        'processed': len(results),
        'errors': errors,
        'results': results,
        'index_stats': build_result
    })

# Search Endpoint
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Empty query'}), 400

    try:
        # Process and weight query terms
        query_tokens = generate_word_tokens(query)
        search_terms = process_and_lemmatize_tokens(query_tokens, stopwords)
        weighted_query_terms = {}
        for term, count in Counter(search_terms).items():
            if term in inverted_index:
                weighted_query_terms[term] = count * inverted_index[term]['idf']

        # Find candidate documents
        candidate_documents = set()
        for term in weighted_query_terms:
            if term in inverted_index:
                candidate_documents.update(inverted_index[term]['document_postings'].keys())

        # Score documents using cosine similarity
        ranked_documents = []
        for document_id in candidate_documents:
            # Calculate dot product
            dot_product = 0.0
            document_term_freqs = forward_index[document_id]['term_frequencies']

            for term, query_weight in weighted_query_terms.items():
                if term in document_term_freqs:
                    term_freq = document_term_freqs[term]
                    term_idf = inverted_index[term]['idf']
                    doc_term_weight = term_freq * term_idf
                    dot_product += query_weight * doc_term_weight

            # Calculate similarity
            document_norm = forward_index[document_id]['normalization_value']
            query_norm = math.sqrt(sum(w**2 for w in weighted_query_terms.values())) or 1.0

            if document_norm != 0:
                similarity = dot_product / (query_norm * document_norm)
                if similarity >= 0.001:  # Threshold to filter very weak matches
                    ranked_documents.append({
                        'doc_id': document_id,
                        'score': similarity,
                        'name': f"{document_id}.txt"
                    })

        # Sort by score descending
        ranked_documents.sort(key=lambda x: -x['score'])

        return jsonify({
            'results': ranked_documents,
            'query': query
        })
    except Exception as error:
        return jsonify({'error': f'Search error: {str(error)}'}), 500


# Retrieve Document Endpoint
@app.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        filename = f"{doc_id}.txt"
        filepath = os.path.join(documents_directory, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'Document not found'}), 404

        content = read_file_with_encoding_fallback(filepath)
        if content is None:
            return jsonify({'error': 'Could not read document content'}), 500

        return jsonify({
            'doc_id': doc_id,
            'name': filename,
            'content': content
        })
    except Exception as error:
        return jsonify({'error': f'Could not retrieve document: {str(error)}'}), 500

# Clear Indexes Endpoint
@app.route('/clear', methods=['POST'])
def clear_indexes():
    try:
        global inverted_index, forward_index
        inverted_index = defaultdict(lambda: {'document_frequency': 0, 'document_postings': defaultdict(int)})
        forward_index = defaultdict(lambda: {'term_frequencies': Counter(), 'normalization_value': 0.0})

        # Remove all files in uploads directory
        for filename in os.listdir(documents_directory):
            file_path = os.path.join(documents_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return jsonify({
            'message': 'Cleared all documents and search indexes',
            'remaining_files': len(os.listdir(documents_directory))
        })
    except Exception as error:
        return jsonify({'error': f'Cleanup failed: {str(error)}'}), 500

# Status Endpoint
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'document_count': len(forward_index),
        'unique_terms': len(inverted_index),
        'stopwords_count': len(stopwords)
    })

if __name__ == '__main__':
    app.run(debug=True)
