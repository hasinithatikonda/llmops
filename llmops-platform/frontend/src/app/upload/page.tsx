'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import Navbar from '@/components/Navbar';
import api from '@/lib/api';
import { Upload as UploadIcon, File, FileText, MessageSquare, CheckCircle2, AlertCircle, Sparkles, Search, Activity, Clock, Database, TrendingUp } from 'lucide-react';

interface RAGMetrics {
  totalUploads: number;
  totalQueries: number;
  avgQueryLatency: number;
  totalDocuments: number;
  lastActivity: string;
}

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [querying, setQuerying] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [queryLatency, setQueryLatency] = useState<number>(0);
  const [uploadCount, setUploadCount] = useState<number>(0);
  const [queryCount, setQueryCount] = useState<number>(0);
  const [avgLatency, setAvgLatency] = useState<number>(0);
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
    
    // Fetch available models
    const fetchModels = async () => {
      try {
        const response = await api.get('/models');
        setAvailableModels(response.data);
      } catch (error) {
        console.error('Failed to fetch models:', error);
      }
    };
    fetchModels();
    
    // Fetch RAG metrics from API (user-specific)
    const fetchRAGMetrics = async () => {
      try {
        const response = await api.get('/metrics/rag');
        setUploadCount(response.data.total_uploads || 0);
        setQueryCount(response.data.total_queries || 0);
        setAvgLatency(response.data.avg_query_latency || 0);
      } catch (error) {
        console.error('Failed to fetch RAG metrics:', error);
        // Fallback to zeros for new users
        setUploadCount(0);
        setQueryCount(0);
        setAvgLatency(0);
      }
    };
    fetchRAGMetrics();
  }, [router]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
      } else {
        alert('Please upload a PDF file');
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadSuccess(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload/pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 5000);
      alert(`PDF uploaded successfully! ${response.data.pages} pages, ${response.data.chunks} chunks`);
      setFile(null);
      
      // Refresh metrics from API
      const metricsResponse = await api.get('/metrics/rag');
      setUploadCount(metricsResponse.data.total_uploads || 0);
      setQueryCount(metricsResponse.data.total_queries || 0);
      setAvgLatency(metricsResponse.data.avg_query_latency || 0);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to upload PDF');
    } finally {
      setUploading(false);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setQuerying(true);
    const startTime = performance.now();
    
    try {
      const result = await api.post('/upload/query', null, {
        params: { 
          query, 
          n_results: 3,
          model: selectedModel 
        },
      });
      const endTime = performance.now();
      const latency = endTime - startTime;
      
      setResponse(result.data.response);
      setQueryLatency(latency);
      
      // Refresh metrics from API
      const metricsResponse = await api.get('/metrics/rag');
      setUploadCount(metricsResponse.data.total_uploads || 0);
      setQueryCount(metricsResponse.data.total_queries || 0);
      setAvgLatency(metricsResponse.data.avg_query_latency || 0);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to query documents');
    } finally {
      setQuerying(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="container mx-auto px-6 py-10 max-w-5xl">
        {/* Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-bold gradient-text mb-2 flex items-center space-x-3">
            <FileText className="h-10 w-10" />
            <span>Document RAG</span>
          </h1>
          <p className="text-gray-600">Upload documents and query them with AI-powered semantic search</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="card p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Upload PDF</h2>
              <UploadIcon className="h-6 w-6 text-blue-500" />
            </div>
            
            <form onSubmit={handleUpload}>
              <div 
                className={`mb-6 relative transition-all duration-200 ${
                  dragActive ? 'scale-105' : ''
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <label className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-200 ${
                  dragActive 
                    ? 'border-blue-500 bg-blue-50' 
                    : file 
                    ? 'border-green-500 bg-green-50' 
                    : 'border-gray-300 bg-gradient-to-br from-gray-50 to-white hover:border-blue-400 hover:bg-blue-50'
                }`}>
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    {file ? (
                      <>
                        <CheckCircle2 className="h-16 w-16 text-green-500 mb-4 animate-bounce" />
                        <p className="text-sm font-semibold text-green-700 mb-2">{file.name}</p>
                        <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                        <p className="text-xs text-gray-500 mt-2">Click to change file</p>
                      </>
                    ) : (
                      <>
                        <div className="mb-4 relative">
                          <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur-xl opacity-30"></div>
                          <div className="relative bg-gradient-to-br from-blue-50 to-purple-50 p-4 rounded-2xl">
                            <File className="h-12 w-12 text-blue-600" />
                          </div>
                        </div>
                        <p className="text-sm font-semibold text-gray-700 mb-2">
                          {dragActive ? 'Drop your PDF here' : 'Click to upload or drag and drop'}
                        </p>
                        <p className="text-xs text-gray-500">PDF files up to 10MB</p>
                      </>
                    )}
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
              
              {uploadSuccess && (
                <div className="mb-4 p-4 bg-green-50 border-2 border-green-200 rounded-xl flex items-center space-x-3 animate-slide-up">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  <span className="text-sm font-medium text-green-700">Document uploaded and indexed successfully!</span>
                </div>
              )}
              
              <button
                type="submit"
                disabled={!file || uploading}
                className="btn-primary w-full group relative overflow-hidden"
              >
                <span className="relative z-10 flex items-center justify-center space-x-2">
                  <UploadIcon className="h-5 w-5" />
                  <span>{uploading ? 'Uploading...' : 'Upload & Process'}</span>
                </span>
              </button>
            </form>
          </div>

          {/* Query Section */}
          <div className="card p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Ask Questions</h2>
              <MessageSquare className="h-6 w-6 text-purple-500" />
            </div>
            
            {/* Model Selector */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-3 flex items-center space-x-2">
                <Sparkles className="h-4 w-4 text-purple-500" />
                <span>Select AI Model</span>
              </label>
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl bg-white hover:border-purple-400 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200 font-medium"
              >
                {availableModels.map((model) => (
                  <option key={model.id} value={model.id}>
                    {model.name}
                  </option>
                ))}
              </select>
              {availableModels.find(m => m.id === selectedModel) && (
                <div className="mt-2 flex items-center justify-between text-xs">
                  <span className="text-gray-500">
                    {availableModels.find(m => m.id === selectedModel)?.description}
                  </span>
                  <span className="font-semibold text-purple-600">
                    {availableModels.find(m => m.id === selectedModel)?.speed} speed
                  </span>
                </div>
              )}
            </div>
            
            <form onSubmit={handleQuery} className="mb-6">
              <div className="relative mb-4">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question about your documents..."
                  className="input pl-12"
                />
              </div>
              <button
                type="submit"
                disabled={querying || !query.trim()}
                className="btn-secondary w-full group relative overflow-hidden"
              >
                <span className="relative z-10 flex items-center justify-center space-x-2">
                  <Sparkles className="h-5 w-5" />
                  <span>{querying ? 'Searching...' : 'Query with AI'}</span>
                </span>
              </button>
            </form>

            {/* Response Display */}
            {response ? (
              <div className="animate-slide-up">
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-6 border-2 border-blue-100 mb-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                      <Sparkles className="h-4 w-4 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-900">AI Response</h3>
                  </div>
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap mb-4">{response}</p>
                  
                  {/* Performance Metrics */}
                  <div className="flex items-center space-x-4 pt-4 border-t border-blue-200 flex-wrap">
                    <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-white rounded-lg border border-blue-200">
                      <Clock className="h-3.5 w-3.5 text-blue-500" />
                      <span className="text-xs font-semibold text-gray-700">{queryLatency.toFixed(0)}ms</span>
                    </div>
                    <div className="badge-blue text-xs">
                      {selectedModel.split('/').pop()?.split('-').slice(0, 3).join(' ').toUpperCase()}
                    </div>
                    <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-white rounded-lg border border-green-200">
                      <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
                      <span className="text-xs font-semibold text-gray-700">RAG Query</span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="mb-4 relative inline-block">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full blur-2xl opacity-20"></div>
                  <div className="relative bg-gradient-to-br from-gray-50 to-white p-6 rounded-3xl border-2 border-gray-100">
                    <MessageSquare className="h-12 w-12 text-gray-400 mx-auto" />
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">No queries yet</h3>
                <p className="text-sm text-gray-500">Upload a document and start asking questions!</p>
              </div>
            )}
          </div>
        </div>

        {/* Info Cards */}
        <div className="grid md:grid-cols-3 gap-6 mt-10">
          <div className="card p-6 hover:shadow-medium transition-all duration-200">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center mb-4 shadow-sm">
              <UploadIcon className="h-6 w-6 text-white" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Upload Documents</h3>
            <p className="text-sm text-gray-600">Drag & drop PDF files or click to browse. Files are processed automatically.</p>
          </div>
          
          <div className="card p-6 hover:shadow-medium transition-all duration-200">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center mb-4 shadow-sm">
              <Search className="h-6 w-6 text-white" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Semantic Search</h3>
            <p className="text-sm text-gray-600">AI-powered search finds relevant information across all your documents.</p>
          </div>
          
          <div className="card p-6 hover:shadow-medium transition-all duration-200">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mb-4 shadow-sm">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Context-Aware</h3>
            <p className="text-sm text-gray-600">Get accurate answers with full context from your document library.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
