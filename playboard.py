from random import randint

# класс точки на игровом поле с декартовыми координатами
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, _dot):
        return self.x == _dot.x and self.y ==_dot.y 

    
# exceptions
class PlayBoardException(Exception):
    pass

class PlayBoardOutException(PlayBoardException):
    pass

class PlayBoardBuzyException(PlayBoardException):
    pass

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

    def __init__(self, size = 6, visible = True):
        self.size = size
        self.visible = visible
        
        self.matrix = [["O"]*size for _ in range(size)]

        self.ships = []
        self.buzy = []

    def add_ship(self, ship):
        for d in ship.ship_dots:
            if not (0 <= d.x < self.size) or not (0 <= d.y < self.size) or d in self.buzy:
                raise PlayBoardBuzyException()
                   

        for p in ship.ship_dots:
            self.matrix[p.y][p.x] = "■"
            self.buzy.append(Dot(p.x, p.y))
        self.ship_env(ship)
        

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
        source = "   | 0 | 1 | 2 | 3 | 4 | 5 |"
        for i, s in enumerate(self.matrix):
            source += f"\n {i} | " + " | ".join(s) + " |"
        if not self.visible:
            source = source.replace("■","O")
        return source


def place_ships(size = 6):
    ships_lenght = [3, 2, 2, 1, 1, 1, 1]
    board = Playboard()
    attempt = 0 # количнство попыток расставить корабли
    for s in ships_lenght:
        while True:
            ship = Ship(Dot(randint(0, size), randint(0, size)), s, randint(0, 1))
            attempt +=1
            if attempt > 2000:
                return False
            try:
                board.add_ship(ship)
                break
            except PlayBoardBuzyException:
                pass
    return board


