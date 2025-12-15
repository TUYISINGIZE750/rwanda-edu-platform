"""Simple HTTP server with no caching for development"""
import http.server
import socketserver

PORT = 5175

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Disable all caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

print("=" * 60)
print(f"🚀 NO-CACHE Development Server")
print("=" * 60)
print(f"Server running at: http://localhost:{PORT}")
print("✅ Cache disabled - Always serves fresh content")
print("Press Ctrl+C to stop")
print("=" * 60)

with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
