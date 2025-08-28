import requests
from openai import OpenAI
from dotenv import load_dotenv
from urllib.parse import urljoin, urlparse
from typing import Optional


def build_robots_url(url: str) -> str:
    """Build the robots.txt URL from a base URL."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # Ensure we have a proper base URL
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    return urljoin(url, 'robots.txt')


def fetch_robots_txt(url: str) -> Optional[str]:
    """
    Fetch the robots.txt file from the given URL.

    Args:
        url: The base URL to fetch robots.txt from

    Returns:
        The robots.txt content as string, or None if failed

    Raises:
        ValueError: If the URL is invalid
        requests.RequestException: If the HTTP request fails
    """
    robots_url = build_robots_url(url)

    response = requests.get(robots_url, timeout=10)
    response.raise_for_status()

    return response.text


def analyze_robots_txt(content: str, model: str = "gpt-4o-mini") -> Optional[str]:
    """
    Use OpenAI to generate a structured, human-readable analysis of robots.txt content.

    Args:
        content: The robots.txt content to analyze
        model: The OpenAI model to use

    Returns:
        The generated structured analysis, or None if failed
    """
    prompt = (
        "You are an expert web crawler analyst. Analyze this robots.txt file and provide a clear, "
        "human-friendly explanation. Use this exact format with proper HTML-like structure:\n\n"
        "<h3>🤖 Robot Access Rules</h3>\n"
        "<ul>\n"
        "<li><strong>Allowed Robots:</strong> [List which search engines/crawlers are welcome]</li>\n"
        "<li><strong>Restricted Robots:</strong> [List which ones have limitations]</li>\n"
        "<li><strong>Special Rules:</strong> [Any unique restrictions or allowances]</li>\n"
        "</ul>\n\n"
        "<h3>🚫 Blocked Pages/Areas</h3>\n"
        "<p>[Explain what directories or pages are off-limits to crawlers in simple terms]</p>\n\n"
        "<h3>✅ Accessible Content</h3>\n"
        "<p>[Describe what content search engines can generally access]</p>\n\n"
        "<h3>💡 Key Insights</h3>\n"
        "<p>[Highlight the most important things developers or SEO specialists should know]</p>\n\n"
        "<h3>📊 Crawl Behavior</h3>\n"
        "<p>[Note any crawl-delay settings or special crawling instructions]</p>\n\n"
        "Robots.txt content:\n"
        f"{content}\n\n"
        "IMPORTANT: Use the exact HTML-like format above. Be conversational and helpful, not technical. "
        "Explain things in simple terms that non-technical people can understand."
    )

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a friendly, expert web crawler analyst who explains robots.txt files in a clear, structured way that non-technical people can understand. Always use the exact format requested and be conversational."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating structured description: {e}")
        return None
