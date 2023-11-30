import threading
import time
import copy
import random
import os
endGame = False


class Snake:

    def __init__(self, field, name, ind):
        self.direction = 0
        self.points = 0
        self.cords = []
        self.cords.append([field.sizeOfField // 2 + 1, field.sizeOfField // 2 + 1])
        self.name = name
        self.ind = ind
        self.timeFreeze = 0

    def rotate(self, newDirection):
        if abs(self.direction - newDirection) % 2 == 1:
            self.direction = newDirection

    def move(self, current_field, snakes):
        if self.timeFreeze > 0:
            self.timeFreeze -= 1
            return
        x, y = self.cords[-1]
        if self.direction == 0:
            x += 1
        if self.direction == 1:
            y -= 1
        if self.direction == 2:
            x -= 1
        if self.direction == 3:
            y += 1
        if [x, y] not in current_field.bonuses:
            self.cords.pop(0)
        else:
            current_field.field[x][y] = "."
            current_field.bonuses.remove([x, y])
            current_field.existBonus.remove([x, y])
            self.points += 1
        if [x, y] in current_field.freezes:
            current_field.field[x][y] = "."
            current_field.freezes.remove([x, y])
            current_field.existBonus.remove([x, y])
            for snake in snakes:
                if snake.ind != self.ind:
                    snake.timeFreeze += 3
        for portal_ind in range(0, len(current_field.portals)):
            if [x, y] in current_field.portals[portal_ind]:
                if current_field.portals[portal_ind][0] == [x, y]:
                    x, y = current_field.portals[portal_ind][1]
                else:
                    x, y = current_field.portals[portal_ind][0]
                toClearX1, toClearY1 = current_field.portals[portal_ind][0]
                toClearX2, toClearY2 = current_field.portals[portal_ind][1]
                current_field.field[toClearX1][toClearY1] = "."
                current_field.field[toClearX2][toClearY2] = "."
                current_field.existBonus.remove(current_field.portals[portal_ind][0])
                current_field.existBonus.remove(current_field.portals[portal_ind][1])
                current_field.portals.pop(portal_ind)
                break
        self.cords.append([x, y])

    def isStuck(self, current_field):
        x, y = self.cords[-1]
        if [x, y] in self.cords[:-1]:
            current_field.field[x][y] = "▦"
            return True
        if current_field.field[x][y] == '#':
            current_field.field[x][y] = "▦"
            return True
        return False


class Field:
    def __init__(self, n):
        self.field = []
        self.bonuses = []
        self.portals = []
        self.freezes = []
        self.existBonus = []
        self.sizeOfField = 0
        for i in range(0, n + 2):
            if i == 0 or i == n + 1:
                self.field.append(list(map(str, "#" * (n + 2))))
            else:
                self.field.append(list(map(str, "#" + "." * n + "#")))
        self.sizeOfField = n

    def createWalls(self, wallsCount):
        while wallsCount > 0:
            x, y = random.randint(1, self.sizeOfField + 1), random.randint(1, self.sizeOfField + 1)
            if self.field[x][y] == ".":
                self.field[x][y] = "#"
                wallsCount -= 1

    def fieldUpdate(self, snakes):
        if len(self.bonuses) == 0:
            self.createBonus(snakes)
        if len(self.portals) == 0:
            self.createPortal(snakes)
        if len(self.freezes) == 0:
            self.createFreeze(snakes)


    def drawField(self, snakes):
        drawingField = copy.deepcopy(self.field)
        for snake in snakes:
            for snakeCords in snake.cords:
                if self.field[snakeCords[0]][snakeCords[1]] != "▦":
                    if snakeCords == snake.cords[-1]:
                        drawingField[snakeCords[0]][snakeCords[1]] = "▣"
                    else:
                        drawingField[snakeCords[0]][snakeCords[1]] = "■"
        for line in drawingField:
            print(*line, sep="")
        for snake in snakes:
            print(f"{snake.name}'s points: {snake.points}")

    def createBonus(self, snakes):
        while True:
            x, y = random.randint(0, self.sizeOfField - 1), random.randint(0, self.sizeOfField - 1)
            if self.field[x][y] == '.':
                if [x, y] in self.existBonus:
                    continue
                isIsSnake = False
                for snake in snakes:
                    if [x, y] in snake.cords:
                        isIsSnake = True
                        break
                if not isIsSnake:
                    self.field[x][y] = "*"
                    self.existBonus.append([x, y])
                    self.bonuses.append([x, y])
                    return


    def createFreeze(self, snakes):
        while True:
            x, y = random.randint(0, self.sizeOfField - 1), random.randint(0, self.sizeOfField - 1)
            if self.field[x][y] == '.':
                if [x, y] in self.existBonus:
                    continue
                isIsSnake = False
                for snake in snakes:
                    if [x, y] in snake.cords:
                        isIsSnake = True
                        break
                if not isIsSnake:
                    self.field[x][y] = "F"
                    self.existBonus.append([x, y])
                    self.freezes.append([x, y])
                    return

    def createPortal(self, snakes):
        while True:
            x, y = random.randint(0, self.sizeOfField - 1), random.randint(0, self.sizeOfField - 1)
            x2, y2 = random.randint(0, self.sizeOfField - 1), random.randint(0, self.sizeOfField - 1)
            if self.field[x][y] == '.' and self.field[x2][y2] == '.' and [x, y] != [x2, y2]:
                if [x, y] in self.existBonus:
                    continue
                isIsSnake = False
                for snake in snakes:
                    if [x, y] in snake.cords or [x2, y2] in snake.cords:
                        isIsSnake = True
                        break
                if not isIsSnake:
                    self.field[x][y] = "P"
                    self.field[x2][y2] = "P"
                    self.existBonus.append([x, y])
                    self.existBonus.append([x2, y2])
                    self.portals.append([[x, y], [x2, y2]])
                    return


while True:
    print("Введите размер поля:")
    try:
        gameField = Field(int(input()))
        break
    except Exception:
        print("Невозможно создать поле данного размера")
allSnakes = []
player = Snake(gameField, "Player", 0)
AISnake = Snake(gameField, "AI", 1)
allSnakes.append(player)
allSnakes.append(AISnake)
while True:
    print("Введите скорость:")
    try:
        speed = float(input())
        if speed <= 0:
            print("Невозможно выбрать данную скорость")
            continue
        break
    except Exception:
        print("Невозможно выбрать данную скорость")
while True:
    print("Введите сложность (количество заблокированных клеток):")
    try:
        n = int(input())
        if n >= gameField.sizeOfField * gameField.sizeOfField:
            print("Неверные данные")
            continue
        gameField.createWalls(n)
        break
    except Exception:
        print("Неверные данные")


def thread_function1():
    global player, AISnake, gameField, endGame, speed
    while not endGame:
        os.system('cls')
        player.move(gameField, allSnakes)
        AISnake.move(gameField, allSnakes)
        gameField.fieldUpdate(allSnakes)
        gameField.drawField(allSnakes)
        if player.isStuck(gameField):
            os.system('cls')
            gameField.drawField(allSnakes)
            endGame = True
            exit(0)
        time.sleep(speed)
    exit(0)



def thread_function2():
    global player, AISnake, gameField, endGame, speed
    while not endGame:
        newDirection = str(input())
        if newDirection == "a":
            player.rotate(1)
        if newDirection == "w":
            player.rotate(2)
        if newDirection == "s":
            player.rotate(0)
        if newDirection == 'd':
            player.rotate(3)
        time.sleep(speed)
    exit(0)


def thread_function3():
    global player, AISnake, gameField, endGame, speed
    while not endGame:
        gameField.fieldUpdate([player, AISnake])
        bonusCords = gameField.bonuses[-1]
        if AISnake.cords[-1][0] < bonusCords[0]:
            if abs(AISnake.direction - 0) % 2 == 1 or AISnake.direction == 0:
                AISnake.rotate(0)
                time.sleep(speed)
                continue
        if AISnake.cords[-1][0] > bonusCords[0]:
            if abs(AISnake.direction - 2) % 2 == 1 or AISnake.direction == 2:
                AISnake.rotate(2)
                time.sleep(speed)
                continue
        if AISnake.cords[-1][1] < bonusCords[1]:
            if abs(AISnake.direction - 3) % 2 == 1 or AISnake.direction == 3:
                AISnake.rotate(3)
                time.sleep(speed)
                continue
        if AISnake.cords[-1][1] > bonusCords[1]:
            if abs(AISnake.direction - 1) % 2 == 1 or AISnake.direction == 1:
                AISnake.rotate(1)
                time.sleep(speed)
                continue
        time.sleep(speed)
    exit(0)


thread1 = threading.Thread(target=thread_function1)
thread2 = threading.Thread(target=thread_function2)
thread3 = threading.Thread(target=thread_function3)

# Starting the threads
thread1.start()
thread2.start()
thread3.start()

# Waiting for both threads to finish
thread1.join()
thread2.join()
thread3.join()

print("Main thread has finished execution")
