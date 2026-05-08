# Computer Graphics – Maze Generator

**Name:** Elroi Tesfaye  
**ID:** UGR/1293/16  
**Section:** 1

---

## description

An interactive maze rendered with **PyOpenGL / GLUT**. A new random maze is generated every run using a stack-based depth-first search. After generation, an animated "mouse" solves the maze in real time using the same DFS logic with visual backtracking.

---

## how it works

### maze generation – stack-based DFS

1. The mouse starts at `(0, 0)`, marks it visited, and pushes it onto a stack.
2. It picks a random unvisited neighbor, removes the shared wall, and moves there.
3. When no unvisited neighbors exist, it backtracks by popping the stack.
4. Repeats until every cell is visited → a perfect maze.

After generation, ~1 in 20 extra walls are randomly removed to create **cycles**. This defeats the classic shoulder-to-wall traversal trick. The start and end cells are also placed in the **interior** of the maze (not on the boundary), making the shoulder-to-wall method fail entirely.

### animated solver

- 🔴 **Red dot** – current mouse position
- 🔵 **Blue cells** – dead ends (mouse backtracked)
- Dim cells – path the mouse has visited
- 🟡 **Gold dot** – maze solved

### data structures

```
northWall[r][c]  True → top edge of cell (r, c) is a wall
eastWall[r][c]   True → right edge of cell (r, c) is a wall
```

South wall of `(r,c)` = `northWall[r+1][c]`  
West wall of `(r,c)` = `eastWall[r][c-1]`

---

## requirements

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

---

## run

```bash
python main.py
```

| key | action |
|-----|--------|
| `R` | generate a new maze |
| `Q` / `ESC` | quit |

---

## configuration (top of `main.py`)

| variable | default | description |
|----------|---------|-------------|
| `ROWS` | 15 | maze rows |
| `COLS` | 20 | maze columns |
| `SEED` | `None` | fixed integer → repeatable maze |
| `STEP_MS` | 40 | animation speed in ms (lower = faster) |
