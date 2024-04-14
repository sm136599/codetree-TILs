from collections import deque

class BTree:
    def __init__(self, N, parents, authority):
        self.N = N
        self.parents = [-1] + parents
        self.authoriy = [-1] + authority
        self.children = [[] for _ in range(N+1)]
        self.depth = [0] * (N+1)
        self.alam = [1] * (N+1)
        self.reset()

    def reset(self):
        for i in range(1, self.N + 1):
            self.children[self.parents[i]].append(i)
            self.depth[i] = self.depth[self.parents[i]] + 1

    def setAlam(self, idx):
        self.alam[idx] ^= 1

    def setPower(self, idx, power):
        self.authoriy[idx] = power

    def changeParent(self, idx1, idx2):
        p1, p2 = self.parents[idx1], self.parents[idx2]
        self.parents[idx1] = p2
        self.parents[idx2] = p1

        self.children[p1].remove(idx1)
        self.children[p2].remove(idx2)
        self.children[p1].append(idx2)
        self.children[p2].append(idx1)

    def countChat(self, idx):
        q = deque()
        q.append(idx)

        cnt = -1
        depth = self.depth[idx]
        while q:
            node = q.popleft()
            if self.depth[node] - depth <= self.authoriy[node]:
                cnt += 1

            for ch in self.children[node]:
                if self.alam[ch]:
                    q.append(ch)
        print(cnt)

    def __str__(self):
        return f'parents: {self.parents}\n' \
               f'children: {self.children}\n' \
               f'authority: {self.authoriy}\n' \
               f'alam: {self.alam}\n' \
               f'depth: {self.depth}\n\n'

def main():
    N, Q = map(int, input().split())
    for _ in range(Q):
        cmd = list(map(int, input().split()))
        c = cmd[0]
        if c == 100:
            tree = BTree(N, cmd[1:N+1], cmd[N+1:])
        elif c == 200:
            tree.setAlam(cmd[1])
        elif c == 300:
            tree.setPower(cmd[1], cmd[2])
        elif c == 400:
            tree.changeParent(cmd[1], cmd[2])
        elif c == 500:
            tree.countChat(cmd[1])

        # print(tree)



main()