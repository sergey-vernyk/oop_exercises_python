class Server:
    """
    Класс для работы серверов в сети
    """
    servers_list = []  # список всех серверов

    def __init__(self):
        self.buffer = []  # список принятых пакетов (объектов класса Data)
        self.linked_routers = []  # список роутеров, к которым подключены сервер
        self.ip = Router.generate_uniq_ip()  # уникальный IP адрес текущего сервера
        self.servers_list.append(self)  # добавление сервера в список серверов

    def send_data(self, data) -> None:
        """
        Функция отправки информационного пакета data роутеру,
        к которому подключен текущий сервер
        Пакет сохраняется в буфере соответствующего роутера
        """
        for r in Router.routers_list:  # поиск связанного роутера с нужным сервером по IP
            for s in r.linked_servers:
                if self.ip == s:
                    r.buffer.append(data)  # отправка данных на правильный роутер

    def get_data(self) -> list:
        """
        Функция возврата списка принятых пакетов
        """
        input_data = self.buffer.copy()
        self.buffer.clear()  # очистка входящего буфера сервера
        return input_data

    def get_ip(self):
        """
        Функция для возвращения собственного IP-адреса
        """
        return self.ip


class Router:
    """
    Класс для работы роутеров в сети
    """

    ip_addresses = []  # ip адреса всех устройств в сети
    routers_list = []  # список всех роутеров

    def __init__(self):
        self.ip = self.generate_uniq_ip()  # свой IP адрес
        self.buffer = []  # список для хранения принятых от сервера пакетов (объектов класса Data)
        self.linked_servers = []  # список IP адресов серверов, к которым роутер подключен в данный момент
        self.routers_list.append(self)  # добавление роутера в список роутеров

    def link(self, server) -> None:
        """
        Функция подключения устройства к роутеру
        """
        self.linked_servers.append(server.ip)  # добавление IP адреса в список подключенных
        server.linked_routers.append(self.ip)  # добавление IP адреса роутера в список сервера с подключенными роутерами

    def unlink(self, server) -> None:
        """
        Функция отключение устройства от роутера
        """
        self.linked_servers.remove(server.ip)  # удаление IP адреса из списка подключенных
        server.linked_routers.remove(self.ip)  # удаление IP адреса роутера из списка сервера с подключенными роутерами

    def send_data(self) -> None:
        for data in self.buffer:  # поиск в данных IP адреса назначения в подключенных к роутеру серверах
            for serv_ip in self.linked_servers:
                if data.ip == serv_ip:  # если адрес назначения найден в подключенных серверах
                    for serv in Server.servers_list:  # поиск самого сервера из списка всех серверов
                        if serv.ip == serv_ip:  # если в пакете совпал IP адрес, то отправка пакета на нужный сервер
                            serv.buffer.append(data)
        self.buffer.clear()  # очистка исходящего буфера данных

    @classmethod
    def generate_uniq_ip(cls) -> str:
        """
        Функция для создания уникального IP адреса
        (каждый следующий больше предыдущего на 1)
        """
        if cls.ip_addresses:  # если есть подключенные устройства
            last_ip = cls.ip_addresses[-1].split('.')  # взятие последнего адреса
            last_octet = int(last_ip[-1])
            last_octet += 1  # изменение значения последнего октета адреса
            last_ip[-1] = str(last_octet)  # и его сохранения
            cls.ip_addresses.append('.'.join(last_ip))
        else:
            cls.ip_addresses.append('192.168.1.0')  # адрес первого подключенного устройства
        return cls.ip_addresses[-1]  # возврат последнего добавленного адреса как текущего


class Data:
    """
    Класс для описания пакета информации
    """

    def __init__(self, data, ip):
        self.data = data  # передаваемые данные
        self.ip = ip  # адрес назначения
