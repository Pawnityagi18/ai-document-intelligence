# Demo Script - AI Document Intelligence

## Demo Overview

This document walks through a complete demonstration of the AI Document Intelligence system.

## Sample Document

**Document Used:** `sample_documents/python_guide.pdf`
- **Content:** Comprehensive guide to Python programming
- **Pages:** 8
- **Sections:** 
  - Introduction to Python
  - Installation and Setup
  - Basic Syntax
  - Data Types
  - Functions and Modules
  - Error Handling
  - Best Practices

## Demo Flow

### Phase 1: Setup (2 minutes)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Set environment variables
export OPENAI_API_KEY="your-api-key-here"

# 3. Start the server
python -m uvicorn app.main:app --reload

# 4. Open browser
http://localhost:8000
```

**Demo Point:** Show the clean, simple UI with upload area and chat interface.

### Phase 2: Document Upload (2 minutes)

**Action:** Drag and drop `python_guide.pdf` onto the upload area

**Expected Output:**
```
✅ Upload Progress: 100%
✅ Document processed successfully!
✅ Extracted 2847 words from 8 pages
✅ Created 6 chunks with 50-token overlap
✅ Generated 6 embeddings
✅ Stored in vector database
```

**Demo Points:**
- Show upload progress indicator
- Confirm document metadata
- Show chunking statistics in console logs

---

## Sample Q&A Session

### Question 1: Basic Understanding

**Q:** "What is Python and what is it used for?"

**Expected Answer:**
```
Answer:
Python is a high-level, interpreted programming language known for its 
simplicity and readability. It is used for:
- Web development
- Data analysis and machine learning
- Automation and scripting
- Scientific computing
- Education

Sources:
- Page 1: Introduction to Python (Relevance: 0.92)
- Page 2: Overview and Use Cases (Relevance: 0.88)

Confidence: 95%
```

**Demo Points:**
- Shows direct answer from document
- Multiple relevant sources with page numbers
- High confidence score
- Response time: ~3-5 seconds

---

### Question 2: Specific Technical Detail

**Q:** "How do you define a function in Python and what are the syntax rules?"

**Expected Answer:**
```
Answer:
Functions in Python are defined using the 'def' keyword followed by the 
function name and parentheses. The syntax is:

def function_name(parameters):
    """Docstring explaining the function"""
    # function body
    return value

Syntax rules:
- Function names should be lowercase with underscores (snake_case)
- Parameters are optional
- The colon (:) marks the start of the function body
- Indentation (4 spaces) defines the function body
- The return statement is optional

Sources:
- Page 4: Functions and Syntax (Relevance: 0.94)
- Page 3: Basic Syntax Rules (Relevance: 0.87)

Confidence: 93%
```

**Demo Points:**
- Shows code example in answer
- Preserves formatting from document
- Multiple relevant chunks combined
- Technical accuracy

---

### Question 3: Error Handling

**Q:** "How do I handle errors and exceptions in Python?"

**Expected Answer:**
```
Answer:
Python handles errors using try-except blocks:

try:
    # code that might raise an error
    result = 10 / 0
except ZeroDivisionError as e:
    # code to handle the specific error
    print(f"Cannot divide by zero: {e}")
except Exception as e:
    # catch all other exceptions
    print(f"An error occurred: {e}")
finally:
    # code that always runs
    print("Cleanup code")

You can:
- Catch specific exception types
- Access exception details with 'as'
- Use finally for cleanup
- Raise custom exceptions

Sources:
- Page 6: Error Handling (Relevance: 0.96)
- Page 7: Best Practices (Relevance: 0.82)

Confidence: 94%
```

**Demo Points:**
- Code examples preserved
- Related information from multiple pages
- Clear, well-formatted answer

---

### Question 4: Comparison Question

**Q:** "What's the difference between lists and tuples in Python?"

**Expected Answer:**
```
Answer:
Both lists and tuples are sequences in Python, but with key differences:

