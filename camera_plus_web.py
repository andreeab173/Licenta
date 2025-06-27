from ultralytics import YOLO
import cv2
import pytesseract
import serial
import time
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from datetime import datetime, timedelta

import webbrowser


# Configurare Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurare Arduino
try:
    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
    time.sleep(2)
    print("✅ Conectat la COM4")
except:
    print("❌ Nu s-a putut conecta la COM4.")

# Liste numere
numere_frecvente = {"CS10CSA"}  # Numere permise
numere_nefrecvente = {}  # Numere înregistrate cu timp limitat

# Configurare aplicație web
app = Flask(__name__)
app.secret_key = 'secret_key'

# Funcție separată pentru procesare număr
def adauga_numar_detectat(text):
    current_time = datetime.now()
    if text in numere_frecvente:
        arduino.write(b'OPEN')
        print(f"✅ {text} este permis (Frecvent).")
    else:
        if text in numere_nefrecvente:
            if current_time - numere_nefrecvente[text] > timedelta(hours=3):
                del numere_nefrecvente[text]
                arduino.write(b'DENY')
                print(f"❌ {text} nu mai are acces (Timp expirat).")
            else:
                arduino.write(b'OPEN')
                print(f"✅ {text} are acces (Nefrecvent, în termen).")
        else:
            numere_nefrecvente[text] = current_time
            arduino.write(b'DENY')
            print(f"❌ {text} nu are acces (Nou).")

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html', 
                               frecvente=sorted(numere_frecvente),
                               numere_nefrecvente=numere_nefrecvente)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/')
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_number():
    if 'logged_in' in session:
        number = request.form['number'].upper().strip()
        if number:
            numere_frecvente.add(number)
        return redirect('/')
    return redirect('/login')

@app.route('/delete/<number>')
def delete_number(number):
    if 'logged_in' in session:
        numere_frecvente.discard(number)
        numere_nefrecvente.pop(number, None)
        return redirect('/')
    return redirect('/login')

@app.route('/camera')
def camera_feed():
    model = YOLO('C:/Users/barti/runs/detect/train25/weights/best.pt')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, conf=0.25, verbose=False)

        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    plate_img = frame[y1:y2, x1:x2]
                    text = pytesseract.image_to_string(plate_img)
                    text = ''.join(filter(str.isalnum, text)).upper()

                    if text:
                        adauga_numar_detectat(text)

        cv2.imshow('Detectie Numar Inmatriculare + OCR', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect('/')

@app.route('/api/nefrecventi', methods=['GET'])
def api_nefrecventi():
    # Convertim datele într-un format simplu pentru API
    nefrecventi_list = [
        {"numar": numar, "timp_intrare": str(timp)}
        for numar, timp in numere_nefrecvente.items()
    ]
    return jsonify(nefrecventi_list)
@app.route('/detect', methods=['POST'])
def detect():
    numar = request.form.get('number')
    if numar:
        from datetime import datetime
        numere_nefrecvente[numar] = datetime.now()
        print(f"✅ Număr primit de la cameră: {numar}")
        return 'OK', 200
    return 'No number', 400


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)