import socket


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    # Получение сообщения от сервера
    data = client_socket.recv(1024)
    print(f"Получено от сервера: {data.decode()}")
    
    # Отправка ответа серверу
    client_socket.send(b"hi, server")
    return client_socket

def socket_termination(client_socket):
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Сервер запущен. Ожидание подключения...")
    
    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")
    
    # Отправка сообщения клиенту
    conn.send(b"hi, clinet!")
    
    # Получение сообщения от клиента
    data = conn.recv(1024)
    print(f"Получено от клиента: {data.decode()}")
    return conn, server_socket

def connection_termination(conn): # server's function 
    conn.close()