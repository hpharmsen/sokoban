from collections import deque


class MazeRunner:
    """ Find a path between to coo's in a 2-D grid """

    def __init__(self, grid):
        self.maze = grid
        self.path_tree = {}  # Stores the tree of possible paths as a dict with key a coo and value the previous coo
        self.queue = deque()  # The list of leaves of the tree that still have to be explored

    def find_path(self, start_coo, end_coo):
        passable = (' ', '.', '@')
        if not self.maze[end_coo] in passable:
            return None
        self.path_tree[end_coo] = None
        self.queue.append(end_coo)
        while self.queue:
            coo = self.queue.popleft()
            for dxdy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                newcoo = (coo[0] + dxdy[0], coo[1] + dxdy[1])
                if newcoo != end_coo and not self.path_tree.get(newcoo) and self.maze[newcoo] in passable:
                    self.path_tree[newcoo] = coo
                    if self.maze[newcoo] == '@':
                        return self.unwind(coo)
                    self.queue.append(newcoo)
        return None

    def unwind(self, coo):
        newcoo = self.path_tree.get(coo)
        if newcoo:
            return [(coo)] + (self.unwind(newcoo))
        else:
            return [(coo)]
