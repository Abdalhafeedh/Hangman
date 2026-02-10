"""
Hangman Game - Text-Based Python Implementation
================================================
A classic word-guessing game where the player tries to uncover a hidden word
by guessing one letter at a time, with a limited number of incorrect guesses.

Author : [Your Name]
Date   : 2026-02-10
Version: 1.0
"""

import random
import os
import sys
import string

# Ensure the console can handle special characters on Windows
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

MAX_INCORRECT_GUESSES = 6  # Number of wrong guesses before the game is over

# Word bank organized by category for variety and educational value
WORD_BANK = {
    "Animals": [
        "elephant", "giraffe", "penguin", "dolphin", "butterfly",
        "kangaroo", "cheetah", "tortoise", "octopus", "flamingo",
    ],
    "Fruits": [
        "strawberry", "pineapple", "blueberry", "watermelon", "banana",
        "mango", "avocado", "pomegranate", "raspberry", "tangerine",
    ],
    "Countries": [
        "australia", "brazil", "canada", "denmark", "egypt",
        "france", "germany", "indonesia", "japan", "mexico",
    ],
    "Programming": [
        "python", "javascript", "algorithm", "variable", "function",
        "database", "compiler", "debugging", "interface", "software",
    ],
    "Sports": [
        "basketball", "football", "swimming", "volleyball", "tennis",
        "baseball", "cricket", "hockey", "badminton", "gymnastics",
    ],
}

# ASCII art stages for the hangman figure (index = number of wrong guesses)
HANGMAN_STAGES = [
    # Stage 0: Empty gallows
    """
      +------+
      |      |
      |
      |
      |
      |
    ===========''
    """,
    # Stage 1: Head
    """
      +------+
      |      |
      |      O
      |
      |
      |
    ===========''
    """,
    # Stage 2: Body
    """
      +------+
      |      |
      |      O
      |      |
      |
      |
    ===========''
    """,
    # Stage 3: Left arm
    """
      +------+
      |      |
      |      O
      |     /|
      |
      |
    ===========''
    """,
    # Stage 4: Right arm
    """
      +------+
      |      |
      |      O
      |     /|\\
      |
      |
    ===========''
    """,
    # Stage 5: Left leg
    """
      +------+
      |      |
      |      O
      |     /|\\
      |     /
      |
    ===========''
    """,
    # Stage 6: Right leg (game over)
    """
      +------+
      |      |
      |      O
      |     /|\\
      |     / \\
      |
    ===========''
    """,
]


# ─────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen for a cleaner display."""
    os.system("cls" if os.name == "nt" else "clear")


def display_title():
    """Display the game's title banner."""
    print("=" * 52)
    print("   _   _                                          ")
    print("  | | | | __ _ _ __   __ _ _ __ ___   __ _ _ __   ")
    print("  | |_| |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\  ")
    print("  |  _  | (_| | | | | (_| | | | | | | (_| | | | | ")
    print("  |_| |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_| ")
    print("                      |___/                       ")
    print("=" * 52)
    print()


def display_word(word, guessed_letters):
    """
    Display the word with guessed letters revealed and unguessed letters
    shown as underscores.

    Args:
        word (str): The secret word to be guessed.
        guessed_letters (set): Set of letters the player has guessed.

    Returns:
        str: The current display string of the word.
    """
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += f" {letter.upper()} "
        else:
            display += " _ "
    return display


def get_random_word():
    """
    Select a random word from a random category in the word bank.

    Returns:
        tuple: A tuple containing (category, word).
    """
    category = random.choice(list(WORD_BANK.keys()))
    word = random.choice(WORD_BANK[category])
    return category, word


def display_game_state(word, guessed_letters, incorrect_guesses, category):
    """
    Display the complete current game state including the hangman figure,
    the word progress, and game information.

    Args:
        word (str): The secret word.
        guessed_letters (set): Set of all guessed letters.
        incorrect_guesses (list): List of incorrectly guessed letters.
        category (str): The category of the word.
    """
    clear_screen()
    display_title()

    # Show category hint
    print(f"  📂 Category: {category}")
    print(f"  ❤️  Lives remaining: {MAX_INCORRECT_GUESSES - len(incorrect_guesses)}"
          f" / {MAX_INCORRECT_GUESSES}")
    print()

    # Show hangman figure
    print(HANGMAN_STAGES[len(incorrect_guesses)])

    # Show word progress
    word_display = display_word(word, guessed_letters)
    print(f"  Word: {word_display}")
    print(f"  ({len(word)} letters)")
    print()

    # Show incorrect guesses
    if incorrect_guesses:
        wrong = ", ".join(letter.upper() for letter in incorrect_guesses)
        print(f"  ❌ Wrong guesses: {wrong}")
    else:
        print("  ❌ Wrong guesses: None")

    # Show available letters
    available = sorted(set(string.ascii_lowercase) - guessed_letters)
    available_display = " ".join(letter.upper() for letter in available)
    print(f"  🔤 Available letters: {available_display}")
    print()


