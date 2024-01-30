
from bs4 import BeautifulSoup
import requests
import re

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def find_line_number(html_content, position):
    return html_content.count('\n', 0, position) + 1

def detect_modifications(html_content):

    #Sprawdzanie potencjalnej zmiany XSS
    xss_pattern = [
    r'<script.*?>.*?</script>',
    r'<body\s+onload=.*?>',
    r'<b\s+onmouseover=.*?>',
    r'<body\s+onbeforeprint=.*?>',
    r'<details\s+ontoggle=.*?>.*?</details>',
    r'<marquee\s+onstart=.*?>.*?</marquee>']

    xss_pattern_combined = '|'.join(xss_pattern)

    for match in re.finditer(xss_pattern_combined, html_content, re.IGNORECASE):
        line_number = find_line_number(html_content, match.start())
        print(f"Potential XSS attack detected on line {line_number}: {match.group()}")

    #Sprawdzanie potencjalnej zmiany PHP
    php_patterns = [
        r'<\?php.*malicious_code.*\?>', 
        r'<\?php.*echo.*\?>' 
    ]
    for pattern in php_patterns:
        malicious_php_code = re.compile(pattern, re.DOTALL)
        for match in malicious_php_code.finditer(html_content):
            line_number = find_line_number(html_content, match.start())
            print(f"Possible malicious PHP code detected on line {line_number}: {match.group()}")

    #Sprawdzanie potencjalnych linków
    malicious_link_patterns = [
        r'https?://[^/]*malicious_site',
        r'https?://[^/]*'
    ]
    for pattern in malicious_link_patterns:
        malicious_link = re.compile(pattern)
        for match in malicious_link.finditer(html_content):
            line_number = find_line_number(html_content, match.start())
            print(f"Possible malicious link detected on line {line_number}: {match.group()}")

if __name__ == "__main__":
    url = input("Podaj URL Storny: ")
    page_content = fetch_page_content(url)

    if page_content:
        detect_modifications(page_content)
    else:
        print("Failed to retrieve page content.")
