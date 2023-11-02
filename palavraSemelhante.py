class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

root = TrieNode()

def insert_word(root, word):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True

words = ["cat", "dog", "bat", "coat", "cog", "cage", "dogs", "coast", "cost", "cast"]
for word in words:
    insert_word(root, word)

# Função para sugestão de palavras similares na árvore Trie usando Levenshtein
def suggest_similar_words(root, word, max_distance):
    similar_words = []

    def dfs(node, current_word, distance):
        if node.is_end_of_word:
            if distance <= max_distance:
                similar_words.append(current_word)

        if len(current_word) < len(word):
            for char, next_node in node.children.items():
                cost = 0 if char == word[len(current_word)] else 1
                dfs(next_node, current_word + char, distance + cost)

    for char, next_node in root.children.items():
        cost = 0 if char == word[0] else 1
        dfs(next_node, char, cost)

    return similar_words

# Encontrar palavras similares à palavra "dog" com distância máxima de 1
similar_words_to_dog = suggest_similar_words(root, "dog", 1)
print(similar_words_to_dog)
