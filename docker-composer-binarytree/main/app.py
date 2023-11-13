import json
from ftplib import FTP
from io import BytesIO
import os

ftp_user = 'username'
ftp_password = 'mypass'


script_dir = os.path.dirname(os.path.realpath(__file__))

# Construir a árvore trie
def build_trie(dictionary):
    trie = {}
    for word, meaning in dictionary.items():
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['meaning'] = meaning
    return trie

# Função para procurar uma palavra na árvore trie
def search_word(trie, word):
    node = trie
    for char in word:
        if char in node:
            node = node[char]
        else:
            return None
    return node.get('meaning', None)

def read_file(file):
    try:
        file_path = os.path.join(script_dir, 'files', file + '.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            dictionary = json.load(file)
            return dictionary
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def download_file(ftp_host, ftp_user, ftp_password, remote_file_path):
    try:
        # Connect to the FTP server
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            # Log in
            ftp.login(user=ftp_user, passwd=ftp_password)

            # Change to the appropriate directory if needed
            # ftp.cwd('/path/to/remote/directory')
            # Open a local file for writing in binary mode
           # Use BytesIO to store the file content in memory
            file_content = BytesIO()

            # Retrieve the remote file and write it to BytesIO
            ftp.retrbinary('RETR ' + remote_file_path, file_content.write)

            # Move the cursor to the beginning of the BytesIO buffer
            file_content.seek(0)

            # Read the content of BytesIO into a JSON variable
            json_data = json.load(file_content)
            return json_data
        
    except Exception as e:
        print(f"An error occurred: {e}")


def call_api(user_input, idiom_input):
    # Verificando a letra digitada, para setar host
    first_letter = user_input[0].lower()
    host = verificar_letra(user_input, first_letter)

    if idiom_input == "i" and host == 1:
        host = 'remote1'
    elif idiom_input == 'i' and host == 2:
        host = 'remote2'
    elif idiom_input == 'e' and host == 1:
        host = 'remote3'
    else:
        host = 'remote4' 
    
    print(host)

    remote_file_path = '/'+first_letter+'.json'
    try:
        json_data = download_file(host, ftp_user, ftp_password, remote_file_path)
        trie = build_trie(json_data)
        meaning = search_word(trie, user_input)
        if meaning:
                print(f'"{user_input}": {meaning}')
        else:
            if idiom_input == "i":
                print(f'The word "{user_input}" was not found in the dictionary.')
            elif idiom_input == "e":
                print(f'La palabra "{user_input}" no se encontró en el diccionario.')
    except Exception as e:
        print("An error occurred:", e)

def verificar_letra(word, first_letter):
    if word and first_letter >= 'a' and first_letter <= 'm':
        return 1
    else:
        return 2

def main():
    idiom_input = 'i'

    while(idiom_input.lower() != 's'):
        # Pedir ao usuário para inserir o idioma
        idiom_input = input("\nDigite o idioma desejado \nI - Inglês \nE - Espanhol \nS - Sair\n\n").lower()
        
        if idiom_input == 'i':
            user_input = input("\nEnter the word you want to search for: ").lower()
            # Chamando a API com a entrada do usuário
            call_api(user_input, idiom_input) 
        
        elif idiom_input == 'e': 
            user_input = input("\nIngrese la palabra que desea buscar: ").lower()
            # Chamando a API com a entrada do usuário
            call_api(user_input, idiom_input) 
        
        elif idiom_input == 's':
            print("\nPrograma encerrado.")
        
if __name__ == "__main__":
    main()
