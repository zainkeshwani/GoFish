import socket
from game_logic import Player, Game
from network_utils import send_data, receive_data

HOST = '127.0.0.1'
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        print(f"Server listening on {HOST}:{PORT}")

        conn1, addr1 = s.accept()
        print(f"Player 1 connected from {addr1}")
        send_data(conn1, "Welcome Player 1! Please enter your name:")
        name1 = receive_data(conn1)
        player1 = Player(name1, False, {}, [])

        conn2, addr2 = s.accept()
        print(f"Player 2 connected from {addr2}")
        send_data(conn2, "Welcome Player 2! Please enter your name:")
        name2 = receive_data(conn2)
        player2 = Player(name2, False, {}, [])

        game = Game(player1, player2, True)
        game.reset()
        game.draw_card(player1, 7)
        game.draw_card(player2, 7)
        
        player1.check_set()
        player2.check_set()

        send_data(conn1, "Game starts!")
        send_data(conn2, "Game starts!")

        turn = 0

        while True:
            if turn == 0:

                if(len(player1.player_deck) == 0):
                    game.draw_card(player1, 7)
                if(len(player2.player_deck) == 0):
                    game.draw_card(player2, 7)


                send_data(conn1, f"\n{player1.name}'s turn!")
                send_data(conn2, f"\n{player1.name}'s turn!")

                send_data(conn1, f"Your hand: {player1.player_deck}")
                send_data(conn2, "Waiting for other player's move...")

                send_data(conn1, "What card are you fishing for (e.g., 2-10, J, Q, K, A)?")
                ask = receive_data(conn1)

                if ask is None:
                    break

                ask = ask.upper()
                if ask not in Game.possible_cards:
                    send_data(conn1, "Invalid card name. Try again.")
                    continue

                """
                if ask not in player1.player_deck:
                    send_data(conn1, f"You don't have any {ask}s in your hand. Try again.")
                    continue
                """

                if ask in player2.player_deck:
                    amount = player2.player_deck.pop(ask)
                    player1.player_deck[ask] = player1.player_deck.get(ask, 0) + amount
                    msg = f"{player2.name} had {amount} {ask}(s). {player1.name} gets another turn!"
                    send_data(conn1, msg)
                    send_data(conn2, msg)
                    player1.check_set()
                    continue
                else:
                    msg = f"{player2.name} says: Go Fish!"
                    send_data(conn1, msg)
                    send_data(conn2, msg)
                    if len(game.deck) > 0:
                        game.draw_card(player1, 1)
                    else:
                        send_data(conn1, "No cards left in deck to draw.")
                        send_data(conn2, "No cards left in deck to draw.")
                    player1.check_set()
                    turn = 1

            else:

                if(len(player1.player_deck) == 0):
                    game.draw_card(player1, 7)
                if(len(player2.player_deck) == 0):
                    game.draw_card(player2, 7)

                send_data(conn1, f"\n{player2.name}'s turn!")
                send_data(conn2, f"\n{player2.name}'s turn!")

                send_data(conn2, f"Your hand: {player2.player_deck}")
                send_data(conn1, "Waiting for other player's move...")

                send_data(conn2, "What card are you fishing for (e.g., 2-10, J, Q, K, A)?")
                ask = receive_data(conn2)

                if ask is None:
                    break

                ask = ask.upper()
                if ask not in Game.possible_cards:
                    send_data(conn2, "Invalid card name. Try again.")
                    continue

                """
                if ask not in player2.player_deck:
                    send_data(conn2, f"You don't have any {ask}s in your hand. Try again.")
                    continue
                """

                if ask in player1.player_deck:
                    amount = player1.player_deck.pop(ask)
                    player2.player_deck[ask] = player2.player_deck.get(ask, 0) + amount
                    msg = f"{player1.name} had {amount} {ask}(s). {player2.name} gets another turn!"
                    send_data(conn1, msg)
                    send_data(conn2, msg)
                    player2.check_set()
                    continue
                else:
                    msg = f"{player1.name} says: Go Fish!"
                    send_data(conn1, msg)
                    send_data(conn2, msg)
                    if len(game.deck) > 0:
                        game.draw_card(player2, 1)
                    else:
                        send_data(conn1, "No cards left in deck to draw.")
                        send_data(conn2, "No cards left in deck to draw.")
                    player2.check_set()
                    turn = 0

            total_sets = len(player1.set) + len(player2.set)
            if total_sets == 13:
                break

            if len(game.deck) == 0:
                if len(player1.player_deck) == 0 or len(player2.player_deck) == 0:
                    break


        game_over_msg = f"\nGame Over!\n{player1.name}'s sets: {player1.set}\n{player2.name}'s sets: {player2.set}"
        send_data(conn1, game_over_msg)
        send_data(conn2, game_over_msg)

        if len(player1.set) > len(player2.set):
            winner_msg = f"{player1.name} wins!"
        elif len(player2.set) > len(player1.set):
            winner_msg = f"{player2.name} wins!"
        else:
            winner_msg = "It's a draw!"

        send_data(conn1, winner_msg)
        send_data(conn2, winner_msg)

        conn1.close()
        conn2.close()

if __name__ == "__main__":
    main()
