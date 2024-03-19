# """
#     1. 분석
#     턴 횟수가 주어질 때, 모든 산타가 얻은 점수를 구하는 문제
#     각 턴 진행시 살아있는 산타 점수 +1
#     부딪칠시 추가점수
#     정지된 산타가 산타와 부딪칠시 특정 칸만큼 밀려남
#     산타가 이동후 루돌프와 부딪칠시 이동방향의 반대방향으로 특정 칸만큼 밀려남
#     격자 밖으로 나갈시 해당 산타 게임 끝

#     각 턴마다: 루돌프 이동 -> 모든 산타 이동    
#     루돌프 이동: 가장 가까운 산타 구하기 + 이동 + 충돌 처리

#     2. 풀이
#     필요한 함수
#     - 1. 루돌프와 가장 가까운 산타 구하는 함수 -> 단일 사용
#     - 2. 해당 산타에 도달하는 방향 구하는 함수 -> 산타, 루돌프 공동 사용
#     - 3. 이동시키는 함수 -> 현재 위치에서 자신 삭제
#     - 4. 충돌날 경우 처리하는 함수 -> 다음 위치 물체 판별 후 처리, 인자: (물체1 종류, 있어야 하는 위치, 방향)
#         - 충돌종류: 루돌프-산타, 산타-산타 
    
#     - 2. 산타가 루돌프에 가까워지기 위한 방향 구하는 함수
#     - 3. 해당 방향으로 이동하는 함수
#     - 4. 이동 후 충돌 처리하는 함수

#     살아있는 산타 집합
#     dic={1:[생존여부, 스턴여부, 위치, 점수]}
    
#     단점: 생존여부 파악하기 위해 전체 순회해야함 -> 구현 쉬워짐
# """

from collections import defaultdict
# """
#     N: 게임판 크기
#     M: 턴 수
#     P: 산타 수
#     C: 루돌프 힘
#     D: 산타 힘
# """
N, M, P, C, D = map(int, input().split(' '))
rX, rY = map(int, input().split(' '))

santas = [[] for _ in range(P + 1)]
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
board[rX][rY] = -1
for _ in range(P):
    idx, sX, sY = map(int, input().split(' '))
    santas[idx] = [True, -1, sX, sY, 0]
    board[sX][sY] = idx

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
turn = 1

def getDist(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2

def getDir(x1, y1, x2, y2): # 루돌프-산타간 방향
    xDiff = x2 - x1
    yDiff = y2 - y1
    
    # x만 같을 경우
    if xDiff == 0:
        return [0, -1] if yDiff < 0 else [0, 1]
    # y만 같을 경우
    if yDiff == 0:
        return [-1, 0] if xDiff < 0 else [1, 0]

    if xDiff > 0:
        # 3사분면
        if yDiff < 0:
            return [1, -1]
        # 4사분면
        return [1, 1]

    # 1사분면
    if yDiff > 0:
        return [-1, 1]
    # 2사분면
    return [-1, -1]

def isIn(x, y):
    return 1 <= x <= N and 1 <= y <= N

def collide(num, x, y, dir):
    global rX, rY

    # 범위 벗어났으면 탈락
    if num != -1 and not isIn(x, y):
        santas[num][0] = False
        return
        
    # 해당 위치에 아무것도 없으면 움직이고 끝
    if board[x][y] == 0:
        board[x][y] = num
        if num == -1:
            rX, rY = x, y
        else:
            santas[num][2] = x
            santas[num][3] = y
        return
    

    # 위치에 누구 있으면, 나와 상대 파악 후 처리

    # 루돌프-산타인 경우
    if num == -1:
        rX, rY = x, y
        s = board[x][y]
        # print(s)
        santas[s][-1] += C
        
        board[x][y] = num
        nx, ny = x + C * dir[0], y + C * dir[1]
        santas[s][1] = turn
        santas[s][2] = nx
        santas[s][3] = ny
        # print(f"여기 어디:{s}")
        collide(s, nx, ny, dir)
    else:
        # 산타 산타일 경우
        if board[x][y] > 0:
            s = board[x][y]
            board[x][y] = num
            nx, ny = x + dir[0], y + dir[1]
            santas[s][2] = nx
            santas[s][3] = ny
            # print(f"여기어디2:{s}")
            collide(s, nx, ny, dir)

        # 산타 루돌프일 경우
        else: 
            santas[num][-1] += D
            nx, ny = x - D * dir[0], y - D * dir[1]
            santas[num][1] = turn
            santas[num][2] = nx
            santas[num][3] = ny
            # print(f"여기어디3:{num}")
            collide(num, nx, ny, [-dir[0], -dir[1]])

        

        
while turn <= M:
    # 턴 시작
    # 루돌프와 가장 가까운 산타 구하기
    s = 0
    r = 0
    c = 0
    minDist = float('inf')
    for x in range(1, P + 1):
        if not santas[x][0]:
            continue

        dist = getDist(rX, rY, santas[x][2], santas[x][3])
        
        if dist < minDist:
            s = x
            minDist = dist
            r = santas[x][2]
            c = santas[x][3]
        elif dist == minDist:
            if r < santas[x][2]:
                s = x
                minDist = dist
                r = santas[x][2]
                c = santas[x][3]
            elif r == santas[x][2]:
                if c < santas[x][3]:
                    s = x
                    minDist = dist
                    r = santas[x][2]
                    c = santas[x][3]

    

    # 방향 구하기
    dir = getDir(rX, rY, santas[s][2], santas[s][3])
    # 해당 방향으로 이동중
    board[rX][rY] = 0

    # 충돌 처리하기
    collide(-1, rX + dir[0], rY + dir[1], dir)
    

    # 산타 움직이기
    for x in range(1, len(santas)):
        if not santas[x][0]:
            continue

        # 스턴시점 체크해서 스턴 시점 + 1 현재 턴
        if santas[x][1] + 1 >= turn:
            continue

        curDist = getDist(rX, rY, santas[x][2], santas[x][3])
        # 4방향 이동 후 거리 구해서 최단거리로 가기
        dir2 = -1
        minDist2 = float('inf')
        nx = 0
        ny = 0
        for i in range(4):
            tempX = santas[x][2] + dx[i]
            tempY = santas[x][3] + dy[i]

            if not isIn(tempX, tempY):
                continue

            if board[tempX][tempY] > 0:
                continue

            dist2 = getDist(rX, rY, tempX, tempY)

            if curDist <= dist2:
                continue

            if dist2 < minDist2:
                nx, ny = tempX, tempY
                minDist2 = dist2
                dir2 = i

        if dir2 == -1:
            continue

        # 이동
        board[santas[x][2]][santas[x][3]] = 0

        # 충돌 처리
        collide(x, nx, ny, [dx[dir2], dy[dir2]])
    
    # 살아 있는 산타 +1
    aliveCnts = 0
    for x in range(1, len(santas)):
        if santas[x][0]:
            santas[x][-1] += 1
            aliveCnts += 1
    
    # print(f"턴:{turn}, 번호:{s}, 방향:{dir}, 루돌프:({rX},{rY}), 산타:{santas}")
    if aliveCnts == 0:
        break

    turn += 1
# print(f"턴:{turn}, 번호:{s}, 방향:{dir}, 루돌프:({rX},{rY}), 산타:{santas}")
for x in range(1, len(santas)):
    print(santas[x][-1], end = ' ')


        

