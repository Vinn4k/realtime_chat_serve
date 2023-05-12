import socket
import threading
import traceback

HEADER_LENGTH = 10
IP = "192.168.1.3"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

# Lista para armazenar os sockets dos clientes conectados
sockets_list = []

def handle_client(client_socket, client_address):
    # Adicionar o socket do cliente na lista
    sockets_list.append(client_socket)

    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not len(message_header):
                print(f"Conexão fechada pelo cliente {client_address}")
                break

            message_length = int(message_header.decode("utf-8").strip())

            message = client_socket.recv(message_length).decode("utf-8")

            print(f"Mensagem recebida de {client_address}: {message}")

            # Enviar a mensagem para todos os clientes, exceto o cliente que enviou a mensagem
            for socket_item in sockets_list:
                if socket_item != client_socket:
                    socket_item.send(message_header + message.encode("utf-8"))

        except:
            print(f"Erro ao receber mensagem do cliente {client_address}")
            break

    client_socket.close()

def start_chat_server():
    while True:
        client_socket, client_address = server_socket.accept()

        print(f"Conexão aceita do cliente {client_address[0]}:{client_address[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    print(f"Iniciando o servidor de chat no endereço {IP}:{PORT}")
    start_chat_server()