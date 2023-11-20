import time
from queue import Queue
from threading import Thread
import csv
from ftplib import FTP
from pygtrie import StringTrie

ftp_user = 'username'
ftp_password = 'mypass'
json_data = None
last_first_letter = None
last_idiom = None

class LineQueue:
    _queue = Queue(50)

    def add(self, s):
        self._queue.put(s)

    def done(self):
        self._queue.put(False)

    def __iter__(self):
        while True:
            s = self._queue.get()
            if s == False:
                break
            yield s



def suggest_similar_words(root, word, max_distance):
    similar_words = []
    word_len = len(word)
    word = word + "a"

    def dfs(node, current_word, distance):
        if 'meaning' in node:
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

def download_file(ftp_host, ftp_user, ftp_password, remote_file_path):

    try:
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.encoding='utf-8'

            q = LineQueue()

            def download():
                ftp.retrlines('RETR ' + remote_file_path, q.add)
                q.done()

            thread = Thread(target=download)
            thread.start()
            start = time.time()
            trie = StringTrie()
            for entry in csv.reader(q):
                if len(entry) != 0:
                    trie[entry[0]] = True
            end = time.time()
            thread.join()
            ftp.quit()
            print(f"Downloaded in {end - start} seconds", flush=True)
            return trie
           
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return False

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
    global trie 
    global last_idiom

    try:
        first_letter = user_input[0]
        if first_letter != last_first_letter and last_idiom != idiom_input:
            remote_file_path = '/'+first_letter+'.csv'
            last_first_letter = first_letter
            last_idiom = idiom_input
            host = get_host(user_input, idiom_input, first_letter)
            trie = download_file(host, ftp_user, ftp_password, remote_file_path)
            if trie == False:
                not_found_print(user_input, idiom_input)
                return
        
        meaning = trie.has_key(user_input)
        if meaning:
            print(f'"{user_input}": {meaning}', flush=True)
            return

        similar_words = suggest_similar_words(trie, user_input, 1)
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
