"""
Giraudo Francesco
Vernam cipher in python3.
"""

key_word = "ITISDELPOZZO" # Definition of the key

# Definition of the numeric values to the corresponding letters
alphabet= {
      0:"A",  1:"B",  2:"C",  3:"D",  4:"E",
      5:"F",  6:"G",  7:"H",  8:"I",  9:"L",
     10:"M", 11:"N", 12:"O", 13:"P", 14:"Q",
     15:"R", 16:"S", 17:"T", 18:"U", 19:"V",
     20:"Z"}

# Creation of a new dictionary where key is the letter and the
# value is a number for encoding.
encode_alphabet = {value:key for key, value in  alphabet.items()}

def vernam_encrypting(word):
    # function to encrypt char
    encrypt_char = lambda a,b: alphabet.get((encode_alphabet.get(a) + encode_alphabet.get(b)) % len(alphabet))

    # word encrypting using list comprehension
    encrypted_chars_list = [encrypt_char(c,key_word[i]) if i<len(key_word) else c for i,c in enumerate(list(word))] 

    # convertion of list of char to string with .join()
    return "".join(encrypted_chars_list)

def vernam_decrypting(encrypted_word):
    # function to decrypt char
    decrypt_char = lambda a,b: alphabet.get( (encode_alphabet.get(a)-encode_alphabet.get(b)+len(alphabet)) % len(alphabet))

    # word decrypting using list comprehension
    decrypted_chars_list = [decrypt_char(c,key_word[i]) if i<len(key_word) else c for i,c in enumerate(list(encrypted_word))]

    # convertion of list of char to string with .join()
    return "".join(decrypted_chars_list)

word = ""

while (not word.isalpha()) and len(word)>=0:
    #input of the word to encrypt
    word = input("Insert the word to encrypt (only letters): ").upper() # to uppercase

encrypted_word = vernam_encrypting(word)
print(f"Encrypted word: {encrypted_word}")

decrypted_word = vernam_decrypting(encrypted_word)
print(f"Decrypted word: {decrypted_word}")
