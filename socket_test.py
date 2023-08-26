import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)  # 클라이언트로부터 데이터 받기
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            response = f"You sent: {data.decode('utf-8')}"
            client_socket.send(response.encode('utf-8'))  # 클라이언트에게 데이터 보내기
        except:
            break

    client_socket.close()

def main():
    host = "0.0.0.0"  # 모든 인터페이스에서 들어오는 연결을 받음
    port = 12345     # 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()  # 클라이언트 연결 대기
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
