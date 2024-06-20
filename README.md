# PersonaNewsLetter

# Newsletter Service

This project is a Django-based newsletter service that allows users to subscribe to topics, add newsletter content, and send newsletters to subscribers.
## Functional Requirements
NOTE: FIND THE UML DIAGRAMS IN THE UML FOLDER IN THE PROJECT
- Three types of users: consumers ,producers and Site Admin.
- **Consumer:**
    - Subscribe to a particular topic using their email and the topic name.
    - Unsubscribe from a particular topic.
    - List all available topics.
- **Producer:**
    - Publish content to a particular topic.
    - Schedule the time to send the email.
    - The application should send the emails to all subscribers of the topic at the scheduled time.
- **Site Admin:**
    - Uses Admin interface to create/modify/delete specific limited topics(eg- sports, music etc.)

## Scoped Out

- Consumer:
    - Subscribe to multiple topics at the same time.
    - Unsubscribe from all topics (i.e., the newsletter).
    - Set the frequency of receiving the newsletter (optional).
- Producer:
    - Send the newsletter on demand as well.

## Non-Functional Requirements

- Handling of mail sending should be done asynchronously and should handle heavy load (use multi-threading or parallel processing).
- No persistence is required after sending the mail.
## Usage

To use the Newsletter Service, follow these steps: \
NOTE : USE POSTMAN COLLECTION ATTACHED IN THE PROJECT FOR EASE OF USE

1. **Add a Subscriber:**
    - Send a POST request to the `/add-subscriber/` endpoint with the subscriber's email and the topic they want to subscribe to.

2. **Remove a Subscriber:**
    - Send a DELETE request to the `/remove-subscriber/` endpoint with the subscriber's email and the topic they want to unsubscribe from.

3. **Add Content:**
    - Send a POST request to the `/add-content/` endpoint with the newsletter content, the time to send it, and the topic it belongs to.

4. **Trigger Send Newsletters:**
    A CronJob is running on the heroku client which send all the due emails every 10 minutes

5. **Get All Topics:**
    - Send a GET request to the `/get-all-topics/` endpoint to retrieve a list of all available topics.

## ToDos/Improvements

### Authentication and Authorization for Producers
- Implement authentication and authorization mechanisms for producers.
- Separate account entities for producers and administrators.

### Rate Limiting
- Limit the number of newsletters that a producer can send to prevent abuse.

### Content Entity
- Create a “Content” entity where producers create a content entity with an ID to solve repetition.

### Input Validation
- Ensure producers cannot enter a date that’s already passed (≥ now).
- Validate email addresses to ensure they are in the correct format.
- Ensure `send_time` is a valid date.

### Security
- Move hard-coded passkeys and emails into Heroku environment variables for better security.

### Database
- Migrate from the built-in SQLite3 to a separate database instance. The file system-based DB behaves strangely under concurrent writes.

### Logging
- Improve logging to capture more detailed information and errors.

### Documentation
- Integrate Swagger for better API documentation.
- Add detailed function documentation.

### Email Retry Logic
- Implement a retry logic (2-3 attempts) for email send failures to ensure reliability.

### Scoped Out Items
- Allow consumers to unsubscribe from all topics at once.
- Enable sending content to multiple topics at once.
- Allow subscription to multiple topics at once.


## API Endpoints

### Add Subscriber

- **URL:** `/add-subscriber/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "email": "subscriber@example.com",
    "topic": "<topic_name>"
  }
- **Response:**
  ```json
    {
    "message": "Subscribed successfully",
    "email": "subscriber@example.com",
    "topic": "Tech News"
    }

- **URL:** `/add-content/`
- **Method:** POST
- **Request Body:**
  ```json
    {
    "content_text": "New Tech Content",
    "send_time": "2023-12-31T23:59:59Z",
    "topic": "<topic_name>"
    }
- **Response:**
  ```json
    {
    "message": "Content added successfully",
    "content_text": "New Tech Content",
    "send_time": "2023-12-31T23:59:59Z",
    "topic_name": "Tech News"
    }

- **URL:** `/remove-subscriber/`
- **Method:** DELETE
- **Request Body:**
  ```json
  {
    "email": "subscriber@example.com",
    "topic": "<topic_name>"
  }
- **Response:**
  ```json
    {
    "message": "Unsubscribed successfully subscriber@example.com"
    }
- **URL:** `/get-all-topics/`
- **Method:** GET
- **Response:**
  ```json
    {
    "topics": [
    {
    "id": 1,
    "name": "Tech News"
    },
    {
    "id": 2,
    "name": "Health News"
    }
    ]
    }
