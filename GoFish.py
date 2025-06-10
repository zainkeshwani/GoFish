"""


*******************************************************************************************************************
NOTE:
This is the beta version of the game. There are no networking capabilities here. Kept for reference purposes.
*******************************************************************************************************************


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
            if(self.player_deck[i] == 2):
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
        self.deck = self.possible_cards*4
        self.turn = turn

    def draw_card(self, player, amount):
        for i in range(amount):
            card = self.deck[random.randint(0, len(self.deck)-1)]
            self.deck.remove(card)

            if(card not in player.player_deck.keys()):
                player.player_deck[card] = 1
            else:
                player.player_deck[card] = player.player_deck[card] + 1

    def reset(self):
        self.deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4

        self.turn = True

        self.player1.player_deck = {}
        self.player2.player_deck = {}

        self.player1.set = []
        self.player2.set = []

    def end_game(self):
        print(f"Player {self.player1.name}'s sets: " + str(self.player1.set))
        print(f"Player {self.player2.name}'s sets: " + str(self.player2.set) + "\n")

        if(len(self.player1.set) > len(self.player2.set)):
            print(f'Player "{self.player1.name}" wins!')
        elif(len(self.player1.set) == len(self.player2.set)):
            print("Draw!")
        else:
            print(f'Player "{self.player2.name}" wins!')
        
    def play(self):
        while(True):
            # Check if either player needs cards
            break_while = False
            for p in [self.player1, self.player2]:
                if(len(p.player_deck) == 0):
                    print(f"Player {p.name}'s deck is empty")
                    if(len(self.deck) == 0):
                        print("No cards left to deal! Game over!")
                        break_while = True
                        break
                    else:
                        print("Adding cards to deck...")
                        if(len(self.deck) < 7):
                            self.draw_card(p, len(self.deck))
                        else:
                            self.draw_card(p, 7)
                if(break_while):
                    break


            # Print current hand for both players
            print(f"\nPlayer {self.player1.name}'s deck: " + str(self.player1.player_deck))
            print(f"Player {self.player2.name}'s deck: " + str(self.player2.player_deck))

            if(self.turn):  # Player 1's turn
                self.turn = not self.turn
                print(f"\nPlayer {self.player1.name}'s Turn!")
                ask = input("Enter the card you are fishing for ('a' for ace, 'k' for king, 'q' for queen, 'j' for jack): ").upper()
                print("\n")

                # Validate input
                if(ask not in self.possible_cards):
                    print("Sorry, that is not a valid card. Please try again.")
                    self.turn = not self.turn
                    continue

                # Check if player 2 has the card
                if(ask in self.player2.player_deck.keys()):
                    self.turn = not self.turn  # Player goes again
                    amount_given = self.player2.player_deck[ask]
                    self.player2.player_deck.pop(ask)

                    print(f"Player {self.player2.name} had {amount_given} {ask}('s)! Adding them to your deck...")

                    if(ask in self.player1.player_deck.keys()):
                        self.player1.player_deck[ask] = amount_given + self.player1.player_deck[ask]
                    else:
                        self.player1.player_deck[ask] = amount_given
                    self.player1.check_set()
                else:
                    # Go Fish: draw from deck
                    print(f"Player {self.player1.name}, GO FISH!")

                    if(len(self.deck) == 0):
                        print("No cards left to deal! Game over!")
                        break
                    else:
                        self.draw_card(self.player1, 1)

                    self.player1.check_set()
            else:  # Player 2's turn
                self.turn = not self.turn
                print(f"\nPlayer {self.player2.name}'s Turn!")

                if self.player2.is_machine:
                    ask = random.choice(list(self.player2.player_deck.keys()))
                    print(f"{self.player2.name} is fishing for: {ask}")
                else:
                    ask = input("Enter the card you are fishing for ('a' for ace, 'k' for king, 'q' for queen, 'j' for jack): ").upper()
                    print("\n")

                    # Validate input
                    if(ask not in self.possible_cards):
                        print("Sorry, that is not a valid card. Please try again.")
                        self.turn = not self.turn
                        continue

                # Check if player 1 has the card
                if(ask in self.player1.player_deck.keys()):
                    self.turn = not self.turn  # Player goes again
                    amount_given = self.player1.player_deck[ask]
                    self.player1.player_deck.pop(ask)

                    print(f"Player {self.player1.name} had {amount_given} {ask}('s)! Adding them to your deck...")

                    if(ask in self.player2.player_deck.keys()):
                        self.player2.player_deck[ask] = amount_given + self.player2.player_deck[ask]
                    else:
                        self.player2.player_deck[ask] = amount_given
                    self.player2.check_set()
                else:
                    # Go Fish: draw from deck
                    print(f"\nPlayer {self.player2.name}, GO FISH!")

                    if(len(self.deck) == 0):
                        print("No cards left to deal! Game over!")
                        break
                    else:
                        self.draw_card(self.player2, 1)

                    self.player2.check_set()

            # Check if game is over (all sets made)
            if((len(self.deck) == 0) and (len(self.player1.set) + len(self.player2.set)) == 13):
                break

# Main function to run the game loop
def main():
    while(True):
        print("=" * 40)
        print("🎣 Welcome to Go Fish! 🎴")
        print("=" * 40)
        print("Instructions:")
        print("1. Try to collect sets of two cards of the same rank (not four to make the game go by a little quicker!).")
        print("2. On your turn, ask another player for a specific rank.")
        print("3. If they have any, you get them and go again.")
        print("4. If not... Go Fish! Draw a card from the deck.")
        print("5. The player with the most sets wins!")
        print("=" * 40)
        print("\n\n\n\n\n\n\n\n")

        type_game = int(input("Will you be playing 1. against the computer, or 2. against another player? (1 or 2) "))

        game = None
        player1 = None
        player2 = None

        if(type_game==2):
            name1 = input("Player 1's name: ")
            player1 = Player(name1, False, {}, [])

            name2 = input("Player 2's name: ")
            player2 = Player(name2, False, {}, [])
        else:
            name1 = input("Player's name: ")
            player1 = Player(name1, False, {}, [])
            player2 = Player("Computer", True, {}, [])

        game = Game(player1, player2, True)

        game.play()
        game.end_game()

        # Ask the user if they want to play again
        again = input("Would you like to play again? (y/n): ")
        if(again.lower() != 'y'):
            print("\nThanks for playing!")
            break

main()





"""