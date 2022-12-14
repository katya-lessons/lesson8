import os
# импорт для подключения к сети
import socket
# импорт для одновременного выполнения задач
import threading

# данные для подключения
host = '127.0.0.1'
port = 5060

# Когда мы определяем наш сокет, нам нужно передать два параметра.
# Они определяют тип сокета, который мы хотим использовать.
# Первый AF_INET указывает, что мы используем интернет-сокет.
# Второй параметр обозначает протокол, который мы хотим использовать.
# SOCK_STREAM - TCP, а SOCK_DGRAM - UDP.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# После определения сокета мы привязываем его к нашему хосту и
# указанному порту, передавая кортеж, содержащий оба значения.
server.bind((host, port))

# Затем мы переводим наш сервер в режим прослушивания,
# чтобы он ждал подключения клиентов.
server.listen()

# Два пустых списка, которые мы будем использовать
# для хранения подключенных клиентов и их никнеймов
clients = []
nicknames = []


# Здесь мы определяем функцию, которая будет транслировать сообщения всем участникам чата.
# Он просто отправляет сообщение каждому клиенту, который подключен и, следовательно,
# находится в списке клиентов.
def broadcast(message):
    for client in clients:
        client.send(message)


# Эта функция будет отвечать за обработку сообщений от клиентов.
# Функция принимает клиента в качестве параметра. Каждый раз,
# когда клиент подключается к нашему серверу, мы запускаем
# для него эту функцию, и она запускает бесконечный цикл.
def handle(client):
    # Цикл не остановится, если только не возникнет
    # исключение из-за того, что что-то пошло не так.
    while True:
        try:
            # Сервер получает сообщение от клиента
            # (если он его отправляет) и рассылает его
            # всем подключенным клиентам. Поэтому, когда
            # один клиент отправляет сообщение,
            # все остальные могут видеть это сообщение.
            message = client.recv(1024)
            broadcast(message)
        except:
            # Если возникает ошибка с подключением к этому
            # клиенту, мы:
            # - удаляем его и его никнейм
            # - закрываем подключение
            # - транслируем, что этот клиент вышел из чата.
            # - разрываем цикл
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Когда мы будем готовы запустить наш сервер,
# мы выполним функцию receive()
def receive():
    # Она также запускает бесконечный цикл while,
    # который постоянно принимает новые подключения от клиентов.
    while True:
        # Принимаем подключение
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Как только клиент подключается,
        # он отправляет ему строку «NICK», которая
        # сообщает клиенту, что запрашивается его псевдоним.
        client.send('NICK'.encode('ascii'))

        # Обратите внимание, что здесь мы всегда кодируем и
        # декодируем сообщения. Причина этого в том, что мы
        # можем отправлять только байты, а не строки. Поэтому
        # нам всегда нужно кодировать сообщения (например, с
        # помощью ASCII), когда мы их отправляем, и
        # декодировать их, когда мы их получаем.

        # После этого он ожидает ответа
        nickname = client.recv(1024).decode('ascii')
        # и добавляет клиента с соответствующим псевдонимом в списки.
        nicknames.append(nickname)
        clients.append(client)

        # После этого мы распечатываем и транслируем эту информацию
        print("Nickname is {}".format(nickname))
        broadcast("{} joined! ".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Наконец, мы запускаем новый поток,
        # который запускает ранее реализованную
        # функцию обработки для этого конкретного клиента.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# очищаем консоль для красоты
os.system('clear')

# Теперь мы можем просто запустить эту функцию.
receive()
