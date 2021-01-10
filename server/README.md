# Snap Plan Web Server

## Dependencies

(Flask)[https://flask.palletsprojects.com/en/1.1.x/] is needed to run the web server.

## Build and Run

To run the server, executing the following commands are needed:
1. `export FLASK_APP=api` for Unix Bash or `set FLASK_APP=hello` for Windows CMD. This is for setting `FLASK_APP` environment variable, used to specify how to load the web server.
1. `flask run` to run the web server.

The app will run on port `http://localhost:5000`.

## Endpoints

The web server contains a single endpoint for knowing the current time.

### Request

**URL:** `GET:/time`

**Body Schema:**


```json
{}
```

### Response

```json
{
    "time": {
        "type": "number"
    }
}
```

