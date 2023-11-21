import time
import csv
from ftplib import FTP
from pygtrie import StringTrie

ftp_user = 'username'
ftp_password = 'mypass'
json_data = None
last_first_letter = None
last_idiom = None

class TrieNode:
    __slots__ = "value", "children"
    def __init__(self):
        self.value = None
        self.children = {}

    def insert( self, word, value):
        node = self
        for letter in word:
            code_point = ord(letter)
            if code_point not in node.children: 
                node.children[code_point] = TrieNode()

            node = node.children[code_point]
        node.value = value #this serves as a signal that it is a word


    def get(self, word, default=None):
        val = self._get_value(word)
        if val is None:
            return default
        else:
            return val

    def _get_value(self, word):
        node = self
        for letter in word:
            code_point = ord(letter)
            try:
                node = node.children[code_point]
            except KeyError:
                return None
        return node.value
    
    def suggest_similar_words(self, query, max_distance=1):
        suggestions = []
        self._suggest_similar_words_recursive(self, "", query + "a", max_distance, suggestions)
         # limit the number of similar words
        filtered  = []
        word_len = len(query)
        for w in suggestions:
            similar_len = len(w)
            if word_len - 1 <= similar_len <= word_len + 1:
                filtered.append(w)

        return filtered

    def _suggest_similar_words_recursive(self, node, current_word, query, max_distance, suggestions):
        if node.value is not None and self._levenshtein_distance(current_word, query) <= max_distance:
            suggestions.append(current_word)

        for code_point, child_node in node.children.items():
            next_char = chr(code_point)
            self._suggest_similar_words_recursive(child_node, current_word + next_char, query, max_distance, suggestions)

    def _levenshtein_distance(self, word1, word2):
        len1, len2 = len(word1), len(word2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[len1][len2]

def download_file(ftp_host, ftp_user, ftp_password, remote_file_path):

    try:
        with FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.encoding='utf-8'
            start = time.time()
            trie = TrieNode()

            temp = './temp.csv'
            with open(temp, 'wb') as fp:
                ftp.retrbinary('RETR ' + remote_file_path, fp.write)
                fp.close()

            with open(temp, 'r')as fp:
                reader = csv.reader(fp, delimiter=",")
                for _, line in enumerate(reader):
                    trie.insert(line[0], True)

            end = time.time()
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
        
        meaning = trie.get(user_input)
        if meaning:
            print(f'"{user_input}": {meaning}', flush=True)
            return

        similar_words = trie.suggest_similar_words(user_input, 1)
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
