from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

# Seturi pentru stocare
numere_frecvente = {"CS10CSA"}
numere_nefrecvente = {}

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect('/login')
    return render_template("index.html",
                           frecvente=numere_frecvente,
                           nefrecvente=numere_nefrecvente)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/')
        else:
            return "Login greșit! <a href='/login'>Înapoi</a>"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_number():
    number = request.form.get('number', '').upper().strip()
    if number:
        numere_frecvente.add(number)
        numere_nefrecvente.pop(number, None)
    return redirect('/')

@app.route('/delete/<number>', methods=['POST', 'GET'])
def delete_number(number):
    numere_frecvente.discard(number)
    numere_nefrecvente.pop(number, None)
    return redirect('/')

@app.route('/detect', methods=['POST'])
def detect_number():
    number = request.form.get('number', '').upper().strip()

    # ✅ Permite doar numere cu 6-7 caractere alfanumerice și care nu sunt deja frecvente
    if number and 6 <= len(number) <= 7 and number.isalnum() and number not in numere_frecvente:
        numere_nefrecvente[number] = datetime.now()
        print(f"📥 Număr detectat și salvat: {number}")
    else:
        print(f"⚠️ Ignorat: {number} (nevalid sau deja frecvent)")

    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
