# Google Docs MCP Server 📝

A Model Context Protocol (MCP) server that provides seamless integration with Google Docs API. Create, read, and edit Google Documents programmatically with structured output and automatic authentication via Nango.

## ✨ Features

- **Complete Google Docs API Integration** - All major endpoints covered
- **Structured Output** - Type-safe responses using Pydantic models
- **Nango Authentication** - Automatic OAuth token management and refresh
- **Easy Document Operations** - Create, read, update, and batch edit documents
- **Error Handling** - Comprehensive error responses with detailed information
- **Helper Functions** - Convenient tools for common document operations
- **Modular Architecture** - Clean, maintainable code structure

## 🏗️ Project Structure

```
google-docs-mcp/
├── main.py                 # Single-file version (backward compatibility)
├── server.py               # Clean modular entry point
├── src/                    # Source code modules
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Pydantic models for structured output
│   ├── auth.py            # Nango authentication utilities
│   ├── api_client.py      # Google Docs API client
│   └── tools.py           # MCP tool definitions
├── tests/                  # Test files
├── examples/              # Usage examples
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- A Nango account with Google Docs integration configured
- Google Cloud Project with Docs API enabled

### Installation

1. **Clone the project**
   ```bash
   cd /path/to/work-projects
   git clone <repository-url> google-docs-mcp
   cd google-docs-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Nango credentials
   ```

4. **Run the server**
   ```bash
   # Using the modular version (recommended)
   python server.py
   
   # Or using the single-file version
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NANGO_CONNECTION_ID` | Your Nango connection ID | `conn_abc123` |
| `NANGO_INTEGRATION_ID` | Integration key in Nango | `google-docs` |
| `NANGO_BASE_URL` | Nango API base URL | `https://api.nango.dev` |
| `NANGO_SECRET_KEY` | Your Nango secret key | `nk_abc123...` |

### Setting up Nango

