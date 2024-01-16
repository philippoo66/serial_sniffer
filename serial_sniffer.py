import serial
import time
import sys


# Hauptfunktion
def main():
    port = 'COM2'

    if(len(sys.argv) > 1):
        port = sys.argv[1]

    # Serielle Port-Einstellungen
    ser = serial.Serial(port, 9600, timeout=0)  # Hier 'COM1' durch den tatsächlichen Port ersetzen und die Baudrate anpassen

    # Dateipfad für die Aufzeichnungsdatei
    file_path = 'serial_data_' + port + '.txt'

    try:
        # Serial Port öffnen
        if not ser.is_open:
            ser.open()

        with open(file_path, 'w') as file:
            data_buffer = b''
            last_receive_time = time.time()

            while True:
                # Zeichen vom Serial Port lesen
                incoming_data = ser.read()

                if incoming_data:
                    # Daten zum Datenpuffer hinzufügen
                    data_buffer += incoming_data
                    last_receive_time = time.time()
                    #print(data_buffer.hex())
                elif time.time() - last_receive_time > 0.02 and data_buffer:
                    # Wenn 0,x Sekunde vergangen ist und der Datenpuffer nicht leer ist,
                    # schreibe ihn in die Datei mit Zeitstempel
                    timestamp_ms = int(last_receive_time * 1000)
                    hex_data = ' '.join([format(byte, '02X') for byte in data_buffer])
                    file.write(f'{timestamp_ms}: {hex_data}\n')
                    file.flush()  # Datei sofort aktualisieren
                    print(f'{timestamp_ms}: {hex_data}')  # Optional: Ausgabe auf der Konsole

                    # Datenpuffer zurücksetzen
                    data_buffer = b''
                time.sleep(0.001)


    except KeyboardInterrupt:
        print("\nAufzeichnung beendet.")
    finally:
        # Serial Port schließen
        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
