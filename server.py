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
        player1 = Player(name1, False, 0, {}, [])

        send_data(conn1, f"Hello, {name1}! Do you want to play against another player (type 1) or against a machine (type 2): ")
        type_player = receive_data(conn1)

        if(type_player=='1'):
            conn2, addr2 = s.accept()
            print(f"Player 2 connected from {addr2}")
            send_data(conn2, "Welcome Player 2! Please enter your name:")
            name2 = receive_data(conn2)
            player2 = Player(name2, False, 0, {}, [])

        else:
            send_data(conn1, "What difficulty machine do you want to play against: easy, medium, or hard (1, 2, or 3)?")
            difficulty = receive_data(conn1)
            player2 = Player("MACHINE", True, int(difficulty), {}, [])

        game = Game(player1, player2)
        game.reset()
        game.draw_card(player1, 7)
        game.draw_card(player2, 7)
        
        set1 = player1.check_set()
        if(set1 is None):
            pass
        else:
            send_data(conn1, f"Player {player1.name} had sets {set1}")
            if(type_player=='1'):
                send_data(conn2, f"Player {player1.name} had sets {set1}")

        set2 = player2.check_set()
        if(set2 is None):
            pass
        else:
            send_data(conn1, f"Player {player2.name} had sets {set2}")
            if(type_player=='1'):
                send_data(conn2, f"Player {player2.name} had sets {set2}")


        if(type_player=='1'):
            send_data(conn1, "Game starts!")
            send_data(conn2, "Game starts!")

            turn = 0

            while True:
                if turn == 0:

                    if(len(player1.player_deck) == 0):
                        game.draw_card(player1, 7)
                    if(len(player2.player_deck) == 0):
                        game.draw_card(player2, 7)


                    #if we could not draw cards bc the deck was empty:
                    if(len(player1.player_deck) == 0 or len(player2.player_deck) == 0):
                        send_data(conn1, "No cards left in deck to draw.")
                        send_data(conn2, "No cards left in deck to draw.")
                        break


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

                    if ask in player2.player_deck:
                        amount = player2.player_deck.pop(ask)
                        player1.player_deck[ask] = player1.player_deck.get(ask, 0) + amount
                        msg = f"{player2.name} had {amount} {ask}(s). {player1.name} gets another turn!"
                        send_data(conn1, msg)
                        send_data(conn2, msg)

                        set1 = player1.check_set()
                        if(set1 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player1.name} had sets {set1}")
                            send_data(conn2, f"Player {player1.name} had sets {set1}")
                        continue
                    else:
                        msg = f"{player2.name} says: Go Fish!"
                        send_data(conn1, msg)
                        send_data(conn2, msg)
                        if len(game.deck) > 0:
                            card = game.draw_card(player1, 1)
                            send_data(conn1, f"You drew a {card}!")
                        else:
                            send_data(conn1, "No cards left in deck to draw.")
                            send_data(conn2, "No cards left in deck to draw.")
                            break
                        set1 = player1.check_set()
                        if(set1 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player1.name} had sets {set1}")
                            send_data(conn2, f"Player {player1.name} had sets {set1}")
                        turn = 1

                else:

                    if(len(player1.player_deck) == 0):
                        game.draw_card(player1, 7)
                    if(len(player2.player_deck) == 0):
                        game.draw_card(player2, 7)

                    #if we could not draw cards bc the deck was empty:
                    if(len(player1.player_deck) == 0 or len(player2.player_deck) == 0):
                        send_data(conn1, "No cards left in deck to draw.")
                        send_data(conn2, "No cards left in deck to draw.")
                        break

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


                    if ask in player1.player_deck:
                        amount = player1.player_deck.pop(ask)
                        player2.player_deck[ask] = player2.player_deck.get(ask, 0) + amount
                        msg = f"{player1.name} had {amount} {ask}(s). {player2.name} gets another turn!"
                        send_data(conn1, msg)
                        send_data(conn2, msg)
                        set2 = player2.check_set()
                        if(set2 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player2.name} had sets {set2}")
                            send_data(conn2, f"Player {player2.name} had sets {set2}")
                        continue
                    else:
                        msg = f"{player1.name} says: Go Fish!"
                        send_data(conn1, msg)
                        send_data(conn2, msg)
                        if len(game.deck) > 0:
                            card = game.draw_card(player2, 1)
                            send_data(conn2, f"You drew a {card}!")
                        else:
                            send_data(conn1, "No cards left in deck to draw.")
                            send_data(conn2, "No cards left in deck to draw.")
                            break
                        player2.check_set()
                        if(set2 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player2.name} had sets {set2}")
                            send_data(conn2, f"Player {player2.name} had sets {set2}")
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

            winner = game.end_game()

            winner_msg = ""

            if(winner == 1):
                winner_msg = f"Player {player1.name} wins!!"
            elif(winner == 2):
                winner_msg = f"Player {player2.name} wins!!"
            else:
                winner_msg = "Draw!!"

            send_data(conn1, winner_msg)
            send_data(conn2, winner_msg)

            conn1.close()
            conn2.close()

        else: #machine is playing
            send_data(conn1, "Game starts!")

            turn = 0

            while True:
                if turn == 0:

                    if(len(player1.player_deck) == 0):
                        game.draw_card(player1, 7)
                    if(len(player2.player_deck) == 0):
                        game.draw_card(player2, 7)

                    #if we could not draw cards bc the deck was empty:
                    if(len(player1.player_deck) == 0 or len(player2.player_deck) == 0):
                        send_data(conn1, "No cards left in deck to draw.")
                        break


                    send_data(conn1, f"\n{player1.name}'s turn!")

                    send_data(conn1, f"Your hand: {player1.player_deck}")

                    send_data(conn1, "What card are you fishing for (e.g., 2-10, J, Q, K, A)?")
                    ask = receive_data(conn1)

                    if ask is None:
                        break

                    ask = ask.upper()


                    if ask not in Game.possible_cards:
                        send_data(conn1, "Invalid card name. Try again.")
                        continue

                    if(player2.level==2):
                        player2.player_asked.add(ask) #store for level 2 difficulty machine

                    elif(player2.level==3):
                        #store for level 3 difficulty
                        if ask in player2.ai_memory["opponent_requests"]:
                            player2.ai_memory["opponent_requests"][ask] += 1
                        else:
                            player2.ai_memory["opponent_requests"][ask] = 1

                    if ask in player2.player_deck:
                        amount = player2.player_deck.pop(ask)
                        player1.player_deck[ask] = player1.player_deck.get(ask, 0) + amount
                        msg = f"{player2.name} had {amount} {ask}(s). {player1.name} gets another turn!"
                        send_data(conn1, msg)

                        set1 = player1.check_set()
                        if(set1 is None):
                            pass
                        else:
                            send_data(conn1, f"You had sets {set1}")

                            if(player2.level==3): #record for level 3 machine
                                for card in set1:
                                    if card in player2.ai_memory["seen_cards"]:
                                        player2.ai_memory["seen_cards"][card] += 1
                                    else:
                                        player2.ai_memory["seen_cards"][card] = 1

                                    player2.ai_memory["sets_made"].add(card)
                                    if(card in player2.ai_memory["opponent_requests"]):
                                        player2.ai_memory["opponent_requests"].pop(card)
                        continue
                    else:
                        msg = f"{player2.name} says: Go Fish!"
                        send_data(conn1, msg)
                        if len(game.deck) > 0:
                            card = game.draw_card(player1, 1)
                            send_data(conn1, f"You drew a {card}!")
                        else:
                            send_data(conn1, "No cards left in deck to draw.")
                            break
                        set1 = player1.check_set()
                        if(set1 is None):
                            pass
                        else:
                            send_data(conn1, f"You had sets {set1}")

                            if(player2.level==3): #record for level 3 machine
                                for card in set1:
                                    if card in player2.ai_memory["seen_cards"]:
                                        player2.ai_memory["seen_cards"][card] += 1
                                    else:
                                        player2.ai_memory["seen_cards"][card] = 1

                                    player2.ai_memory["sets_made"].add(card)
                                    if(card in player2.ai_memory["opponent_requests"]):
                                        player2.ai_memory["opponent_requests"].pop(card)
                        turn = 1

                else:

                    if(len(player1.player_deck) == 0):
                        game.draw_card(player1, 7)
                    if(len(player2.player_deck) == 0):
                        game.draw_card(player2, 7)

                    #if we could not draw cards bc the deck was empty:
                    if(len(player1.player_deck) == 0 or len(player2.player_deck) == 0):
                        send_data(conn1, "No cards left in deck to draw.")
                        break
                

                    send_data(conn1, f"\n{player2.name}'s turn!")
                    send_data(conn1, "Waiting for other player's move...")

                    ask = player2.ask_card() ######################################################################

                    send_data(conn1, f"Player {player2.name} asked for {ask}!")

                    if ask in player1.player_deck:
                        amount = player1.player_deck.pop(ask)
                        player2.player_deck[ask] = player2.player_deck.get(ask, 0) + amount
                        msg = f"{player1.name} had {amount} {ask}(s). {player2.name} gets another turn!"
                        send_data(conn1, msg)

                        set2 = player2.check_set()
                        if(set2 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player2.name} had sets {set2}")
                        
                            if(player2.level==3): #record for level 3 machine
                                for card in set2:
                                    if card in player2.ai_memory["seen_cards"]:
                                        player2.ai_memory["seen_cards"][card] += 1
                                    else:
                                        player2.ai_memory["seen_cards"][card] = 1

                                    player2.ai_memory["sets_made"].add(card)
                                    if(card in player2.ai_memory["opponent_requests"]):
                                        player2.ai_memory["opponent_requests"].pop(card)


                        continue
                    else:
                        msg = f"{player1.name} says: Go Fish!"
                        send_data(conn1, msg)
                        if len(game.deck) > 0:
                            card = game.draw_card(player2, 1)
                        else:
                            send_data(conn1, "No cards left in deck to draw.")

                        set2 = player2.check_set()
                        if(set2 is None):
                            pass
                        else:
                            send_data(conn1, f"Player {player2.name} had sets {set2}")
                        
                            if(player2.level==3): #record for level 3 machine
                                for card in set2:
                                    if card in player2.ai_memory["seen_cards"]:
                                        player2.ai_memory["seen_cards"][card] += 1
                                    else:
                                        player2.ai_memory["seen_cards"][card] = 1

                                    player2.ai_memory["sets_made"].add(card)
                                    if(card in player2.ai_memory["opponent_requests"]):
                                        player2.ai_memory["opponent_requests"].pop(card)

                        turn = 0

                total_sets = len(player1.set) + len(player2.set)
                if total_sets == 13:
                    break

                if len(game.deck) == 0:
                    if len(player1.player_deck) == 0 or len(player2.player_deck) == 0:
                        break


            game_over_msg = f"\nGame Over!\n\n{player1.name}'s sets: {player1.set}\n{player2.name}'s sets: {player2.set}"
            send_data(conn1, game_over_msg)

            winner = game.end_game()

            winner_msg = ""

            if(winner == 1):
                winner_msg = f"\nPlayer {player1.name} wins!!"
            elif(winner == 2):
                winner_msg = f"\nPlayer {player2.name} wins!!"
            else:
                winner_msg = "\nDraw!!"

            send_data(conn1, winner_msg)

            conn1.close()


if __name__ == "__main__":
    main()
