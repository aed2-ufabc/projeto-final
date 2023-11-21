from ftplib import FTP
from Levenshtein import distance
import time

FTP.maxline = 16384

ftp_user = 'username'
ftp_password = 'mypass'
last_first_letter = None
last_idiom = None
trie = {}

def build_trie(word_meaning_pairs):
    trie = {}
    for word, meaning in word_meaning_pairs:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['me'] = meaning
    return trie

# Função para procurar uma palavra na árvore trie
def search_word(trie, word):
    node = trie
    for char in word:
        if char in node:
            node = node[char]
        else:
            return None
    return node.get('me', None)

def suggest_similar_words(root, word, max_distance):
    similar_words = []
    word_len = len(word)
    word = word + "a"

    def dfs(node, current_word, distance):
        if 'me' in node:
            if distance <= max_distance:
                similar_words.append(current_word)

        if len(current_word) < len(word):
            if not hasattr(node, 'items'):
                return
            for char, next_node in node.items():
                cost = 0 if char == word[len(current_word)] else 1
                dfs(next_node, current_word + char, distance + cost)

    for char, next_node in root.items():
        cost = 0 if char == word[0] else 1
        dfs(next_node, char, cost)

    # limit the number of similar words
    filtered  = []
    for w in similar_words:
        similar_len = len(w)
        if word_len - 1 <= similar_len <= word_len + 1:
            filtered.append(w)

    return filtered


def download_file(ftp_host, ftp_user, ftp_password, remote_file_path, user_input):
    try:
        # Connect to the FTP server
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            # Log in
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.encoding='utf-8'
            
            word_len = len(user_input)
            word_meaning_pairs = []
            def callback(l):
                if l == '':
                    return
                
                a = l.split(',', maxsplit=1)
                word = a[0]
                meaning = a[1]

                similar_len = len(word)
                # this code will ensure that we only load words that are similar to the user input
                if word_len - 1 <= similar_len <= word_len + 1 and (distance(word, user_input) <= 1):
                    word_meaning_pairs.append((word, meaning))

            ftp.retrlines('RETR ' + remote_file_path, callback)
            ftp.quit()
            return word_meaning_pairs
           
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return None

def not_found_print(user_input, idiom_input):
    if idiom_input == "e":
        print(f'La palabra "{user_input}" no se encontró en el diccionario.', flush=True)
        return 
    print(f'The word "{user_input}" was not found in the dictionary.', flush=True)

def similar_print(user_input, idiom_input, similar_words):
    if idiom_input == "e":
        print(f'La palabra "{user_input}" no se encontró. Aca están palabras similares: {", ".join(similar_words)}', flush=True)
        return 
    print(f'The word "{user_input}" was not found in the dictionary. Here are similar words: {", ".join(similar_words)}', flush=True)

def get_host(user_input, idiom_input, first_letter):
    host = verificar_letra(user_input, first_letter)

    if idiom_input == "i" and host == 1:
        return 'remote1'
    elif idiom_input == 'i' and host == 2:
        return 'remote2'
    elif idiom_input == 'e' and host == 1:
        return 'remote3'
    else:
        return 'remote4'

def call_api(user_input, idiom_input):
    global last_first_letter  
    global last_idiom
    global trie

    try:
        first_letter = user_input[0]
        remote_file_path = '/'+first_letter+'.csv'
        host = get_host(user_input, idiom_input, first_letter)
        start_time = time.time()
        word_meaning_pairs = download_file(host, ftp_user, ftp_password, remote_file_path, user_input)
        print("time to download similar words: %s seconds" % (time.time() - start_time))

        if word_meaning_pairs == None:
            not_found_print(user_input, idiom_input)
            return
        
        start_time = time.time()
        trie = build_trie(word_meaning_pairs)
        print("time to build trie: %s seconds" % (time.time() - start_time))

        start_time = time.time()
        meaning = search_word(trie, user_input)
        print("time to search word: %s seconds" % (time.time() - start_time))
        if meaning:
            print(f'"{user_input}": {meaning}', flush=True)
            return

        start_time = time.time()
        similar_words = suggest_similar_words(trie, user_input, 1)
        print("time to find similar words: %s seconds" % (time.time() - start_time))
        if len(similar_words) != 0:
            similar_print(user_input, idiom_input, similar_words)
            return

        not_found_print(user_input, idiom_input)
    except Exception as e:
        print("An error occurred:", e, flush=True)

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
            call_api(user_input.strip(), idiom_input) 
        
        elif idiom_input == 'e': 
            user_input = input("\nIngrese la palabra que desea buscar: ").lower()
            # Chamando a API com a entrada do usuário
            call_api(user_input.strip(), idiom_input) 
        
        elif idiom_input == 's':
            print("\nPrograma encerrado.", flush=True)
        
if __name__ == "__main__":
    main()