def get_player_guess(guessed_letters):
    """
    Prompt the player for a letter guess with input validation.

    Args:
        guessed_letters (set): Set of already guessed letters.

    Returns:
        str: A valid single lowercase letter not previously guessed.
    """
    while True:
        guess = input("  👉 Enter your guess (a single letter): ").strip().lower()

        # Validate input
        if len(guess) != 1:
            print("  ⚠️  Please enter exactly one letter.")
            continue
        if not guess.isalpha():
            print("  ⚠️  Please enter a valid letter (a-z).")
            continue
        if guess in guessed_letters:
            print(f"  ⚠️  You already guessed '{guess.upper()}'. Try a different letter.")
            continue

        return guess


def check_win(word, guessed_letters):
    """
    Check if all letters in the word have been guessed.

    Args:
        word (str): The secret word.
        guessed_letters (set): Set of all guessed letters.

    Returns:
        bool: True if the player has guessed all letters, False otherwise.
    """
    return all(letter in guessed_letters for letter in word)


def display_game_result(won, word, total_guesses, incorrect_guesses):
    """
    Display the final game result with a summary.

    Args:
        won (bool): Whether the player won the game.
        word (str): The secret word.
        total_guesses (int): Total number of guesses made.
        incorrect_guesses (list): List of wrong guesses.
    """
    print("-" * 52)
    if won:
        print()
        print("  🎉🎉🎉  CONGRATULATIONS! YOU WON!  🎉🎉🎉")
        print()
        print(f"  The word was: {word.upper()}")
        print(f"  Total guesses: {total_guesses}")
        print(f"  Wrong guesses: {len(incorrect_guesses)}")
        accuracy = ((total_guesses - len(incorrect_guesses)) / total_guesses * 100
                     if total_guesses > 0 else 0)
        print(f"  Accuracy: {accuracy:.1f}%")
    else:
        print()
        print("  💀💀💀  GAME OVER! YOU LOST!  💀💀💀")
        print(HANGMAN_STAGES[-1])
        print(f"  The word was: {word.upper()}")
        print(f"  Better luck next time!")
    print()
    print("-" * 52)


# ─────────────────────────────────────────────────────────────────────────────
# Core Game Logic
# ─────────────────────────────────────────────────────────────────────────────

def play_round():
    """
    Play a single round of Hangman.

    Returns:
        bool: True if the player won, False otherwise.
    """
    # Initialize game state
    category, word = get_random_word()
    guessed_letters = set()
    incorrect_guesses = []
    total_guesses = 0

    # Main game loop
    while len(incorrect_guesses) < MAX_INCORRECT_GUESSES:
        # Display current state
        display_game_state(word, guessed_letters, incorrect_guesses, category)

        # Get player's guess
        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)
        total_guesses += 1

        # Check if guess is correct
        if guess in word:
            print(f"\n  ✅ Great! '{guess.upper()}' is in the word!")
        else:
            incorrect_guesses.append(guess)
            remaining = MAX_INCORRECT_GUESSES - len(incorrect_guesses)
            print(f"\n  ❌ Sorry! '{guess.upper()}' is not in the word. "
                  f"({remaining} lives left)")

        # Check for win
        if check_win(word, guessed_letters):
            display_game_state(word, guessed_letters, incorrect_guesses, category)
            display_game_result(True, word, total_guesses, incorrect_guesses)
            return True

        input("\n  Press Enter to continue...")

    # Player lost — show final state
    display_game_state(word, guessed_letters, incorrect_guesses, category)
    display_game_result(False, word, total_guesses, incorrect_guesses)
    return False


def play_game():
    """
    Main game controller that manages multiple rounds, keeps score,
    and handles the play-again loop.
    """
    clear_screen()
    display_title()
    print("  Welcome to the Hangman Game!")
    print("  Try to guess the hidden word one letter at a time.")
    print(f"  You have {MAX_INCORRECT_GUESSES} lives (incorrect guesses).")
    print()
    print("  Word categories: " + ", ".join(WORD_BANK.keys()))
    print()
    input("  Press Enter to start playing...")

    # Score tracking
    wins = 0
    losses = 0

    while True:
        # Play a round
        result = play_round()
        if result:
            wins += 1
        else:
            losses += 1

        # Show running score
        print(f"\n  📊 Score — Wins: {wins} | Losses: {losses}")
        print()

        # Ask to play again
        while True:
            play_again = input("  🔄 Would you like to play again? (yes/no): ").strip().lower()
            if play_again in ("yes", "y"):
                break
            elif play_again in ("no", "n"):
                # Farewell message
                clear_screen()
                display_title()
                print("  Thanks for playing Hangman! 🎮")
                print(f"\n  📊 Final Score — Wins: {wins} | Losses: {losses}")
                total = wins + losses
                if total > 0:
                    win_rate = wins / total * 100
                    print(f"  🏆 Win Rate: {win_rate:.1f}%")
                print("\n  Goodbye! See you next time! 👋\n")
                return
            else:
                print("  ⚠️  Please enter 'yes' or 'no'.")


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    play_game()
