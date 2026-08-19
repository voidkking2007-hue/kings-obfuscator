from flask import Flask, render_template, request
import re
import random

app = Flask(__name__)

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

@app.route("/", methods=["GET", "POST"])
def index():
    obfuscated_code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        if code:
            # Eliminare comentarii
            code = re.sub(r'--.*', '', code)
            def replace_string(match):
                return '"' + text_to_hex(match.group(1)) + '"'
            code = re.sub(r'"([^"]*)"', replace_string, code)
            obfuscated_code = code
    return render_template("index.html", obfuscated_code=obfuscated_code)

if __name__ == "__main__":
    app.run(debug=True)
