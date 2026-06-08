export interface User {
  id: number;
  email: string;
  username: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface MetricsSummary {
  total_requests: number;
  active_models: number;
  average_latency: number;
  error_rate: number;
  total_tokens: number;
  total_cost: number;
  max_tokens: number;
}

export interface UsageMetrics {
  date: string;
  requests: number;
  tokens: number;
  cost: number;
  avg_latency: number;
}

export interface ModelMetrics {
  model: string;
  requests: number;
  tokens: number;
  avg_latency: number;
  error_rate: number;
}

export interface EvaluationMetrics {
  avg_faithfulness: number | null;
  avg_relevance: number | null;
  avg_context_precision: number | null;
  avg_context_recall: number | null;
  avg_hallucination_risk: number | null;
  avg_ragas_score: number | null;
}

export interface ChatMessage {
  id: number;
  content: string;
  role: 'user' | 'assistant';
  model: string;
  tokens_used: number;
  latency_ms: number;
  cost: number;
  timestamp: string;
}

export interface Alert {
  id: number;
  type: string;
  severity: string;
  message: string;
  is_resolved: boolean;
  created_at: string;
}
