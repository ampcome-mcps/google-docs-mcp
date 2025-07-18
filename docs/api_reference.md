# API Reference

## Models

### DocumentResponse

Complete response structure for document retrieval operations.

**Fields:**
- `documentId` (str): The ID of the document
- `title` (str): The title of the document  
- `body` (Optional[Dict]): The document body content
- `revisionId` (Optional[str]): The revision ID of the document
- `suggestionsViewMode` (Optional[str]): The suggestions view mode
- `namedRanges` (Optional[Dict]): Named ranges in the document
- `lists` (Optional[Dict]): Lists in the document
- `documentStyle` (Optional[Dict]): The document style
- `footers` (Optional[Dict]): Document footers
- `headers` (Optional[Dict]): Document headers
- `footnotes` (Optional[Dict]): Document footnotes
- `inlineObjects` (Optional[Dict]): Inline objects in the document
- `positionedObjects` (Optional[Dict]): Positioned objects in the document

### CreateDocumentResponse

Response structure for document creation operations.

**Fields:**
- `documentId` (str): The ID of the created document
- `title` (str): The title of the created document
- `revisionId` (str): The revision ID of the created document
- `body` (Optional[Dict]): The document body content

### BatchUpdateResponse

Response structure for batch update operations.

**Fields:**
- `documentId` (str): The ID of the updated document
- `writeControl` (Optional[Dict]): Write control information
- `replies` (Optional[List[Dict]]): Replies to the update requests

### NangoCredentials

Nango connection credentials structure.

**Fields:**
- `connection_id` (str): The Nango connection ID
- `provider_config_key` (str): The provider configuration key
- `credentials` (Dict): The OAuth credentials
- `metadata` (Optional[Dict]): Additional connection metadata

### ErrorResponse

Error response structure for failed operations.

**Fields:**
- `error` (str): Error message
- `status_code` (int): HTTP status code
- `details` (Optional[str]): Additional error details

## Tools

### get_document(document_id: str) -> DocumentResponse | ErrorResponse

Gets the latest version of the specified Google Docs document.

**Parameters:**
- `document_id`: The ID of the document to retrieve

**Returns:** DocumentResponse with document data or ErrorResponse if failed

### create_document(title: str = "Untitled document") -> CreateDocumentResponse | ErrorResponse

Creates a blank Google Docs document.

**Parameters:**
- `title`: The title for the new document

**Returns:** CreateDocumentResponse with created document data or ErrorResponse if failed

### batch_update_document(document_id: str, requests_data: List[Dict], write_control: Optional[Dict] = None) -> BatchUpdateResponse | ErrorResponse

Applies one or more updates to the Google Docs document.

**Parameters:**
- `document_id`: The ID of the document to update
- `requests_data`: List of update requests to apply
- `write_control`: Optional write control settings

**Returns:** BatchUpdateResponse with update results or ErrorResponse if failed

### insert_text(document_id: str, text: str, index: int = 1) -> BatchUpdateResponse | ErrorResponse

Inserts text at the specified index in the document.

**Parameters:**
- `document_id`: The ID of the document to update
- `text`: The text to insert
- `index`: The index where to insert the text

**Returns:** BatchUpdateResponse with update results or ErrorResponse if failed

### replace_all_text(document_id: str, find_text: str, replace_text: str, match_case: bool = False) -> BatchUpdateResponse | ErrorResponse

Replaces all instances of text in the document.

**Parameters:**
- `document_id`: The ID of the document to update
- `find_text`: The text to find and replace
- `replace_text`: The text to replace with
- `match_case`: Whether to match case when finding text

**Returns:** BatchUpdateResponse with update results or ErrorResponse if failed

### delete_content_range(document_id: str, start_index: int, end_index: int) -> BatchUpdateResponse | ErrorResponse

Deletes content in the specified range from the document.

**Parameters:**
- `document_id`: The ID of the document to update
- `start_index`: The start index of the range to delete
- `end_index`: The end index of the range to delete

**Returns:** BatchUpdateResponse with update results or ErrorResponse if failed

### get_nango_connection_info() -> NangoCredentials | ErrorResponse

Get current Nango connection information and credentials status.

**Returns:** NangoCredentials with connection info or ErrorResponse if failed

## Authentication

The server uses Nango for OAuth authentication with Google Docs API. The following environment variables are required:

- `NANGO_CONNECTION_ID`: Your Nango connection ID
- `NANGO_INTEGRATION_ID`: Integration key in Nango  
- `NANGO_BASE_URL`: Nango API base URL
- `NANGO_SECRET_KEY`: Your Nango secret key

Authentication is handled automatically for all API calls.

## Error Handling

All tools return either a success response with the appropriate model type or an ErrorResponse model containing:

- Error message
- HTTP status code  
- Additional error details (if available)

Always check the response type to handle errors appropriately.
