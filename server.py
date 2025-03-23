import socket
import re
from datetime import datetime
import os

users = {}

def validate_login_password(login, password):
    if not re.match(r'^[a-zA-Z0-9]{6,}$', login):
        return False
    if not (len(password) >= 8 and re.search(r'\d', password)):
        return False
    return True

def handle_http_request(request):
    headers = request.split('\n')
    method, path, _ = headers[0].split()

    if path == '/':
        response = "HTTP/1.1 200 OK\n\n<h1>Главная страница</h1>"
    elif re.match(r'^/test/\d+/$', path):
        test_number = re.search(r'\d+', path).group()
        response = f"HTTP/1.1 200 OK\n\n<h1>Тест с номером {test_number} запущен</h1>"
    elif re.match(r'^/message/[^/]+/[^/]+/$', path):
        login, text = re.findall(r'/([^/]+)', path)[1:3]
        message = f"{datetime.now()} - сообщение от пользователя {login} - {text}"
        print(message)
        response = f"HTTP/1.1 200 OK\n\n<h1>{message}</h1>"
    elif os.path.isfile('.' + path):
        with open('.' + path, 'r') as file:
            response = f"HTTP/1.1 200 OK\n\n{file.read()}"
    else:
        response = f"HTTP/1.1 404 Not Found\n\n<h1>Пришли неизвестные данные по HTTP - путь {path}</h1>"

    return response

def handle_non_http_request(data):
    if data.startswith("command:reg;"):
        login_match = re.search(r'login:([^;]+)', data)
        password_match = re.search(r'password:([^;]+)', data)
        if login_match and password_match:
            login = login_match.group(1)
            password = password_match.group(1)
            if validate_login_password(login, password):
                users[login] = password
                response = f"{datetime.now()} - пользователь {login} зарегистрирован"
            else:
                response = f"{datetime.now()} - ошибка регистрации {login} - неверный пароль/логин"
        else:
            response = f"{datetime.now()} - ошибка регистрации - неверный формат данных"
    elif data.startswith("command:signin;"):
        login_match = re.search(r'login:([^;]+)', data)
        password_match = re.search(r'password:([^;]+)', data)
        if login_match and password_match:
            login = login_match.group(1)
            password = password_match.group(1)
            if login in users and users[login] == password:
                response = f"{datetime.now()} - пользователь {login} произведен вход"
            else:
                response = f"{datetime.now()} - ошибка входа {login} - неверный пароль/логин"
        else:
            response = f"{datetime.now()} - ошибка входа - неверный формат данных"
    else:
        response = f"пришли неизвестные данные - {data}"

    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)

print("Сервер запущен и ожидает подключений...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключение от {addr}")

    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        continue

    if data.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS')):
        response = handle_http_request(data)
    else:
        response = handle_non_http_request(data)

    client_socket.send(response.encode('utf-8'))
    client_socket.close()


