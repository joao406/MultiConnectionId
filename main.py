import socket
import threading
import time
import random

client_connections = {}
random_messages = [
    "Nao briguem\n",
    "Respeitem as regras\n",
    "O adm ama voces <3\n",
    "Se fizer besteira voce vai de kick >:(\n",
    "Python é incrivel, porem nao tao rapido ):\n"
]

server_ready = False

def handle_client(client_socket, client_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Dados de {client_id}: {data.decode()}")
        except Exception as err:
            print(f"Erro: {str(err)}")
            break
    client_socket.close()
    del client_connections[client_id]
    print(f"{client_id} SAIU.")

def random_server_messages():
    while True:
        time.sleep(40)
        for client_id, client_socket in client_connections.items():
            random_message = random.choice(random_messages)
            server_message_prefix = f"SERVIDOR: {random_message}"
            client_socket.send(server_message_prefix.encode())

def server_input():
    global server_ready
    while not server_ready:
        time.sleep(1)
    while True:
        message = input("")
        for client_id, client_socket in client_connections.items():
            server_message_prefix = f"SERVIDOR: {message}\n"
            client_socket.send(server_message_prefix.encode())

def main():
    host = "127.0.0.1"
    port = 5001
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.bind((host, port))
    sock_server.listen()
    print(f"RODANDO EM {host}:{port}")
    global server_ready
    server_ready = True

    client_id = 0
    while True:
        client_socket, client_address = sock_server.accept()
        print(f"{client_address} ENTROU!\n")
        client_id += 1
        client_connections[client_id] = client_socket

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

        message_thread = threading.Thread(target=random_server_messages)
        message_thread.start()

if __name__ == "__main__":
    input_thread = threading.Thread(target=server_input)
    input_thread.start()
    main()
