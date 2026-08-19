from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

# Lista ta de chei VIP
VALID_VIP_KEYS = ["KING2026", "VIP_ROBLOX", "SECRET_KEY_123"]

def get_limiter_key():
    # Dacă utilizatorul a introdus o cheie validă, îi dăm un ID unic de VIP
    key = request.form.get("vip_key")
    if key in VALID_VIP_KEYS:
        return "VIP_USER"
    # Altfel, folosim IP-ul pentru limitare normală
    return get_remote_address()

limiter = Limiter(
    key_func=get_limiter_key,
    app=app,
    default_limits=["2 per day"],
    storage_uri="memory://"
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("index.html", obfuscated="-- [!] Limita atinsă! Introdu o cheie VIP pentru acces nelimitat.")

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

@app.route("/", methods=["GET", "POST"])
@limiter.limit("2 per day", methods=["POST"], key_func=get_limiter_key)
def index():
    obfuscated = ""
    if request.method == "POST":
        code = request.form.get("lua_code", "")
        if code:
            code = re.sub(r'--.*', '', code)
            def replace_string(match):
                return '"' + text_to_hex(match.group(1)) + '"'
            code = re.sub(r'"([^"]*)"', replace_string, code)
            obfuscated = code
    return render_template("index.html", obfuscated=obfuscated)

if __name__ == "__main__":
    app.run(debug=True)
