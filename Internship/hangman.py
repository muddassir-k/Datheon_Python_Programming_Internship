import random


WORDS = ["PYTHON", "GALLOWS", "TERMINAL", "PROGRAM"]
MAX_MISTAKES = 6

HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =======
    """,
]


def play() -> None:
    word = random.choice(WORDS)
    guessed_letters: set[str] = set()
    mistakes = 0

    print("Welcome to Hangman!")

    while mistakes < MAX_MISTAKES:
        print(HANGMAN_STAGES[mistakes])
        print("Word: " + " ".join(letter if letter in guessed_letters else "_" for letter in word))
        print(f"Guessed letters: {' '.join(sorted(guessed_letters)) or '(none)'}")
        print(f"Mistakes remaining: {MAX_MISTAKES - mistakes}")

        guess = input("Guess a letter: ").strip().upper()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.\n")
            continue
        if guess in guessed_letters:
            print(f"You already guessed {guess}; no attempt is deducted.\n")
            continue

        guessed_letters.add(guess)
        if guess in word:
            print("Good guess!\n")
            if all(letter in guessed_letters for letter in word):
                print(f"You win! The word was {word}.")
                return
        else:
            mistakes += 1
            print("That letter is not in the word.\n")

    print(HANGMAN_STAGES[mistakes])
    print(f"You are out of attempts. The word was {word}.")


if __name__ == "__main__":
    play()
