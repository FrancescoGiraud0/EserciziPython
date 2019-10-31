"""
Giraudo Francesco
Vernam cipher in python3.
"""

# Definition of the numeric values to the corresponding letters
alphabet= {chr(65+k) for k in range(0,26)}

# Creation of a new dictionary where key is the letter and the
# value is a number for encoding.
encode_alphabet = {value:key for key, value in  alphabet.items()}

def vernam_encrypting(word):
    # function to encrypt char
    encrypt_char = lambda a,b: alphabet.get((encode_alphabet.get(a)+encode_alphabet.get(b)) % len(alphabet))

    # word encrypting using list comprehension
    encrypted_chars_list = [encrypt_char(c,key_word[i]) if i<len(key_word) else c for i,c in enumerate(list(word))] 

    # convertion of list of char to string with .join()
    return "".join(encrypted_chars_list)

def vernam_decrypting(encrypted_word):
    # function to decrypt char
    decrypt_char = lambda a,b: alphabet.get( (encode_alphabet.get(a)-encode_alphabet.get(b)+len(alphabet))%len(alphabet) )

    # word decrypting using list comprehension
    decrypted_chars_list = [decrypt_char(c,key_word[i]) if i<len(key_word) else c for i,c in enumerate(list(encrypted_word))]

    # convertion of list of char to string with .join()
    return "".join(decrypted_chars_list)

key_word = "" # Definition of the key
word = ""  # Definition of the word encrypt / decrypt

while (not word.isalpha()) and len(word)>=0:
    #input of the word to encrypt
    word = input("Insert the word to encrypt (only letters): ").upper() # to uppercase

while (not key_word.isalpha()) and len(key_word)>=0:
    #input of the word to encrypt
    key_word = input("Insert the key word to encrypt the word (only letters): ").upper() # to uppercase

encrypted_word = vernam_encrypting(word)
print(f"Encrypted word: {encrypted_word}")

decrypted_word = vernam_decrypting(encrypted_word)
print(f"Decrypted word: {decrypted_word}")
