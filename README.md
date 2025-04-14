# Vector Space Search System

A sophisticated document search engine built with Flask and React that implements the Vector Space Model with TF-IDF weighting for efficient and accurate information retrieval. This system allows users to upload text documents, manage stopwords, and perform semantic searches with relevance scoring.

## DEMO VIDEO

[![Project Demo Video](https://img.youtube.com/vi/ahWYop10nA0/0.jpg)](https://www.youtube.com/watch?v=ahWYop10nA0)


*Click the image above to watch the full demo video*

## Screenshots

![Screenshot From 2025-04-14 21-45-53](https://github.com/user-attachments/assets/dbc66d3a-9cac-4f84-b8f8-21fcf9480276)

![Screenshot From 2025-04-14 21-46-00](https://github.com/user-attachments/assets/e0f653da-9d57-415f-bf39-7163414cf6d3)

![Screenshot From 2025-04-14 21-46-26](https://github.com/user-attachments/assets/2f64e498-1c1b-434d-b245-7a9020d0899e)

![Screenshot From 2025-04-14 21-46-31](https://github.com/user-attachments/assets/811957e4-769a-4014-8864-ea8789ef2d25)


## Features


- **Vector Space Model Implementation** - Semantic search with TF-IDF weighting
- **Cosine Similarity Scoring** - Relevance-based document ranking
- **Stopwords Management** - Customize stopword filtering
- **Interactive Document Viewer** - View full document content
- **Virtualized Document List** - Efficient handling of large document collections
- **Responsive UI Design** - Works on desktop and mobile devices

## How It Works

The system uses the Vector Space Model (VSM) with TF-IDF weighting to represent both documents and queries as vectors in a high-dimensional space:

1. **Term Frequency (TF)** - Measures how frequently a term occurs in a document
2. **Inverse Document Frequency (IDF)** - Measures how important a term is across all documents
3. **TF-IDF Weighting** - Combines TF and IDF to score term importance
4. **Cosine Similarity** - Measures the angle between document and query vectors

This approach enables the system to return documents ranked by their semantic relevance to the query, not just keyword matching.

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

## 🛠️ Installation

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install flask flask-cors nltk
```

3. Create required directory:
```bash
mkdir uploads
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the Flask backend:
```bash
python app.py
```
The server will start at http://localhost:5000

2. In a new terminal, start the React frontend:
```bash
cd frontend
npm start
```
Access the application at http://localhost:3000

## Usage Guide

### Stopwords Management

1. Create a text file with stopwords (one per line):
```
a
an
the
of
in
on
```

2. Upload via the "Upload Stopwords File" button
3. The system automatically applies stopwords filtering during search

### Document Upload

1. Click "Choose Files" button
2. Select one or more .txt files to upload
3. Documents are immediately processed and indexed

### Vector Space Search

1. Type your search query in the search box
2. Click "Search" or press Enter
3. Results are displayed in order of relevance score (0-1)
4. Click on any result to view the full document content

## Vector Space Model Details

### Document Indexing Process

1. **Text Tokenization** - Documents are tokenized into individual words
2. **Stopword Removal** - Common stopwords are filtered out
3. **Lemmatization** - Terms are reduced to their base form
4. **TF-IDF Calculation** - Term weights are calculated for each document
5. **Document Vector Normalization** - Vectors are normalized for cosine similarity

### Search Query Processing

1. **Query Tokenization** - Search terms are extracted and processed
2. **Query Weighting** - TF-IDF weights are calculated for query terms
3. **Vector Comparison** - Query vector is compared to document vectors
4. **Similarity Scoring** - Documents are ranked by cosine similarity score
5. **Result Ranking** - Results are presented in descending order of relevance

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload-stopwords` | POST | Upload a stopwords file |
| `/upload` | POST | Upload documents |
| `/search` | POST | Perform vector space search |
| `/document/<doc_id>` | GET | Get document content |
| `/clear` | POST | Clear all documents and indexes |
| `/status` | GET | Get system status |

## Technical Implementation

### Backend (Flask)

- **Document Processing** - Tokenization, stopword removal, and lemmatization
- **Index Building** - Creation of inverted and forward indexes
- **TF-IDF Calculation** - Document and term weight calculation
- **Cosine Similarity** - Vector space model implementation for search

### Frontend (React)

- **Modern UI** - Clean, responsive interface using Tailwind CSS
- **Real-time Updates** - Instant feedback on operations
- **Document Virtualization** - Efficient rendering of large document lists
- **Modal Document Viewer** - Full-text document viewing
- **Pagination** - Both document list and search results are paginated

## Troubleshooting

If you encounter issues:

1. Check if both servers are running
2. Verify uploads directory permissions
3. Check browser console and server logs for error messages
4. Ensure all dependencies are installed
5. Try clearing indexes and restarting

## Development Notes

- Uses Flask for the backend API
- React with Tailwind CSS for the frontend
- Uses NLTK for natural language processing
- Memory-efficient indexing with optimized data structures
- Implements the complete Vector Space Model algorithm

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request
