from googlesearch import search
import requests
from bs4 import BeautifulSoup
import time

def extract_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 429:
             return {
            'url': "Exception Occurred",
            'title': 'Exception Occurred',
            'content': 'The engine was unable to get more information; please come back later .'
        }

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.text.strip() if soup.title else 'No Title'

        # Attempting to find main content using common tags
        content_tags = [
            'article',
            'main',
            'div[role="main"]',
            'div.content',
            'div#content',
            'div.main',
            'div.main-content',
            'div#main',
            'div#main-section',
            'section.main-section',
            'section#main-section'
        ]
        main_content = None
        for tag in content_tags:
                main_content = soup.select_one(tag)
                if main_content:
                    break
            
        if main_content is None:
                return None

            # Use '\n' as the separator to preserve visual separation of elements
        text_content = BeautifulSoup(str(main_content), 'html.parser').get_text(separator='\n', strip=True)
            
        return {
                'url': url,
                'title': title,
                'content': text_content  # Now returns text content with preserved line breaks
            }

    except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None

def search_and_extract(query, num_results=4):
    results = []
    urls_attempted = 0

    for url in search(query, num_results=num_results):
        if urls_attempted >= 4:
            break

        content = extract_content(url)
        urls_attempted += 1
        
        if content:
            results.append(content)
            break
        else:
            time.sleep(10)  # Wait for 10 seconds before trying the next URL

    if not results:
        # If no content was found after 4 attempts
        return {
            'url': url,
            'title': 'Exception Occurred',
            'content': 'The engine was unable to get the information content; please check this url for more.'
        }

    return results
