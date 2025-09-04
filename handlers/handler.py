import os

def root_handler():
    return "200 OK", "<h1>Welcome to HTTP server :)</h1><h4>Developed by Thush</h4>", {"Content-Type": "text/html"}


def echo_handler(request):
    parts = request.path.strip("/").split("/")
    message = parts[1] if len(parts) > 1 else ""
    return "200 OK", message, {"Content-Type": "text/plain"}


def user_agent_handler(request):
    ua = request.headers.get("User-Agent", "No user-agent found")
    return "200 OK", ua, {"Content-Type": "text/plain"}


def files_get_handler(request):
    parts = request.path.strip("/").split("/")
    if len(parts) < 2:
        return "400 Bad Request", "<h1>400 Bad Request</h1>", {"Content-Type": "text/html"}

    file_path = "/".join(parts[1:])
    if not os.path.isfile(file_path):
        return "404 Not Found", "<h1>404 File Not Found</h1>", {"Content-Type": "text/html"}

    try:
        with open(file_path, "rb") as f:
            return "200 OK", f.read(), {"Content-Type": "application/octet-stream"}
    except Exception:
        return "500 Internal Server Error", "<h1>Internal Server Error</h1>", {"Content-Type": "text/html"}


def files_post_handler(request):
    parts = request.path.strip("/").split("/")
    if len(parts) < 2:
        return "400 Bad Request", "File creation failed", {"Content-Type": "text/plain"}

    file_path = "/".join(parts[1:])
    try:
        with open(file_path, "wb") as f:
            f.write(request.body)
        return "201 Created", f"File {file_path} created", {"Content-Type": "text/plain"}
    except Exception:
        return "500 Internal Server Error", "Could not create file", {"Content-Type": "text/plain"}

