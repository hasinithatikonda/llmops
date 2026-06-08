'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import Navbar from '@/components/Navbar';
import api from '@/lib/api';
import { ChatMessage } from '@/types';
import { Send, Clock, DollarSign, Bot, User, Sparkles, Cpu, Zap } from 'lucide-react';

interface ModelInfo {
  id: string;
  name: string;
  description: string;
  context_window: number;
  max_tokens: number;
  speed: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');
  const [conversations, setConversations] = useState<Array<{id: string, title: string, timestamp: string, messages: ChatMessage[]}>>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
      return;
    }
    fetchModels();
    loadConversations();
  }, [router]);

  const loadConversations = () => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('chat_conversations');
      if (saved) {
        const parsed = JSON.parse(saved);
        setConversations(parsed);
      }
    }
  };

  const saveConversations = (convs: typeof conversations) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('chat_conversations', JSON.stringify(convs));
    }
  };

  const createNewConversation = () => {
    const newConv = {
      id: Date.now().toString(),
      title: 'New Chat',
      timestamp: new Date().toISOString(),
      messages: []
    };
    const updated = [newConv, ...conversations];
    setConversations(updated);
    setCurrentConversationId(newConv.id);
    setMessages([]);
    saveConversations(updated);
  };

  const loadConversation = (convId: string) => {
    const conv = conversations.find(c => c.id === convId);
    if (conv) {
      setCurrentConversationId(convId);
      setMessages(conv.messages);
    }
  };

  const deleteConversation = (convId: string) => {
    const updated = conversations.filter(c => c.id !== convId);
    setConversations(updated);
    saveConversations(updated);
    if (currentConversationId === convId) {
      setMessages([]);
      setCurrentConversationId(null);
    }
  };

  const updateConversation = (msgs: ChatMessage[]) => {
    if (!currentConversationId && msgs.length > 0) {
      // Create new conversation
      const title = msgs[0].content.slice(0, 50) + (msgs[0].content.length > 50 ? '...' : '');
      const newConv = {
        id: Date.now().toString(),
        title,
        timestamp: new Date().toISOString(),
        messages: msgs
      };
      const updated = [newConv, ...conversations];
      setConversations(updated);
      setCurrentConversationId(newConv.id);
      saveConversations(updated);
    } else if (currentConversationId) {
      // Update existing conversation
      const updated = conversations.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: msgs, timestamp: new Date().toISOString() }
          : c
      );
      setConversations(updated);
      saveConversations(updated);
    }
  };

  const fetchModels = async () => {
    try {
      const response = await api.get('/models');
      setModels(response.data);
    } catch (error) {
      console.error('Failed to fetch models:', error);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    setLoading(true);
    const userMessage = input;
    setInput('');

    const userMsg: ChatMessage = {
      id: Date.now(),
      content: userMessage,
      role: 'user',
      timestamp: new Date().toISOString(),
      tokens_used: 0,
      latency_ms: 0,
      cost: 0,
      model: '',
    };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);

    try {
      const response = await api.post('/chat', {
        message: userMessage,
        model: selectedModel,
      });

      const botMsg: ChatMessage = {
        id: Date.now() + 1,
        content: response.data.response,
        role: 'assistant',
        timestamp: response.data.timestamp,
        tokens_used: response.data.tokens_used,
        latency_ms: response.data.latency_ms,
        cost: (response.data.tokens_used * 0.0000002),
        model: response.data.model,
      };
      const finalMessages = [...updatedMessages, botMsg];
      setMessages(finalMessages);
      updateConversation(finalMessages);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to send message');
      setInput(userMessage);
      setMessages(messages);
    } finally {
      setLoading(false);
    }
  };

  const getSelectedModelInfo = () => {
    return models.find(m => m.id === selectedModel);
  };

  return (
    <>
      <Navbar />
      <div className="flex pt-16 min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        {/* Chat History Sidebar */}
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-72 bg-white border-r border-gray-200 overflow-y-auto shadow-lg z-10">
          <div className="p-4 bg-gradient-to-b from-blue-50 to-white">
            <button
              onClick={createNewConversation}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-3 rounded-xl text-sm font-semibold shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200 flex items-center justify-center space-x-2"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              <span>New Chat</span>
            </button>
          </div>
          
          <div className="px-4 pb-4">
            <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-2 flex items-center space-x-2">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>History</span>
            </h3>
            {conversations.length === 0 ? (
              <div className="text-center py-8">
                <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                  <svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-500 font-medium">No conversations yet</p>
                <p className="text-xs text-gray-400 mt-1">Start a new chat to begin</p>
              </div>
            ) : (
              <div className="space-y-2">
                {conversations.map((conv) => (
                  <div
                    key={conv.id}
                    className={`group relative p-3 rounded-xl cursor-pointer transition-all duration-200 ${
                      currentConversationId === conv.id
                        ? 'bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-300 shadow-md'
                        : 'bg-gray-50 hover:bg-gradient-to-r hover:from-gray-100 hover:to-gray-50 border border-gray-200 hover:border-gray-300 hover:shadow-sm'
                    }`}
                    onClick={() => loadConversation(conv.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0 flex items-start space-x-3">
                        <div className={`mt-0.5 w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                          currentConversationId === conv.id 
                            ? 'bg-gradient-to-br from-blue-500 to-purple-600' 
                            : 'bg-gradient-to-br from-gray-400 to-gray-500'
                        }`}>
                          <svg className="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                          </svg>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className={`text-sm font-semibold truncate ${
                            currentConversationId === conv.id ? 'text-blue-900' : 'text-gray-800'
                          }`}>
                            {conv.title}
                          </p>
                          <div className="flex items-center space-x-2 mt-1">
                            <p className="text-xs text-gray-500">
                              {new Date(conv.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                            </p>
                            <span className="text-gray-400">•</span>
                            <p className={`text-xs px-2 py-0.5 rounded-full ${
                              currentConversationId === conv.id 
                                ? 'bg-blue-100 text-blue-700' 
                                : 'bg-gray-200 text-gray-600'
                            }`}>
                              {conv.messages.length} msgs
                            </p>
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          if (confirm('Delete this conversation?')) {
                            deleteConversation(conv.id);
                          }
                        }}
                        className="opacity-0 group-hover:opacity-100 transition-opacity ml-2 p-1.5 hover:bg-red-100 rounded-lg text-red-500 hover:text-red-700"
                        title="Delete conversation"
                      >
                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="ml-72 flex-1 flex flex-col max-h-[calc(100vh-4rem)]">
          <div className="container mx-auto px-6 py-6 flex-1 flex flex-col max-w-6xl">
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2 flex items-center space-x-3">
                    <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-2xl shadow-lg">
                      <Bot className="h-8 w-8 text-white" />
                    </div>
                    <span>AI Chat</span>
                  </h1>
                  <p className="text-gray-600 text-sm">Powered by Groq's ultra-fast LLM inference</p>
                </div>
                
                <div className="flex flex-col items-end bg-white p-4 rounded-2xl shadow-md border border-gray-200">
                  <label className="text-xs font-semibold text-gray-600 mb-2 flex items-center space-x-2">
                    <Zap className="h-3.5 w-3.5 text-yellow-500" />
                    <span>AI Model</span>
                  </label>
                  <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="px-4 py-2 border-2 border-gray-300 rounded-xl bg-white hover:border-blue-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 font-medium text-sm cursor-pointer"
                  >
                    {models.map((model) => (
                      <option key={model.id} value={model.id}>
                        {model.name}
                      </option>
                    ))}
                  </select>
                  {getSelectedModelInfo() && (
                    <div className="mt-2 text-xs text-right space-y-1">
                      <div className="flex items-center justify-end space-x-1 text-gray-700 font-semibold">
                        <span className="text-blue-600">{getSelectedModelInfo()?.max_tokens.toLocaleString()}</span>
                        <span>tokens max</span>
                      </div>
                      <div className="flex items-center justify-end space-x-1">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                        <span className="text-gray-500">{getSelectedModelInfo()?.speed} speed</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

        <div className="card p-6 mb-6 flex-1 overflow-y-auto scrollbar-thin bg-white shadow-lg rounded-2xl border border-gray-200">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="mb-6 relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-3xl opacity-20 animate-pulse"></div>
                <div className="relative bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-10 rounded-3xl border-2 border-blue-200 shadow-xl">
                  <Sparkles className="h-20 w-20 text-blue-600 mx-auto animate-pulse" />
                </div>
              </div>
              <h3 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">Start a conversation</h3>
              <p className="text-gray-600 mb-6 max-w-md">Ask me anything! Select a model and start chatting with AI.</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-6 w-full max-w-2xl">
                {['Summarize Bahubali movie', 'Explain quantum physics', 'Write Python code', 'Tell me about AI'].map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(suggestion)}
                    className="px-5 py-4 bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 rounded-xl text-sm font-medium text-gray-700 transition-all duration-200 border-2 border-blue-200 hover:border-blue-400 hover:shadow-md transform hover:scale-105"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div key={message.id} className="animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className={`flex items-start space-x-4 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className="flex-shrink-0">
                      <div className={`w-10 h-10 rounded-xl ${message.role === 'user' ? 'bg-gradient-to-br from-green-500 to-teal-600' : 'bg-gradient-to-br from-blue-500 to-purple-600'} flex items-center justify-center shadow-md`}>
                        {message.role === 'user' ? <User className="h-5 w-5 text-white" /> : <Bot className="h-5 w-5 text-white" />}
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className={`${message.role === 'user' ? 'bg-gradient-to-br from-green-50 to-teal-50 border-green-100' : 'bg-gradient-to-br from-blue-50 to-purple-50 border-blue-100'} rounded-2xl p-5 border shadow-soft`}>
                        <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{message.content}</p>
                      </div>
                      
                      {message.role === 'assistant' && (
                        <div className="flex items-center space-x-4 mt-3 text-xs flex-wrap">
                          <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-white rounded-lg border border-gray-200">
                            <Clock className="h-3.5 w-3.5 text-blue-500" />
                            <span className="font-semibold text-gray-700">{message.latency_ms.toFixed(0)}ms</span>
                          </div>
                          <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-white rounded-lg border border-gray-200">
                            <DollarSign className="h-3.5 w-3.5 text-green-500" />
                            <span className="font-semibold text-gray-700">${message.cost.toFixed(5)}</span>
                          </div>
                          <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-white rounded-lg border border-gray-200">
                            <Cpu className="h-3.5 w-3.5 text-purple-500" />
                            <span className="font-semibold text-gray-700">{message.tokens_used} tokens</span>
                          </div>
                          <div className="badge-blue text-xs">
                            {message.model}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex items-start space-x-4 animate-pulse">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-md">
                    <Bot className="h-5 w-5 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-5 border border-blue-100">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

            <form onSubmit={sendMessage} className="bg-white p-5 rounded-2xl shadow-lg border-2 border-gray-200">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={loading}
                  className="flex-1 px-6 py-4 border-2 border-gray-300 rounded-xl hover:border-blue-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 bg-white disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 placeholder-gray-400 font-medium"
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
                >
                  <Send className="h-5 w-5" />
                  <span className="hidden sm:inline">{loading ? 'Sending...' : 'Send'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
