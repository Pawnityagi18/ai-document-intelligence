# Test Cases - AI Document Intelligence

## Testing Strategy

### Test Pyramid
```
        ▲
       /|\
      / | \  End-to-End (5%)
     /  |  \
    /───┼───\
   /    |    \  Integration (25%)
  /─────┼─────\
 /      |      \ Unit (70%)
/───────┴───────\
```

### Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_document_processor.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_qa_service.py::test_answer_with_high_confidence -v

# Run in watch mode (requires pytest-watch)
ptw tests/
```

## Unit Tests

### 1. Document Processor Tests
**File:** `tests/test_document_processor.py`

#### UC1.1: PDF Text Extraction
```
Test: test_extract_text_from_pdf
Given: A valid PDF file with 3 pages
When: Calling extract_text_from_pdf()
Then: 
  - Returns extracted text
  - Text length > 100 characters
  - Page numbers are tracked
```

#### UC1.2: PDF with Invalid Format
```
Test: test_extract_text_from_corrupted_pdf
Given: A corrupted/invalid PDF file
When: Calling extract_text_from_pdf()
Then:
  - Raises DocumentProcessingError
  - Error message is descriptive
  - Logging captures the error
```

#### UC1.3: Text File Extraction
```
Test: test_extract_text_from_txt
Given: A valid text file
When: Calling extract_text()
Then:
  - Returns extracted text
  - Text matches file content
  - Encoding is handled correctly
```

#### UC1.4: Content Chunking
```
Test: test_chunk_content_basic
Given: Text content (2000 tokens)
When: Calling chunk_content(chunk_size=500, overlap=50)
Then:
  - Returns list of chunks
  - All chunks have metadata (page, index)
  - Chunk overlap is correct
  - First chunk starts at beginning
  - Last chunk ends at end
```

#### UC1.5: Chunk Boundaries
```
Test: test_chunk_content_preserves_context
Given: Sentence ending at chunk boundary
When: Chunking with overlap
Then:
  - Complete sentences are not split
  - Context is preserved across chunks
  - No data loss
```

#### UC1.6: Empty Document
```
Test: test_chunk_content_empty_document
Given: Empty text
When: Calling chunk_content()
Then:
  - Returns empty list
  - No errors raised
  - Logging notes empty document
```

### 2. Embedding Service Tests
**File:** `tests/test_embedding_service.py`

#### UC2.1: Generate Single Embedding
```
Test: test_generate_embedding_single
Given: A text string "Hello world"
When: Calling generate_embedding()
Then:
  - Returns embedding vector
  - Vector length = 1536 (OpenAI size)
  - All values are floats
  - Result is cached
```

#### UC2.2: Generate Batch Embeddings
```
Test: test_generate_embeddings_batch
Given: List of 5 text chunks
When: Calling generate_embeddings()
Then:
  - Returns list of 5 embeddings
  - All embeddings have same dimension
  - Batch processed efficiently
  - Cached for reuse
```

#### UC2.3: Caching Works
```
Test: test_embedding_cache_hit
Given: Same text queried twice
When: Calling generate_embedding() twice
Then:
  - Second call returns cached result
  - API not called second time
  - Same embedding vector returned
```

#### UC2.4: API Error Handling
```
Test: test_embedding_api_error
Given: OpenAI API key is invalid
When: Calling generate_embedding()
Then:
  - Raises EmbeddingError
  - Error message includes API error
  - Retry logic triggered
  - After 3 retries, fails gracefully
```

### 3. Vector Store Tests
**File:** `tests/test_vector_store.py`

#### UC3.1: Add Documents to Store
```
Test: test_add_documents_to_store
Given: 
  - Collection name "test_doc"
  - List of 5 chunks with embeddings and metadata
When: Calling add_documents()
Then:
  - All documents stored successfully
  - Documents retrievable by ID
  - Metadata preserved
```

#### UC3.2: Search Similar Documents
```
Test: test_search_similar_documents
Given:
  - Store with 10 documents
  - Query embedding
