# Robots.txt AI Analyzer

A web application that fetches and intelligently analyzes any website's `robots.txt` file using OpenAI's GPT models.

---

## Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/iliamunaev/robots-txt-ai-analyzer.git
cd robots-txt-ai-analyzer
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Set Up OpenAI API Key**
Create a `.env` file in the project directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. **Run the Web Application**
```bash
python app.py
```

### 5. **Open Your Browser**
Navigate to: `http://localhost:5000`

---

## How to Use

1. **Enter a Website URL** (e.g., `www.example.com`)
2. **Click "Analyze robots.txt"** or press `Enter`
3. **View Results** in the three panels:
   - **Left**: Input controls and status
   - **Middle**: Raw robots.txt content
   - **Right**: AI-powered analysis with insights

---

## Technical Details

### **Backend**
- Python, Flask, OpenAI API, Requests, Python-dotenv

### **Frontend**
- simple MVP

## Project Structure

```
robots-txt-ai-analyzer/
├── app.py                 # Flask web application
├── analyzer.py  # Core robots.txt analysis logic
├── templates/
│   └── index.html        # Modern web interface
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            # This file
```
