from collections import Counter
from pathlib import Path
import re

import requests


WORD_RE = re.compile(r"[a-zA-Z']+")


def get_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def load_words_to_count(words_file: str) -> list[str]:
    with open(words_file, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in WORD_RE.findall(text)]


def count_word_frequencies(url: str, words_to_count: list[str]) -> dict[str, int]:
    tokens = tokenize(get_text(url))
    counters = Counter(tokens)
    return {word: counters[word] for word in words_to_count}


def main() -> None:
    words_file = str(Path(__file__).with_name("words.txt"))
    url = "https://eng.mipt.ru/why-mipt/"
    words_to_count = load_words_to_count(words_file)
    frequencies = count_word_frequencies(url, words_to_count)
    print(frequencies)


if __name__ == "__main__":
    main()