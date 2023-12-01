import queue
import copy


def smartMove(c, startCords, h, rotate, isStuck):
    n = len(c)
    portal = []
    endPoint = -1
    field = []
    for i in range(0, n):
        r = []
        for g in range(0, n):
            r.append(-1)
        field.append(r)
    for i in range(0, n):
        for g in range(0, n):
            if c[i][g] == '.' or [i, g] == startCords:
                field[i][g] = 0
                continue
            if c[i][g] == '*':
                field[i][g] = 1
                endPoint = i * n + g
                continue
            if c[i][g] == 'P':
                field[i][g] = 2
                portal.append(i * n + g)
                continue
            if c[i][g] == 'F':
                field[i][g] = 3
                continue
            if c[i][g] == 'B':
                field[i][g] = 4
                continue
            if c[i][g] == 'H':
                field[i][g] = 5
                continue
            if isStuck:
                field[i][g] = -1
            else:
                if c[i][g] == '#' or c[i][g] == '▦':
                    field[i][g] = -1
                else:
                    field[i][g] = 0
    #for v in field:
    #    print(*v)
    gr = []
    for i in range(0, n * n):
        gr.append([])
    for i in range(0, n):
        for g in range(0, n):
            p = 0
            f = 0
            if field[i][g] == 5:
                p = -1
            if field[i][g] == 3:
                f = 1
            if field[i][g] >= 0 and field[i][g] != 2:
                if i - 1 >= 0:
                    p = 0
                    f = 0
                    if field[i - 1][g] == 5:
                        p = -1
                    if field[i - 1][g] == 3:
                        f = 1
                    gr[i * n + g].append([(i - 1) * n + g, 1, p, 2, f])
                if i + 1 < n:
                    p = 0
                    f = 0
                    if field[i + 1][g] == 5:
                        p = -1
                    if field[i + 1][g] == 3:
                        f = 1
                    gr[i * n + g].append([(i + 1) * n + g, 1, p, 0, f])
                if g - 1 >= 0:
                    p = 0
                    f = 0
                    if field[i][g - 1] == 5:
                        p = -1
                    if field[i][g - 1] == 3:
                        f = 1
                    gr[i * n + g].append([i * n + g - 1, 1, p, 1, f])
                if g + 1 < n:
                    p = 0
                    f = 0
                    if field[i][g + 1] == 5:
                        p = -1
                    if field[i][g + 1] == 3:
                        f = 1
                    gr[i * n + g].append([i * n + g + 1, 1, p, 3, f])
            if field[i][g] == -1:
                f = 0
                if field[n // 2 + 1][n // 2 + 1] == 3:
                    f = 1
                gr[i * n + g].append([(n // 2 + 1) * n + n // 2 + 1, 1, 1, 4, f])
    if len(portal) > 0:
        gr[portal[0]].append([portal[1], 1, 0, 4, 0])
        gr[portal[1]].append([portal[0], 1, 0, 4, 0])
    dist = []
    used = []
    for i in range(0, n * n):
        dist.append([100000000000000, 0, -1])
        used.append(False)
    q = queue.PriorityQueue()
    q.put([0, h, startCords[0] * n + startCords[1], rotate])
    dist[startCords[0] * n + startCords[1]] = [0, h, rotate]
    while not q.empty():
        t = q.get()
        direction = t[3]
        w = t[2]
        heart = t[1]
        if used[w]:
            continue
        used[w] = True
        for v in gr[w]:
            if v[3] == 4 or abs(v[3] - direction) != 2:
                if dist[w][0] + v[1] - v[4] * 3 < dist[v[0]][0]:
                    if heart - v[2] <= 0:
                        continue
                    dist[v[0]][0] = dist[w][0] + v[1] - v[4] * 3
                    dist[v[0]][1] = heart - v[2]
                    dist[v[0]][2] = w
                    q.put([dist[v[0]][0], dist[v[0]][1], v[0], v[3]])
                if dist[w][0] + v[1] - v[4] * 3 == dist[v[0]][0]:
                    if heart - v[2] <= 0:
                        continue
                    if heart + v[2] >= dist[v[0]][1]:
                        dist[v[0]][1] = heart + v[2]
                        dist[v[0]][2] = v[3]
                        dist[v[0]][2] = w
                        q.put([dist[v[0]][0], dist[v[0]][1], v[0], v[3]])
    moves = []
    x = endPoint
    while True:
        moves.append(x)
        x = dist[x][2]
        if x == startCords[0] * n + startCords[1]:
            break
    if moves[-1] // n > startCords[0]:
        return 0
    if moves[-1] // n < startCords[0]:
        return 2
    if moves[-1] % n > startCords[1]:
        return 3
    return 1


def check():
    n = int(input()) + 2
    field = []
    for i in range(0, n):
        field.append(list(map(str, input())))
    start = list(map(int, input().split()))
    h = int(input())
    rotate = int(input())
    stuck = bool(int(input()))
    print(smartMove(field, start, h, rotate, stuck))


#check()
