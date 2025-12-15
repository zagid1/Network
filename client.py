# client.py
import connection_tools.connection as connect
from display_tools.display import draw_table_corrected
from math_tools.operations import encode_hamming, compute_syndrome, correct_error

def main():
    conn = connect.start_client()
    info_word = 0b10101010100  # 11-битное информационное слово
    n = 15
    k = 11
    m = n - k
    encoded_word = encode_hamming(info_word, n, k, m)  # Кодируем информационное слово для сравнения
    
    # Подготовка статистики
    corrected_errors = [0] * n
    found_errors = [0] * n
    number_of_errors = [0] * n
    
    i = 1
    while True:
        data = conn.recv(2)

        if data == b'END' or i >= 2**n:
            break
        
        received_word = int.from_bytes(data, byteorder='big')
        
        syndrome = compute_syndrome(received_word, n, k, m)
        
        error_weight = bin(i).count('1') - 1
        i += 1
        
        if 0 <= error_weight < n:
            number_of_errors[error_weight] += 1
        
        if syndrome != 0:
            if 0 <= error_weight < n:
                found_errors[error_weight] += 1
        
        corrected_word = correct_error(received_word, syndrome, n, k, m)

        if corrected_word == encoded_word:
            if 0 <= error_weight < n:
                corrected_errors[error_weight] += 1
    
    draw_table_corrected(n, number_of_errors, found_errors, corrected_errors)
    
    connect.socket_termination(conn)

if __name__ == "__main__":
    main()