import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection closed.")
            break

def main():
    host = '127.0.0.1'  # 첫 번째 클라이언트의 IP 주소
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((host, port))
    client_socket.listen(1)

    print(f"[*] Listening on {host}:{port}")

    other_client, addr = client_socket.accept()
    print(f"[*] Connected to: {addr[0]}:{addr[1]}")

    receive_thread = threading.Thread(target=receive_messages, args=(other_client,))
    receive_thread.start()

    while True:
        message = input()
        other_client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
