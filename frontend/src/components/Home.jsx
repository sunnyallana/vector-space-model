import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Search, Code, Zap, FileText, Filter } from "lucide-react";

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 pt-20 pb-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">
            Document Search System
          </h1>
          <p className="text-xl text-gray-300 mb-10 leading-relaxed">
            A high-performance document search system using vector space model
            with TF-IDF weighting. Find documents based on semantic similarity
            to your query, ranked by relevance. This implementation features a
            Flask API backend with efficient cosine similarity calculations.
          </p>
          <Link
            to="/search"
            className="inline-flex items-center px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl text-lg font-semibold"
          >
            Start Searching
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <h2 className="text-2xl md:text-3xl font-bold text-center mb-12 text-blue-300">
          Powerful Search Capabilities
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 shadow-lg border border-gray-700 hover:border-blue-500 transition-all group">
            <div className="h-12 w-12 bg-blue-900 rounded-lg flex items-center justify-center mb-5 group-hover:bg-blue-700 transition-colors">
              <Search className="h-6 w-6 text-blue-300" />
            </div>
            <h3 className="text-xl font-semibold text-blue-200 mb-3">
              Semantic Search
            </h3>
            <p className="text-gray-300">
              Find documents based on conceptual relevance using our vector
              space model with TF-IDF weighting and cosine similarity scoring.
            </p>
          </div>

          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 shadow-lg border border-gray-700 hover:border-blue-500 transition-all group">
            <div className="h-12 w-12 bg-blue-900 rounded-lg flex items-center justify-center mb-5 group-hover:bg-blue-700 transition-colors">
              <Zap className="h-6 w-6 text-blue-300" />
            </div>
            <h3 className="text-xl font-semibold text-blue-200 mb-3">
              Relevance Ranking
            </h3>
            <p className="text-gray-300">
              Results are automatically ranked by relevance score, showing you
              the most conceptually similar documents first.
            </p>
          </div>

          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 shadow-lg border border-gray-700 hover:border-blue-500 transition-all group">
            <div className="h-12 w-12 bg-blue-900 rounded-lg flex items-center justify-center mb-5 group-hover:bg-blue-700 transition-colors">
              <FileText className="h-6 w-6 text-blue-300" />
            </div>
            <h3 className="text-xl font-semibold text-blue-200 mb-3">
              Document Indexing
            </h3>
            <p className="text-gray-300">
              Upload your documents and let our system automatically build
              vector representations for fast similarity searches.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
