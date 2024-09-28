import string
import time

def load_maze(filename="map.txt"):
    with open(filename, "r") as f:
        data = f.read()
    return list(map(lambda x: list(x), data.split("\n")))[:-1]

def find_start_and_goal(maze):
    start, goal = None, None
    for i in range(len(maze)):
        if "A" in maze[i]:
            start = (i, maze[i].index("A"))
            maze[i][start[1]] = "." 
        if "B" in maze[i]:
            goal = (i, maze[i].index("B"))
            maze[i][goal[1]] = "."  
    return start, goal

def find_portals(maze):
    portals = {}
    for pl in string.ascii_lowercase:
        o1, o2 = None, None
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == pl:
                    if o1:
                        o2 = (i, j)
                        portals[pl] = (o1, o2)
                        break
                    else:
                        o1 = (i, j)
    return portals

def safe_get(maze, x, y, dx, dy):
    if x + dx < 0 or x + dx >= len(maze):
        return None
    if y + dy < 0 or y + dy >= len(maze[0]):
        return None
    return maze[x+dx][y+dy]

def safe_v_get(maze, visited, x, y, dx, dy):
    if (x + dx, y + dy) in visited:
        return None
    return safe_get(maze, x, y, dx, dy)

def deepcopy(maze):
    return [row[:] for row in maze]

def destroy_portals(maze, pl, newstate):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == pl:
                maze[i][j] = newstate

class State:
    def __init__(self, mazeState, px, py, depth, portalcount, path, visited):
        self.mazeState = mazeState
        self.px = px
        self.py = py
        self.depth = depth
        self.portalcount = portalcount
        self.path = path
        self.visited = visited

    def dump(self):
        print(f"{self.depth} {self.portalcount} [{self.px},{self.py}] {self.path}")

class MazeState:
    def __init__(self, maze, portals):
        self.maze = maze
        self.portals = portals

    def dump_maze(self):
        print("\n".join(map(lambda x: "".join(x), self.maze)))

    def get_next_maze(self):
        newmaze = deepcopy(self.maze)
        newportals = self.portals.copy()
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                around = sum([1 for (dx, dy) in surrounding if safe_get(self.maze, i, j, dx, dy) == "&"])
                
                if self.maze[i][j] == "&": 
                    if around != 2 and around != 3:
                        newmaze[i][j] = "."
                else:
                    if around >= 3:
                        newmaze[i][j] = "&"
                        if self.maze[i][j] in string.ascii_lowercase and self.maze[i][j] in newportals:
                            del newportals[self.maze[i][j]]
                            destroy_portals(newmaze, self.maze[i][j], "&")

        return MazeState(newmaze, newportals)

    def destroyed_portal(self, pl):
        newmaze = deepcopy(self.maze)
        newportals = self.portals.copy()
        del newportals[pl]
        destroy_portals(newmaze, pl, ".")
        return MazeState(newmaze, newportals)
 
# global vars
surrounding = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)] 
moves = {
    "N": (-1,0),
    "E": (0, -1),
    "S": (0,1),
    "W": (1,0),
}

if __name__ == "__main__":
    initial_maze = load_maze()
    start, goal = find_start_and_goal(initial_maze)
    portals = find_portals(initial_maze)
    
    first_state = MazeState(initial_maze, portals)
    q = [State(first_state, start[0], start[1], 0, 0, "", [])]
    
    solutions = []
    mindepth = -1
    
    start_time = time.time()
    while q:
        state = q.pop(0)
        
        if mindepth != -1 and state.depth > mindepth:
            break
        if (state.px, state.py) == goal:
            mindepth = state.depth
            solutions.append(state)
            continue
        
        next_maze_state = state.mazeState.get_next_maze()
        for move in moves:
            dx, dy = moves[move]
            origtarg = safe_v_get(state.mazeState.maze, state.visited, state.px, state.py, dx, dy)
            if origtarg is None or origtarg == "&":
                continue
            nexttarg = safe_get(next_maze_state.maze, state.px, state.py, dx, dy)
            if nexttarg == "&":
                continue
            if origtarg in next_maze_state.portals:
                if (state.px+dx, state.py+dy) == state.mazeState.portals[origtarg][0]:
                    newpx, newpy = state.mazeState.portals[origtarg][1]
                else:
                    newpx, newpy = state.mazeState.portals[origtarg][0]
                q.append(State(next_maze_state.destroyed_portal(origtarg), newpx, newpy, state.depth+1, state.portalcount+1, state.path + move, state.visited + [(newpx, newpy), (state.px+dx, state.py+dy)]))
            else:
                newpx, newpy = state.px + dx, state.py + dy
                q.append(State(next_maze_state, newpx, newpy, state.depth+1, state.portalcount, state.path + move, state.visited + [(newpx, newpy)]))
    
    if solutions:
        max_portals = max(sol.portalcount for sol in solutions)
        maxsols = filter(lambda x: x.portalcount == max_portals, solutions)
        paths = sorted([sol.path for sol in maxsols])
        print(f"{len(paths)}-{''.join(paths)}-{max_portals}")

    end_time = time.time()  
    elapsed_time = end_time - start_time 
    print(f"\nProcess completed in {elapsed_time:.2f} seconds.")
