from tkinter import *
import random

snakeSpeed = 500
appleSpeed = 5000
snakeLength = 0
areaSize = 0
boardSize = 0
class App():
    def __init__(self):
        self.root = Tk()
        self.root.title('Snake')
        self.root.resizable(True, True)
        self.createCounter()
        self.w = Canvas(self.root, width=boardSize*areaSize+5, height=boardSize*areaSize+5, background="black")
        self.w.pack(padx=14, pady=14)
        self.board = Board(self.root, self.w)
        self.snake = Snake(self.root, self.w, self)
        self.root.mainloop()

    def createCounter(self):
        self.label = Label(self.root, text=f"Snake Length: {snakeLength}", width=70, height=2, font=("Arial", 20))
        self.label.pack()
        global boardSize, areaSize
        x = input("Enter board size: ")
        boardSize = int(x)
        areaSize = 700 // boardSize

    def updateCounter(self):
        global snakeLength
        self.label.config(text=f"Snake Length: {snakeLength}")

class Board():
    def __init__(self, root, w):
        self.root = root
        self.w = w
        self.createBoard()

    def createBoard(self):
        for i in range(boardSize):
            for j in range(boardSize):
                Area(self.root, i, j, self.w, "white", "black")

class Apple():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake():
    def __init__(self, root, w, app):
        self.apple = None
        self.x = None
        self.y = None
        self.root = root
        self.w = w
        self.app = app
        self.go = True
        self.list = list()
        self.direction = "right"
        self.createSnake()
        self.bindKeys()
        self.moveSnake()
        self.addApple()
        self.changeSpeeds()

    def changeSpeeds(self):
        self.root.after(20000, self.changeSpeeds)
        global appleSpeed, snakeSpeed
        appleSpeed = int(appleSpeed // 1.2)
        snakeSpeed = int(snakeSpeed // 1.2)

    def createApple(self, x, y):
        self.x = x
        self.y = y
        self.apple = self.w.create_oval(4 + x * areaSize, 4 + y * areaSize, 4 + (x + 1) * areaSize, 4 + (y + 1) * areaSize, fill="red", outline="red")

    def destroyApple(self):
        self.w.delete(self.apple)
        self.apple = None

    def bindKeys(self):
        self.root.bind("<Left>", self.update_direction)
        self.root.bind("<Right>", self.update_direction)
        self.root.bind("<Up>", self.update_direction)
        self.root.bind("<Down>", self.update_direction)

    def update_direction(self, event):
        new_direction = {
            "Left": "left",
            "Right": "right",
            "Up": "up",
            "Down": "down"
        }.get(event.keysym, self.direction)

        # Ensure the snake cannot reverse direction directly
        if (self.direction == "right" and new_direction != "left" or
                self.direction == "left" and new_direction != "right" or
                self.direction == "up" and new_direction != "down" or
                self.direction == "down" and new_direction != "up"):
            self.direction = new_direction

    def addApple(self):
        self.root.after(appleSpeed, self.addApple)
        if(self.apple == None):
            x = random.randint(0, boardSize-1)
            y = random.randint(0, boardSize - 1)
            add = True
            for i in list(range(0, snakeLength-1)):
                if(self.list[i].row == x and self.list[i].column == y):
                    add = False
            if(add):
                self.createApple(x, y)

    def moveSnake(self):
            self.root.after(snakeSpeed, self.moveSnake)
            if (self.go):
                self.createSnakeArea()
            if (self.go):
                if(self.apple != None):
                    if(self.x == self.list[0].row and self.y == self.list[0].column):
                        self.destroyApple()
                    else:
                        self.deleteSnakeArea()
                else:
                    self.deleteSnakeArea()
            self.app.updateCounter()

    def createSnake(self):
        x = random.randint(1, boardSize - 2)
        y = random.randint(1, boardSize - 2)
        global snakeLength
        snakeLength += 1
        z = Area(self.root, x, y, self.w, "green", "green")
        self.list.insert(0, z)

        direk = random.randint(0, 3)
        match direk:
            case 0:
                x+=1
            case 1:
                x-=1
            case 2:
                y+=1
            case 3:
                y-=1

        snakeLength += 1
        z = Area(self.root, x, y, self.w, "green", "green")
        self.list.insert(0, z)
        self.app.updateCounter()

    def createSnakeArea(self):
        match self.direction:
            case "right":
                x = self.list[0].row + 1
                y = self.list[0].column
            case "left":
                x = self.list[0].row - 1
                y = self.list[0].column
            case "up":
                x = self.list[0].row
                y = self.list[0].column - 1
            case "down":
                x = self.list[0].row
                y = self.list[0].column + 1

        global snakeLength
        snakeLength += 1
        if x < 0 or y < 0 or x >= boardSize or y >= boardSize:
            self.error()
        else:
            for element in self.list:
                if(element.row == x and element.column == y):
                    self.error()
                    return
            z = Area(self.root, x, y, self.w, "green", "green")
            self.list.insert(0, z)

        self.app.updateCounter()

    def error(self):
        print("error")
        exit()

    def deleteSnakeArea(self):
        global snakeLength
        snakeLength -= 1
        tail = self.list.pop()
        tail.delete()
        self.app.updateCounter()

class Area():
    def __init__(self, root, row, column, w, fill, outline):
        self.root = root
        self.row = row
        self.column = column
        self.w = w
        self.fill = fill
        self.outline = outline
        self.createArea()

    def delete(self):
        self.w.delete(self.rect)
    def createArea(self):
        self.rect = self.w.create_rectangle(4 + self.row * areaSize, 4 + self.column * areaSize, 4 + (self.row + 1) * areaSize, 4 + (self.column + 1) * areaSize, fill=self.fill, outline=self.outline)

myApp = App()