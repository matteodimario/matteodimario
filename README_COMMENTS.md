# Blog with Comment System

Your website now has a **real, working comment system** like antirez.com.

## How to Run

### Option 1: Python Backend (Recommended - Exact antirez.com-like implementation)

**Start the server with the comment API:**

```bash
python3 app.py
```

This runs on `http://localhost:8000` and handles:
- Serving all static HTML/CSS/JS files
- API endpoint: `/api/comments` (GET/POST)
- Persistent storage of comments in `data/comments.json`

### Option 2: Simple HTTP Server (No comments)

```bash
python3 -m http.server 8000
```

This serves files but won't process comments.

---

## How It Works

1. **Write a comment** on any blog post
2. **Submit the form** - it sends to `/api/comments`
3. **Comments are stored** in `data/comments.json` (persistent)
4. **Comments display** in real-time after submission
5. **List auto-refreshes** every 30 seconds

## Features Implemented

✅ **Real persistent storage** - Comments saved to JSON file
✅ **Exact antirez.com style** - Minimalist design, same typography
✅ **Form validation** - Name and comment required
✅ **Author links** - Optional website URLs for commenters
✅ **Time formatting** - Shows "2 hours ago", "3 days ago", etc.
✅ **HTML escaping** - Prevents XSS attacks
✅ **Auto-refresh** - Comments load automatically
✅ **Email not published** - Email stored but never shown

## File Structure

```
matteodimario/
├── app.py                 # Backend API server
├── index.html            # Homepage with blog posts
├── posts/
│   └── on-simplicity.html # Blog post with comments
└── data/
    └── comments.json     # Persistent comment storage (auto-created)
```

## Creating New Blog Posts

1. Copy `posts/on-simplicity.html` to a new file
2. Update the post ID: `const POST_ID = 'your-post-slug';`
3. Link it from `index.html`
4. Comments will automatically work!

## Customization

### Add Moderation
Edit `app.py` line 87:
```python
'approved': True  # Change to False for manual moderation
```

### Change Storage Backend
Replace JSON storage with:
- SQLite database
- PostgreSQL
- MongoDB
- etc.

### Add Email Notifications
Add when a new comment is posted (recommended tools: SendGrid, AWS SES)

---

Everything is now **exactly like antirez.com** - minimalist design with real, persistent comments!
