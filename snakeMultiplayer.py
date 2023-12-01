import threading
import time
import copy
import random
import os
import smartAI
endGame = False


class Snake:

    def __init__(self, current_field, name, ind, speed, enableStuck):
        self.direction = 0
        self.points = 0
        self.cords = []
        self.cords.append([current_field.sizeOfField // 2 + 1, current_field.sizeOfField // 2 + 1])
        self.name = name
        self.ind = ind
        self.timeFreeze = 0
        self.count_of_bricks = 0
        self.speed = speed
        self.lives = 3
        self.enableStuck = enableStuck
        self.immortalTime = 5


    def isInField(self, current_field, snakes):
        x, y = self.cords[-1]
        if x >= 0 and x < current_field.sizeOfField + 1 and y >= 0 and y < current_field.sizeOfField + 1:
            return True
        return False
    def isStuck(self, current_field, snakes):
        x, y = self.cords[-1]
        if self.enableStuck:
            for snake in snakes:
                if [x, y] in snake.cords and snake.ind != self.ind:
                    if self.immortalTime == 0:
                        current_field.field[x][y] = "▦"
                        self.lives -= 1
                        if self.lives == 0:
                            current_field.drawField(snakes)
                            exit(0)
                    if self.immortalTime == 0 or not self.isInField(current_field, snakes):
                        self.immortalTime += 5
                        self.cords = [[current_field.sizeOfField // 2 + 1, current_field.sizeOfField // 2 + 1]]
                    return True
        if [x, y] in self.cords[:-1]:
            if self.immortalTime == 0:
                current_field.field[x][y] = "▦"
                self.lives -= 1
                if self.lives == 0:
                    current_field.drawField(snakes)
                    exit(0)
            if self.immortalTime == 0 or not self.isInField(current_field, snakes):
                self.immortalTime += 5
                self.cords = [[current_field.sizeOfField // 2 + 1, current_field.sizeOfField // 2 + 1]]
            return True
        if current_field.field[x][y] == '#':
            if self.immortalTime == 0:
                current_field.field[x][y] = "▦"
                self.lives -= 1
                if self.lives == 0:
                    current_field.drawField(snakes)
                    exit(0)
            if self.immortalTime == 0 or not self.isInField(current_field, snakes):
                self.immortalTime += 5
                self.cords = [[current_field.sizeOfField // 2 + 1, current_field.sizeOfField // 2 + 1]]
            return True
        return False

    def rotate(self, newDirection, snakes):
        if abs(self.direction - newDirection) % 2 == 1:
            self.direction = newDirection

    def move(self, current_field, snakes):
        if self.immortalTime > 0:
            self.immortalTime -= 1
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
            if self.count_of_bricks > 0:
                self.count_of_bricks -= 1
                current_field.field[self.cords[0][0]][self.cords[0][1]] = "#"
            self.cords.pop(0)
        else:
            current_field.field[x][y] = "."
            current_field.bonuses.remove([x, y])
            current_field.existBonus.remove([x, y])
            self.points += 1
        if [x, y] in current_field.extraLives:
            self.lives += 1
            current_field.field[x][y] = "."
            current_field.extraLives.remove([x, y])
            current_field.existBonus.remove([x, y])
        if [x, y] in current_field.bricks:
            self.count_of_bricks += 5
            current_field.field[x][y] = "."
            current_field.bricks.remove([x, y])
            current_field.existBonus.remove([x, y])
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
        self.isStuck(current_field, snakes)


class Field:
    def __init__(self, n, speed):
        self.field = []
        self.bonuses = []
        self.portals = []
        self.freezes = []
        self.bricks = []
        self.extraLives = []
        self.existBonus = []
        self.sizeOfField = 0
        self.speed = speed
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
        if len(self.bricks) == 0:
            self.createBricks(snakes)
        if len(self.extraLives) == 0:
            self.createExtraLives(snakes)


    def drawField(self, snakes):
        self.fieldUpdate(snakes)
        drawingField = copy.deepcopy(self.field)
        for snake in snakes:
            for snakeCords in snake.cords:
                if self.field[snakeCords[0]][snakeCords[1]] != "▦":
                    if snakeCords == snake.cords[-1]:
                        drawingField[snakeCords[0]][snakeCords[1]] = "▣"
                    else:
                        drawingField[snakeCords[0]][snakeCords[1]] = "■"
        for x in range(0, self.sizeOfField + 2):
            for y in range(0, self.sizeOfField + 2):
                if self.field[x][y] == "▦":
                    self.field[x][y] = "#"
        for line in drawingField:
            print(*line, sep="")
        for snake in snakes:
            print(f"{snake.name}'s points: {snake.points} | {snake.name}'s lives: {snake.lives}")


    def getFieldWithAll(self, snakes):
        self.fieldUpdate(snakes)
        drawingField = copy.deepcopy(self.field)
        for snake in snakes:
            for snakeCords in snake.cords:
                if self.field[snakeCords[0]][snakeCords[1]] != "▦":
                    if snakeCords == snake.cords[-1]:
                        drawingField[snakeCords[0]][snakeCords[1]] = "▣"
                    else:
                        drawingField[snakeCords[0]][snakeCords[1]] = "■"
        for x in range(0, self.sizeOfField + 2):
            for y in range(0, self.sizeOfField + 2):
                if self.field[x][y] == "▦":
                    self.field[x][y] = "#"
        return drawingField

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


    def createExtraLives(self, snakes):
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
                    self.field[x][y] = "H"
                    self.existBonus.append([x, y])
                    self.extraLives.append([x, y])
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


    def createBricks(self, snakes):
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
                    self.field[x][y] = "B"
                    self.existBonus.append([x, y])
                    self.bricks.append([x, y])
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
        n = int(input())
        break
    except Exception:
        print("Невозможно создать поле данного размера")
while True:
    print("Введите скорость:")
    try:
        startSpeed = float(input())
        if startSpeed <= 0:
            print("Невозможно выбрать данную скорость")
            continue
        break
    except Exception:
        print("Невозможно выбрать данную скорость")
while True:
    print("Включить возможность змей сталкиваться? (0 - нет, 1 - да):")
    try:
        enableStucking = int(input())
        if enableStucking > 1 or enableStucking < 0:
            print("Неверный формат данных")
            continue
        enableStucking = bool(enableStucking)
        break
    except Exception:
        print("Неверный формат данных")
gameField = Field(n, startSpeed)
allSnakes = []
player = Snake(gameField, "Player", 0, startSpeed, enableStucking)
AISnake = Snake(gameField, "AI", 1, startSpeed, enableStucking)
allSnakes.append(player)
allSnakes.append(AISnake)
for snake in allSnakes:
    snake.speed = startSpeed
gameField.speed = startSpeed
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
        if player.lives == 0:
            endGame = True
            exit(0)
        time.sleep(gameField.speed)
    exit(0)



def thread_function2():
    global player, AISnake, gameField, endGame, speed
    while not endGame:
        newDirection = str(input())
        if newDirection == "a":
            player.rotate(1, allSnakes)
        if newDirection == "w":
            player.rotate(2, allSnakes)
        if newDirection == "s":
            player.rotate(0, allSnakes)
        if newDirection == 'd':
            player.rotate(3, allSnakes)
        time.sleep(player.speed)
    exit(0)


def thread_function3():
    global player, AISnake, gameField, endGame, speed
    while not endGame:
        gameField.fieldUpdate([player, AISnake])
        AISnake.rotate(smartAI.smartMove(gameField.getFieldWithAll(allSnakes), AISnake.cords[-1], AISnake.lives, AISnake.direction, enableStucking), allSnakes)
        time.sleep(AISnake.speed)
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
