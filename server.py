import socket

HOST = "127.0.0.1"
PORT = 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            connection, address = server.accept()

            with connection:
                print(f"Connected by {address}")

                data = connection.recv(1024)

                if not data:
                    continue

                message = data.decode("utf-8")
                print(f"Received: {message}")

                response = f"ACK: {message}"
                connection.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    main()
