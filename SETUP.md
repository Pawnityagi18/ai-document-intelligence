# Setup & Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.10+
- pip or poetry
- OpenAI API key (or local Ollama)
- Git

### Step-by-Step Installation

#### 1. Clone Repository
```bash
git clone https://github.com/Pawnityagi18/ai-document-intelligence.git
cd ai-document-intelligence
```

#### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk_your_key_here
```

#### 5. Run Application
```bash
# Start FastAPI server
python -m uvicorn app.main:app --reload

# Server will be available at http://localhost:8000
```

#### 6. Open in Browser
Navigate to `http://localhost:8000` and you should see:
- Upload area for documents
- Chat interface for asking questions
- Source references and confidence scores

---

## Running Tests

### Unit Tests
```bash
# Run all unit tests
pytest tests/test_document_processor.py -v
pytest tests/test_embedding_service.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Integration Tests
```bash
# Run full pipeline tests
pytest tests/test_integration.py -v
```

---

## Quick Demo

### 1. Upload Sample Document
- Go to http://localhost:8000
- Drag and drop `data/sample_documents/python_guide.txt`
- Wait for processing (should take 5-10 seconds)
- Should see success message with chunk count

### 2. Ask Sample Questions

**Question 1:** "What is Python and what is it used for?"
- **Expected**: Answer about Python being a programming language with use cases
- **Confidence**: Should be high (>80%)
- **Sources**: Should show page numbers

**Question 2:** "How do I define a function?"
- **Expected**: Code example with syntax rules
- **Confidence**: High
- **Sources**: References to function documentation

**Question 3:** "What is the capital of France?"
- **Expected**: "I don't know" response
- **Confidence**: Very low (<10%)
- **Sources**: None or minimal

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:**
- Check `.env` file exists and has valid key
- Verify key starts with `sk_`
- Try restarting the server

### Issue: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install --upgrade openai
```

### Issue: "ChromaDB initialization error"
**Solution:**
- Ensure `data/chroma_db/` directory has write permissions
- Delete existing db: `rm -rf data/chroma_db/`
- Restart server

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Use different port
python -m uvicorn app.main:app --port 8001 --reload
```

### Issue: "PDF extraction not working"
**Solution:**
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Test with sample text file first: `python_guide.txt`
- Check PDF is not corrupted

---

## Performance Optimization

### For Development
- Reduce chunk size: `CHUNK_SIZE=250` in `.env`
- Use fewer results: `TOP_K_RESULTS=2` in `.env`
- Enable debug mode: `DEBUG=True`

### For Production
- Set `DEBUG=False` in `.env`
- Use production ASGI server: `gunicorn app.main:app`
- Implement caching layer
- Use async processing for large documents

---

## Deployment Options

### Option 1: Local Machine
```bash
# Just follow the setup steps above
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option 2: Docker (Future)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Option 3: Cloud Platforms
- **Heroku**: `heroku create`, `git push heroku main`
- **AWS Lambda**: Package with serverless framework
- **Google Cloud Run**: Deploy as container
- **Replit**: Import repo directly

---

## Project Structure Reminder

```
ai-document-intelligence/
├── app/                    # Main application
│   ├── services/          # Business logic (5 services)
│   ├── routes/            # API endpoints (3 routes)
│   ├── models/            # Data models
│   ├── utils/             # Utilities & errors
│   ├── main.py            # FastAPI app
│   └── config.py          # Configuration
├── frontend/              # Web UI
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── tests/                 # Test suite
├── data/                  # Data & samples
├── requirements.txt       # Dependencies
└── README.md             # This guide
```

---

## Next Steps

1. ✅ Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. ✅ Check [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for demo walkthrough
3. ✅ Review [LEARNINGS.md](LEARNINGS.md) for insights
4. ✅ Run [TEST_CASES.md](TEST_CASES.md) to understand testing
5. ✅ Try uploading your own documents

---

## Support & Contributions

- Found a bug? [Create an issue](https://github.com/Pawnityagi18/ai-document-intelligence/issues)
- Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)
- Have questions? Check [README.md](README.md)

---

**Happy learning! 🚀**
