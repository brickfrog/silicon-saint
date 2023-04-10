import streamlit as st
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from typing import List
from urllib.parse import urlparse

class URL:
    def __init__(self, url: str):
        self.url = url
        self.parsed_url = urlparse(url)

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"URL('{self.url}')"

    def __eq__(self, other):
        return isinstance(other, URL) and self.url == other.url

    def __hash__(self):
        return hash(self.url)

@st.cache_data
def scrape_vatican_word(date: str) -> List:
    """Scrapes the Vatican's Word of the Day page for the given date."""

    url = f"https://www.vaticannews.va/en/word-of-the-day/{date}.html"

    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making a request: {e}")
        return []

    soup = BeautifulSoup(page.content, "html.parser")

    div_headers = soup.find_all("div", class_="section__head")
    div_content = soup.find_all("div", class_="section__content")

    if not div_headers or not div_content:
        print(f"No content found for date {date}")
        return []

    content = [
        str(header) + str(content) for header, content in zip(div_headers, div_content)
    ]

    return content


def scrape_vatican_saint(date: str) -> Tag:
    """Scrapes the Vatican's Saint of the Day page for the given date."""

    url = f"https://www.vaticannews.va/en/saints/{date[-5:]}.html"

    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making a request: {e}")
        return []

    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find_all("div", class_="section__head")

    return content


def verse_extract(text: str) -> List:
    """Extracts the verses from the Vatican's Word of the Day page."""

    soup = BeautifulSoup(text, "html.parser")
    p_tags = soup.find_all("p")
    verse_list = []

    for p in p_tags:
        text = p.get_text()

        if (
            "A reading" in text
            or "First reading" in text
            or "Second reading" in text
            or "From the" in text
        ):

            text = text.replace("A reading from the ", "")
            text = text.replace("First reading from the ", "")
            text = text.replace("Second reading from the ", "")

            verse_list.append(text)

    return verse_list


def extract_text(text: str) -> str:
    """A utility function to extract text from a BeautifulSoup based string."""
    soup = BeautifulSoup(text, "html.parser")
    p_tags = soup.find_all("p")
    text = ""

    for p in p_tags:
        text += p.get_text()

    return text