When: Calling search(query_embedding, k=3)
Then:
  - Returns exactly 3 results
  - Results sorted by relevance (distance)
  - Distances are valid (0-1 range)
  - Top result most similar
```

#### UC3.3: Empty Search Results
```
Test: test_search_no_results
Given:
  - Empty vector store
When: Calling search()
Then:
  - Returns empty list
  - No error raised
  - Appropriate logging
```

#### UC3.4: Delete Collection
```
Test: test_delete_collection
Given:
  - Collection with 5 documents
When: Calling delete_collection()
Then:
  - Collection deleted
  - New search returns empty
  - Memory freed
```

### 4. QA Service Tests
**File:** `tests/test_qa_service.py`

#### UC4.1: High Confidence Answer
```
Test: test_answer_with_high_confidence
Given:
  - Question: "What is Python?"
  - Document contains clear answer
  - Confidence threshold: 0.5
When: Calling answer_question()
Then:
  - Returns answer
  - confidence_score > 0.7
  - sources list not empty
  - answer is non-empty string
```

#### UC4.2: Low Confidence (I don't know)
```
Test: test_answer_with_low_confidence
Given:
  - Question: "What is the purpose of life?"
  - Document about Python programming
  - Confidence threshold: 0.5
When: Calling answer_question()
Then:
  - Returns "I don't know" response
  - confidence_score < 0.5
  - Explains why answer not found
  - sources list is empty or minimal
```

#### UC4.3: Multiple Relevant Sources
```
Test: test_answer_with_multiple_sources
Given:
  - Question with answer in multiple places
When: Calling answer_question()
Then:
  - Returns consolidated answer
  - Multiple sources listed
  - Sources ranked by relevance
  - All sources have page numbers
```

#### UC4.4: Follow-up Question
```
Test: test_follow_up_question
Given:
  - Initial question answered
  - Follow-up question in same context
When: Calling answer_question()
Then:
  - Follows up appropriately
  - Uses relevant context
  - Answer is contextually correct
```

### 5. LLM Service Tests
**File:** `tests/test_llm_service.py`

#### UC5.1: Generate Answer from Context
```
Test: test_generate_answer
Given:
  - Context: "Python is a programming language"
  - Question: "What is Python?"
When: Calling generate_answer()
Then:
  - Returns answer string
  - Answer is non-empty
  - Answer mentions Python
  - Response time < 10s
```

#### UC5.2: Handle API Error
```
Test: test_llm_api_error
Given:
  - OpenAI API returns error
When: Calling generate_answer()
Then:
  - Raises LLMError
  - Error message is helpful
  - Retry logic applied
```

#### UC5.3: Token Counting
```
Test: test_token_counting
Given: Text of 100 words
When: Calling count_tokens()
Then:
  - Returns reasonable token count
  - Approximately 100-150 tokens
  - Consistent across calls
```

## Integration Tests

### 1. End-to-End Document Processing
**File:** `tests/test_integration.py`

#### IT1.1: Upload → Extract → Chunk → Embed → Store
```
Test: test_full_document_processing_pipeline
Given:
  - Sample PDF file (3 pages, 5000 tokens)
When: Running full processing pipeline
Then:
  - Document successfully processed
  - Text extracted (length > 1000 chars)
  - Chunks created (count = 10-12)
  - All chunks embedded
  - All chunks stored in vector DB
  - Can retrieve chunks by similarity
```

#### IT1.2: Query Document
```
Test: test_full_query_pipeline
Given:
  - Processed document in vector store
  - Valid question
When: Running full query pipeline
Then:
  - Query embedded
  - Similar chunks retrieved
  - Answer generated
  - Sources included
  - Response time < 10s
```

#### IT1.3: Multiple Queries on Same Document
```
Test: test_multiple_queries_same_document
Given:
  - One processed document
  - 5 different questions
When: Asking all 5 questions
Then:
  - All questions answered
  - Answers are different and contextual
  - Vector store not duplicated
  - Performance remains consistent
```

### 2. API Integration Tests
**File:** `tests/test_api_integration.py`

#### IT2.1: POST /api/documents/upload
```
Test: test_upload_document_api
Given:
  - FastAPI test client
  - Valid PDF file