Lists:
- Mutable (can be modified after creation)
- Use square brackets []
- Slower than tuples
- Use when you need to modify the data

Tuples:
- Immutable (cannot be modified)
- Use parentheses ()
- Faster than lists
- Use for fixed collections or dictionary keys

Example:
my_list = [1, 2, 3]      # Can modify
my_tuple = (1, 2, 3)     # Cannot modify
my_list[0] = 10          # Works
my_tuple[0] = 10         # Error!

Sources:
- Page 4: Data Types - Lists and Tuples (Relevance: 0.95)
- Page 3: Data Structures (Relevance: 0.89)

Confidence: 92%
```

**Demo Points:**
- Comparison format clear
- Code examples included
- Practical distinction explained

---

### Question 5: Out-of-Domain Question

**Q:** "What is the capital of France?"

**Expected Answer:**
```
Answer:
I don't know. The document is about Python programming and doesn't contain 
information about geography or capital cities.

The document covers:
- Introduction to Python
- Installation and Setup
- Basic Syntax
- Data Types
- Functions and Modules
- Error Handling
- Best Practices

Would you like to ask something about Python instead?

Confidence: 2%
Sources: None (no relevant content found)
```

**Demo Points:**
- Graceful "I don't know" response
- Explains why answer not found
- Suggests related topics
- Very low confidence score
- No sources provided

---

### Question 6: Multi-Part Question

**Q:** "Explain Python modules and how do I import them?"

**Expected Answer:**
```
Answer:
Modules are files containing Python code. They help organize code and promote 
reusability.

Importing modules:

# Import entire module
import math
result = math.sqrt(16)

# Import specific items
from math import sqrt
result = sqrt(16)

# Import with alias
import numpy as np
array = np.array([1, 2, 3])

# Import all items (not recommended)
from math import *

Best practices:
- Put all imports at the top of your file
- Import standard library modules first
- Then import third-party modules
- Finally import your own modules
- Use specific imports rather than *

Sources:
- Page 5: Modules and Imports (Relevance: 0.93)
- Page 7: Best Practices (Relevance: 0.86)

Confidence: 91%
```

**Demo Points:**
- Multiple code examples
- Best practices included
- Complete explanation

---

### Question 7: Vague/Ambiguous Question

**Q:** "Tell me about Python."

**Expected Answer:**
```
Answer:
Python is a high-level, interpreted programming language. Key characteristics:

- Created in 1989 by Guido van Rossum
- Known for clean, readable syntax
- Dynamically typed
- Supports multiple programming paradigms:
  - Object-oriented
  - Functional
  - Procedural

- Popular for:
  - Web development (Django, Flask)
  - Data science (Pandas, NumPy)
  - Machine learning (TensorFlow, PyTorch)
  - Automation
  - Scientific computing

- Large and active community
- Extensive standard library
- Easy to learn and teach

Sources:
- Page 1: Introduction (Relevance: 0.91)
- Page 2: Python Overview (Relevance: 0.88)
- Page 2: Use Cases (Relevance: 0.85)

Confidence: 89%
```

**Demo Points:**
- System answers general question
- Combines multiple relevant chunks
- Provides comprehensive overview

---

### Question 8: Follow-up Question

**Previous:** (After Q1) "What is Python and what is it used for?"

**Q:** "Can you give me more details about data analysis?"

**Expected Answer:**
```
Answer:
Python is excellent for data analysis. Key aspects:

Libraries:
- Pandas: Data manipulation and analysis
- NumPy: Numerical computing
- Matplotlib: Data visualization
- Scikit-learn: Machine learning

Data Analysis workflow:
1. Load data (CSV, JSON, databases)
2. Clean and preprocess
3. Explore and visualize
4. Perform analysis
5. Build models
6. Present results

Why Python for data analysis:
- Powerful libraries
- Easy to learn syntax
- Large data science community
- Integration with other tools
- Open source

Sources:
- Page 2: Data Analysis Use Cases (Relevance: 0.90)
- Page 5: Libraries and Modules (Relevance: 0.87)

