import asyncio
import http.server
import socketserver
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import websockets
from pathlib import Path
from threading import Timer
import webbrowser
import argparse

####
# creates a local server that watches a python sketch file for changes. When the file
# changes, the website will refresh the code, but not refresh the entire site.
# this makes it much faster to iterate on changes (close to instant)
####


# This(whole file) is pretty hacky, there is certainly a cleaner way to do this... but it
# works fine for now

PORT = 8002
WEBSOCKET_PORT = 6780

root_dir = Path(__file__).resolve().parent.parent
print("Servig files at ", root_dir)
user_path = "../examples"


# Custom HTTPRequestHandler to inject JavaScript into HTML
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(root_dir), **kwargs)

    def end_headers(self):
        # Add headers to prevent caching
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        self.path = self.path.split("?")[0]

        # Check if the requested path is an HTML file or root
        # print(self.path)
        if self.path.endswith(".html") or self.path == "/":
            self.path = "/index.html" if self.path == "/" else self.path
            file_path = root_dir / self.path.strip("/")

            # Check if the file exists and is an HTML file
            if file_path.is_file() and file_path.suffix == ".html":
                # Read and modify the HTML content
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                modified_html = self.inject_javascript(html_content)

                # Send the response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header(
                    "Content-Length", str(len(modified_html.encode("utf-8")))
                )
                self.end_headers()
                self.wfile.write(modified_html.encode("utf-8"))
                return
        elif self.path.split("/")[1] == "user_file":
            # print(f"requested path: {self.path}")
            user_python_file_name = self.path.split("/")[2]
            relative_path = user_path + "/" + user_python_file_name
            self.path = os.path.abspath(relative_path)
            # Read and modify the HTML content
            with open(self.path, "r", encoding="utf-8") as file:
                content = file.read()
            # Send the response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(content.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
            return

        # Handle other requests normally
        super().do_GET()

    def inject_javascript(self, html_content):
        js_code = f"""
        <script>
        const socket = new WebSocket('ws://localhost:{WEBSOCKET_PORT}');
        socket.onmessage = function(event) {{
            if (event.data === 'browser_reload') {{
                window.location.reload();
            }} 
            else if (event.data === 'sketch_reload') {{
                reloadSketch();
            }} 
            else if (event.data === 'diver_reload') {{
                reloadDiver();
            }} 
            else {{
                console.log("Received custom command:", event.data);
            }}
        }};
        </script>
        """
        # Insert the JavaScript before the closing </body> tag
        return html_content.replace("</body>", js_code + "</body>")

    # turn off messages, because they are noisy, and not relevant here.
    # TODO add a verbose flag
    def log_message(self, format, *args):
        return


class TCPServerWithReuseAddr(socketserver.TCPServer):
    allow_reuse_address = True


# WebSocket server for live reload
async def reload_server(websocket, _):
    active_websockets.add(websocket)
    # if we need to handle messages from websocket:
    try:
        async for message in websocket:
            # Handle messages if needed
            pass
    finally:
        active_websockets.remove(websocket)


class ReloadEventHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop
        self.debounce_timer = None
        self.throttled_events = set()

    # def on_any_event(self, event):
    #     print(event)
    #     return super().on_any_event(event)

    def on_modified(self, event):
        file_name = os.path.basename(event.src_path)
        file_extension = os.path.splitext(file_name)[1]
        # Check if the file extension is one of the desired types

        if file_extension in [".html", ".js", ".css"]:
            message = "browser_reload"
        elif file_extension == ".py":
            if file_name == "diver.py":
                message = "diver_reload"
            elif file_name == "serve.py":
                print("server file changed, restart server to test changes")
                return
            else:
                message = "sketch_reload"
        else:
            return
        if message in self.throttled_events:
            return
        # we are good to run!
        print(event.src_path, " modified, sending message: ", message)
        self.trigger_reload(message)
        self.throttled_events.add(message)

        # could cause message to be removed multiple times,
        # but I think that's ok for now. Worse case we send an extra message
        Timer(1.0, lambda: self.throttled_events.discard(message)).start()

    def trigger_reload(self, message):
        asyncio.run_coroutine_threadsafe(self.broadcast_reload(message), self.loop)

    async def broadcast_reload(self, message):
        global reload_count
        for ws in active_websockets:
            reload_count = reload_count + 1
            await ws.send(message)


active_websockets = set()
reload_count = 0


def main():
    global user_path
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "python_sketch",
        type=str,
        help="This file will be run in the browser, and monitored for changes",
    )
    args = parser.parse_args()
    sketch_path = args.python_sketch
    print(sketch_path)
    abs_sketch_path = os.path.abspath(sketch_path)
    print(abs_sketch_path)
    sketch_file = os.path.basename(abs_sketch_path)
    print(sketch_file)
    user_path = os.path.dirname(abs_sketch_path)
    print(user_path)
    # Start the HTTP server
    httpd = TCPServerWithReuseAddr(("", PORT), CustomHTTPRequestHandler)
    url = f"http://localhost:{PORT}/?filename=user_file/{sketch_file}"
    print(f"Serving at {url}")
    webbrowser.open(url)

    asyncio.get_event_loop().run_in_executor(None, httpd.serve_forever)

    start_server = websockets.serve(reload_server, "localhost", WEBSOCKET_PORT)

    # Get the current event loop
    current_loop = asyncio.get_event_loop()

    # Start the file watcher with the event loop reference
    event_handler = ReloadEventHandler(current_loop)
    observer = Observer()
    observer.schedule(event_handler, path=str(root_dir), recursive=True)
    observer.schedule(event_handler, path=str(sketch_path))
    observer.start()

    # Run the WebSocket server
    current_loop.run_until_complete(start_server)
    current_loop.run_forever()


if __name__ == "__main__":
    main()
