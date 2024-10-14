# Late Show API

## Introduction

The Late Show API is a Flask-RESTful application that manages data for a late-night talk show. It provides endpoints to interact with episodes, guests, and their appearances on the show.

## Features

- Manage episodes, guests, and appearances
- RESTful API endpoints for CRUD operations
- Data validation and error handling
- SQLite database for data persistence

## Requirements

- Python 3.7+
- Flask
- Flask-RESTful
- Flask-SQLAlchemy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/aggreyrc/Late-show
   cd Late show
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install flask flask-restful flask-sqlalchemy
   ```

4. Set up the database:
   ```
   cd server
   flask db init
   flask db migrate -m 'Initial Migration'
   flask db upgrade head
   ```

## Running the Application

To start the server, run:

```
python app.py
```

The API will be available at `http://127.0.0.1:5555/`.

## API Endpoints

### Episodes

- `GET /episodes`: List all episodes
- `GET /episodes/<id>`: Get details of a specific episode

### Guests

- `GET /guests`: List all guests

### Appearances

- `POST /appearances`: Create a new appearance

## Data Models

### Episode

- `id`: Integer (Primary Key)
- `date`: String
- `number`: Integer

### Guest

- `id`: Integer (Primary Key)
- `name`: String
- `occupation`: String

### Appearance

- `id`: Integer (Primary Key)
- `rating`: Integer (1-5)
- `episode_id`: Integer (Foreign Key to Episode)
- `guest_id`: Integer (Foreign Key to Guest)

## Error Handling

The API returns appropriate HTTP status codes and error messages for invalid requests or when resources are not found.

## Testing

You can test the API using tools like cURL, Postman, or by writing Python scripts that make HTTP requests.

Example cURL command:
```
curl http://127.0.0.1:5555/episodes
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
