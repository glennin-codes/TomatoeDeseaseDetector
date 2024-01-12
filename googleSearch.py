from googlesearch import search
import requests
from bs4 import BeautifulSoup

def extract_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting title
        title = soup.title.text.strip() if soup.title else 'No Title'

        # Extracting main content (adjust 'div' to the appropriate tag)
        main_content = soup.findAll('div')

        # Convert the main content to HTML
        html_content = str(main_content) if main_content else 'No Content'
        harmful_text = "[<div id=\"error\">\n<p>Your bot have been rated as a harmful activity and will be blocked to prevent potential damage, please get in touch with support team: "
        if harmful_text not in html_content:
                return {
                    'url': url,
                    'title': title,
                    'content': html_content
                }

    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None
def search_and_extract(query, num_results):
    results = []

    for url in search(query, num_results=num_results):
        content = extract_content(url)
        if content:
            results.append(content)
            break

    return results

