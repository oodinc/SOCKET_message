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
            try:
                client_socket.send(message)
            except:
                pass

def private_message(sender_name, target_name, message):
    print(f"[PRIVATE] {sender_name} -> {target_name}: {message.decode('utf-8').split(']:', 1)[1].strip() if ']:' in message.decode('utf-8') else message.decode('utf-8')}")
    if target_name in clients:
        try:
            clients[target_name].send(message)
            return True
        except:
            print(f"Failed to send message to {target_name}")
            return False
    else:
        print(f"Client '{target_name}' tidak ditemukan.")
        return False

def handle_client(client_socket):
    name = None
    try:
        name = client_socket.recv(1024).decode('utf-8')
        clients[name] = client_socket
        
        print(f"{name} bergabung.")
        
        broadcast(f"{name} telah bergabung ke chat!".encode('utf-8'), client_socket)
        
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:  
                    raise Exception("Client disconnected")
                    
                message_text = message.decode('utf-8')
                if message_text == '/list':
                    user_list = "\n".join(clients.keys())
                    response = f"User Online:\n{user_list}"
                    client_socket.send(response.encode('utf-8'))

                if message_text.startswith("@"):
                    split = message_text.split(' ', 1)
                    if len(split) == 2:
                        target_name = split[0][1:]
                        private_msg = f"[Private from {name}]: {split[1]}".encode('utf-8')
                        if not private_message(name, target_name, private_msg):
                            client_socket.send(f"User {target_name} tidak ditemukan.".encode('utf-8'))
                    else:
                        client_socket.send("Format salah. Gunakan @nama pesanmu".encode('utf-8'))
                else:
                    broadcast(message, client_socket, name)
            except Exception as e:
                raise  
    except Exception as e:
        if name and name in clients:
            print(f"{name} keluar. Error: {str(e)}")
            broadcast(f"{name} keluar dari chat.".encode('utf-8'))
            try:
                client_socket.close()
            except:
                pass
            del clients[name]
    finally:
        if name and name in clients:
            try:
                del clients[name]
            except:
                pass
        try:
            client_socket.close()
        except:
            pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server aktif di {HOST}:{PORT}")
    
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Koneksi baru dari {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True 
            thread.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()