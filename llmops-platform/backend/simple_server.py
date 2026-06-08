"""
Simple mock backend server for demonstration
Run with: python simple_server.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import random

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json_response({"status": "healthy"})
        elif self.path.startswith('/metrics/summary'):
            self.send_json_response({
                "total_requests": 247,
                "active_users": 12,
                "average_latency": 1250.5,
                "error_rate": 2.4,
                "total_tokens": 125840,
                "total_cost": 0.0302,
                "average_feedback_score": 4.3
            })
        elif self.path.startswith('/metrics/usage'):
            usage_data = []
            for i in range(7):
                date = datetime.now().strftime('%Y-%m-%d')
                usage_data.append({
                    "date": date,
                    "requests": random.randint(20, 50),
                    "tokens": random.randint(1000, 5000),
                    "cost": round(random.uniform(0.002, 0.01), 4),
                    "avg_latency": round(random.uniform(800, 2000), 2)
                })
            self.send_json_response(usage_data)
        elif self.path.startswith('/metrics/models'):
            self.send_json_response([
                {"model": "mixtral-8x7b-32768", "requests": 150, "tokens": 75000, "avg_latency": 1200.5, "error_rate": 1.5},
                {"model": "llama2-70b-4096", "requests": 97, "tokens": 50840, "avg_latency": 1350.2, "error_rate": 3.2}
            ])
        elif self.path.startswith('/metrics/evaluation'):
            self.send_json_response({
                "avg_faithfulness": 0.875,
                "avg_relevance": 0.892,
                "avg_context_precision": 0.815,
                "avg_context_recall": 0.782,
                "avg_hallucination_risk": 0.156,
                "avg_ragas_score": 0.841
            })
        else:
            self.send_json_response({"error": "Not found"}, 404)
    
    def do_POST(self):
        if self.path == '/auth/login':
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            
            # Mock login - accept any credentials
            self.send_json_response({
                "access_token": "mock-jwt-token-" + str(random.randint(1000, 9999)),
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": body.get("email"),
                    "username": "testuser",
                    "role": "user",
                    "is_active": True,
                    "created_at": datetime.now().isoformat()
                }
            })
        elif self.path == '/auth/register':
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            
            # Mock register
            self.send_json_response({
                "access_token": "mock-jwt-token-" + str(random.randint(1000, 9999)),
                "token_type": "bearer",
                "user": {
                    "id": 2,
                    "email": body.get("email"),
                    "username": body.get("username"),
                    "role": "user",
                    "is_active": True,
                    "created_at": datetime.now().isoformat()
                }
            })
        else:
            self.send_json_response({"error": "Not found"}, 404)
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

if __name__ == '__main__':
    PORT = 8000
    print(f"\n{'='*60}")
    print(f"🚀 Mock Backend Server Starting...")
    print(f"{'='*60}")
    print(f"\n📡 Server running at: http://localhost:{PORT}")
    print(f"📊 API Docs: http://localhost:{PORT}/health")
    print(f"🌐 Frontend: http://localhost:3000")
    print(f"\n{'='*60}")
    print(f"✅ Mock credentials:")
    print(f"   Email: any@email.com")
    print(f"   Password: anything")
    print(f"{'='*60}\n")
    
    server = HTTPServer(('localhost', PORT), MockAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        server.shutdown()
