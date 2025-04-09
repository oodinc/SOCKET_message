import socket
import threading

HOST = '192.168.88.61'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

name = input("Masukkan nama kamu: ")
client.send(name.encode('utf-8'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Terputus dari server")
            client.close()
            break

def write():
    while True:
        message = input("Masukkan Pesan: ")
        if message == '/list':
            client.send('/list'.encode('utf-8'))
        elif message.startswith('@'):
            client.send(message.encode('utf-8'))
        else:
            full_message = f"{name}: {message}"
            client.send(full_message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
