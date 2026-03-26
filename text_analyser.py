import random
import re
from collections import Counter

FILE_PATH = "POINT TO A DIRECTORY HERE"

# 0 for all
TOP_N = 20
TOP_HAPAX_WORDS = 25
MAX_PHRASE_LENGTH = 2
MAX_WORD_LENGTH_BINS = 12
MAX_LONGEST_WORDS = 20

SHOW_LONGEST   = True
SHOW_WORD_DIST = True
SHOW_PHRASES   = True
SHOW_HAPAX     = True
SHOW_TABLE     = True

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    raw_text = f.read()

total_characters = len(raw_text)

normalised = raw_text.replace('—', ' ').replace('–', ' ').replace('-', ' ')

cleaned = re.sub(r"'s\b", '', normalised)
cleaned = re.sub(r"'", '', cleaned)
cleaned = re.sub(r'[^\w\s]', ' ', cleaned)

words = cleaned.lower().split()
alpha_words = [w for w in words if w.isalpha()]  # single filtered list

alpha_counts = Counter(alpha_words)

total_words = len(alpha_words)
unique_words = len(alpha_counts)
lexical_diversity = unique_words / total_words if total_words else 0
hapax = sum(1 for c in alpha_counts.values() if c == 1)

sentences = [s for s in re.split(r'[.!?]+', normalised) if s.strip()]
avg_sentence_length = total_words / len(sentences) if sentences else 0

longest_words = sorted(alpha_counts, key=len, reverse=True)[:MAX_LONGEST_WORDS or None]

word_lengths = Counter(len(w) for w in alpha_words)
avg_word_length = sum(len(w) for w in alpha_words) / total_words if total_words else 0

top_words = alpha_counts.most_common(TOP_N or None)

phrases_by_length = {}
if SHOW_PHRASES:
    for n in range(2, MAX_PHRASE_LENGTH + 1):
        phrases_by_length[n] = Counter(
            ' '.join(alpha_words[i:i + n])
            for i in range(len(alpha_words) - n + 1)
        ).most_common(TOP_N or None)

print("\n--- Text Analysis ---")

print(f"\nTotal characters: {total_characters:,}")
print(f"Total words: {total_words:,}")
print(f"Unique words: {unique_words}")
print(f"Lexical diversity: {lexical_diversity:.5f}")
print(f"Hapax words: {hapax}")
print(f"Total sentences: {len(sentences)}")
print(f"Avg sentence length: {avg_sentence_length:.2f} words")
print(f"Avg word length: {avg_word_length:.3f} characters")

if SHOW_LONGEST:
    print(f"\nLongest {MAX_LONGEST_WORDS or 'all'} words:")
    for w in longest_words:
        print(f"{len(w)} : {w}")

if SHOW_WORD_DIST:
    print("\nWord length distribution:")
    for length in sorted(l for l in word_lengths if l <= MAX_WORD_LENGTH_BINS):
        print(f"{length} letters: {word_lengths[length]}")

if SHOW_PHRASES:
    for n, top_phrases in phrases_by_length.items():
        print(f"\nTop {n}-word phrases:")
        for phrase, count in top_phrases:
            print(f"{count} : {phrase}")

if SHOW_HAPAX:
    hapax_words = [word for word, count in alpha_counts.items() if count == 1]
    print(f"\n{TOP_HAPAX_WORDS} random hapax words:")
    for word in random.sample(hapax_words, min(TOP_HAPAX_WORDS, len(hapax_words))):
        print(f"{word}")

if SHOW_TABLE:
    top_n_label = TOP_N if TOP_N else "All"
    print(f"\n--- Table (Top {top_n_label}) ---\n")
    print(f"{'Rank':>8} | {'Word':<8} | Frequency")
    print('-' * 30)
    for rank, (word, count) in enumerate(top_words, start=1):
        print(f"{rank:>8} | {word:<8} | {count}")
