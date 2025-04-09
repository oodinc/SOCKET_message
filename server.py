import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = {}

def broadcast(message, sender_socket=None, sender_name=None):
    if sender_name:
        print(f"[BROADCAST] {sender_name} mengirim pesan")
    
    for client_name, client_socket in clients.items():
        if client_socket != sender_socket:
            client_socket.send(message)

def private_message(sender_name, target_name, message):
    print(f"[PRIVATE] {sender_name} -> {target_name}: {message.decode('utf-8').split(']:', 1)[1].strip() if ']:'  in message.decode('utf-8') else message.decode('utf-8')}")
    
    if target_name in clients:
        clients[target_name].send(message)
        return True
    else:
        print(f"Client '{target_name}' tidak ditemukan.")
        return False

def handle_client(client_socket):
    try:
        name = client_socket.recv(1024).decode('utf-8')
        clients[name] = client_socket
        print(f"{name} bergabung.")
        broadcast(f"{name} telah bergabung ke chat!".encode('utf-8'))
    except:
        return
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            if message == '/list':
                # Kirim daftar nama client ke pengirim
                list_clients = ', '.join(clients.keys())
                client_socket.send(f"[Daftar Client Online]: {list_clients}".encode('utf-8'))
            elif message.startswith("@"):
                # Private message
                split = message.split(' ', 1)
                if len(split) == 2:
                    target_name = split[0][1:]
                    private_message(target_name, f"[Private from {name}]: {split[1]}".encode('utf-8'))
                else:
                    client_socket.send("Format salah. Gunakan @nama pesanmu".encode('utf-8'))
            else:
                # Broadcast biasa
                broadcast(f"{message}".encode('utf-8'), client_socket)

        except Exception as e:
            print(f"{name} keluar. Error: {str(e)}")
            broadcast(f"{name} keluar dari chat.".encode('utf-8'))
            client_socket.close()
            del clients[name]
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server aktif di {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"Koneksi baru dari {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()