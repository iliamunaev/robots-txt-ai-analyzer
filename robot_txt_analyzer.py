import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
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
    Use OpenAI to generate a human-readable description of robots.txt content.

    Args:
        content: The robots.txt content to analyze
        model: The OpenAI model to use

    Returns:
        The generated description, or None if failed
    """
    prompt = (
        "You are an expert web crawler analyst. "
        "Given the following robots.txt file content, provide a concise, human-readable summary of the rules, "
        "including which user-agents are allowed or disallowed, and any important notes:\n\n"
        f"{content}\n\n"
        "Summary:"
    )

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains robots.txt files."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating description: {e}")
        return None


def analyze_robots_txt_with_structured_prompt(content: str, model: str = "gpt-4o-mini") -> Optional[str]:
    """
    Use OpenAI to generate a structured, human-readable analysis of robots.txt content.

    Args:
        content: The robots.txt content to analyze
        model: The OpenAI model to use

    Returns:
        The generated structured analysis, or None if failed
    """
    prompt = (
        "You are an expert web crawler analyst. Analyze this robots.txt file and provide a structured, "
        "human-friendly explanation. Follow this format exactly:\n\n"
        "**General Overview**\n"
        "Provide a brief, friendly summary of what this robots.txt file does.\n\n"
        "** Robot Access Rules**\n"
        "• **Allowed Robots:** List which search engines/crawlers are welcome\n"
        "• **Restricted Robots:** List which ones have limitations\n"
        "• **Special Rules:** Any unique restrictions or allowances\n\n"
        "** Blocked Pages/Areas**\n"
        "List the main directories or pages that are off-limits to crawlers.\n\n"
        "** Accessible Areas**\n"
        "Mention what content is generally accessible to search engines.\n\n"
        "** Key Insights**\n"
        "Highlight the most important things developers or SEO specialists should know.\n\n"
        "** Crawl Behavior**\n"
        "Note any crawl-delay settings or special crawling instructions.\n\n"
        "Robots.txt content:\n"
        f"{content}\n\n"
        "Provide your analysis in the exact format above, being conversational and helpful rather than technical."
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
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating structured description: {e}")
        return None


def analyze_website_robots(url: str, model: str = "gpt-4o-mini") -> None:
    """
    Fetch and analyze robots.txt for a given website.

    Args:
        url: The website URL to analyze
        model: The OpenAI model to use for analysis
    """
    try:
        print(f"Analyzing robots.txt for: {url}")

        # Fetch robots.txt
        content = fetch_robots_txt(url)
        if content is None:
            return

        print(f"Status: Successfully fetched robots.txt ({len(content)} characters)")

        # Analyze content
        description = analyze_robots_txt(content, model)
        if description:
            print("\nAI Analysis:")
            print("=" * 50)
            print(description)
            print("=" * 50)

    except ValueError as e:
        print(f"Error: {e}")
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Main function to run the robots.txt analyzer."""
    # Load environment variables
    load_dotenv()

    # Check for required environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in .env file.")
        print("AI analysis will not be available.")
        return

    # Get model from environment or use default
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Example usage
    website = 'www.kone.fi'
    analyze_website_robots(website, model)


if __name__ == "__main__":
    main()
