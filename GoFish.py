import random

# We can ignore suits since Go Fish does not need them; just use ranks.
possible_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = possible_cards * 4  # Full deck with 4 of each rank

turn = True  # True = player 1's turn, False = player 2's turn

# Initialize each player's hand as a dictionary (card -> count)
player1_deck = {}
player2_deck = {}

# Lists to store completed sets for each player
player1_set = []
player2_set = []

# Main function to run the game loop
def main():
    while(True):
        print("\n\n\n\n\n\n\n")

        welcome()
        init()
        play()
        end_game()

        # Ask the user if they want to play again
        again = input("Would you like to play again? (y/n): ")
        if(again.lower() != 'y'):
            print("\nThanks for playing!")
            break
        else:
            reset()

# Resets all variables to their initial state for a new game
def reset():
    global deck, turn, player1_deck, player1_set, player2_deck, player2_set
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4

    turn = True

    player1_deck = {}
    player2_deck = {}

    player1_set = []
    player2_set = []

# Display final scores and winner
def end_game():
    print("Player 1's sets: " + str(player1_set))
    print("Player 2's sets: " + str(player2_set) + "\n")

    if(len(player1_set) > len(player2_set)):
        print("Player 1 wins!")
    elif(len(player1_set) == len(player2_set)):
        print("Draw!")
    else:
        print("Player 2 wins!")

# Welcome screen and instructions
def welcome():
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
    print()

# Helper function to draw cards from the deck and add to a player's hand
def draw_card(player, amount):
    if(player == 1):
        for i in range(amount):
            card = deck[random.randint(0, len(deck)-1)]
            deck.remove(card)

            if(card not in player1_deck.keys()):
                player1_deck[card] = 1
            else:
                player1_deck[card] = player1_deck[card] + 1
    elif(player == 2):
        for i in range(amount):
            card = deck[random.randint(0, len(deck)-1)]
            deck.remove(card)

            if(card not in player2_deck.keys()):
                player2_deck[card] = 1
            else:
                player2_deck[card] = player2_deck[card] + 1

# Checks both players' decks for any completed sets of 2 cards
def check_set(player):
    to_remove = []
    if(player == 1):
        for i in player1_deck:
            if(player1_deck[i] == 2):
                print(f"\nPlayer 1 has a set of {i}!")
                player1_set.append(i)
                to_remove.append(i)
        for i in to_remove:
            player1_deck.pop(i)

    elif(player == 2):
        for i in player2_deck:
            if(player2_deck[i] == 2):
                print(f"\nPlayer 2 has a set of {i}!")
                player2_set.append(i)
                to_remove.append(i)
        for i in to_remove:
            player2_deck.pop(i)

# Deals 7 cards to each player and checks for starting sets
def init():
    for i in range(0, 7):
        draw_card(1, 1)
        draw_card(2, 1)

    check_set(1)
    check_set(2)

# The core gameplay loop
def play():
    global turn
    while(True):
        # Check if player 1 needs cards
        if(len(player1_deck) == 0):
            print("Player 1's deck is empty")
            if(len(deck) == 0):
                print("No cards left to deal! Game over!")
                break
            else:
                print("Adding cards to deck...")
                draw_card(1, 7)

        # Check if player 2 needs cards
        if(len(player2_deck) == 0):
            print("Player 2's deck is empty")
            if(len(deck) == 0):
                print("No cards left to deal! Game over!")
                break
            else:
                print("Adding cards to deck...")
                draw_card(2, 7)

        # Print current hand for both players
        print("\nPlayer 1's deck: " + str(player1_deck))
        print("Player 2's deck: " + str(player2_deck))

        if(turn):  # Player 1's turn
            turn = not turn
            print("\nPlayer 1's Turn!")
            ask = input("Enter the card you are fishing for ('a' for ace, 'k' for king, 'q' for queen, 'j' for jack): ").upper()
            print("\n")

            # Validate input
            if(ask not in possible_cards):
                print("Sorry, that is not a valid card. Please try again.")
                turn = not turn
                continue

            # Check if player 2 has the card
            if(ask in player2_deck.keys()):
                turn = not turn  # Player goes again
                amount_given = player2_deck[ask]
                player2_deck.pop(ask)

                print(f"Player 2 had {amount_given} {ask}('s)! Adding them to your deck...")

                if(ask in player1_deck.keys()):
                    player1_deck[ask] = amount_given + player1_deck[ask]
                else:
                    player1_deck[ask] = amount_given
                check_set(1)
            else:
                # Go Fish: draw from deck
                print("Player 1, GO FISH!")

                if(len(deck) == 0):
                    print("No cards left to deal! Game over!")
                    break
                else:
                    draw_card(1, 1)

                check_set(1)
        else:  # Player 2's turn
            turn = not turn
            print("\nPlayer 2's Turn!")
            ask = input("Enter the card you are fishing for ('a' for ace, 'k' for king, 'q' for queen, 'j' for jack): ").upper()
            print("\n")

            # Validate input
            if(ask not in possible_cards):
                print("Sorry, that is not a valid card. Please try again.")
                turn = not turn
                continue

            # Check if player 1 has the card
            if(ask in player1_deck.keys()):
                turn = not turn  # Player goes again
                amount_given = player1_deck[ask]
                player1_deck.pop(ask)

                print(f"Player 1 had {amount_given} {ask}('s)! Adding them to your deck...")

                if(ask in player2_deck.keys()):
                    player2_deck[ask] = amount_given + player2_deck[ask]
                else:
                    player2_deck[ask] = amount_given
                check_set(2)
            else:
                # Go Fish: draw from deck
                print("\nPlayer 2, GO FISH!")

                if(len(deck) == 0):
                    print("No cards left to deal! Game over!")
                    break
                else:
                    draw_card(2, 1)

                check_set(2)

        # Check if game is over (all sets made)
        if((len(deck) == 0) and (len(player1_set) + len(player2_set)) == 13):
            break

# Start the game
main()