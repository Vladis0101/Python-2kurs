#import socket

#HOST = '127.0.0.1'
#PORT = 8883

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((HOST, PORT))

#def send_command_to_server(command):
    #try:
    #    sock.send(command.encode('utf-8'))
   #     response = sock.recv(1024).decode('utf-8')
  #      print(f"Ответ от сервера: {response}")

 #   except Exception as e:
#        print(f"Ошибка при отправке команды: {e}")

#def register_user(login, password):
   # command = f"command:reg; login:{login};password:{password}"
  #  print(f"Регистрация пользователя {login}...")
 #   send_command_to_server(command)

#def sign_in_user(login, password):
   # command = f"command:signin; login:{login};password:{password}"
  #  print(f"Попытка входа пользователя {login}...")
 #   send_command_to_server(command)

#def main():
   # register_user("user1", "password123")
  #  register_user("user2", "password456")
 #   register_user("user3", "password789")
#
   # sign_in_user("user1", "password123")
  #  sign_in_user("user2", "password456")
 #   sign_in_user("user3", "password789")

#if __name__ == "__main__":
#    main()
#    sock.close()

import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

def send_data_to_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.send(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ от сервера: {response}")

def register_users():
    users = [
        {"login": "user1", "password": "password1"},
        {"login": "user2", "password": "password2"},
        {"login": "user3", "password": "password3"}
    ]

    for user in users:
        data = f"command:reg; login:{user['login']}; password:{user['password']}"
        send_data_to_server(data)

def login_users():
    users = [
        {"login": "user1", "password": "password1"},
        {"login": "user2", "password": "password2"},
        {"login": "user3", "password": "password3"}
    ]

    for user in users:
        data = f"command:signin; login:{user['login']}; password:{user['password']}"
        send_data_to_server(data)

if __name__ == "__main__":
    print("Регистрация пользователей...")
    register_users()

    print("\nВход пользователей...")
    login_users()













