# Robotics Book Project - Developer Skill

## Overview
This skill helps Claude work efficiently on the "Physical AI and Humanoids" book website project without needing to ask repetitive questions or web search for project-specific information.

---

## 🏗️ Project Architecture

### Tech Stack
- **Frontend**: Docusaurus 3.9.2 (React-based documentation framework)
- **Backend**: FastAPI (Python) - RAG Chatbot API
- **Vector Database**: Qdrant (stores embedded book chunks)
- **Metadata Database**: Neon PostgreSQL (stores chunk metadata)
- **Embeddings**: OpenAI `text-embedding-3-small` (1024 dimensions)
- **LLM**: OpenAI `gpt-4o-mini` (via OpenAI Agents framework)
- **Deployment**: Vercel (frontend), separate backend deployment

### Project Structure
```
robotics-book-project/
├── docs/                          # Docusaurus content (MDX files)
│   ├── module-1/                  # ROS 2 & URDF
│   ├── module-2/                  # Digital Twin (Gazebo, Unity)
│   ├── module-3/                  # AI-Robot Brain (Isaac Sim, Nav2)
│   └── module-4/                  # Vision-Language-Action
│       ├── 01-voice-to-action-whisper.mdx
│       ├── 02-cognitive-planning-llms.mdx
│       ├── 03-computer-vision-object-recognition.mdx
│       └── 04-capstone-autonomous-humanoid.mdx
├── src/                           # React components
├── static/                        # Images, assets
├── docusaurus.config.js           # Site configuration
├── sidebars.js                    # Sidebar navigation
├── package.json                   # Node dependencies
├── main.py                        # Book ingestion pipeline
├── api.py                         # FastAPI chatbot endpoint
├── db.py                          # Database utilities
└── requirements.txt               # Python dependencies
```

---

## 📚 Module Structure

The book has 4 main modules with a consistent chapter structure:

### Standard Chapter Template
```mdx
---
sidebar_position: X
---

# Chapter Title

## Introduction
Brief overview of what this chapter covers.

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Section 1: Main Content
Detailed explanation with code examples.

### Subsection 1.1
More granular content.

## Hands-On Exercise
Step-by-step practical activity.

## What You Learned
- Key takeaway 1
- Key takeaway 2

## Next Steps
Where to go from here.

**Resources**:
- Link 1
- Link 2
```

### Code Block Style
Use syntax-highlighted code blocks with explanations:

````mdx
```python
# ROS 2 publisher example
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Node implementation
```
````

---

## 🔧 Common Development Tasks

### 1. Adding a New Chapter to a Module

**Steps**:
1. Create new MDX file: `docs/module-X/##-chapter-name.mdx`
2. Follow the content structure template
3. Update `sidebars.js` to add the new chapter
4. Build and preview: `npm start`
5. After deployment, run ingestion pipeline to update chatbot

**Example**:
```bash
# Add new chapter
touch docs/module-3/05-new-topic.mdx

# Preview locally
npm start

# After deployment, update RAG
python main.py
```

### 2. Updating the RAG Chatbot Knowledge Base

**When to run**:
- After adding new chapters
- After editing existing content
- After deployment to Vercel

**Command**:
```bash
python main.py
```

**What it does**:
1. Fetches all pages from `sitemap.xml`
2. Scrapes content with BeautifulSoup
3. Chunks content into ~1000 character segments
4. Generates embeddings with OpenAI
5. Stores vectors in Qdrant
6. Stores metadata in Neon PostgreSQL

**Expected output**:
```
Fetching sitemap from https://ai-native-book-website.vercel.app/sitemap.xml
Found 42 URLs
Processing: /module-1/ros2-basics
Processing: /module-2/gazebo-simulation
...
Ingested 287 chunks into Qdrant collection 'padh_book'
```

### 3. Testing the Chatbot Locally

**Start the API**:
```bash
uvicorn api:app --reload
```

**Test endpoint**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?"}'
```

### 4. Debugging RAG Issues

**Common Issues**:

| Problem | Cause | Solution |
|---------|-------|----------|
| "No relevant context" | Qdrant empty or outdated | Run `python main.py` |
| Dimension mismatch error | Embedding model changed | Check `dimensions=1024` in both `main.py` and `api.py` |
| Rate limit errors | Too many API calls | Add retry logic or upgrade OpenAI plan |
| Chatbot gives wrong answers | Context not retrieved | Check Qdrant search results manually |

**Debug Commands**:
```python
# Test Qdrant connection
from qdrant_client import QdrantClient
qdrant = QdrantClient(url="...", api_key="...")
print(qdrant.get_collection("padh_book"))

# Test embedding
from openai import OpenAI
client = OpenAI(api_key="...")
res = client.embeddings.create(
    model="text-embedding-3-small",
    input="test query",
    dimensions=1024
)
print(len(res.data[0].embedding))  # Should be 1024
```

### 5. Updating Frontend Dependencies

```bash
# Update Docusaurus
npm update @docusaurus/core @docusaurus/preset-classic

# Update all dependencies
npm update

