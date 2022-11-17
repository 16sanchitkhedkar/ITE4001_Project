import socket
import threading
import nacl.secret
import nacl.utils
import base64

host = 'localhost'
port = 5858

key = b'\xe3\x9a\xd2ls\x10\x8b\xfc\xa6\xd93\xf6*\xd0\x06\x9e\x13U\xdbJ\xf09\xf8\x93\xd5\xaa\x870s\xce\x11N'

def encryptmessage(message, key):
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted)

def decryptmessage(message, key):
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(base64.b64decode(message))
    return decrypted

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    while True:
        try:
            message = decryptmessage(client.recv(1024), key).decode('utf-8')
            if message == 'CLIENT_NICKNAME':
                client.send(encryptmessage(nickname, key))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(encryptmessage(message, key))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
