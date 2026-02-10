# Hangman (Python) — Category-Based Text Game

A polished, terminal-based **Hangman** game built in Python.  
The game randomly selects a word from a **category-based word bank**, then the player guesses **one letter at a time** with a limited number of mistakes. A full ASCII hangman figure is drawn step-by-step as incorrect guesses increase.

---

##  Features

- ✅ **Random word selection** from multiple categories (Animals, Fruits, Countries, Programming, Sports)
- ✅ **Category hint** shown to the player (helps guide guesses)
- ✅ **ASCII Hangman drawing** that updates with each wrong guess
- ✅ **Input validation** (single letter only, alphabet only, no repeated guesses)
- ✅ **Available letters display** (shows remaining letters to guess)
- ✅ **Lives system** (default: 6 incorrect guesses)
- ✅ **Round summary** (word reveal, attempts, wrong guesses, accuracy %)
- ✅ **Multi-round gameplay** with **Win/Loss scoreboard**
- ✅ **Cross-platform terminal support** (Windows / macOS / Linux)
- ✅ Windows console encoding handling for better symbol/emoji display

---

##  How the Game Works

1. The computer picks a **random category** and a **secret word**
2. The player guesses **one letter at a time**
3. If the guess is correct → letters are revealed in the word
4. If the guess is wrong → a life is lost, and the hangman drawing progresses
5. The player wins by revealing **all letters** before losing all lives  
6. The player loses after **6 incorrect guesses**

---

##  Project Structure (Core Components)

### Constants
- `MAX_INCORRECT_GUESSES`: number of allowed mistakes (default: 6)
- `WORD_BANK`: dictionary of categories mapped to word lists
- `HANGMAN_STAGES`: list of ASCII drawings (0 → 6 wrong guesses)

### Key Functions
- `get_random_word()` → selects random category + word
- `display_word()` → shows guessed letters and `_` for hidden letters
- `get_player_guess()` → validates player input
- `check_win()` → checks if all letters are guessed
- `display_game_state()` → prints the full game UI (drawing + word + stats)
- `play_round()` → controls a single round loop until win/lose
- `play_game()` → manages multiple rounds + scoreboard






