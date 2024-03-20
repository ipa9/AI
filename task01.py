import random

class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.family_tree = []

    def add_child(self, child_node):
        self.family_tree.append(child_node)


class QueueSpace:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(0)

    def is_empty(self):
        return len(self.frontier) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)


def generate_maze(rows, cols, start, finish):
    maze = [['#' for _ in range(cols)] for _ in range(rows)]

    # Generate walls and empty spaces
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if random.random() < 0.3:
                maze[row][col] = '#'  # Wall
            else:
                maze[row][col] = ' '  # Empty space

    # Mark start and finish positions
    maze[start[0]][start[1]] = 'S'
    maze[finish[0]][finish[1]] = 'F'

    return maze



def bfs(maze, start, finish):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = QueueSpace()
    queue.add(Node(start))
    visited[start[0]][start[1]] = True

    while not queue.is_empty():
        node = queue.remove()
        row, col = node.state
        if (row, col) == finish:
            return node

        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        random.shuffle(neighbors)
        for r, c in neighbors:
            if 0 <= r < rows and 0 <= c < cols and not visited[r][c] and maze[r][c] != '#':
                visited[r][c] = True
                queue.add(Node((r, c), parent=node))

    return None


def print_maze(maze):
    for row in maze:
        print(''.join(row))


# Generate random maze
rows = 12
cols = 12
start = (1, 1)
finish = (10, 10)
maze = generate_maze(rows, cols, start, finish)
print("Generated Maze:")
print_maze(maze)

# Find solution path using BFS
solution_node = bfs(maze, start, finish)
if solution_node:
    solution_path = []
    while solution_node.parent:
        solution_path.append(solution_node.state)
        solution_node = solution_node.parent
    solution_path.reverse()
    for row, col in solution_path:
        maze[row][col] = 'X'
    print("\nSolution Found:")
    print_maze(maze)
else:
    print("No solution found.")