# Rebuild
npm run build
```

---

## 🚀 Deployment Workflow

### Frontend (Docusaurus)
1. Make content changes in `docs/` folder
2. Test locally: `npm start`
3. Build: `npm run build`
4. Deploy to Vercel (automatic on git push)

### Backend (FastAPI Chatbot)
1. Update `api.py` or dependencies
2. Test locally: `uvicorn api:app --reload`
3. Deploy to hosting provider (Railway, Render, etc.)
4. Update CORS origins if domain changes

### After Content Updates
1. Deploy frontend to Vercel
2. Wait for deployment to complete
3. Run ingestion pipeline: `python main.py`
4. Verify chatbot has new knowledge

---

## 🎯 Chatbot Behavior Guidelines

### System Prompt (in `api.py`)
```
You are an expert assistant for the book "Physical AI and Humanoids".
Answer questions accurately using only the provided context from the book.
If the answer is not in the context, say: "I don't know based on the book content."
Be helpful, concise, and friendly.
When relevant, cite the source URLs at the end.
```

### Response Format
- Answer the question directly
- Use context from retrieved chunks
- Cite sources at the end
- If uncertain, admit limitations

**Good Response Example**:
```
ROS 2 uses a publisher-subscriber pattern for communication between nodes.
Publishers send messages to topics, and subscribers receive them. This allows
decoupled, asynchronous communication.

**Sources:**
• https://ai-native-book-website.vercel.app/module-1/ros2-basics
```

---

## 🛠️ Technology-Specific Notes

### Docusaurus
- **Build command**: `npm run build`
- **Dev server**: `npm start` (hot reload enabled)
- **Config file**: `docusaurus.config.js`
- **Sidebar**: Auto-generated from `sidebars.js`
- **MDX support**: Can use React components in Markdown

### FastAPI
- **CORS**: Configured for `localhost:3000` and production domain
- **Streaming**: Uses `StreamingResponse` for chatbot replies
- **Async**: OpenAI agent client is async, embedding client is sync

### Qdrant
- **Collection**: `padh_book`
- **Vector size**: 1024 (matches OpenAI embedding dimensions)
- **Distance metric**: Cosine similarity
- **Recreate on ingestion**: Collection is deleted and recreated each time

### OpenAI
- **Embedding model**: `text-embedding-3-small` (1024 dims)
- **Chat model**: `gpt-4o-mini` (via Agents framework)
- **Agent framework**: Uses OpenAI Agents library (not raw API)

---

## 📋 Quick Reference

### File Extensions
- `.mdx` - Markdown with JSX (book content)
- `.py` - Python (backend, ingestion)
- `.js`/`.jsx` - JavaScript/React (frontend)

### Key URLs
- **Production**: `https://ai-native-book-website.vercel.app`
- **Sitemap**: `https://ai-native-book-website.vercel.app/sitemap.xml`
- **API**: Backend deployed separately

### Python Dependencies
```
fastapi          # Web framework
uvicorn          # ASGI server
openai-agents    # OpenAI agent framework
qdrant-client    # Vector DB client
openai           # Embeddings
beautifulsoup4   # HTML parsing
psycopg          # PostgreSQL (Neon)
```

### Node Dependencies
```
@docusaurus/core         # Core framework
@docusaurus/preset-classic  # Classic theme
react                    # UI library
tailwindcss             # Styling
```

---

## 🎓 Module-Specific Context

### Module 1: ROS 2 & Robotics Basics
- Focus on `rclpy` (Python ROS 2 client library)
- URDF for robot description
- Nodes, topics, services, actions

### Module 2: Simulation & Digital Twins
- Gazebo for physics simulation
- Unity for visual/interactive environments
- Sensor simulation (LiDAR, cameras)

### Module 3: AI Perception & Navigation
- NVIDIA Isaac Sim for synthetic data
- Isaac ROS for GPU-accelerated perception
- Visual SLAM, Nav2 for navigation

### Module 4: Vision-Language-Action (VLA)
- Whisper for speech-to-text
- LLMs for task planning
- Computer vision for object detection
- Integration of voice, planning, and vision

---

## 🚨 Important Reminders

1. **Always run ingestion after content updates** - The chatbot won't know about new content until `main.py` is run

2. **Match embedding dimensions** - Both `main.py` and `api.py` use 1024 dimensions

3. **CORS configuration** - Update `api.py` if frontend domain changes

4. **Environment variables** - Never commit `.env` file, use `.env.example` for templates

5. **Content consistency** - Follow naming conventions and structure templates

6. **Test locally first** - Always test changes with `npm start` before deploying

---

## 💡 Best Practices

### When Adding Content
- Use clear, descriptive titles
- Include code examples for technical concepts
- Add "What You Learned" summaries
- Link to relevant resources
- Use consistent formatting

### When Updating RAG
- Run during off-peak hours (ingestion can take time)
- Check Qdrant collection size after ingestion
- Test chatbot with sample queries
- Monitor for errors in logs

### When Debugging
- Check browser console for frontend errors
- Check FastAPI logs for backend errors
- Verify environment variables are set
- Test API endpoints independently

---

## 📞 When to Use This Skill

Claude should reference this skill when:
- Adding new chapters or modules
- Updating chatbot knowledge
- Debugging RAG pipeline issues
- Modifying backend API
- Explaining project architecture
- Running ingestion or deployment tasks
- Working with Docusaurus configuration
- Troubleshooting embedding/vector issues

This skill eliminates the need to ask repetitive questions and enables Claude to work efficiently on the robotics book project.
