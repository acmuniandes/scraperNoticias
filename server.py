import os
import redis
from flask import Flask , send_from_directory

r = redis.from_url(os.environ.get('REDIS_URL'))

app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return "Helloooo World!"

@app.route("/news")
def show():
    return r.get('news').decode('utf8')

@app.route("/<path:path>")
def serve_file(path):
    app.logger.debug(path)
    return send_from_directory('public', path)

if __name__ == "__main__":
    app.run()
