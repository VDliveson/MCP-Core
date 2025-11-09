# Web Scraping MCP Server

A Model Context Protocol server that provides web scraping capabilities using BeautifulSoup and aiohttp.

## Features

- **scrape_url**: Extract text content from any webpage with optional CSS selectors
- **extract_links**: Get all links from a page with their text and titles
- **extract_metadata**: Extract page metadata (title, description, Open Graph tags)
- **extract_structured_data**: Extract tables, headings, or lists in structured format

## Installation

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python server.py
```

Make sure to replace `/absolute/path/to/server.py` with the actual path to your server file.

## Tool Examples

### 1. Scrape Full Page Content
```
Use the scrape_url tool to get the content from https://example.com
```

### 2. Extract Specific Elements
```
Use the scrape_url tool with selector ".article-content" from https://news.example.com
```

### 3. Get All Links
```
Use the extract_links tool to find all links on https://example.com
```

### 4. Extract Metadata
```
Use the extract_metadata tool to get metadata from https://example.com
```

### 5. Extract Tables
```
Use the extract_structured_data tool with type "tables" from https://example.com
```

## Dependencies

- **mcp**: Model Context Protocol SDK
- **beautifulsoup4**: HTML parsing and scraping
- **aiohttp**: Async HTTP client
- **lxml**: Fast HTML parser backend

## License

MIT License