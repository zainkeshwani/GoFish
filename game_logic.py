import random

class Player:
    def __init__(self, name, is_machine, level, player_deck, set1):
        self.name = name
        self.is_machine = is_machine
        self.player_deck = player_deck
        self.set = set1

        if(level != 0):
            self.level = level
            self.player_asked = set()  # For level two
            self.ai_memory = {
                "opponent_requests": {},
                "seen_cards": {},
                "sets_made": set(),
                "last_asked": None,
                "rank_scores": {rank: 0.0 for rank in Game.possible_cards}
            }

    def check_set(self):
        to_remove = []
        copy = None
        found = False
        for i in self.player_deck:
            if self.player_deck[i] >= 4:
                print(f"\nPlayer {self.name} has a set of {i}!")
                self.set.append(i)
                to_remove.append(i)
        if to_remove:
            found = True
            copy = to_remove
        for i in to_remove:
            self.player_deck.pop(i)

        return copy if found else None

    def ask_card(self):
        if not self.is_machine or self.level == 0:
            return None

        hand = list(self.player_deck.keys())
        if not hand:
            return None

        if self.level == 1:
            return random.choice(hand)
        elif self.level == 2:
            hand_set = set(hand)
            possible = hand_set.intersection(self.player_asked)
            return random.choice(list(possible)) if possible else random.choice(hand)
        else:
            self.decay_scores()  # <--- decay each turn for recency

            epsilon = 0.2  # Explore 20% of time
            if random.random() < epsilon:
                choice = random.choice(hand)
            else:
                card_scores = {}
                for card in hand:
                    if card in self.set:
                        continue

                    score = self.ai_memory["rank_scores"].get(card, 0.0)

                    # Slight penalty for asking same card twice
                    if card == self.ai_memory.get("last_asked"):
                        score -= 0.5

                    card_scores[card] = score

                choice = max(card_scores, key=card_scores.get) if card_scores else random.choice(hand)

            self.ai_memory["last_asked"] = choice
            return choice

    def learn_from_result(self, rank, success):
        if self.level != 3:
            return

        if success:
            self.ai_memory["rank_scores"][rank] += 1.0  # reward
        else:
            self.ai_memory["rank_scores"][rank] -= 0.3  # penalty

        # Clamp the score to avoid extreme growth
        self.ai_memory["rank_scores"][rank] = max(min(self.ai_memory["rank_scores"][rank], 5.0), -2.0)

    def decay_scores(self):
        if self.level != 3:
            return

        decay_factor = 0.95  # Every move, scores decay by 5%
        for rank in self.ai_memory["rank_scores"]:
            self.ai_memory["rank_scores"][rank] *= decay_factor





class Game:
    possible_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.deck = self.possible_cards * 4

    def draw_card(self, player, amount):
        for _ in range(amount):
            if not self.deck:
                return
            card = random.choice(self.deck)
            self.deck.remove(card)

            if card not in player.player_deck:
                player.player_deck[card] = 1
            else:
                player.player_deck[card] += 1
                
        if(amount==1):
            return card
        return None

    def reset(self):
        self.deck = self.possible_cards * 4
        self.player1.player_deck.clear()
        self.player2.player_deck.clear()
        self.player1.set.clear()
        self.player2.set.clear()

    def end_game(self):
        #print(f"Player {self.player1.name}'s sets: {self.player1.set}")
        #print(f"Player {self.player2.name}'s sets: {self.player2.set}\n")

        if len(self.player1.set) > len(self.player2.set):
            #print(f'Player "{self.player1.name}" wins!')
            return 1
        elif len(self.player1.set) == len(self.player2.set):
            #print("Draw!")
            return 0
        else:
            #print(f'Player "{self.player2.name}" wins!')
            return 2