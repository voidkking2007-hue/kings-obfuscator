from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import random

app = Flask(__name__)

# Codul tău secret (schimbă-l cu ce vrei tu)
ADMIN_KEY = "ParolaMeaSecreta123"

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("index.html", obfuscated_code="-- [!] Ai epuizat cele 2 încercări gratuite! Revino mâine.")

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

@app.route("/", methods=["GET", "POST"])
@limiter.limit("2 per day", methods=["POST"], key_func=lambda: "admin" if request.form.get("admin_key") == ADMIN_KEY else get_remote_address())
def index():
    obfuscated_code = ""
    if request.method == "POST":
        # Verificăm dacă ai introdus codul secret
        if request.form.get("admin_key") == ADMIN_KEY:
            # Bypass - acces nelimitat
            pass
        
        code = request.form.get("code", "")
        code = re.sub(r'--.*', '', code)
        def replace_string(match):
            return '"' + text_to_hex(match.group(1)) + '"'
        code = re.sub(r'"([^"]*)"', replace_string, code)
        obfuscated_code = code
        
    return render_template("index.html", obfuscated_code=obfuscated_code)

if __name__ == "__main__":
    app.run(debug=True)
