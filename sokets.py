import socket
import os
import threading

# Función del servidor
def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Servidor escuchando en {host}:{port}')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Conexión establecida con {client_address}')
        handle_client(client_socket)

def handle_client(client_socket):
    try:
        file_name = client_socket.recv(1024).strip().decode()
        file_size = int(client_socket.recv(1024).strip().decode())
        
        print(f'Recibiendo archivo: {file_name} de tamaño: {file_size} bytes')
        
        with open(file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if data == b'EOF':
                    break
                file.write(data)
        
        print(f'Transferencia de archivo {file_name} completada')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()

# Función del cliente
def start_client(server_host='127.0.0.1', server_port=12345, file_path='path/to/file.txt'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print(f'Conectado al servidor en {server_host}:{server_port}')
    
    send_file_info(client_socket, file_path)
    send_file(client_socket, file_path)
    
    client_socket.sendall(b'EOF')  # Indicar fin de la transferencia
    client_socket.close()

def send_file_info(client_socket, file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    client_socket.sendall(file_name.encode() + b'\n')
    client_socket.sendall(str(file_size).encode() + b'\n')

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)

# Función principal
def main():
    mode = input("¿Quieres iniciar el servidor (s) o el cliente (c)? ")
    if mode == 's':
        host = input("Introduce la dirección IP del servidor (por defecto 0.0.0.0): ") or '0.0.0.0'
        port = int(input("Introduce el puerto del servidor (por defecto 12345): ") or 12345)
        start_server(host, port)
    elif mode == 'c':
        server_host = input("Introduce la dirección IP del servidor (por defecto 127.0.0.1): ") or '127.0.0.1'
        server_port = int(input("Introduce el puerto del servidor (por defecto 12345): ") or 12345)
        file_path = input("Introduce la ruta del archivo a enviar: ")
        start_client(server_host, server_port, file_path)
    else:
        print("Modo no válido. Por favor, elige 's' para servidor o 'c' para cliente.")

if __name__ == '__main__':
    main()
