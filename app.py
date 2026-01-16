import sys
import re
import threading
import webbrowser
import time
from flask import Flask, request, render_template_string

# Initialize Flask App
app = Flask(__name__)

# Modern Professional UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>String Sanitizer Tool</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --danger: #ef4444;
            --border: #334155;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: flex-start; /* Allows scrolling */
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            width: 100%;
            max-width: 600px;
            background-color: var(--card-bg);
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            margin-top: 5vh;
            border: 1px solid var(--border);
        }

        h1 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-main);
            text-align: center;
        }

        .subtitle {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        textarea, input[type="text"] {
            background-color: var(--bg-color);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 12px 16px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.2s;
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        textarea:focus, input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        button.submit-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.2s, transform 0.1s;
            margin-top: 10px;
        }

        button.submit-btn:hover {
            background-color: var(--primary-hover);
        }

        button.submit-btn:active {
            transform: translateY(1px);
        }

        /* Result Section */
        .result-container {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            animation: fadeIn 0.4s ease-out;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .result-box {
            background-color: rgba(15, 23, 42, 0.5);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.95rem;
            word-break: break-word;
            white-space: pre-wrap;
        }

        .copy-btn {
            background-color: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .copy-btn:hover {
            background-color: var(--bg-color);
            color: var(--text-main);
            border-color: var(--text-muted);
        }

        .error-message {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1.5rem;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Sanitizer</h1>
        <p class="subtitle">Securely remove specific words from your text.</p>

        <form method="POST">
            <div class="form-group">
                <label for="sentence">Source Text</label>
                <textarea id="sentence" name="sentence" placeholder="Paste your text here..." required autofocus>{{ original_text if original_text else '' }}</textarea>
            </div>
            
            <div class="form-group">
                <label for="word">Word to Remove</label>
                <input type="text" id="word" name="word" placeholder="e.g. Secret" required value="{{ target_word if target_word else '' }}">
            </div>
            
            <button type="submit" class="submit-btn">Process Text</button>
        </form>

        {% if error %}
            <div class="error-message">
                <strong>Error:</strong> {{ error }}
            </div>
        {% endif %}

        {% if result %}
            <div class="result-container">
                <div class="result-header">
                    <label>Cleaned Output</label>
                    <button class="copy-btn" onclick="copyToClipboard()">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        Copy Result
                    </button>
                </div>
                <div class="result-box" id="result-text">{{ result }}</div>
            </div>
        {% endif %}
    </div>

    <script>
        function copyToClipboard() {
            const text = document.getElementById('result-text').innerText;
            navigator.clipboard.writeText(text).then(() => {
                const btn = document.querySelector('.copy-btn');
                const originalContent = btn.innerHTML;
                
                // Visual feedback
                btn.style.borderColor = '#10b981';
                btn.style.color = '#10b981';
                btn.innerHTML = '<span>Copied!</span>';
                
                setTimeout(() => {
                    btn.innerHTML = originalContent;
                    btn.style.borderColor = '';
                    btn.style.color = '';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    original_text = ""
    target_word = ""

    if request.method == 'POST':
        original_text = request.form.get('sentence', '')
        target_word = request.form.get('word', '')

        # 1. Validation: Empty inputs check
        if not original_text or not target_word:
             error = "Input data is missing."
        
        else:
            # 2. Processing: Case insensitive removal
            try:
                # re.escape handles special characters safely
                # Using 3rd argument for flags inside compile or directly in sub
                modified_sentence = re.sub(
                    re.escape(target_word), 
                    '', 
                    original_text, 
                    flags=re.IGNORECASE
                )
                result = modified_sentence
            except Exception as e:
                error = f"Processing Error: {str(e)}"

    return render_template_string(
        HTML_TEMPLATE, 
        result=result, 
        error=error,
        original_text=original_text,
        target_word=target_word
    )

def open_browser():
    """Opens the browser automatically after a short delay"""
    time.sleep(1.5)
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the Flask server
    app.run(port=5000, debug=False)
