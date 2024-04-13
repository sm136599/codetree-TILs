from heapq import heappush, heappop

# 루돌프 이동
drr = [-1, -1, 0, 1, 1, 1, 0, -1]
dcc = [0, 1, 1, 1, 0, -1, -1, -1]

N, M, P, C, D = map(int, input().split())
rudolf = list(map(int, input().split()))
santas = [list(map(int, input().split())) for _ in range(P)]
mapp = [[0] * (N + 1) for _ in range(N + 1)]
mapp[rudolf[0]][rudolf[1]] = -1
for i, r, c in santas:
    mapp[r][c] = i

global_flag = False
santas = {i: [r, c] for i, r, c in santas}

score = [0] * (P + 1)
faint = [0] * (P + 1)
fail = [False] * (P + 1)

def getDist(r1, r2, c1, c2):
    return ((r1-r2)**2 + (c1-c2)**2)**0.5

def turnR():
    global rudolf, santas, mapp, score, faint, fail, N, M, P, C, D
    r_r, r_c = rudolf
    # 가장 가까운 산타 고르기
    dist = []
    for s_i, value in santas.items():
        if fail[s_i]:
            continue
        s_r, s_c = value
        d = getDist(r_r, s_r, r_c, s_c)
        heappush(dist, (d, -s_r, -s_c, s_i))

    _, s_r, s_c, s_i = heappop(dist)
    s_r *= -1
    s_c *= -1

    # 방향 정하기
    dist = []
    for k in range(8):
        nr = r_r + drr[k]
        nc = r_c + dcc[k]

        if 0 < nr <= N and 0 < nc <= N:
            d = getDist(nr, s_r, nc, s_c)
            heappush(dist, (d, nr, nc, k))

    _, nr, nc, direction = heappop(dist)

    # 충돌처리
    if mapp[nr][nc] > 0:
        crash(-1, mapp[nr][nc], direction)

    # 맵에 입력, 움직이기
    rudolf = [nr, nc]
    mapp[r_r][r_c] = 0
    mapp[nr][nc] = -1

def turnS():
    global rudolf, santas, mapp, score, faint, fail, N, M, P, C, D
    r_r, r_c = rudolf
    for s_i in range(1, P+1):
        # 탈락했거나 기절한 산타는 움직이지 않는다.
        if fail[s_i] or faint[s_i] != 0:
            continue

        s_r, s_c = santas[s_i]

        # 현재 거리
        dist_now = getDist(s_r, r_r, s_c, r_c)
        dist = []
        for k in range(0, 8, 2):
            nr = s_r + drr[k]
            nc = s_c + dcc[k]
            if 0<nr<=N and 0<nc<=N:
                if mapp[nr][nc] <= 0:
                    d = getDist(nr, r_r, nc, r_c)
                    if d < dist_now:
                        heappush(dist, (d, k))
        nr = -1
        nc = -1
        movement = False
        flag = True
        while dist:
            _, direction = heappop(dist)
            nr = s_r + drr[direction]
            nc = s_c + dcc[direction]
            if mapp[nr][nc] > 0:
                continue

            movement = True
            santas[s_i] = [nr, nc]
            mapp[s_r][s_c] = 0
            if mapp[nr][nc] == -1:
                flag = False
                crash(s_i, -1, direction)
            break

        if movement and flag and not fail[s_i]:
            mapp[nr][nc] = s_i

        # print(s_i, '번 차례')
        # printMap()

    for i in range(1, P+1):
        if not fail[i]:
            score[i] += 1
        if faint[i] > 0:
            faint[i] -= 1

def crash(obj1, obj2, direction):
    global rudolf, santas, mapp, score, faint, fail, N, M, P, C, D
    # obj1이 obj2를 치는 경우
    # obj 가 -1이면 루돌프, 1이상이면 산타
    if obj1 == -1:
        # 루돌프가 산타와 충돌할 경우
        s_r, s_c = santas[obj2]
        nr = s_r + drr[direction]*C
        nc = s_c + dcc[direction]*C

        if 0<nr<=N and 0<nc<=N:
            if mapp[nr][nc] > 0:
                # 다른 산타가 있으면
                crash(obj2, mapp[nr][nc], direction)
            santas[obj2] = [nr, nc]
            mapp[nr][nc] = obj2
        else:
            # 산타가 밖으로 나가면
            santas[obj2] = [nr, nc]
            fail[obj2] = True
        score[obj2] += C
        faint[obj2] = 2
    elif obj2 == -1:
        # 산타가 루돌프와 충돌할 경우
        # 반대방향으로 튕겨 나감
        direction = (direction+4) % 8
        s_r, s_c = santas[obj1]
        nr = s_r + drr[direction]*D
        nc = s_c + dcc[direction]*D

        if 0<nr<=N and 0<nc<=N:
            if mapp[nr][nc] > 0:
                crash(obj1, mapp[nr][nc], direction)
            santas[obj1] = [nr, nc]
            mapp[nr][nc] = obj1
        else:
            santas[obj1] = [nr, nc]
            fail[obj1] = True
        score[obj1] += D
        faint[obj1] = 2
    else:
        # 산타와 산타가 충돌할 경우
        s_r, s_c = santas[obj2]
        nr = s_r + drr[direction]
        nc = s_c + dcc[direction]

        if 0<nr<=N and 0<nc<=N:
            if mapp[nr][nc] > 0:
                crash(obj2, mapp[nr][nc], direction)
            santas[obj2] = [nr, nc]
            mapp[nr][nc] = obj2
        else:
            santas[obj2] = [nr, nc]
            fail[obj2] = True

def updateGlobalFlag():
    global fail, global_flag, P
    for i in range(1, P+1):
        if not fail[i]:
            global_flag = False
            return

    global_flag = True
    return

def printMap():
    global N, mapp
    for i in range(1, N+1):
        for j in range(1, N+1):
            print(f'{mapp[i][j]}', end=' ')
        print()
    print(fail)
    print(score)
    print()


# printMap()
for _ in range(M):
    if global_flag:
        break
    # print('루돌프 차례')
    turnR()
    # printMap()
    # print('산타 차례')
    turnS()
    # printMap()
    updateGlobalFlag()

for i in range(1, P+1):
    print(score[i], end=' ')