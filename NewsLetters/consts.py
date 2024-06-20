# Error messages
ERROR_INVALID_JSON = "Invalid JSON format"
ERROR_MISSING_FIELD = "Missing required field: {}"
ERROR_TOPIC_NOT_EXIST = 'Topic "{}" does not exist'
ERROR_DATA_INTEGRITY = "Data integrity error"
ERROR_ONLY_POST_ALLOWED = "Only POST requests are allowed"
ERROR_ONLY_DELETE_ALLOWED = "Only DELETE requests are allowed"

# GENERIC STRING
STR_ERROR = "error"
STR_SUCCESS = "success"
STR_MESSAGE = "message"
STR_STATUS = "status"
STR_ID = "id"
STR_NAME = "name"
STR_SUBSCRIBED_SUCCESSFULLY = "Subscribed successfully"
STR_CONTENT_ADDED_SUCCESSFULLY = "Content added successfully"
STR_EMAIL_SENT_SUCCESSFULLY = "email successfully sent to {}"
STR_NEWSLETTER_TASK_TRIGGERED = "Newsletter task triggered"
STR_NEWSLETTER_TASK_ERROR = "Newsletter task failed"
STR_UNSUBSCRIBED_SUCCESSFULLY = "Unsubscribed successfully"
STR_EMAIL_NOT_SUBSCRIBED = "Email not subscribed"
STR_FAILED_TO_UNSUBSCRIBE = "Failed to Unsubscribe to email"

#   RESPONSE TYPE
RESPONSE_OK_200 = 200
RESPONSE_CREATED_201 = 201
RESPONSE_BAD_REQUEST_400 = 400
RESPONSE_NOT_FOUND_404 = 404
RESPONSE_METHOD_NOT_ALLOWED_405 = 405
RESPONSE_INTERNAL_SERVER_ERROR_500 = 500

# Request Types
METHOD_POST = 'POST'
METHOD_DELETE = 'DELETE'

# Keys
JSON_TOPIC_KEY = 'topic'
JSON_TOPICS_KEY = 'topics'
JSON_ID_KEY = 'id'
JSON_EMAIL_KEY = 'email'
JSON_TOPIC_NAME_KEY = 'topic_name'
JSON_CONTENT_TEXT_KEY = 'content_text'
JSON_SEND_TIME_KEY = 'send_time'

# MAIL CONSTANTS
SENDER_EMAIL = 'personanewsletter@gmail.com'

# Threading Constants
MAX_WORKERS_SEND_EMAIL = 1
