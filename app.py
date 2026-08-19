from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import random

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("index.html", obfuscated_code="-- [!] Ai epuizat cele 2 încercări gratuite! Revino mâine pentru altele noi.")

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

@app.route("/", methods=["GET", "POST"])
@limiter.limit("2 per day", methods=["POST"])
def index():
    obfuscated_code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        code = re.sub(r'--.*', '', code)
        def replace_string(match):
            return '"' + text_to_hex(match.group(1)) + '"'
        code = re.sub(r'"([^"]*)"', replace_string, code)
        obfuscated_code = code
    return render_template("index.html", obfuscated_code=obfuscated_code)

if __name__ == "__main__":
    app.run(debug=True)
