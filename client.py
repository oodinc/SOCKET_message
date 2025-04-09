import socket
import threading

# Konfigurasi ke server
HOST = '192.168.88.28'
PORT = 12345

# Inisialisasi client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Minta nama client
name = input("Masukkan nama kamu: ")
client.send(name.encode('utf-8'))

# Fungsi untuk menerima pesan dari server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Terputus dari server")
            client.close()
            break

# Fungsi untuk mengirim pesan ke server
def write():
    while True:
        message = input()
        if message.startswith('@'):
            # Kirim apa adanya (biar server yang proses)
            client.send(message.encode('utf-8'))
        else:
            # Kirim dengan nama prefix untuk broadcast
            full_message = f"{name}: {message}"
            client.send(full_message.encode('utf-8'))


# Mulai thread untuk membaca dan menulis
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
