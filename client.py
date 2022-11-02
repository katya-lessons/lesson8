# необходимые импорта
import os
import socket
import threading

# вводим никнейм
nickname = input("Choose your nickname: ")

# подключаемся к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5060))

# Здесь мы используем другую функцию - не bind(), а connect()
# Вместо привязки данных и прослушивания мы подключаемся к существующему серверу.

# Теперь клиенту необходимо иметь два потока, работающих одновременно. Первый будет постоянно
# получать данные с сервера, а второй будет отправлять на сервер собственные сообщения.
# Значит понадобятся две функции - receive() и write()


# Функция, прослушивающая сервер и отправляющая сообщения
def receive():
    # Цикл постоянно пытается получать сообщения и печатать их на экране.
    while True:
        try:
            # если сообщение «NICK», оно не печатается, а отправляет свой псевдоним на сервер.
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # В случае какой-либо ошибки мы закрываем соединение и разрываем цикл
            print("Error!")
            client.close()
            break


# Функция отправления сообщений на сервер
def write():
    # цикл, который всегда ожидает ввода от пользователя
    while True:
        # Как только он их получает, он объединяет их с никнеймом и отправляет на сервер.
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# очищаем консоль
os.system('clear')
# нужно запустить два потока, которые запускают эти две функции.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

