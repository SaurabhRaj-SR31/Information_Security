import time
import matplotlib.pyplot as plt

# Define a function to measure encryption time


def create_playfair_matrix(key):
    # Remove spaces and convert to uppercase
    key = key.replace(' ', '').upper()
    key = ''.join(filter(str.isalpha, key))  # Remove non-alphabetic characters
    key = "".join(dict.fromkeys(key))  # Remove duplicate characters

    # Initialize the matrix with the key
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I/J are treated as one letter
    matrix = list(key)

    # If 'I' or 'J' is in the key, treat them as one letter
    if 'I' in matrix:
        matrix.remove('J')
    elif 'J' in matrix:
        matrix.remove('I')

    # Fill the matrix with the remaining letters of the alphabet
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)

    # Replace 'I' with 'I/J' in the matrix
    for i in range(5):
        for j in range(5):
            if matrix[i*5 + j] == 'I':
                matrix[i*5 + j] = 'I/J'
            elif matrix[i*5 + j] == 'J':
                matrix[i*5 + j] = 'I/J'

    # Create a 5x5 matrix
    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return playfair_matrix


def playfair_encrypt(plaintext, key):
    playfair_matrix = create_playfair_matrix(key)
    plaintext = plaintext.replace(' ', '').upper()
    # Remove non-alphabetic characters
    plaintext = ''.join(filter(str.isalpha, plaintext))

    if len(plaintext) % 2 != 0:
        plaintext += 'X'  # Pad with 'X' to have an even number of characters

    pairs = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]

    ciphertext = ''
    for pair in pairs:
        char1, char2 = pair
        row1, col1 = 0, 0
        row2, col2 = 0, 0

        # Find the positions of the characters in the matrix
        for i in range(5):
            for j in range(5):
                if char1 == 'I' or char1 == 'J':
                    if playfair_matrix[i][j] == 'I' or playfair_matrix[i][j] == 'J':
                        row1, col1 = i, j
                        break
                if playfair_matrix[i][j] == char1:
                    row1, col1 = i, j
                if char2 == 'I' or char2 == 'J':
                    if playfair_matrix[i][j] == 'I' or playfair_matrix[i][j] == 'J':
                        row2, col2 = i, j
                        break
                if playfair_matrix[i][j] == char2:
                    row2, col2 = i, j

        if row1 == row2:
            ciphertext += playfair_matrix[row1][(col1 + 1) % 5]
            if char1 == 'I' or char1 == 'J':
                ciphertext += 'I/J'
            else:
                ciphertext += playfair_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += playfair_matrix[(row1 + 1) % 5][col1]
            if char1 == 'I' or char1 == 'J':
                ciphertext += 'I/J'
            else:
                ciphertext += playfair_matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += playfair_matrix[row1][col2]
            if char1 == 'I' or char1 == 'J':
                ciphertext += 'I/J'
            else:
                ciphertext += playfair_matrix[row2][col1]

    return ciphertext


def measure_encryption_time(matrix_size):
    key = "KEY" * matrix_size
    plaintext = "PLAINTEXT" * matrix_size

    start_time = time.time()
    create_playfair_matrix(key)
    playfair_encrypt(plaintext, key)
    return time.time() - start_time

# Define a function to measure security level (key space size)


def measure_security_level(matrix_size):
    key = "KEY" * matrix_size
    matrix = create_playfair_matrix(key)
    key_space_size = len(set(char for row in matrix for char in row))
    return key_space_size


# Matrix sizes to test
matrix_sizes = [5, 8, 9, 10, 11]

# Measure encryption time and security level for different matrix sizes
encryption_times = [measure_encryption_time(size) for size in matrix_sizes]
security_levels = [measure_security_level(size) for size in matrix_sizes]

# Plot the graph
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(matrix_sizes, encryption_times, marker='o', label='Encryption Time')
plt.xlabel('Matrix Size')
plt.ylabel('Encryption Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(matrix_sizes, security_levels, marker='o', label='Security Level')
plt.xlabel('Matrix Size')
plt.ylabel('Security Level (Key Space Size)')
plt.legend()

plt.tight_layout()
plt.show()
