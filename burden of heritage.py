from math import inf
from collections import deque


class Vertex:
    """Класс для представления вершин графа (например, остановки)"""
    __vertex_id = -1  # id вершины

    def __init__(self):
        self._links = []  # список связей с другими вершинами графа(Объекты класса Link)
        self._id = self.__get_uniq_id()

    @classmethod
    def __get_uniq_id(cls):  # метод для получения уникального id вершины
        cls.__vertex_id += 1
        return cls.__vertex_id

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, link):
        if isinstance(link, Link):
            self._links.append(link)

    @property
    def id(self):
        return self._id


class Link:
    """Класс для описания связи между двумя произвольными вершинами графа,
    например маршруты"""

    def __init__(self, v1: Vertex, v2: Vertex, dist=1):
        self._v1 = v1  # ссылки на объекты класса Vertex, которые соединяются этой связью
        self._v2 = v2
        self._dist = dist  # длина связи

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        if isinstance(value, int):
            self._dist = value


class LinkedGraph:
    """Класс для представления связного графа в целом (карта целиком)"""

    def __init__(self):
        self._links = []  # список из всех связей графа (Links)
        self._vertex = []  # список из всех вершин графа (Vertex)

    def _get_id_s(self) -> tuple:
        """Метод для получения id из вершин, которые добавлены в список с вершинами"""
        return tuple(map(lambda x: x.id, self._vertex))

    def _get_links(self) -> tuple:
        """Метод для получения связей между вершинами,
         которые добавлены в список со связями"""
        return tuple(map(lambda x: (x.v1.id, x.v2.id), self._links))

    def add_vertex(self, v: Vertex) -> None:
        """Метод для добавления новой вершины в список вершин,
        если этой вершины нет в списке"""
        if v.id not in self._get_id_s():
            self._vertex.append(v)

    def add_link(self, link: Link) -> None:
        """Метод для добавления новой связи в список связей,
        если этой связи нет в списке"""
        v1, v2 = getattr(link, 'v1'), getattr(link, 'v2')
        self.add_vertex(v1)
        self.add_vertex(v2)
        v1.links = v2.links = link  # добавление связи с другими вершинами для конкретной вершины

        vertex_ids = (v1.id, v2.id)  # id полученных связанных объектов
        cur_links = self._get_links()
        if vertex_ids not in cur_links and vertex_ids[::-1] not in cur_links:
            self._links.append(link)

    def find_path(self, start_v: Vertex, stop_v: Vertex) -> tuple:
        """Метод для поиска кратчайшего маршрута из start_v в stop_v"""
        vertex = self._vertex.index(start_v)  # вершина для начала маршрута

        queue_vertex = deque()  # создание очереди из вершин на проверку
        queue_vertex.append(self._vertex[vertex])  # добавление в очередь стартовой вершины для трекинга
        connections = {k: inf for k in self._vertex}  # словарь с расстояниями от v_start до v_stop
        connections[self._vertex[vertex]] = 0

        routes = {vertex: 0}  # словарь с key - id вершины(куда "пришли"); value - вершина с которой "пришли" в key

        while queue_vertex:  # пока есть необработанные вершины
            cur_v = queue_vertex.pop()
            for end_point in cur_v.links:
                v1, v2 = getattr(end_point, 'v1'), getattr(end_point, 'v2')
                related_v = v2 if cur_v.id != v2.id else v1  # определение связанной вершины с текущей вершиной
                if connections[cur_v] + end_point.dist < connections[related_v]:  # если расстояние уменьшилось
                    connections[related_v] = connections[cur_v] + end_point.dist  # обновляем в словаре расстояний
                    queue_vertex.append(related_v)  # и добавляем в очередь связанную вершину
                    routes[related_v.id] = cur_v.id  # необходимо для получения вершин между первой и последней

        # формирование списка id вершин между первой и последней включительно
        path_points = []
        for end_point in routes.keys():
            if end_point == stop_v.id:
                path_points.append(routes[end_point])
                while path_points[-1] != start_v.id:
                    path_points.append(routes[path_points[-1]])
                else:
                    path_points.insert(0, stop_v.id)

        path_points.reverse()  # так как создание пути идет с конца, необходимо развернуть список с вершинами
        vertex_in_path = {k: v for k in path_points for v in self._vertex if v.id == k}
        vertex_in_path_list = [v for v in vertex_in_path.values()]  # формирование списка с вершинами для возврата

        # формирование списка со связями между вершинами между первой и последней включительно
        links_in_path = []
        for i in range(len(vertex_in_path_list) - 1):
            for link in self._links:
                # проверка присутствия соседних вершин в данной связи link(вершина может быть как слева, так и справа)
                if (link.v1 is vertex_in_path_list[i] and link.v2 is vertex_in_path_list[i + 1]) or \
                        (link.v2 is vertex_in_path_list[i] and link.v1 is vertex_in_path_list[i + 1]):
                    links_in_path.append(link)

        return vertex_in_path_list, links_in_path


class Station(Vertex):
    """Класс для описания станций метро"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    """Класс для описания связей между станциями метро"""

    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2, dist)

    def __repr__(self):
        return f'{self.v1} - {self.v2} -> {self.dist}'
