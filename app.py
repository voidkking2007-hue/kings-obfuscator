from flask import Flask, render_template, request
import re

app = Flask(__name__)

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

@app.route("/", methods=["GET", "POST"])
def index():
    obfuscated = ""
    if request.method == "POST":
        # Preluăm corect din 'lua_code' (cum ai în HTML)
        code = request.form.get("lua_code", "")
        if code:
            # Eliminare comentarii
            code = re.sub(r'--.*', '', code)
            def replace_string(match):
                return '"' + text_to_hex(match.group(1)) + '"'
            code = re.sub(r'"([^"]*)"', replace_string, code)
            obfuscated = code
    return render_template("index.html", obfuscated=obfuscated)

if __name__ == "__main__":
    app.run(debug=True)
