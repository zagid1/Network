def get_parity_positions(m):
    """
    Возвращает позиции проверочных битов (1-based индексация)
    """
    parity_positions = []
    for i in range(m):
        parity_positions.append(1 << i)  # 1, 2, 4, 8, 16, ...
    return parity_positions


def get_info_positions(n, m):
    """
    Возвращает позиции информационных битов (1-based индексация)
    """
    parity_positions = get_parity_positions(m)
    info_positions = []
    for pos in range(1, n + 1):
        if pos not in parity_positions:
            info_positions.append(pos)
    return info_positions


# hamming.py

def encode_hamming(info_word, n=None, k=None, m=None):
    """
    Кодирование слова в код Хэмминга произвольной длины
    """
    
    # Получаем позиции информационных и проверочных битов
    info_positions = get_info_positions(n, m)
    parity_positions = get_parity_positions(m)
    
    code_word = 0
    
    # Размещаем информационные биты
    for i, pos in enumerate(info_positions):
        bit = (info_word >> i) & 1
        if bit:
            code_word |= 1 << (pos - 1)
    
    # Вычисляем и устанавливаем проверочные биты
    for i in range(m):
        parity_pos = 1 << i  # Позиция проверочного бита
        parity_value = 0
        
        # Проходим по всем битам кодового слова
        for bit_pos in range(1, n + 1):
            if (bit_pos >> i) & 1:
                bit_value = (code_word >> (bit_pos - 1)) & 1
                parity_value ^= bit_value
        
        # Устанавливаем проверочный бит
        if parity_value:
            code_word |= 1 << (parity_pos - 1)
    
    return code_word

def compute_syndrome(received_word, n=None, k=None, m=None):
    """
    Вычисление синдрома для кода Хэмминга [n,k] по алгоритму
    """
    
    # Инициализируем синдром
    syndrome = 0
    
    for i in range(m):
        parity_bit_value = 0
        # Проверяем все биты кодового слова
        for bit_pos in range(1, n + 1):
            if (bit_pos >> i) & 1:
                bit_value = (received_word >> (bit_pos - 1)) & 1
                parity_bit_value ^= bit_value
        
        # Формируем синдром: h4 h3 h2 h1
        syndrome |= (parity_bit_value << i)
    
    return syndrome


def correct_error(received_word, syndrome, n=None, k=None, m=None):
    """
    Исправление ошибки в коде Хэмминга
    """
    
    if syndrome == 0:
        return received_word
    
    # Если синдром указывает на позицию ошибки (от 1 до n)
    if 1 <= syndrome <= n:
        corrected_word = received_word ^ (1 << (syndrome - 1))
        return corrected_word
    
    return received_word  # Множественная ошибка, не исправляем


def extract_info_bits(code_word, n=None, k=None, m=None):
    """
    Извлечение информационных битов из кодового слова Хэмминга
    """
    
    # Получаем позиции информационных битов
    info_positions = get_info_positions(n, m)
    
    # Извлекаем информационные биты
    info_word = 0
    for i, pos in enumerate(info_positions):
        bit = (code_word >> (pos - 1)) & 1  
        info_word |= (bit << i)  
    
    return info_word