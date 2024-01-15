import requests

from bs4 import BeautifulSoup
from template import FAKE_HEADERS


def get_categories(url_home="https://cellphones.com.vn/",
                   headers=FAKE_HEADERS):
    request_data = requests.get(url_home, headers=headers)
    soup = BeautifulSoup(request_data.text, 'html.parser')
    all_href = [link for link in soup.find_all('a', href=True)]
    category_to_link = {" ".join(link.text.split()): link.get("href") for link in all_href if
                        link.text is not None and link.text != " " and len(link.get("href")) > 0}
    return category_to_link


def get_categories_html_text(category_url):
    request_data = requests.get(category_url, headers=FAKE_HEADERS)
    soup = BeautifulSoup(request_data.text, 'html.parser')
    return soup.text

