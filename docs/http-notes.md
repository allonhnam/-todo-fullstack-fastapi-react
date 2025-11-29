What is an HTTP request?

An HTTP request is a message sent by a client (like a web browser or mobile app) to a server to request a specific action or resource. It consists of:
- **Request line**: Contains the HTTP method (GET, POST, etc.), the URL/path, and HTTP version
- **Headers**: Metadata about the request (Content-Type, Authorization, User-Agent, etc.)
- **Body** (optional): Data sent with the request (used in POST, PUT, PATCH requests)

Example: When you visit a website, your browser sends an HTTP GET request to the server asking for the webpage.

What is an HTTP response?

An HTTP response is a message sent by a server back to the client in reply to an HTTP request. It consists of:
- **Status line**: Contains the HTTP version, status code (200 OK, 404 Not Found, etc.), and status message
- **Headers**: Metadata about the response (Content-Type, Content-Length, Set-Cookie, etc.)
- **Body** (optional): The actual data/content being returned (HTML, JSON, images, etc.)

Example: After receiving a request, the server sends back an HTTP response with status code 200 and the requested webpage content.

Explain GET vs POST vs PUT vs DELETE.

These are HTTP methods that indicate the intended action:

- **GET**: Retrieves data from the server. Should not modify data (idempotent and safe). No request body. Example: Fetching a list of todos.

- **POST**: Creates new resources on the server. Not idempotent (calling twice may create duplicates). Includes request body. Example: Creating a new todo item.

- **PUT**: Updates or replaces an entire resource at a specific URL. Idempotent (calling multiple times has the same effect). Includes request body. Example: Replacing all fields of a todo item.

- **DELETE**: Removes a resource from the server. Idempotent. Usually no request body. Example: Deleting a todo item.

Note: PATCH is another common method that partially updates a resource (unlike PUT which replaces the entire resource).

Describe the lifecycle:
 Browser → Frontend → Backend → Database → Backend → Frontend

1. **Browser**: User interacts with the web page (clicks a button, submits a form)
2. **Frontend**: JavaScript/React code captures the user action and makes an HTTP request (e.g., fetch API) to the backend
3. **Backend**: FastAPI receives the HTTP request, processes it, validates data, and may need to interact with the database
4. **Database**: Backend queries/updates the database (SELECT, INSERT, UPDATE, DELETE operations)
5. **Backend**: Receives data from database, processes it, formats the response (often as JSON), and sends HTTP response back
6. **Frontend**: Receives the HTTP response, parses the data, and updates the UI (React re-renders components with new data)
7. **Browser**: Displays the updated UI to the user

This cycle repeats for each user interaction that requires server-side processing.

Why do APIs use JSON?

APIs use JSON (JavaScript Object Notation) because:

1. **Human-readable**: Easy for developers to read and debug
2. **Language-agnostic**: Can be parsed by virtually any programming language
3. **Lightweight**: More compact than XML, reducing bandwidth usage
4. **Native JavaScript support**: JavaScript can directly parse JSON (JSON.parse()), making it perfect for web applications
5. **Structured data**: Supports objects, arrays, strings, numbers, booleans, and null - covering most data needs
6. **Standard format**: Widely adopted industry standard, making API integration easier
7. **Fast parsing**: Efficient to parse and generate compared to XML

Example: `{"id": 1, "title": "Buy groceries", "completed": false}` is much simpler than equivalent XML.
