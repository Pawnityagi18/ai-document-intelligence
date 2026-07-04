"""Frontend JavaScript interaction"""

// Configuration
const API_BASE = "http://localhost:8000/api";
let currentDocumentId = null;

// DOM Elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const uploadStatus = document.getElementById("uploadStatus");
const uploadProgress = document.getElementById("uploadProgress");
const querySection = document.getElementById("querySection");
const documentInfo = document.getElementById("documentInfo");
const messages = document.getElementById("messages");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");

// Event Listeners
uploadArea.addEventListener("click", () => fileInput.click());
uploadArea.addEventListener("dragover", handleDragOver);
uploadArea.addEventListener("dragleave", handleDragLeave);
uploadArea.addEventListener("drop", handleDrop);
fileInput.addEventListener("change", handleFileSelect);
browseBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
});
askBtn.addEventListener("click", handleAskQuestion);
questionInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleAskQuestion();
});

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add("dragover");
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

async function handleFile(file) {
    uploadStatus.style.display = "none";
    uploadProgress.style.display = "block";
    uploadProgress.querySelector(".progress-fill").style.width = "0%";

    const formData = new FormData();
    formData.append("file", file);

    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += Math.random() * 30;
                updateProgress(Math.min(progress, 90));
            }
        }, 200);

        const response = await fetch(`${API_BASE}/documents/upload`, {
            method: "POST",
            body: formData
        });

        clearInterval(progressInterval);
        updateProgress(100);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Upload failed");
        }

        const data = await response.json();
        currentDocumentId = data.document_id;

        // Show success message
        showStatus(
            `✅ Document uploaded successfully!\nChunks: ${data.total_chunks} | Time: ${data.processing_time_seconds.toFixed(2)}s`,
            "success"
        );

        // Show query section
        querySection.style.display = "block";
        documentInfo.innerHTML = `
            <strong>Document:</strong> ${data.filename}<br>
            <strong>Chunks:</strong> ${data.total_chunks} | 
            <strong>Text Length:</strong> ${data.extracted_text_length} characters
        `;
        messages.innerHTML = "";
        questionInput.value = "";

        // Hide upload area
        uploadArea.style.display = "none";

    } catch (error) {
        showStatus(`❌ Error: ${error.message}`, "error");
        uploadProgress.style.display = "none";
    }
}

function updateProgress(percent) {
    uploadProgress.querySelector(".progress-fill").style.width = percent + "%";
}

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status-message ${type}`;
    uploadStatus.style.display = "block";
}

// Question Handler
async function handleAskQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) return;
    if (!currentDocumentId) {
        showStatus("❌ Please upload a document first", "error");
        return;
    }

    // Add user message
    addMessage(question, "user");
    questionInput.value = "";
    askBtn.disabled = true;

    // Add loading indicator
    const loadingId = addMessage('Thinking...', "assistant");

    try {
        const response = await fetch(`${API_BASE}/queries/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                document_id: currentDocumentId
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Query failed");
        }

        const data = await response.json();

        // Build answer message
        let answerText = data.answer;
        if (data.sources && data.sources.length > 0) {
            answerText += `\n\n📚 Sources (${data.sources.length}):`;n            data.sources.forEach((source) => {
                answerText += `\n• Page ${source.page_number} (Relevance: ${(source.relevance_score * 100).toFixed(0)}%)`;
            });
        }
        answerText += `\n\n📊 Confidence: ${(data.confidence_score * 100).toFixed(0)}%`;

        // Remove loading and add answer
        removeMessage(loadingId);
        addMessage(answerText, "assistant");

    } catch (error) {
        removeMessage(loadingId);
        addMessage(`❌ Error: ${error.message}`, "error");
    } finally {
        askBtn.disabled = false;
        questionInput.focus();
    }
}

// Message Display
function addMessage(text, role) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    messageDiv.id = `msg-${Date.now()}-${Math.random()}`;
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
    return messageDiv.id;
}

function removeMessage(messageId) {
    const msg = document.getElementById(messageId);
    if (msg) msg.remove();
}

function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}
