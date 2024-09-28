file = "coding100/challenge.txt"

with open(file, "r") as f:
    data = f.read().strip()
    rgrid, rwords = data.split("\n\n\n")


grid = [row.split(" ") for row in rgrid[:-1].split("\n", 1)[1].split(" \n")]
words = rwords.split("\n")[1:]

all_dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]


def search_dir(
    word: str, pos: tuple[int, int], dir: tuple[int, int], can_turn: bool
) -> list[tuple[int, int]] | None:
    x, y = pos

    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or grid[x][y] != word[0]:
        return None

    if len(word) == 1:
        return [(x, y)]

    next = search_dir(word[1:], (x + dir[0], y + dir[1]), dir, can_turn)
    if next:
        return [(x, y)] + next

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)] if can_turn else [dir]

    for d in dirs:
        dx, dy = d
        if d == dir or (dx != 0 and dy != 0) or (dx == -dir[0] and dy == -dir[1]):
            continue
        next = search_dir(word[1:], (x + dx, y + dy), d, False)
        if next:
            return [(x, y)] + next

    return next


def search(
    word: str, pos: tuple[int, int], dirs: list[tuple[int, int]]
) -> list[tuple[int, int]] | None:
    for dir in dirs:
        result = search_dir(word, pos, dir, dir[0] == 0 or dir[1] == 0)
        if result:
            return result
    return None


fwords: dict[str, tuple[int, int]] = {}
for c, word in enumerate(words):
    print(word)
    found = False
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "_":
                continue
            if grid[i][j] == word[0]:
                print(i, j)
                pos = search(word, (i, j), dirs=all_dirs)
                if pos:
                    for p in pos:
                        grid[p[0]][p[1]] = "_"

for row in grid:
    print(" ".join(row))

for row in grid:
    for cell in row:
        if cell != "_":
            print(cell, end="")


for w, p in fwords.items():
    print(f"{w}: {p[0] + 1} {p[1] + 1}")
