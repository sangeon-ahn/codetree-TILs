from collections import deque

MAX_N = 31
MAX_L = 41
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


board = [[0 for _ in range(MAX_L)] for _ in range(MAX_L)]
healthSaved = [0 for _ in range(MAX_N)]

r = [0 for _ in range(MAX_N)]
c = [0 for _ in range(MAX_N)]
h = [0 for _ in range(MAX_N)]
w = [0 for _ in range(MAX_N)]
k = [0 for _ in range(MAX_N)]

# 새로운 r과 c 저장소
nr = [0 for _ in range(MAX_N)]
nc = [0 for _ in range(MAX_N)]

dmg = [0 for _ in range(MAX_N)]
isMoved = [False for _ in range(MAX_N)]


def tryMoving(idx, dir):
    q = deque()
    isPos = True

    # 초기화 작업
    for i in range(1, n + 1):
        dmg[i] = 0
        isMoved[i] = False
        nr[i] = r[i]
        nc[i] = c[i]
    
    q.append(idx)
    isMoved[idx] = True # 움직이는지 유무 체크하는 변수인데 움직였다고 체크함.

    while q:
        cur = q.popleft()

        nr[cur] += dx[dir]
        nc[cur] += dy[dir]

        # 보드 밖인지 체크
        if nr[cur] < 1 or nr[cur] > l or nc[cur] < 1 or nc[cur] > l:
            return False
        
        # 이동시 충돌 체크
        for i in range(nr[cur], nr[cur] + h[cur]):
            for j in range(nc[cur], nc[cur] + w[cur]):
                if board[i][j] == 1: # 지뢰면 데미지
                    dmg[cur] += 1
                elif board[i][j] == 2: # 벽이면 끝
                    return False
        
        # 다른 기사랑 충돌하면
        for i in range(1, n + 1):
            # 이미 움직였거나 죽은거면 패스
            if isMoved[i] or k[i] <= 0:
                continue

            # 여기서 행 기준, 열 기준으로 해서 겹치는 부분이 없는걸 각각 제거해준다.
            if r[i] > nr[cur] + h[cur] - 1 or nr[cur] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[cur] + w[cur] - 1 or nc[cur] > c[i] + w[i] - 1: 
                continue

            # 여기 오면 부딪친것
            isMoved[i] = True
            q.append(i)
    # 처음에 움직인 애도 데미지 추가됐으므로 다시 돌리기
    dmg[idx] = 0
    # 여기까지 왔으면 벽 안만난거라 이동할 수 있다는 True 리턴 
    return True

def moveSoldier(idx, dir):
    if k[idx] <= 0:
        return
    
    if tryMoving(idx, dir):
        for i in range(1, n + 1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

l, n, q = map(int, input().split())

for i in range(1, l + 1):
    board[i][1:] = map(int, input().split())

for i in range(1, n + 1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    healthSaved[i] = k[i]
    
for _ in range(q):
    idx, d = map(int, input().split())
    moveSoldier(idx, d)

ans = sum(healthSaved[i] - k[i] for i in range(1, n + 1) if k[i] > 0)
print(ans)