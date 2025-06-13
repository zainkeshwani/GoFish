🐟 Go Fish — Networked Python Game with Smart AI

A fully playable, networked version of the classic card game Go Fish, built in Python with multiple AI levels including a self-learning reinforcement agent. Play against friends or challenge a machine opponent that learns from you as you play.

🎮 Features

✅ Multiplayer support over network using TCP sockets

🧠 Three levels of AI difficulty:

Level 1: Random guessing

Level 2: Memory-based decision making

Level 3: Low-level reinforcement learning that improves during gameplay

🔒 Hidden hands — Each player only sees their own cards

🂿 Card tracking and set detection (collect 4-of-a-kind to score!)

↻ Replayable game flow with fair turn alternation

📉 AI rank preferences decay over time to simulate forgetfulness

⚙️ Modular code structure for easy expansion and debugging

🧠 AI: Reinforcement Learning (Level 3)

Uses an Epsilon-Greedy approach (80% exploit, 20% explore)

Learns card preferences based on:

Past successes (+1.0 reward)

Past failures (-0.3 penalty)

Time decay (-5% per turn)

Avoids asking for the same rank back-to-back

Maintains and updates rank scores based on player behavior

The more you play against Level 3, the smarter it becomes!

🧹 File Structure

go_fish/
├── game_logic.py        # Core game rules, Player and Game classes
├── network_utils.py     # JSON-based send/receive wrappers
├── server.py            # Hosts the game, handles player turns and game state
├── client.py            # Connects to server, lets a human or AI play
├── README.md            # You're reading it!

🚀 How to Play

🢑 Multiplayer Setup

Open two terminals (or two machines).

In one terminal, run the server:

python server.py

In the other terminal(s), connect a player:

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