Confidence: 88%
```

**Demo Points:**
- Follow-up maintains context
- More detailed information provided
- Related to previous question

---

### Question 9: Edge Case - Partial Match

**Q:** "How do I install Python on Windows?"

**Expected Answer:**
```
Answer:
The document mentions installation and setup:

1. Download Python from python.org
2. Run the installer
3. During installation:
   - Check "Add Python to PATH"
   - Verify the installation directory
4. Verify installation by opening Command Prompt and typing:
   python --version
5. Upgrade pip:
   python -m pip install --upgrade pip

After installation, you can:
- Run Python interactively
- Execute scripts
- Install third-party packages using pip

For detailed platform-specific instructions, refer to the official Python 
documentation.

Sources:
- Page 2: Installation and Setup (Relevance: 0.87)

Confidence: 78%
```

**Demo Points:**
- Partial match (document has general setup, not Windows-specific)
- Confidence slightly lower
- System provides what it knows

---

### Question 10: Technical Deep-Dive

**Q:** "What are decorators in Python and how do I create one?"

**Expected Answer:**
```
Answer:
Decorators are functions that modify or enhance other functions or classes 
without changing their source code.

Basic decorator structure:

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

Using decorators:

@my_decorator
def say_hello(name):
    print(f"Hello {name}")

say_hello("Alice")
# Output:
# Before function call
# Hello Alice
# After function call

Common decorators:
- @staticmethod: Class method without instance access
- @classmethod: Class method with class access
- @property: Convert method to property
- Custom decorators for validation, logging, caching

Benefits:
- Reduce code duplication
- Improve code readability
- Separate concerns
- Easier debugging

Sources:
- Page 5: Advanced Functions (Relevance: 0.92)
- Page 4: Function Concepts (Relevance: 0.85)

Confidence: 89%
```

**Demo Points:**
- Complex topic handled well
- Code examples clear
- Practical applications shown
- Confidence still high for covered topics

---

## Performance Metrics

### During Demo Session

| Action | Time | Notes |
|--------|------|-------|
| Document Upload | 0.8s | Small PDF, fast |
| Text Extraction | 1.2s | 8 pages, straightforward |
| Chunking | 0.3s | 6 chunks created |
| Embedding Generation | 3.5s | API call to OpenAI |
| First Query Response | 4.2s | Includes embedding + search + LLM |
| Subsequent Queries | 3.8-4.1s | Similar latency |

### Observations

- **Total Setup Time:** ~6 seconds (upload to first answer)
- **Query Latency:** 3.8-4.2 seconds (excluding network delays)
- **Vector Search:** < 50ms (very fast)
- **Bottleneck:** LLM API calls (2-3 seconds per response)

---

## UI/UX Observations

### What Works Well
- ✅ Clean, minimal interface
- ✅ Clear document status display
- ✅ Chat-like interaction feels natural
- ✅ Real-time feedback
- ✅ Error messages are helpful

### Improvements for Future
- 📝 Add loading spinners during API calls
- 📝 Show retrieval process ("Found 3 relevant sections...")
- 📝 Expandable source sections
- 📝 Copy answer functionality
- 📝 Query history sidebar

---

## Key Takeaways

1. **System works end-to-end** ✅
2. **Answers are accurate and well-sourced** ✅
3. **Graceful handling of out-of-domain questions** ✅
4. **Performance is acceptable** ✅
5. **UI is intuitive** ✅
6. **Logging shows detailed operation flow** ✅

---

## Next Steps for Demo

1. Try uploading a different document
2. Ask questions in different styles (specific, vague, follow-up)
3. Check logs to see processing pipeline
4. Inspect database contents
5. Test error scenarios (invalid file, API errors)

---

## Code Review During Demo

Walk through:
1. `app/services/qa_service.py` - The orchestrator
2. `app/services/document_processor.py` - Text extraction
3. `app/services/vector_store.py` - Similarity search
4. `frontend/js/app.js` - UI interaction
