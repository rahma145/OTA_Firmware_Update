import serial
import time
import argparse
import io
import os


def write(port, filePath) : 
    #chunk length 
    max_length = 256
    chunks = []
    ser = serial.Serial(port, 9600, timeout = 10)

    print("Synchronisation avec le STM32...")
    time.sleep(2)

    #open the file
    with open(filePath, 'rb') as file: 
        firmware_data = file.read()
        # Boucle pour découper le fichier en chunks
        for i in range(0, len(firmware_data), max_length):
            chunks.append(firmware_data[i:i+max_length])  # Découpe par blocs de 256 octets
        print(f"Nombre de chunks à envoyer : {len(chunks)}")
        
                # Envoi uniquement du dernier chunk
        last_chunk = chunks[-1]
        taille_chunk = len(last_chunk)
        taille_chunk_bytes = taille_chunk.to_bytes(2, 'big')  # 2 octets pour la taille

        # Logs pour déboguer
         # Envoi du dernier chunk

         #Send data
        last_chunk.insert(0, taille_chunk_bytes)
        print(f"Envoi des données : {last_chunk.hex()}")
            
        ser.write(last_chunk)

    ser.close()


    #print(list(firmware_data))
    




if __name__ == '__main__':
    # Utilisation d'argparse pour lire les arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Communicate with STM32 via Bluetooth")
    parser.add_argument('port', type=str, help="Serial port (e.g., COM5, /dev/ttyUSB0)")
    parser.add_argument('filePath', type=str, help="the path of the binary file")

    args = parser.parse_args()

    # Appel de la fonction avec les arguments passés depuis la ligne de commande
    #connect(args.port)
    write(args.port, args.filePath)