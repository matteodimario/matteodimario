#!/usr/bin/env python3
"""
Simple blog comment system similar to antirez.com
Stores comments in JSON and serves them dynamically
"""

import json
import os
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import uuid

# Data directory for comments
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
COMMENTS_FILE = DATA_DIR / "comments.json"

def load_comments():
    """Load all comments from JSON file"""
    if COMMENTS_FILE.exists():
        with open(COMMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_comments(comments):
    """Save comments to JSON file"""
    with open(COMMENTS_FILE, 'w') as f:
        json.dump(comments, f, indent=2)

def format_time_ago(timestamp):
    """Convert timestamp to 'X days ago' format"""
    dt = datetime.fromisoformat(timestamp)
    now = datetime.now()
    delta = now - dt
    
    seconds = delta.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        mins = int(seconds / 60)
        return f"{mins} minute{'s' if mins > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    else:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"

class BlogCommentHandler(SimpleHTTPRequestHandler):
    """Custom handler for blog with comment API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # API endpoint: /api/comments?post=on-simplicity
        if parsed_path.path == '/api/comments':
            query_params = parse_qs(parsed_path.query)
            post_id = query_params.get('post', [''])[0]
            
            if post_id:
                comments = load_comments()
                post_comments = comments.get(post_id, [])
                
                # Add formatted time to each comment
                for comment in post_comments:
                    comment['time_formatted'] = format_time_ago(comment['timestamp'])
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(post_comments).encode())
                return
        
        # Default: serve static files
        super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for comment submission"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/comments':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                
                # Validate required fields
                if not data.get('author') or not data.get('text') or not data.get('post_id'):
                    self.send_error(400, "Missing required fields")
                    return
                
                # Create comment object
                comment = {
                    'id': str(uuid.uuid4())[:8],
                    'author': data.get('author', '').strip()[:100],
                    'email': data.get('email', '').strip()[:100],
                    'website': data.get('website', '').strip()[:200] if data.get('website') else None,
                    'text': data.get('text', '').strip()[:5000],
                    'timestamp': datetime.now().isoformat(),
                    'post_id': data.get('post_id', '').strip()[:100],
                    'parent_id': data.get('parent_id'),
                    'approved': True  # Auto-approve for now, but could add moderation
                }
                
                # Load existing comments
                comments = load_comments()
                post_id = comment['post_id']
                
                if post_id not in comments:
                    comments[post_id] = []
                
                comments[post_id].append(comment)
                save_comments(comments)
                
                # Return the comment with formatted time
                comment['time_formatted'] = "just now"
                
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(comment).encode())
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.send_error(500, str(e))
            return
        
        super().do_POST()
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    PORT = 8000
    handler = BlogCommentHandler
    httpd = HTTPServer(('', PORT), handler)
    print(f"Server running on http://localhost:{PORT}")
    print(f"Comments stored in: {COMMENTS_FILE}")
    httpd.serve_forever()
