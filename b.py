class TrieNode:
    def __init__(self):
        self.children={}
        self.end=False
class Trie:
    def __init__(self):
        self.root=TrieNode()

    def insert(self, word: str) -> None:
        curr=self.root
        for i in word:
            if i not in curr.children:
                curr.children[i]=TrieNode()
            curr=curr.children[i]
        curr.end=True

    def search(self, word: str) -> bool:
        curr=self.root
        for i in word:
            if i not in curr.children:
                return False
            curr=curr.children[i]
        return curr.end

    def startsWith(self, prefix: str) -> bool:
        curr=self.root
        for i in prefix:
            if i not in curr.children:
                return False
            curr=curr.children[i]
        return True

trie = Trie()
trie.insert("a")
trie.insert("aba")
trie.insert("abaá")

print(trie.search("a"))
print(trie.search("abaá"))