When: POST to /api/documents/upload
Then:
  - Response status: 200
  - Response JSON includes document_id
  - Response includes chunk_count
  - Document stored in vector DB
```

#### IT2.2: POST /api/queries/ask
```
Test: test_query_api
Given:
  - FastAPI test client
  - Processed document in store
  - Question: "What is the main topic?"
When: POST to /api/queries/ask
Then:
  - Response status: 200
  - Response includes "answer" field
  - Response includes "sources" list
  - Response includes "confidence" score
  - Answer is non-empty string
```

#### IT2.3: Query Without Document
```
Test: test_query_without_document
Given:
  - No document processed
  - Question in POST body
When: POST to /api/queries/ask
Then:
  - Response status: 400
  - Error message: "No document loaded"
  - Clear error explanation
```

## Edge Case Tests

### 1. File Handling
```
Test: test_very_large_pdf
- File size: 50MB
- Expected: Graceful handling or clear error

Test: test_encrypted_pdf
- Password-protected PDF
- Expected: Error with instructions

Test: test_malformed_text_file
- Binary file with .txt extension
- Expected: Error handling

Test: test_empty_file
- 0-byte file
- Expected: Error or graceful handling
```

### 2. Content Handling
```
Test: test_extremely_long_question
- Question: 5000 characters
- Expected: Handled correctly

Test: test_special_characters
- Question with emojis, symbols
- Expected: Correct embedding and search

Test: test_multiple_languages
- Question in non-English language
- Expected: Best-effort attempt
```

### 3. API/External Service Handling
```
Test: test_rate_limiting
- Rapid API calls
- Expected: Queued or throttled

Test: test_network_timeout
- OpenAI API times out
- Expected: Retry and fallback

Test: test_api_quota_exceeded
- API quota exhausted
- Expected: Clear error message
```

## Performance Tests

### 1. Load Tests
```
Test: test_concurrent_uploads
- 5 concurrent document uploads
- Expected: All succeed within 30s

Test: test_concurrent_queries
- 10 concurrent queries on same document
- Expected: All respond within 5s each
```

### 2. Benchmark Tests
```
Test: test_document_processing_speed
- Measure: Time to process 10-page PDF
- Target: < 10 seconds

Test: test_query_response_time
- Measure: Time from question to answer
- Target: < 5 seconds (excluding LLM latency)

Test: test_vector_search_speed
- Measure: Time to search 1000 embeddings
- Target: < 100ms
```

## Test Data

### Sample Documents

#### sample1.pdf
- Content: Technical article about Python
- Pages: 5
- Size: 200KB
- Purpose: Test PDF extraction and chunking

#### sample2.pdf
- Content: Business document (report)
- Pages: 10
- Size: 500KB
- Purpose: Test larger documents

#### sample3.txt
- Content: Plain text content
- Size: 50KB
- Purpose: Test non-PDF documents

### Sample Questions & Answers

For each document, we have defined 10 questions with expected answers:

**Sample Question Set for sample1.pdf (Python article):**

1. Q: "What is Python?"
   A: Should mention it's a programming language

2. Q: "When was Python created?"
   A: Should provide creation year/date

3. Q: "What are Python's use cases?"
   A: Should list common applications

4. Q: "Is Python compiled or interpreted?"
   A: Should mention it's interpreted

5. Q: "What is the Python community like?"
   A: Should describe community characteristics

## Test Coverage Goals

- **Overall:** > 80%
- **Services:** > 90%
- **Routes/API:** > 85%
- **Utilities:** > 75%
- **Models:** > 80%

## Continuous Testing

### Pre-commit Checks
```bash
# Run quick tests before commit
pytest tests/test_*.py -v --tb=short
```

### CI/CD Pipeline (GitHub Actions)
```yaml
- Run all tests
- Check code coverage (must be > 80%)
- Linting with pylint/flake8
- Type checking with mypy
```

## Test Execution Schedule

- **Unit Tests:** Every commit
- **Integration Tests:** Every pull request
- **Performance Tests:** Weekly
- **Load Tests:** Before release
