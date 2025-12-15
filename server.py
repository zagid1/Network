# server.py
import connection_tools.connection as connect
from math_tools.operations import encode_hamming

def main():
    conn, server_socket = connect.start_server()
    info_word = 0b10101010100  # 11-битное информационное слово
    n = 15
    k = 11
    m = n - k
  
    encoded_word = encode_hamming(info_word, n, k, m)
    
    # Отправка всех возможных ошибок
    for error_pattern in range(1, 2**n):
        corrupted_word = encoded_word ^ error_pattern
        
        bin_data = corrupted_word.to_bytes(2, byteorder='big')
        conn.send(bin_data)
    
    # Сигнал окончания
    conn.send(b'END')
    connect.connection_termination(conn)
    connect.socket_termination(server_socket)

if __name__ == "__main__":
    main()