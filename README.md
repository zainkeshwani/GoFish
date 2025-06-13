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

You’ll be prompted to enter your name and choose if the player is human or AI (and at what level).

🕹️ Game Rules

Each player starts with a hand of cards.

On your turn, ask the opponent for a rank you have.

If they have it, you get their cards and go again.

If not: "Go Fish!" — draw from the deck.

Collect 4 cards of the same rank to make a set.

The game ends when all sets are collected. Highest number of sets wins.

🤖 AI Levels Explained

Level

Behavior

Strategy

1

Random guess

Purely chance

2

Memory-based

Remembers cards the opponent asked for

3

Self-learning AI (Reinforcement)

Adapts and improves over time

🛠️ Requirements

Python 3.x

No external libraries required

📚 Educational Value

This project showcases:

Socket programming in Python

Modular design and separation of logic

Low-level reinforcement learning concepts

AI decision-making strategies

Real-time multiplayer architecture

🏆 Author -- Zain Keshwani

Built and developed as a hands-on software engineering project. Adaptable, smart, and endlessly replayable — Go Fish has never been this fun to beat.

Have fun fishing! 🎣