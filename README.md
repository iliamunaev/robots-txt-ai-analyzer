# robots-txt-ai-analyzer

A Python tool to fetch and explain any website's `robots.txt` file using OpenAI's GPT models.

---

## What is robots.txt?

A `robots.txt` file is a standard used by websites to communicate with web crawlers (also known as web robots, wanderers, spiders). It tells these bots which parts of the site they are allowed or not allowed to access. This is called the Robots Exclusion Protocol.

- **User-agent:** Specifies which robot the rule applies to (e.g., `*` means all robots).
- **Disallow:** Tells the robot not to visit certain pages or directories.
- **Allow:** (Optional) Tells the robot it can visit specific pages, even if a broader disallow rule exists.

For more details:
- [Robots Exclusion Protocol](https://www.robotstxt.org/)
- [Original Specification](https://www.robotstxt.org/orig.html)
- [Google's Guide](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt#create_rules)

---

## How it works

This tool:
1. Downloads the `robots.txt` file from any website.
2. Uses OpenAI's GPT model to generate a human-readable summary of the rules.

---

## Usage

1. **Set your OpenAI API key**
   Create a `.env` file in the project directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Run the script**
   Example:
   ```bash
   python robot_txt_analyzer.py
   ```
   By default, the script fetches and explains the `robots.txt` for `www.kone.fi`.
   You can modify the script to analyze any site by changing the URL in the last line.

---

## Example Output
Analyzing robots.txt for: www.kone.fi
Status: Successfully fetched robots.txt (692 characters)

AI Analysis:
==================================================
### Summary of robots.txt Rules

1. **User-Agent: Swiftbot**
   - **Allowed:** All pages (no restrictions).

2. **User-Agent: * (All Other Bots)**
   - **Disallowed Pages:**
     - `/sureroute-test-object.html`
     - Any URL ending with `/404.aspx`
     - Any URL ending with `/500.aspx`
     - Any URL starting with `/?*` (query parameters)
     - Any URL ending with `*.aspx?*`
     - Any URL ending with `*.pdf?*`
     - URLs containing the following query parameters:
       - `?country`
       - `?cpUrl`
       - `?ens_consent=`
       - `?tfa_next`
       - `?rdrsrc=`
       - `?aspxerrorpath`
       - `?storytype`
       - `?persona`
       - `?custom-tag`
       - `?id`
     - URLs containing `/searchresults*`
     - URLs containing `/studio/tool*`
     - URLs containing `?expandMenu=true*`

   - **Allowed Pages:**
     - JavaScript files: `/Scripts/*.js?*`
     - CSS files: `/Content/*.css?*`
     - Global JavaScript files: `/kone/global/*.js?*`
     - Any URL with `?v=*`
     - Any URL with `?&page=*`

3. **Sitemap:**
   - The sitemap is located at: `https://www.kone.fi/sitemap.xml`

### Important Notes:
- Swiftbot has no restrictions and can access all content.
- All other user agents are heavily restricted from accessing specific pages and query parameters, which helps control the crawling and indexing behavior on the site.
==================================================

---

## Notes

- This tool is for educational and research purposes.
- Always respect website owners' wishes as expressed in their `robots.txt` files.
- For more info, see [robots.txt documentation](https://www.robotstxt.org/).
