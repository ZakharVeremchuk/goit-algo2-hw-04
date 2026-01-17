class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def put(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"Ключ має бути рядком, отримано: {type(key).__name__}")

        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.value = value

    def keys_with_prefix(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        results = []
        self._collect(current, list(prefix), results)
        return results

    def _collect(self, node, path, results):
        if node.value is not None:
            results.append("".join(path))

        for char, next_node in node.children.items():
            path.append(char)
            self._collect(next_node, path, results)
            path.pop()


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        # Перевірка вхідних даних
        if not isinstance(pattern, str):
            raise TypeError(f"Суфікс має бути рядком, отримано: {type(pattern).__name__}")

        # Отримуємо всі слова з дерева (префікс "")
        all_words = self.keys_with_prefix("")

        # Підраховуємо кількість слів, що закінчуються на pattern
        count = sum(1 for word in all_words if word.endswith(pattern))
        return count

    def has_prefix(self, prefix) -> bool:
        # Перевіряємл вхідних даних
        if not isinstance(prefix, str):
            raise TypeError(f"Префікс має бути рядком, отримано: {type(prefix).__name__}")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]

        return True


# Тестування
if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка count_words_with_suffix
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat
    print("Все окей")

    # Перевірка has_prefix
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
    print("Все окей")

    try:
        trie.has_prefix(123)
    except TypeError as e:
        print(f"Помилка появилася (очікувано): {e}")