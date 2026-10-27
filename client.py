
import socket

HOST = "127.0.0.1"
PORT = 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(3.0)
        client.connect((HOST, PORT))

        message = "Hello from automation"
        client.sendall(message.encode("utf-8"))

        response = client.recv(1024).decode("utf-8")
        print(f"Server response: {response}")


if __name__ == "__main__":
    main()
