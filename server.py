import socket
import threading
import nacl.secret
import nacl.utils
import base64

host = 'localhost'
port = 5858

key = b'\xe3\x9a\xd2ls\x10\x8b\xfc\xa6\xd93\xf6*\xd0\x06\x9e\x13U\xdbJ\xf09\xf8\x93\xd5\xaa\x870s\xce\x11N'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def encryptmessage(message, key):
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted)

def decryptmessage(message, key):
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(base64.b64decode(message))
    return decrypted

def broadcast(message, key):
    for client in clients:
        client.send(encryptmessage(message, key))

def handle(client):
    while True:
        try:
            message = decryptmessage(client.recv(1024), key).decode('utf-8')
            print(message)
            broadcast(message, key)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!', key)
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send(encryptmessage('CLIENT_NICKNAME', key))
        nickname = decryptmessage(client.recv(1024), key).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!", key)
        client.send(encryptmessage('Connected to the server!', key))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
