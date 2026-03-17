import re
from collections import Counter

def analyze_text(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Normalize text
    text = text.lower().strip()

    # Extract words
    words = re.findall(r'\b\w+\b', text)

    if not words:
        return {
            "word_count": 0,
            "unique_words": 0,
            "most_common": [],
            "average_length": 0
        }

    word_count = len(words)
    unique_words = len(set(words))
    most_common = Counter(words).most_common(3)
    average_length = sum(len(word) for word in words) / word_count

    return {
        "word_count": word_count,
        "unique_words": unique_words,
        "most_common": most_common,
        "average_length": round(average_length, 2)
    }


if __name__ == "__main__":
    sample_text = input("Enter text: ")
    result = analyze_text(sample_text)
    print("\nAnalysis:")
    for key, value in result.items():
        print(f"{key}: {value}")
