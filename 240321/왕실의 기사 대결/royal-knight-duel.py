L, N, Q = map(int, input().split())
board = []
for _ in range(L):
    line = list(map(int, input().split()))
    board.append(line)

healths = [0 for _ in range(N)]
pos = [(0, 0) for _ in range(N)]
size = [(0, 0) for _ in range(N)]

# 솔저 정보 저장
for i in range(N):
    r, c, h, w, k = map(int, input().split())

    healths[i] = k
    pos[i] = (r - 1, c - 1)
    size[i] = (h, w)

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

bumped = []

def move(idx, dir, cumul):
    r = pos[idx][0]
    c = pos[idx][1]

    # 지뢰 체크
    for i in range(size[idx][(dir + 1)%2]): # 1, 0, 1, 0
        # 상
        if dir == 0 and (r - 1 < 0 or board[r - 1][c + i]) == 2:
            return False
        # 하
        if dir == 2 and (r + size[idx][0] >= L or board[r + size[idx][0]][c + i]) == 2:
            return False
        # 좌
        if dir == 3 and (c - 1 < 0 or board[r + i][c - 1]) == 2:
            return False
        # 우
        if dir == 1 and (c + size[idx][1] >= L or board[r + i][c + size[idx][1]]) == 2:
            return False


    # 상, 하
    if (dir + 1) % 2 == 1:
        for j in range(N):
            if idx == j or healths[j] <= 0 or j in bumped:
                continue

            # j번째 기사랑 부딪치나 확인
            jr = pos[j][0] 
            jc = pos[j][1]

            # x가 사이에 있고 y가 1 차이면 충돌
            if (c <= jc <= c + size[idx][(dir + 1)%2] - 1 or jc <= c <= jc + size[j][(dir + 1)%2] - 1):
                if dir == 0 and jr + size[j][0] == r:
                    if j not in bumped:
                        bumped.append(j)
                        res = move(j, dir, cumul + 1)

                        if not res:
                            return False
                            
                elif dir == 2 and jr == r + size[idx][0]:
                    if j not in bumped:
                        bumped.append(j)
                        res = move(j, dir, cumul + 1)

                        if not res:
                            return False
    # 좌, 우
    else:
        for j in range(N):
            if idx == j or healths[j] <= 0 or j in bumped:
                continue

            # j번째 기사랑 부딪치나 확인
            jr = pos[j][0]
            jc = pos[j][1] + (-1)**(dir + 1) * cumul

            # x가 사이에 있고 y가 1 차이면 충돌
            if (r <= jr <= r + size[idx][(dir + 1)%2] - 1 or jr <= r <= jr + size[j][(dir + 1)%2] - 1):
                if dir == 1 and jc == c + size[idx][1]:
                    if j not in bumped:
                        bumped.append(j)
                        res = move(j, dir, cumul + 1)

                        if not res:
                            return False

                elif dir == 3 and jc + size[j][1] == c:
                    if j not in bumped:
                        bumped.append(j)
                        res = move(j, dir, cumul + 1)
                        if not res:
                            return False
    return True

damages = 0

for _ in range(Q):
    idx, dir = map(int, input().split())
    idx -= 1

    if healths[idx] <= 0:
        continue

    # dir 방향으로 idx 이동

    res = move(idx, dir, 0)
 
    # 충돌했으면 넘어가기
    if not res:
        bumped = []
        continue

    # 충돌 안했는데 부딪친거 없으면 그냥 이동
    if not bumped:
        pos[idx] = (pos[idx][0] + dx[dir], pos[idx][1] + dy[dir])
        continue

    # 충돌했으면, 충돌한 기사들 구했으니 bumped 맨 뒤부터 이동시키기
    moved = set()
    for i in range(len(bumped) - 1, -1, -1):
        if bumped[i] in moved:
            continue
        moved.add(bumped[i])
        # 위치 이동
        pos[bumped[i]] = (pos[bumped[i]][0] + dx[dir], pos[bumped[i]][1] + dy[dir])
        r = pos[bumped[i]][0]    
        c = pos[bumped[i]][1] 

        # 지뢰 확인
        for j in range(size[bumped[i]][0]):
            for k in range(size[bumped[i]][1]):
                if board[r + j][c + k] == 1:
                    healths[bumped[i]] -= 1
                    damages += 1

    # 충돌난 기사 다 이동시켰으면 이제 초기화
    bumped = []

print(damages)