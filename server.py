import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = {}

def broadcast(message, sender_socket=None):
    for client_socket in clients.values():
        if client_socket != sender_socket:
            client_socket.send(message)

def private_message(target_name, message):
    if target_name in clients:
        clients[target_name].send(message)
    else:
        print(f"Client '{target_name}' tidak ditemukan.")

def handle_client(client_socket):
    try:
        name = client_socket.recv(1024).decode('utf-8')
        clients[name] = client_socket
        print(f"{name} bergabung.")
        broadcast(f"{name} telah bergabung ke chat!".encode('utf-8'), client_socket)
    except:
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("@"):
                
                split = message.split(' ', 1)
                if len(split) == 2:
                    target_name = split[0][1:]  
                    private_message(target_name, f"[Private from {name}]: {split[1]}".encode('utf-8'))
                else:
                    client_socket.send("Format salah. Gunakan @nama pesanmu".encode('utf-8'))
            else:
                broadcast(f"{message}".encode('utf-8'), client_socket)
        except:
            print(f"{name} keluar.")
            broadcast(f"{name} keluar dari chat.".encode('utf-8'), client_socket)
            client_socket.close()
            del clients[name]
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server aktif di {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_socket,)).start()
