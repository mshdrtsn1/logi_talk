from socket import *
import threading

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 8081))
server_socket.listen(5)  # Треба додати listen(), щоб сервер міг приймати підключення

print("Server running...")

clients = []  # Список для збереження клієнтських сокетів

def broadcast(message):
    for client in clients:
        try:
            # send() працює з байтами, тому нам треба кодувати рядок за допомогою encode()
            client.send((message + "\n").encode())
        except:
            pass

def handle_client(client_socket):
    try:
        # recv() повертає байти, потрібно декодувати для цього використовуємо decode()
        name = client_socket.recv(1024).decode().strip()
        clients.append(client_socket)  #  додаємо клієнтський сокет у список

        broadcast(f"{name} joined!")

        while True:
            try:
                # recv() повертає байти, потрібно декодувати
                message = client_socket.recv(1024).decode().strip()
                if not message:  # Якщо клієнт відключився
                    break
                broadcast(f"{name}: {message}")

            except:
                break

    finally:
        # Видаляємо саме client_socket, а не name
        if client_socket in clients:
            clients.remove(client_socket)
        broadcast(f"{name} left!")
        client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    # Додаємо кому після args=(client_socket,)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
