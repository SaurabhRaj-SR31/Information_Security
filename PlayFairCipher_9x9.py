def create_playfair_matrix(keyword):
    # Step 2: Eliminate repeated characters in the keyword
    keyword = ''.join(dict.fromkeys(keyword))

    # Check if the matrix size is sufficient for the keyword
    if len(keyword) > 9 * 9:
        raise ValueError("Keyword is too long for a 9x9 matrix")

    # Create a 9x9 matrix to store characters
    matrix = [['' for _ in range(9)] for _ in range(9)]
    used_chars = set()
    row, col = 0, 0

    # Define preferred character sets for the matrix
    preferred_characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    symbol_characters = "!@#$%^&*()_-+=<>,.?/;:[]{}|"

    # Combine preferred characters and symbols
    all_characters = preferred_characters + symbol_characters

    # Step 3: Fill the matrix with characters from the keyword
    for char in keyword:
        matrix[row][col] = char
        used_chars.add(char)
        col += 1
        if col == 9:
            col = 0
            row += 1

    # Step 4: Fill the remaining matrix with characters, giving preference to letters, digits, and symbols
    for char in all_characters:
        if char not in used_chars:
            matrix[row][col] = char
            used_chars.add(char)
            col += 1
            if col == 9:
                col = 0
                row += 1
            if row == 9:
                break  # Matrix is full

    return matrix


def display_matrix(matrix):
    print("Playfair Matrix:")
    border = "+-------" * 9 + "+"
    print(border)
    for row in matrix:
        print("|", end="")
        for col in row:
            print(f"   {col}   |", end="")
        print("\n" + border)


def playfair_encrypt(plaintext, matrix):
    plaintext = plaintext.upper().replace("J", "I")
    plaintext = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]

    if len(plaintext[-1]) == 1:
        plaintext[-1] += 'X'

    ciphertext = []

    for pair in plaintext:
        if len(pair) == 2:
            char1, char2 = pair[0], pair[1]

            position1 = get_position(matrix, char1)
            position2 = get_position(matrix, char2)

            if position1 is not None and position2 is not None:
                row1, col1 = position1
                row2, col2 = position2

                if row1 == row2:
                    ciphertext.append(
                        matrix[row1][(col1 + 1) % 9] + matrix[row2][(col2 + 1) % 9])
                elif col1 == col2:
                    ciphertext.append(
                        matrix[(row1 + 1) % 9][col1] + matrix[(row2 + 1) % 9][col2])
                else:
                    ciphertext.append(matrix[row1][col2] + matrix[row2][col1])
        else:
            # Handle single characters if any
            char1 = pair[0]
            position1 = get_position(matrix, char1)
            if position1 is not None:
                row1, col1 = position1
                ciphertext.append(matrix[row1][(col1 + 1) % 9] + 'X')

    return ''.join(ciphertext)


def get_position(matrix, char):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == char:
                return i, j
    return None


# Get the keyword and plaintext from the user
keyword = input("Enter the keyword: ")
plaintext = input("Enter the plaintext: ")

matrix = create_playfair_matrix(keyword)

print("Generated Playfair Matrix:")
display_matrix(matrix)

encrypted_text = playfair_encrypt(plaintext, matrix)
print("\nEncrypted Text:", encrypted_text)
