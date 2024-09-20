import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv

def is_valid(url):
    """Check if URL is valid"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """Get all links from a website"""
    urls = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Remove fragments and query string
            href = href.split('#')[0].split('?')[0]
            # Convert relative URL to absolute URL
            href = urljoin(url, href)
            if is_valid(href):
                urls.add(href)
    except Exception as e:
        print(f"Error occurred: {e}")
    return urls

def write_to_csv(file_name, urls):
    """Write URLs to a CSV file"""
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for url in urls:
            writer.writerow([url])

def write_to_text(file_name, urls):
    """Write URLs to a text file"""
    with open(file_name, 'a') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    url = input("Enter the URL of the website: ")
    urls = get_all_website_links(url)
    write_to_csv('urls.csv', urls)
    write_to_text('urls.txt', urls)
    print("URLs have been written to urls.csv and urls.txt files")