1. **Create a Nango account** at [nango.dev](https://nango.dev)
2. **Add Google Docs integration** in your Nango dashboard
3. **Configure OAuth scopes** (minimum required):
   - `https://www.googleapis.com/auth/documents`
4. **Create a connection** and note the connection ID
5. **Get your secret key** from the Nango dashboard

## 🛠 Available Tools

### Core Document Operations

#### `get_document(document_id: str)`
Retrieves the complete content of a Google Docs document.

**Parameters:**
- `document_id`: The ID of the document (found in the Google Docs URL)

**Returns:** Complete document structure with content, styling, and metadata

**Example:**
```python
# Get document content
doc = get_document("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
print(f"Title: {doc.title}")
print(f"Document ID: {doc.documentId}")
```

#### `create_document(title: str)`
Creates a new blank Google Docs document.

**Parameters:**
- `title`: Title for the new document (default: "Untitled document")

**Returns:** Created document information including new document ID

**Example:**
```python
# Create a new document
new_doc = create_document("My Project Report")
print(f"Created document with ID: {new_doc.documentId}")
```

#### `batch_update_document(document_id: str, requests_data: List[Dict], write_control: Optional[Dict])`
Applies multiple updates to a document in a single operation.

**Parameters:**
- `document_id`: Target document ID
- `requests_data`: List of update operations
- `write_control`: Optional write control settings

**Returns:** Update results and operation responses

### Helper Operations

#### `insert_text(document_id: str, text: str, index: int)`
Inserts text at a specific position in the document.

**Parameters:**
- `document_id`: Target document ID
- `text`: Text to insert
- `index`: Position to insert (1 = beginning, default)

**Example:**
```python
# Insert text at the beginning
insert_text("doc_id", "Hello, World!\n\n", 1)
```

#### `replace_all_text(document_id: str, find_text: str, replace_text: str, match_case: bool)`
Replaces all occurrences of specific text in the document.

**Parameters:**
- `document_id`: Target document ID
- `find_text`: Text to find
- `replace_text`: Replacement text
- `match_case`: Case-sensitive matching (default: False)

**Example:**
```python
# Replace all instances of "old" with "new"
replace_all_text("doc_id", "old text", "new text")
```

#### `delete_content_range(document_id: str, start_index: int, end_index: int)`
Deletes content within a specific range.

**Parameters:**
- `document_id`: Target document ID
- `start_index`: Start position of deletion
- `end_index`: End position of deletion

**Example:**
```python
# Delete characters from position 10 to 50
delete_content_range("doc_id", 10, 50)
```

### Utility Tools

#### `get_nango_connection_info()`
Checks your Nango connection status and credentials.

**Returns:** Connection information and credential status

**Example:**
```python
# Check connection status
info = get_nango_connection_info()
print(f"Connection ID: {info.connection_id}")
print(f"Has credentials: {'access_token' in info.credentials}")
```

## 📋 Common Use Cases

### Creating and Populating a New Document

```python
# Create a new document
doc = create_document("Weekly Report")
doc_id = doc.documentId

# Add title and content
insert_text(doc_id, "Weekly Report - Week 45\n\n", 1)
insert_text(doc_id, "## Summary\nThis week we accomplished...\n\n", -1)
insert_text(doc_id, "## Goals for Next Week\n- Complete project X\n- Review docs", -1)
```

### Batch Document Updates

```python
# Multiple operations in one request
updates = [
    {
        "insertText": {
            "location": {"index": 1},
            "text": "CONFIDENTIAL\n\n"
        }
    },
    {
        "updateTextStyle": {
            "range": {"startIndex": 1, "endIndex": 13},
            "textStyle": {"bold": True, "foregroundColor": {"color": {"rgbColor": {"red": 1.0}}}}
        }
    }
]

batch_update_document(doc_id, updates)
```

### Document Content Analysis

```python
# Get document and analyze content
doc = get_document("your_doc_id")

# Extract text content
if doc.body and doc.body.get("content"):
    for element in doc.body["content"]:
        if "paragraph" in element:
            # Process paragraph content
            pass
```

## 🔍 Document ID Location

You can find the document ID in the Google Docs URL:
```
https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
                                   ↑ This is the document ID ↑
```

## ⚠️ Error Handling

All tools return either a success response or an `ErrorResponse` object:

```python
result = get_document("invalid_id")

if hasattr(result, 'error'):
    print(f"Error: {result.error}")
    print(f"Status: {result.status_code}")
    print(f"Details: {result.details}")
else:
    print(f"Success! Document title: {result.title}")
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Code Structure

- **`src/models.py`** - Pydantic models for structured output
- **`src/auth.py`** - Nango authentication handling
- **`src/api_client.py`** - Google Docs API client utilities
- **`src/tools.py`** - MCP tool definitions
- **`server.py`** - Clean entry point using modular structure
- **`main.py`** - Single-file version for simple deployment

### Adding New Tools

1. Define the response model in `src/models.py`
2. Add API client function in `src/api_client.py`
3. Create the tool function in `src/tools.py`
4. Register the tool in the `register_tools()` function

## 🔐 Security & Permissions

- **OAuth Scopes**: Ensure your Nango integration has the required Google Docs scopes
- **Document Access**: You can only access documents you have permission to view/edit
- **Token Management**: Nango automatically handles token refresh and security
- **Rate Limits**: Google Docs API has rate limits - implement appropriate delays for bulk operations

## 🐛 Troubleshooting

### Common Issues

**"Failed to get credentials from Nango"**
- Check that all Nango environment variables are set correctly
- Verify your Nango connection is active and authorized
- Ensure the integration ID matches your Nango configuration

**"Document not found"**
- Verify the document ID is correct
- Check that you have access to the document
- Make sure the document hasn't been deleted

**"Insufficient permissions"**
- Ensure your Google account has edit access to the document
- Check that the OAuth scopes include document editing permissions

**"API request failed"**
- Check your internet connection
- Verify Google Docs API is enabled in your Google Cloud project
- Review the error details for specific API error messages

### Debug Connection

Use the connection info tool to debug authentication issues:

```python
info = get_nango_connection_info()
print(f"Connection status: {info}")
```

## 📚 Additional Resources

- [Google Docs API Documentation](https://developers.google.com/docs/api)
- [Nango Documentation](https://docs.nango.dev)
- [FastMCP Documentation](https://github.com/pydantic/fastmcp)
- [Model Context Protocol](https://github.com/anthropics/mcp)

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this MCP server.

## 📄 License

This project is open source and available under the MIT License.
