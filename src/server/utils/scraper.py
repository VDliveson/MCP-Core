import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin


async def fetch_url(url: str, timeout: int = 30) -> str:
    """
    Fetch URL content asynchronously

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        HTML content as string

    Raises:
        aiohttp.ClientError: On network errors
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            return await response.text()


def extract_text(html: str, selector: str = None) -> str:
    """
    Extract text from HTML using BeautifulSoup

    Args:
        html: HTML content
        selector: Optional CSS selector to target specific elements

    Returns:
        Extracted text content
    """
    soup = BeautifulSoup(html, "html.parser")

    if selector:
        elements = soup.select(selector)
        return "\n\n".join([elem.get_text(strip=True) for elem in elements])

    # Remove script, style, and navigation elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()

    return soup.get_text(separator="\n", strip=True)


def extract_links(html: str, base_url: str) -> list:
    """
    Extract all links from HTML

    Args:
        html: HTML content
        base_url: Base URL for resolving relative links

    Returns:
        List of dicts with url, text, and title for each link
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for link in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, link["href"])
        links.append(
            {
                "url": absolute_url,
                "text": link.get_text(strip=True),
                "title": link.get("title", ""),
            }
        )

    return links


def extract_metadata(html: str) -> dict:
    """
    Extract metadata from HTML (title, meta tags, Open Graph)

    Args:
        html: HTML content

    Returns:
        Dict containing metadata fields
    """
    soup = BeautifulSoup(html, "html.parser")

    metadata = {
        "title": "",
        "description": "",
        "keywords": "",
        "author": "",
        "og_title": "",
        "og_description": "",
        "og_image": "",
    }

    # Extract title
    if soup.title:
        metadata["title"] = soup.title.string

    # Extract meta tags
    meta_tags = {
        "description": ["name", "description"],
        "keywords": ["name", "keywords"],
        "author": ["name", "author"],
        "og_title": ["property", "og:title"],
        "og_description": ["property", "og:description"],
        "og_image": ["property", "og:image"],
    }

    for key, (attr, value) in meta_tags.items():
        tag = soup.find("meta", attrs={attr: value})
        if tag and tag.get("content"):
            metadata[key] = tag["content"]

    return metadata


def extract_structured_data(html: str, structure_type: str) -> list:
    """
    Extract structured data like tables, lists, or headings

    Args:
        html: HTML content
        structure_type: Type of structure ('tables', 'headings', or 'lists')

    Returns:
        List of structured data elements
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []

    if structure_type == "tables":
        tables = soup.find_all("table")
        for i, table in enumerate(tables):
            rows = []
            for row in table.find_all("tr"):
                cells = [
                    cell.get_text(strip=True) for cell in row.find_all(["td", "th"])
                ]
                if cells:
                    rows.append(cells)
            if rows:
                results.append({"table_index": i, "data": rows})

    elif structure_type == "headings":
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            results.append(
                {"level": heading.name, "text": heading.get_text(strip=True)}
            )

    elif structure_type == "lists":
        for list_elem in soup.find_all(["ul", "ol"]):
            items = [
                li.get_text(strip=True)
                for li in list_elem.find_all("li", recursive=False)
            ]
            if items:
                results.append({"type": list_elem.name, "items": items})

    return results
