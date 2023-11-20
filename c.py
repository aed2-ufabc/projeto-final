from pygtrie import StringTrie
trie = StringTrie()
words = ["apple", "banana", "cherry"]
for w in words:
    trie[w] = True

print(trie.has_key('apple'))
print(trie.has_key('appl'))
print(trie.has_node('appl'))
print(trie.has_subtrie('appl'))
print(trie.items(prefix='apple'))
