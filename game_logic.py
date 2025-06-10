import random

class Player:
    def __init__(self, name, is_machine, player_deck, set):
        self.name = name
        self.is_machine = is_machine
        self.player_deck = player_deck
        self.set = set

    def check_set(self):
        to_remove = []
        for i in self.player_deck:
            if self.player_deck[i] >= 2:
                print(f"\nPlayer {self.name} has a set of {i}!")
                self.set.append(i)
                to_remove.append(i)
        for i in to_remove:
            self.player_deck.pop(i)


class Game:
    possible_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, player1, player2, turn):
        self.player1 = player1
        self.player2 = player2
        self.deck = self.possible_cards * 4
        self.turn = turn

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

    def reset(self):
        self.deck = self.possible_cards * 4
        self.turn = True
        self.player1.player_deck.clear()
        self.player2.player_deck.clear()
        self.player1.set.clear()
        self.player2.set.clear()

    def end_game(self):
        print(f"Player {self.player1.name}'s sets: {self.player1.set}")
        print(f"Player {self.player2.name}'s sets: {self.player2.set}\n")

        if len(self.player1.set) > len(self.player2.set):
            print(f'Player "{self.player1.name}" wins!')
        elif len(self.player1.set) == len(self.player2.set):
            print("Draw!")
        else:
            print(f'Player "{self.player2.name}" wins!')
