import socket
from network_utils import send_data, receive_data

HOST = input("Enter server IP address (e.g., 127.0.0.1): ")
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        try:
            while True:
                server_message = receive_data(s)
                if server_message is None:
                    print("Connection closed by server.")
                    break

                print(f"\nSERVER: {server_message}")

                # Prompt for input if message ends with a colon or question
                if server_message.strip().endswith((':', '?')):
                    user_input = input("> ")
                    send_data(s, user_input)

        except KeyboardInterrupt:
            print("\nDisconnected from server.")

if __name__ == "__main__":
    main()
