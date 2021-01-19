# класс точки на игровом поле с декартовыми координатами
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, _dot):
        return self.x == _dot.x and self.y ==_dot.y 


# exception
class PlayBoardException(Exception):
    pass""

class PlayBoardOutException(PlayBoardException):
    def __str__(self):
        return "Попытка выхода за игровое поле."

class PlayBoardBuzyException(PlayBoardException):
    def __str__(self):
        return "Попытка хода в отстреляную точку"

class PlayBoardOccupiedException(PlayBoardException):
    pass

# класс корабля
class Ship:
    def __init__(self, xy, l, horiz):   # xy  - координаты точки на игровом поле; 
        self.xy = xy                    # l - размерность корабля, horiz - горизонтальность (True, False)
        self.l = l
        self.horiz = horiz

    @property                          #возвращает точки, принадлежащие кораблю
    def ship_dots(self):
        list = []
        for i in range(self.l):
            _x = self.xy.x
            _y = self.xy.y
            if self.horiz:
                _x += i
            else:
                _y += i
            list.append(Dot(_x, _y))
        return list

    def shuted(self, shut):             # проверка: попал выстрел в корабль?
        return shut in self.ship_dots


class Playboard:

    def __init__(self, size = 6, visible = True): # size - размерность игрового поля, visible - видимость кораблей
        self.size = size
        self.visible = visible

        self.matrix = [["O"]*size for _ in range(size)]

        self.ships = []
        self.buzy = []

    def add_ship(self, ship):
        for d in ship.ship_dots:
            if not (0 <= d.x < self.size) and (0 <= d.y < self.size) or d in self.buzy:
                raise PlayBoardOccupiedException()

        for p in ship.ship_dots:
            self.matrix[p.y][p.x] = "■"

    def ship_env(self, ship):
        env = [(1, 1), (1, 0), (1, -1),
               (0, -1), (-1, -1), (-1, 0),
               (-1, 1), (0, 1)] # точки вокруг корабля
        
        for d in ship.ship_dots:
            for ex, ey in env:
                cur = Dot(d.x + ex, d.y + ey)
                if (0 <= cur.x < self.size) and (0 <= cur.y < self.size) and cur not in self.buzy:
                    self.matrix[cur.y][cur.x] = "."
                    self.buzy.append(cur)


    def __str__(self):
        source = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, s in enumerate(self.matrix):
            source += f"\n {i+1} | " + " | ".join(s) + " |"
        if not self.visible:
            source = source.replace("■","O")
        return source




d1 = Dot(2, 2)
s1 = Ship(d1, 3, True)
print(s1.ship_dots)
print(s1.shuted(Dot(1,2)))
pb = Playboard(visible = True)
pb.add_ship(s1)
pb.ship_env(s1)
print(pb)
print()
s2 = Ship(Dot(2, 4),2, True)
pb.add_ship(s2)
pb.ship_env(s2)
print(pb)