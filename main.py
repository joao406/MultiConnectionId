import socket
import threading
import time

client_connections = {}
received_messages = {}

server_ready = False

def handle_client(client_socket, client_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            if client_id not in received_messages:
                received_messages[client_id] = []
            received_messages[client_id].append(message)
        except Exception as err:
            print(f"Erro: {str(err)}")
            break
    client_socket.close()
    del client_connections[client_id]

def list_connected_clients():
    print("Clientes conectados:")
    for client_id in client_connections:
        print(f"ID: {client_id}")

def server_input():
    global server_ready
    while not server_ready:
        time.sleep(1)
    while True:
        print("Escolha uma opção:")
        print("1. Listar IDs conectados")
        print("2. Enviar mensagem para um cliente")
        print("3. Visualizar mensagens")
        option = input("Opção: ")

        if option == "1":
            list_connected_clients()
        elif option == "2":
            print("Lista de IDs disponíveis:")
            for client_id in client_connections:
                print(f"ID: {client_id}")
            client_id = int(input("ID do cliente: "))
            if client_id in client_connections:
                message = input("Mensagem: ")
                client_socket = client_connections[client_id]
                server_message_prefix = f"SERVIDOR: {message}\n"
                client_socket.send(server_message_prefix.encode())
            else:
                print(f"Cliente com ID {client_id} não encontrado.")
        elif option == "3":
            print("Mensagens recebidas:")
            for client_id in received_messages:
                if received_messages[client_id]:
                    print(f"ID {client_id}:")
                    for message in received_messages[client_id]:
                        print(message)
                else:
                    print(f"ID {client_id}: Sem mensagens.")
        else:
            print("Opção inválida")

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
        client_id += 1
        client_connections[client_id] = client_socket

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

if __name__ == "__main__":
    input_thread = threading.Thread(target=server_input)
    input_thread.start()
    main()
