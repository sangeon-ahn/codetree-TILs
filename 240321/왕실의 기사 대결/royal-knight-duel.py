"""
    5:15
    1. 분석
    L*l 격자 체스판 1,1 시작
    각칸: 빈칸, 함정, 벽
    마력으로 밀쳐내기
    각 기사 초기위치 r,c 이고 (r,c)왼쪽위 기준으로 h*w 크기의 직사각형 형태
    체력 k

    - 기사 이동
        - 기사 상하좌우 이동 가능
        - 다른 기사 있으면 기사 연쇄적으로 밀려남
        - 죽은 기사 명령 못내림

    - 대결 데미지
        - A -> B : B가 피해 입음. 밀려진 위치에서 w*h 직사각형 내 함정 수만큼 피해입음.
        - 체력 0 이하되면 죽음
    
    Q번 턴 이후 모든 데미지의 합 구하기

    2. 풀이
    이동하려는 기사와 방향을 가지고, 해당 방향쪽의 한 줄을 구한다.
    이후, 해당 줄 + 해당 방향으로 1칸 위치에 기사 있나 파악 후, 있는 기사에 대해 각각 연쇄적으로 같은 로직 수행
    중간에 만약 벽을 발견해서 이동할 수 없는 명령이었다면 이동불가로 다음 턴으로 넘어감.
    만약 벽이 없어 이동할 수 있는 명령이면, 해당 방향의 끝 기사부터 움직이며, 함정 있으면 체력 소진 + 총 데미지에 추가한다.
    체력이 0 이하가 되면 보드에서 지우고 생존여부 바꾼다.
    
    각 기사의 셀을 set으로 관리할까? no
    배열로 관리해야 더할 때 편함.
    벽, 함정 판단은 그냥 보드에서 직접.

    벽 = -1, 함정 = -2, 빈칸 = -3, 솔저 = 0부터 시작

    가장 dir 방향에 있는 셀들을 다 찾은 후, 해당 셀의 dir 한칸 더 간곳이 벽이 아니면 이동, 이동

    dir별로 확인해야 하는 라인이 다르다.
    0상: 맨위-맨아래
    1우: 맨오른-맨왼
    2하: 맨아래-맨위
    3좌: 맨왼-맨오른

    배열에는 기사 번호를 넣고, 연쇄 충돌 끝났으면 맨 뒤에서부터 dir 방향으로 이동

    이동하는 법: 그냥 r,c만 이동
    충돌 따지는 법: r, c, w, h 2중 for문 돌면서 함정 있으면 -1
    
"""
import sys
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

if N == 1:
    print(0)
    sys.exit()

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

damages = [0 for _ in range(N)]

for _ in range(Q):
    idx, dir = map(int, input().split())
    idx -= 1

    if healths[idx] <= 0:
        continue

    # dir 방향으로 idx 이동

    res = move(idx, dir, 0)
    # print(bumped, res)
    # 충돌했으면 넘어가기
    if not res:
        bumped = []
        continue

    # 충돌 안했는데 부딪친거 없으면 그냥 이동
    pos[idx] = (pos[idx][0] + dx[dir], pos[idx][1] + dy[dir])
    if not bumped:
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
                    damages[bumped[i]] += 1

    # 충돌난 기사 다 이동시켰으면 이제 초기화
    bumped = []

ans = 0
for i in range(N):
    if healths[i] > 0:
        ans += damages[i]
print(ans)