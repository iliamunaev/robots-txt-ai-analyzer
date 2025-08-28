from flask import Flask, render_template, request, jsonify
from analyzer import fetch_robots_txt, analyze_robots_txt
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        website = data.get('website', '').strip()

        if not website:
            return jsonify({'error': 'Please provide a website URL'}), 400

        # Fetch robots.txt content
        content = fetch_robots_txt(website)
        if content is None:
            return jsonify({'error': 'Failed to fetch robots.txt'}), 500

        # Get AI analysis
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        description = analyze_robots_txt(content, model)

        if description is None:
            return jsonify({'error': 'Failed to generate AI analysis'}), 500

        return jsonify({
            'success': True,
            'website': website,
            'robots_content': content,
            'ai_analysis': description
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
