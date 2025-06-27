import serial
import serial.tools.list_ports

def conectare_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        try:
            arduino = serial.Serial(port=port.device, baudrate=9600, timeout=1)
            print(f"✅ Conectat la {port.device}")
            return arduino
        except:
            continue
    print("❌ Nu am putut găsi niciun port COM disponibil.")
    return None

arduino = conectare_arduino()
