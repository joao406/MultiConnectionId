import socket
import threading

client_connections = {}

def handle_client(client_socket, client_id):
	while True:
		try:
			data = client_socket.recv(1024)
			if not data:
				break
			print(f"Dados de {client_id}: {data.decode()}")
		except Exception as e:
			print(f"Erro de conexao com {client_id}: {str(e)}")
			break
	client_socket.close()
	del client_connections[client_id]
	print(f"Conexao com {client_id} encerrada.")

def main():
	host = "127.0.0.1"
	port = 4343

	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.bind((host, port))
	server_sock.listen()

	print(f"Servidor rodando em {host}:{port}")
	client_id = 0
	while True:
		client_socket, client_address = server_sock.accept()
		print(f"Conexao recebida de {client_address}")
		client_id += 1
		client_connections[client_id] = client_socket

		client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
		client_thread.start()

if __name__ == "__main__":
	main()
