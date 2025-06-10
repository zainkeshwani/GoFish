def send_data(conn, message: str):
    if not message.endswith("\n"):
        message += "\n"
    conn.sendall(message.encode())

def receive_data(conn):
    buffer = ""
    #while True:
    part = conn.recv(1024).decode()
    if not part:
        return None
    buffer += part
    if '\n' in buffer:
        buffer = buffer.split("\n")
        line = ""
        for s in buffer:
            if s:
                line += s
                line += "\n"
        return line.strip()
