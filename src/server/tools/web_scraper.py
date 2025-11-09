import json
from typing import Literal
from utils.scraper import (
    fetch_url,
    extract_text as extract_text_util,
    extract_links as extract_links_util,
    extract_metadata as extract_metadata_util,
    extract_structured_data as extract_structured_data_util,
)


async def scrape_url(url: str, selector: str = None) -> str:
    """
    Fetch and extract text content from a URL. Can optionally use CSS selectors to target specific elements.

    Args:
        url: The URL to scrape
        selector: Optional CSS selector to extract specific elements (e.g., '.article-content', '#main', 'p.description')

    Returns:
        Extracted text content from the webpage
    """
    html = await fetch_url(url)
    text = extract_text_util(html, selector)

    result = f"Content from {url}:\n\n{text}"
    return result


async def extract_links(url: str) -> str:
    """
    Extract all links from a webpage with their text and titles.

    Args:
        url: The URL to extract links from

    Returns:
        JSON formatted list of links with their text and titles
    """
    html = await fetch_url(url)
    links = extract_links_util(html, url)

    result = f"Found {len(links)} links on {url}:\n\n"
    result += json.dumps(links, indent=2)

    return result


async def extract_metadata(url: str) -> str:
    """
    Extract metadata from a webpage including title, description, and Open Graph tags.

    Args:
        url: The URL to extract metadata from

    Returns:
        JSON formatted metadata (title, description, keywords, author, og tags)
    """
    html = await fetch_url(url)
    metadata = extract_metadata_util(html)

    result = f"Metadata from {url}:\n\n"
    result += json.dumps(metadata, indent=2)

    return result


async def extract_structured_data(
    url: str, type: Literal["tables", "headings", "lists"]
) -> str:
    """
    Extract structured data like tables, headings, or lists from a webpage.

    Args:
        url: The URL to scrape
        type: Type of structured data to extract (tables, headings, or lists)

    Returns:
        JSON formatted structured data
    """
    html = await fetch_url(url)
    data = extract_structured_data_util(html, type)

    result = f"Extracted {type} from {url}:\n\n"
    result += json.dumps(data, indent=2)

    return result
