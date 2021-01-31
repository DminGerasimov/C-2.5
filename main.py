from random import randint
from menu import Menu, ClearScreen

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
    pass

class PlayBoardOutException(PlayBoardException):
    pass

class PlayBoardBuzyException(PlayBoardException):
    pass

class PlayBoardOccupiedException(PlayBoardException): #исключение невозможности установки корабля в данной точке
    pass
class NotImplementedYet(PlayBoardException):
    pass
    
    
# класс корабля
class Ship:
    def __init__(self, xy, l, horiz):   # xy  - координаты точки на игровом поле; 
        self.xy = xy                    # l - размерность корабля, horiz - горизонтальность (True, False)
        self.l = l
        self.horiz = horiz
        self.lives = l

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
    

class Playboard:

    def __init__(self, visible, size = 6):
        self.size = size
        self.visible = visible
        self.counter = 0 #Счетчик подбитых кораблей
        self.matrix = [["O"]*size for _ in range(size)]

        self.ships = []
        self.buzy = []

        
    def dot_out(self, d):
        return not (0 <= d.x < self.size) or not (0 <= d.y < self.size)
    
    def add_ship(self, ship, visible):
        for d in ship.ship_dots:
            if self.dot_out(d) or d in self.buzy:
                raise PlayBoardOccupiedException()
                   

        for p in ship.ship_dots:
            if visible:
                self.matrix[p.y][p.x] = "■"
            self.buzy.append(Dot(p.x, p.y))
        self.ship_env(ship, False)
        self.ships.append(ship)
        

    def ship_env(self, ship, visible):
        env = [(1, 1), (1, 0), (1, -1),
               (0, -1), (-1, -1), (-1, 0),
               (-1, 1), (0, 1)] # точки вокруг корабля
        
        for d in ship.ship_dots:
            for ex, ey in env:
                cur = Dot(d.x + ex, d.y + ey)
                if not self.dot_out(cur) and cur not in self.buzy:
                    if visible:
                        self.matrix[cur.y][cur.x] = "."
                    self.buzy.append(cur)
                    
    def shut(self, d):             # проверка: попал выстрел в корабль?
        
        if self.dot_out(d):
            raise PlayBoardOutException()
                
        for ship in self.ships:
            
            for shd in ship.ship_dots:
                if d in self.buzy:
                    raise PlayBoardBuzyException()
                 
                self.matrix[d.y][d.x] = "T"
                if d == shd and ship.lives:
                    self.matrix[d.y][d.x] = "X"
                    self.buzy.append(d)  
                    ship.lives -= 1
                    if ship.lives <= 0:
                        self.counter += 1
                        print("Корабль потоплен!")
                        self.ship_env(ship, visible = True)
                        return True
                    print("Корабль ранен...")
                    return True
        self.buzy.append(d)                        
        print("Мимо!")            
        return False

                    
                        
    def __str__(self):
        source = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, s in enumerate(self.matrix):
            source += f"\n {i+1} | " + " | ".join(s) + " |"
        if not self.visible:
            source = source.replace("■","O")
        return source

class Player:
    
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
        
    def ask(self):
        raise NotImplementedYet()
        
    def move(self):
            while True:
                try:
                    ask_dot = self.ask()
                    shot_dot = self.enemy.shut(ask_dot)
                    return shot_dot
                except PlayBoardBuzyException:
                    print("В эту точку уже стреляли! Повторите ввод координат выстрела!")

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f"Ход компьютера :{d.x+1}, {d.y+1}")
        return d
           
class Me(Player):
    
    def ask_step(self, v_h_str):                     # ввод игроком позиции на игровом поле
        number = None
        while number is None:
            num_str =  input(f"  Игрок, ведите номер {v_h_str} от 1 до 6: ")
            if num_str.isdigit():
                number = int(num_str)
                if 1 <= number <= 6:                # проверка диапазона введенного числа
                    return number - 1
                print(" Вы ввели некорректное число!")
                number = None
                continue
            else:
                print(" Вы ввели некорректное число!")
                continue
            
    def ask(self):
        while True:
            x = self.ask_step("позиции по горизонтали")
            y = self.ask_step("позиции по вертикали")
            
            return Dot(x, y)

class Game:
    def __init__(self, size = 6):
        self.size = size
        player_board = self.place_board(True)
        computer_board = self.place_board(False)
        
        self.ai = AI(computer_board, player_board)
        self.me = Me(player_board, computer_board)
    
    def place_board(self, visible):
        board = False
        while not board:
            board = self.place_ships(visible)
        return board
    
    def place_ships(self, visible):
        ships_lenght = [3, 2, 2, 1, 1, 1, 1]
        board = Playboard(visible)
        attempt = 0 # количнство попыток расставить корабли
        for s in ships_lenght:
            while True:
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), s, randint(0, 1))
                attempt +=1
                if attempt > 2000:
                    return False
                try:
                    board.add_ship(ship, visible)
                    break
                except PlayBoardOccupiedException:
                    pass
        board.buzy =[]
        return board
    
    def menuloop(self):         # цикл обработки меню
        while True:
            mode = menu()
            clear()
            if mode == "1":     # описание
                description()
                clear()
            elif mode == "2":   # правила игры
                rules()
                clear()
            elif mode == "3":   # играть
                playgame()
                clear()
            elif mode == "4":   # выход из программы
                break
            else:
                wrong()

   
    def main_loop(self):
        step = 0
        
        while True:
            # cls.cls()
            print("_"*28)
            print("Игровая доска пользователя")
            print(self.me.board)
            print("_"*28)
            print("Игровая доска комьютера")
            print(self.ai.board)
            if step % 2 == 0:
                # print("-"*28)
                print("\nХодит Пользователь\n")
                shut = self.me.move()
                if shut:
                    step -= 1
            else:
                # print("-"*28)
                print("\nХодит компьютер\n")
                shut = self.ai.move()
                if shut:
                    step -= 1
            if self.ai.board.counter == 7:
                print("!"*36)
                print("Пользователь победитель!")
                input("Для продолжения введите Enter")
                break
            if self.me.board.counter == 7:
                print("!"*36)
                print("Компьютер победитель!")
                input("Для продолжения введите Enter")
                break
#             print(f"Подбитых кораблей компьютера: {self.ai.board.counter}")
#             print(f"Подбитых кораблей игрока: {self.me.board.counter}")
            step += 1

m = Menu()              #Экземпляр класса меню
# cls = ClearScreen()
while True:             #Основной цикл программы
    if m.menuloop():
        g = Game()
        g.main_loop()
    else:
        break