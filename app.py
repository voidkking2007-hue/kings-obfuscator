from flask import Flask, render_template, request
import re
import random

app = Flask(__name__)

def text_to_hex(text):
    return "".join([f"\\x{ord(c):02x}" for c in text])

def generate_random_name(length=12):
    chars = "Il"
    return "".join(random.choice(chars) for _ in range(length))

def obfuscate_code(code):
    try:
        # 1. Eliminare comentarii
        code = re.sub(r'--.*', '', code)

        # 2. Codificare string-uri
        def replace_string(match):
            return '"' + text_to_hex(match.group(1)) + '"'
        code = re.sub(r'"([^"]*)"', replace_string, code)

        # 3. Redenumire variabile
        local_vars = set(re.findall(r'local\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code))
        var_map = {var: generate_random_name() for var in local_vars}
        for old_var, new_var in var_map.items():
            code = re.sub(rf'\b{old_var}\b', new_var, code)

        # 4. Minificare
        code = code.replace('\n', ' ')
        code = re.sub(r'\s+', ' ', code)

        return code.strip()
    except Exception as e:
        return f"-- A apărut o eroare la ofuscare: {e}"

# Ruta principală a site-ului
@app.route('/', methods=['GET', 'POST'])
def index():
    original_code = ""
    obfuscated_code = ""

    # Dacă utilizatorul a apăsat butonul
    if request.method == 'POST':
        original_code = request.form.get('lua_code', '')
        if original_code.strip():
            obfuscated_code = obfuscate_code(original_code)

    return render_template('index.html', original=original_code, obfuscated=obfuscated_code)

if __name__ == '__main__':
    # Pornim serverul web pe portul 5000
    app.run(host='0.0.0.0', port=5000)
