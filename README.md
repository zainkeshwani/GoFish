# 🐟 Go Fish — Multiplayer Python Network Game

This is a two-player **Go Fish** card game built in Python with networked multiplayer using sockets. One player runs the server, and both players connect via clients.

---

## 🎮 How to Play

- Players take turns asking each other for cards to form **sets of four** (e.g., four Kings).
- If the other player has any cards of the rank requested, they must hand them over.
- If not, they say **“Go Fish,”** and the asking player draws a card from the deck.
- When a player forms a set, it is scored automatically.
- The game ends when:
  - All 13 sets have been completed,
  - The deck is empty **and** both players have no cards,
  - Or no more valid moves are possible.

---

## 🧠 Features

- ✅ Turn-based gameplay with clear player prompts
- ✅ Hidden hands — each player only sees their own
- ✅ Real-time networked communication between two terminals
- ✅ Automatic set detection and scoring
- ✅ Graceful game-over handling

---

## 🛠 Requirements

- Python 3.x

No external libraries required. Only Python’s built-in `socket` module is used.

---

## 🚀 How to Run

1. **Start the server:**

   python server.py
In two separate terminals (or machines), run the client:
python client.py


Follow the prompts:

Enter your name.

View your hand.

Ask for a card (e.g., A, 10, Q, etc.).

Try to complete as many sets as you can!

📂 Project Structure

📁 go-fish/
├── server.py          # Main server hosting the game
├── client.py          # Client interface for players
├── game_logic.py      # Core classes: Player, Game
├── network_utils.py   # Functions to send/receive string data
└── README.md          # You're here!

📝 Notes
Designed strictly for 2 players only

Meant to be run on the same machine or over a LAN (use the local IP for remote connection)

All data is transmitted using plain newline-terminated strings

Hands and moves are kept private for fairness

If either player disconnects, the game ends

📸 Sample Gameplay

Player 1: What card are you fishing for?
> Q
Player 2 says: Go Fish!
You drew: 7

Player 2: What card are you fishing for?
> 10
Player 1 had 2 10(s). You get another turn!

👥 Authors

Created by Zain Keshwani
