'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import Navbar from '@/components/Navbar';
import api from '@/lib/api';
import { MetricsSummary, UsageMetrics, ModelMetrics, EvaluationMetrics } from '@/types';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Activity, Users, Clock, AlertTriangle, DollarSign, Star, TrendingUp, Zap, Database, Award, Upload, Search, FileText } from 'lucide-react';

interface RAGMetrics {
  totalUploads: number;
  totalQueries: number;
  avgQueryLatency: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<MetricsSummary | null>(null);
  const [usage, setUsage] = useState<UsageMetrics[]>([]);
  const [models, setModels] = useState<ModelMetrics[]>([]);
  const [evaluation, setEvaluation] = useState<EvaluationMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [ragMetrics, setRagMetrics] = useState<RAGMetrics>({ totalUploads: 0, totalQueries: 0, avgQueryLatency: 0 });

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
      return;
    }

    fetchDashboardData();
  }, [router]);

  const fetchDashboardData = async () => {
    try {
      // Fetch available models first
      const modelsListRes = await api.get('/models');
      setAvailableModels(modelsListRes.data);
      
      const [summaryRes, usageRes, modelsRes, evalRes, ragRes] = await Promise.all([
        api.get<MetricsSummary>(`/metrics/summary?model=${selectedModel}`),
        api.get<UsageMetrics[]>('/metrics/usage'),
        api.get<ModelMetrics[]>('/metrics/models'),
        api.get<EvaluationMetrics>('/metrics/evaluation'),
        api.get('/metrics/rag'),
      ]);

      setSummary(summaryRes.data);
      setUsage(usageRes.data);
      setModels(modelsRes.data);
      setEvaluation(evalRes.data);
      
      // Set RAG metrics from API
      setRagMetrics({
        totalUploads: ragRes.data.total_uploads || 0,
        totalQueries: ragRes.data.total_queries || 0,
        avgQueryLatency: ragRes.data.avg_query_latency || 0
      });
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Refetch summary when model changes
  useEffect(() => {
    if (selectedModel && availableModels.length > 0) {
      const fetchSummary = async () => {
        try {
          const summaryRes = await api.get<MetricsSummary>(`/metrics/summary?model=${selectedModel}`);
          setSummary(summaryRes.data);
        } catch (error) {
          console.error('Failed to fetch summary:', error);
        }
      };
      fetchSummary();
    }
  }, [selectedModel]);

  // Get tokens for selected model
  const getTokensForModel = (modelId: string) => {
    console.log('Looking for model:', modelId);
    console.log('Available models:', models);
    const modelMetrics = models.find(m => m.model === modelId);
    console.log('Found model metrics:', modelMetrics);
    
    if (modelMetrics) {
      return modelMetrics.tokens.toLocaleString();
    }
    
    // If no data yet for this model, return 0
    return '0';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="container mx-auto px-6 py-10">
        {/* Header */}
        <div className="mb-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold gradient-text mb-2">Analytics Dashboard</h1>
              <p className="text-gray-600">Monitor your LLM application performance in real-time</p>
            </div>
            <div className="flex flex-col items-end">
              <label className="text-sm font-medium text-gray-700 mb-2">
                Model for Max Tokens:
              </label>
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="px-4 py-2 border-2 border-gray-200 rounded-xl bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 font-medium"
              >
                {availableModels.map((model) => (
                  <option key={model.id} value={model.id}>
                    {model.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard
            title="Total Requests"
            value={(summary?.total_requests || 0).toLocaleString()}
            icon={Activity}
            gradient="from-blue-500 to-blue-600"
            trend="+12.5%"
          />
          <StatCard
            title="Active Models"
            value={(summary?.active_models || 0).toLocaleString()}
            icon={Users}
            gradient="from-green-500 to-green-600"
            trend="+8.2%"
          />
          <StatCard
            title="Avg Latency"
            value={`${summary?.average_latency.toFixed(0) || 0}ms`}
            icon={Zap}
            gradient="from-yellow-500 to-yellow-600"
            trend="-5.3%"
          />
          <StatCard
            title="Error Rate"
            value={`${summary?.error_rate.toFixed(1) || 0}%`}
            icon={AlertTriangle}
            gradient="from-red-500 to-red-600"
            trend="-2.1%"
          />
        </div>

        {/* Additional Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <MetricCard
            title={`Tokens (${selectedModel.split('/').pop()?.split('-').slice(0, 3).join(' ') || 'Current Model'})`}
            value={getTokensForModel(selectedModel)}
            icon={Database}
            iconColor="from-purple-500 to-purple-600"
            subtitle={`Tokens used by this model`}
          />
          <MetricCard
            title="Total Cost"
            value={`$${summary?.total_cost.toFixed(4) || 0}`}
            icon={DollarSign}
            iconColor="from-emerald-500 to-emerald-600"
            subtitle="Last 7 days"
          />
          <MetricCard
            title={`Max Tokens (${selectedModel.split('/').pop()?.split('-').slice(0, 3).join(' ') || 'Current Model'})`}
            value={(summary?.max_tokens || 0).toLocaleString()}
            icon={Star}
            iconColor="from-amber-500 to-amber-600"
            subtitle="Current model limit"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
          {/* Usage Trends */}
          <div className="card p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Usage Trends</h2>
                <p className="text-gray-500 text-sm">Daily request volume and latency</p>
              </div>
              <TrendingUp className="h-6 w-6 text-green-500" />
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={usage}>
                <defs>
                  <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" stroke="#6b7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                <Tooltip contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb', borderRadius: '12px' }} />
                <Legend />
                <Area type="monotone" dataKey="requests" stroke="#3b82f6" fill="url(#colorRequests)" strokeWidth={2} name="Requests" />
                <Line type="monotone" dataKey="avg_latency" stroke="#10b981" strokeWidth={2} name="Latency (ms)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Model Performance */}
          <div className="card p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Model Performance</h2>
                <p className="text-gray-500 text-sm">Comparison across models</p>
              </div>
              <Award className="h-6 w-6 text-purple-500" />
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={models}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="model" stroke="#6b7280" style={{ fontSize: '11px' }} angle={-20} textAnchor="end" />
                <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                <Tooltip contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="requests" fill="url(#blueGradient)" radius={[8, 8, 0, 0]} name="Requests" />
                <Bar dataKey="avg_latency" fill="url(#greenGradient)" radius={[8, 8, 0, 0]} name="Latency (ms)" />
                <defs>
                  <linearGradient id="blueGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#3b82f6" />
                    <stop offset="100%" stopColor="#2563eb" />
                  </linearGradient>
                  <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" />
                    <stop offset="100%" stopColor="#059669" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Model Token Usage Comparison */}
        <div className="card p-8 mb-10">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Token Usage by Model</h2>
              <p className="text-gray-500 text-sm mt-1">Compare which models consume more tokens per request</p>
            </div>
            <Database className="h-8 w-8 text-purple-500" />
          </div>
          
          {/* Model Comparison Cards - Improved */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            {models.map((model, index) => {
              const modelName = model.model.split('/').pop()?.replace(/-/g, ' ').toUpperCase() || model.model;
              const avgTokensPerRequest = model.requests > 0 ? Math.round(model.tokens / model.requests) : 0;
              const maxModel = models.reduce((max, m) => 
                (m.requests > 0 && (m.tokens / m.requests) > (max.tokens / (max.requests || 1))) ? m : max
              , models[0]);
              const isMax = model.model === maxModel.model && model.requests > 0;
              
              const colors = [
                { bg: 'bg-blue-500', lightBg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-600' },
                { bg: 'bg-purple-500', lightBg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-600' },
                { bg: 'bg-pink-500', lightBg: 'bg-pink-50', border: 'border-pink-200', text: 'text-pink-600' }
              ];
              const color = colors[index % colors.length];
              
              return (
                <div 
                  key={model.model}
                  className={`relative ${color.lightBg} rounded-2xl border-2 ${color.border} p-6 hover:shadow-xl transition-all duration-300 ${
                    isMax ? 'ring-4 ring-yellow-400 shadow-2xl' : 'shadow-md'
                  }`}
                >
                  {isMax && (
                    <div className="absolute -top-4 -right-4 w-14 h-14 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-xl z-10">
                      <Star className="h-7 w-7 text-white fill-white drop-shadow-lg" />
                    </div>
                  )}
                  
                  <div className="text-center">
                    <div className={`inline-flex items-center justify-center w-16 h-16 ${color.bg} rounded-2xl shadow-lg mb-4`}>
                      <Database className="h-9 w-9 text-white" />
                    </div>
                    
                    <h3 className={`text-xs font-bold uppercase tracking-wider ${color.text} mb-4`}>
                      {modelName}
                    </h3>
                    
                    <div className="mb-6">
                      <div className="text-5xl font-bold text-gray-900 mb-2">
                        {avgTokensPerRequest}
                      </div>
                      <p className="text-sm text-gray-600 font-medium">Avg tokens/request</p>
                    </div>
                    
                    <div className="space-y-3 bg-white bg-opacity-60 rounded-xl p-4">
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-600 font-medium">Total Tokens:</span>
                        <span className="text-sm font-bold text-gray-900">{model.tokens.toLocaleString()}</span>
                      </div>
                      <div className="w-full h-px bg-gray-300"></div>
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-600 font-medium">Requests:</span>
                        <span className="text-sm font-bold text-gray-900">{model.requests.toLocaleString()}</span>
                      </div>
                    </div>
                    
                    {isMax && model.requests > 0 && (
                      <div className="mt-4">
                        <span className="inline-flex items-center space-x-1 px-3 py-1.5 bg-gradient-to-r from-yellow-100 to-orange-100 border-2 border-yellow-400 rounded-full shadow-sm">
                          <Star className="h-3.5 w-3.5 text-yellow-600 fill-yellow-600" />
                          <span className="text-xs font-bold text-yellow-700">MOST TOKENS</span>
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Bar Chart - Cleaner Design */}
          <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl p-8 mb-8 border-2 border-purple-100">
            <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-md">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <span>Average Tokens per Request</span>
            </h3>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart 
                data={models.filter(m => m.requests > 0).map(m => ({
                  ...m,
                  avgTokens: Math.round(m.tokens / m.requests),
                  modelName: m.model.split('/').pop()?.split('-').slice(0, 2).join(' ').toUpperCase() || m.model
                }))}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#c7d2fe" vertical={false} />
                <XAxis 
                  dataKey="modelName" 
                  stroke="#4338ca" 
                  style={{ fontSize: '14px', fontWeight: '700' }}
                  tick={{ fill: '#4338ca' }}
                  height={80}
                />
                <YAxis 
                  stroke="#4338ca" 
                  style={{ fontSize: '13px', fontWeight: '600' }}
                  tick={{ fill: '#4338ca' }}
                  width={80}
                  label={{ 
                    value: 'Tokens per Request', 
                    angle: -90, 
                    position: 'insideLeft', 
                    style: { fontSize: '14px', fill: '#4338ca', fontWeight: '700' } 
                  }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '3px solid #8b5cf6', 
                    borderRadius: '16px',
                    boxShadow: '0 20px 25px rgba(139, 92, 246, 0.3)',
                    padding: '16px',
                    fontWeight: '600'
                  }}
                  labelStyle={{ 
                    fontWeight: 'bold', 
                    fontSize: '15px',
                    marginBottom: '8px',
                    color: '#4338ca'
                  }}
                  cursor={{ fill: 'rgba(139, 92, 246, 0.1)' }}
                  formatter={(value: any) => [
                    <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#7c3aed' }}>{value}</span>, 
                    'Tokens/Request'
                  ]}
                />
                <Bar 
                  dataKey="avgTokens" 
                  fill="url(#colorfulTokenGradient)" 
                  radius={[16, 16, 0, 0]}
                  maxBarSize={120}
                  label={{ 
                    position: 'top', 
                    fill: '#4338ca', 
                    fontSize: 16, 
                    fontWeight: 'bold',
                    formatter: (value: number) => value
                  }}
                />
                <defs>
                  <linearGradient id="colorfulTokenGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#a78bfa" />
                    <stop offset="50%" stopColor="#8b5cf6" />
                    <stop offset="100%" stopColor="#7c3aed" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
            
            {/* Quick Stats Below Chart */}
            <div className="grid grid-cols-3 gap-4 mt-6">
              {models.filter(m => m.requests > 0).map((model, idx) => {
                const avgTokens = Math.round(model.tokens / model.requests);
                const modelShort = model.model.split('/').pop()?.split('-').slice(0, 2).join(' ').toUpperCase();
                return (
                  <div key={model.model} className="bg-white rounded-xl p-4 shadow-md border border-purple-200">
                    <div className="text-xs font-bold text-purple-600 mb-1">{modelShort}</div>
                    <div className="text-2xl font-bold text-gray-900">{avgTokens}</div>
                    <div className="text-xs text-gray-500">tokens/req</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Insights Panel - Improved */}
          {models.filter(m => m.requests > 0).length > 0 && (
            <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-6 text-white shadow-xl">
              <div className="flex items-start space-x-4">
                <div className="w-14 h-14 bg-white bg-opacity-20 backdrop-blur-sm rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg">
                  <Activity className="h-7 w-7 text-white" />
                </div>
                <div className="flex-1">
                  <h4 className="text-xl font-bold mb-4">💡 Token Efficiency Insights</h4>
                  <div className="space-y-3 text-sm">
                    <div className="flex items-start space-x-2">
                      <span className="text-yellow-300 font-bold text-lg">•</span>
                      <p className="flex-1">
                        <span className="font-bold text-yellow-200">
                          {models.reduce((max, m) => 
                            (m.requests > 0 && (m.tokens / m.requests) > (max.tokens / (max.requests || 1))) ? m : max
                          , models[0]).model.split('/').pop()?.split('-').slice(0, 2).join(' ').toUpperCase()}
                        </span> uses the most tokens per request - best for complex tasks requiring detailed responses
                      </p>
                    </div>
                    <div className="flex items-start space-x-2">
                      <span className="text-green-300 font-bold text-lg">•</span>
                      <p className="flex-1">
                        <span className="font-bold text-green-200">
                          {models.reduce((min, m) => 
                            (m.requests > 0 && (m.tokens / m.requests) < (min.tokens / (min.requests || 1))) ? m : min
                          , models.find(m => m.requests > 0) || models[0]).model.split('/').pop()?.split('-').slice(0, 2).join(' ').toUpperCase()}
                        </span> is most token-efficient - ideal for fast, cost-effective simple queries
                      </p>
                    </div>
                    <div className="flex items-start space-x-2">
                      <span className="text-blue-300 font-bold text-lg">•</span>
                      <p className="flex-1">
                        <span className="font-bold">Pro Tip:</span> Use larger models for analysis and complex tasks, switch to smaller models for simple Q&A to reduce costs by up to 70%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* RAG Analytics Section - Combined with Chatbot */}
        <div className="card p-8 mb-10">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">RAG & Document Analytics</h2>
              <p className="text-gray-500 text-sm mt-1">Document processing and AI-powered semantic search performance</p>
            </div>
            <FileText className="h-8 w-8 text-indigo-500" />
          </div>

          {/* RAG Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Total Uploads */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border-2 border-blue-200 p-6 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center justify-between mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Upload className="h-7 w-7 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-blue-600 uppercase tracking-wide mb-1">Documents</p>
                  <p className="text-4xl font-bold text-gray-900">{ragMetrics.totalUploads}</p>
                </div>
              </div>
              <div className="space-y-2 bg-white bg-opacity-60 rounded-xl p-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Status:</span>
                  <span className="text-xs font-bold text-green-600">Processed</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Ready for:</span>
                  <span className="text-xs font-bold text-gray-900">Querying</span>
                </div>
              </div>
              <div className="mt-4">
                <div className="inline-flex items-center px-3 py-1.5 bg-blue-100 border border-blue-300 rounded-full">
                  <span className="text-xs font-bold text-blue-700">Total Uploaded</span>
                </div>
              </div>
            </div>

            {/* Total Queries */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border-2 border-purple-200 p-6 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center justify-between mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Search className="h-7 w-7 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-purple-600 uppercase tracking-wide mb-1">AI Queries</p>
                  <p className="text-4xl font-bold text-gray-900">{ragMetrics.totalQueries}</p>
                </div>
              </div>
              <div className="space-y-2 bg-white bg-opacity-60 rounded-xl p-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Type:</span>
                  <span className="text-xs font-bold text-purple-600">Semantic Search</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Powered by:</span>
                  <span className="text-xs font-bold text-gray-900">Vector DB</span>
                </div>
              </div>
              <div className="mt-4">
                <div className="inline-flex items-center px-3 py-1.5 bg-purple-100 border border-purple-300 rounded-full">
                  <span className="text-xs font-bold text-purple-700">RAG Queries</span>
                </div>
              </div>
            </div>

            {/* Average Latency */}
            <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl border-2 border-yellow-200 p-6 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center justify-between mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Clock className="h-7 w-7 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-yellow-600 uppercase tracking-wide mb-1">Avg Latency</p>
                  <p className="text-4xl font-bold text-gray-900">{ragMetrics.avgQueryLatency > 0 ? ragMetrics.avgQueryLatency.toFixed(0) : 0}<span className="text-2xl">ms</span></p>
                </div>
              </div>
              <div className="space-y-2 bg-white bg-opacity-60 rounded-xl p-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Performance:</span>
                  <span className="text-xs font-bold text-green-600">
                    {ragMetrics.avgQueryLatency < 1000 ? 'Excellent' : ragMetrics.avgQueryLatency < 2000 ? 'Good' : 'Fair'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-600 font-medium">Response:</span>
                  <span className="text-xs font-bold text-gray-900">Fast</span>
                </div>
              </div>
              <div className="mt-4">
                <div className="inline-flex items-center px-3 py-1.5 bg-yellow-100 border border-yellow-300 rounded-full">
                  <span className="text-xs font-bold text-yellow-700">Query Time</span>
                </div>
              </div>
            </div>
          </div>

          {/* Combined Analytics: Chatbot + RAG */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Comparison Bar */}
            <div className="bg-gradient-to-br from-gray-50 to-white rounded-2xl p-6 border-2 border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center space-x-2">
                <Activity className="h-5 w-5 text-blue-500" />
                <span>Chatbot vs RAG Usage</span>
              </h3>
              <div className="space-y-6">
                {/* Chatbot Requests */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">Chatbot Requests</span>
                    <span className="text-lg font-bold text-blue-600">{summary?.total_requests || 0}</span>
                  </div>
                  <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(((summary?.total_requests || 0) / Math.max((summary?.total_requests || 0) + ragMetrics.totalQueries, 1)) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>

                {/* RAG Queries */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">RAG Queries</span>
                    <span className="text-lg font-bold text-purple-600">{ragMetrics.totalQueries}</span>
                  </div>
                  <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-purple-600 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min((ragMetrics.totalQueries / Math.max((summary?.total_requests || 0) + ragMetrics.totalQueries, 1)) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>

                {/* Total Combined */}
                <div className="pt-4 border-t-2 border-gray-300">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-gray-900">Total Interactions</span>
                    <span className="text-2xl font-bold text-indigo-600">{(summary?.total_requests || 0) + ragMetrics.totalQueries}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Comparison */}
            <div className="bg-gradient-to-br from-gray-50 to-white rounded-2xl p-6 border-2 border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center space-x-2">
                <Zap className="h-5 w-5 text-yellow-500" />
                <span>Performance Comparison</span>
              </h3>
              <div className="space-y-6">
                {/* Chatbot Latency */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">Chatbot Latency</span>
                    <span className="text-lg font-bold text-blue-600">{summary?.average_latency.toFixed(0) || 0}ms</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full"
                        style={{ width: `${Math.min(((summary?.average_latency || 0) / 3000) * 100, 100)}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500">out of 3s</span>
                  </div>
                </div>

                {/* RAG Latency */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">RAG Query Latency</span>
                    <span className="text-lg font-bold text-purple-600">{ragMetrics.avgQueryLatency.toFixed(0)}ms</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-purple-400 to-purple-600 rounded-full"
                        style={{ width: `${Math.min((ragMetrics.avgQueryLatency / 3000) * 100, 100)}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500">out of 3s</span>
                  </div>
                </div>

                {/* Winner Badge */}
                <div className="pt-4 border-t-2 border-gray-300">
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-3">
                    <div className="flex items-center space-x-2">
                      <Star className="h-5 w-5 text-green-600 fill-green-600" />
                      <span className="text-sm font-bold text-green-900">
                        {(summary?.average_latency || 0) < ragMetrics.avgQueryLatency ? 'Chatbot' : 'RAG'} is faster
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Insights Panel */}
          <div className="bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-600 rounded-2xl p-6 text-white shadow-xl">
            <div className="flex items-start space-x-4">
              <div className="w-14 h-14 bg-white bg-opacity-20 backdrop-blur-sm rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg">
                <TrendingUp className="h-7 w-7 text-white" />
              </div>
              <div className="flex-1">
                <h4 className="text-xl font-bold mb-4">💡 Combined System Insights</h4>
                <div className="space-y-3 text-sm">
                  <div className="flex items-start space-x-2">
                    <span className="text-yellow-300 font-bold text-lg">•</span>
                    <p className="flex-1">
                      <span className="font-bold text-yellow-200">Total System Interactions: </span>
                      {(summary?.total_requests || 0) + ragMetrics.totalQueries} requests across Chatbot and RAG
                    </p>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-green-300 font-bold text-lg">•</span>
                    <p className="flex-1">
                      <span className="font-bold text-green-200">Document Coverage: </span>
                      {ragMetrics.totalUploads} documents indexed and ready for semantic search
                    </p>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-300 font-bold text-lg">•</span>
                    <p className="flex-1">
                      <span className="font-bold text-blue-200">Recommendation: </span>
                      {ragMetrics.totalQueries > 0 
                        ? 'RAG is active! Use it for document-specific questions to get accurate, contextual answers.'
                        : 'Upload documents to enable RAG capabilities and semantic search.'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Evaluation Metrics */}
        {evaluation && (
          <div className="card p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Evaluation Metrics (RAGAS)</h2>
              <p className="text-gray-500 text-sm">Quality assessment scores</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              <EvaluationCard label="Faithfulness" value={evaluation.avg_faithfulness} />
              <EvaluationCard label="Relevance" value={evaluation.avg_relevance} />
              <EvaluationCard label="Precision" value={evaluation.avg_context_precision} />
              <EvaluationCard label="Recall" value={evaluation.avg_context_recall} />
              <EvaluationCard label="Hallucination" value={evaluation.avg_hallucination_risk} warning />
              <EvaluationCard label="RAGAS Score" value={evaluation.avg_ragas_score} highlight />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, gradient, trend }: any) {
  return (
    <div className="stat-card group cursor-pointer">
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
            <p className="text-3xl font-bold text-gray-900">{value}</p>
          </div>
          <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-200`}>
            <Icon className="h-7 w-7 text-white" />
          </div>
        </div>
        {trend && (
          <div className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold ${
            trend.startsWith('+') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {trend} from last period
          </div>
        )}
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon: Icon, iconColor, subtitle, rating }: any) {
  return (
    <div className="card p-6 hover:shadow-medium transition-all duration-200">
      <div className="flex items-start space-x-4">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${iconColor} flex items-center justify-center shadow-sm`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="flex-1">
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mb-1">{value}</p>
          <p className="text-xs text-gray-500">{subtitle}</p>
          {rating > 0 && (
            <div className="flex items-center mt-2">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`h-3 w-3 ${
                    i < Math.round(rating) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function EvaluationCard({ label, value, warning, highlight }: { label: string; value: number | null; warning?: boolean; highlight?: boolean }) {
  const score = value !== null ? value : 0;
  const percentage = score * 100;
  
  return (
    <div className={`p-5 rounded-2xl transition-all duration-200 border-2 ${
      highlight 
        ? 'bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200 shadow-medium' 
        : warning
        ? 'bg-gradient-to-br from-red-50 to-orange-50 border-red-200'
        : 'bg-gradient-to-br from-gray-50 to-white border-gray-200 hover:border-blue-200 hover:shadow-soft'
    }`}>
      <p className={`text-xs font-semibold mb-3 ${highlight ? 'text-blue-700' : warning ? 'text-red-700' : 'text-gray-600'}`}>
        {label}
      </p>
      <div className="relative">
        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-2">
          <div 
            className={`h-full rounded-full transition-all duration-500 ${
              highlight ? 'bg-gradient-to-r from-blue-500 to-purple-600' :
              warning ? 'bg-gradient-to-r from-red-500 to-orange-500' :
              'bg-gradient-to-r from-green-400 to-green-600'
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
        <p className={`text-2xl font-bold ${highlight ? 'gradient-text' : 'text-gray-900'}`}>
          {value !== null ? value.toFixed(3) : 'N/A'}
        </p>
      </div>
    </div>
  );
}
