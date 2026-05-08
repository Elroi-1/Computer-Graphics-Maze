# Computer Graphics – Maze Generator

An interactive maze generator rendered with **PyOpenGL / GLUT**.  
A new random maze is produced every run using an iterative **stack-based Depth-First Search** – sometimes called the *"mouse in a maze"* algorithm.

---

## How It Works

### Algorithm – Stack-based DFS ("Mouse" Logic)

1. **Start** – the "mouse" is placed at cell `(0, 0)` and pushed onto a stack; that cell is marked visited.
2. **Explore** – at each step the mouse peeks at the top of the stack and randomly picks one of its unvisited cardinal neighbours (N / S / E / W).
3. **Carve** – the wall shared between the current cell and the chosen neighbour is removed (set to `False` in the wall array).
4. **Move** – the neighbour is marked visited and pushed onto the stack.
5. **Backtrack** – when no unvisited neighbours exist the mouse *backtracks* by popping from the stack.
6. **Done** – the algorithm ends when the stack is empty, meaning every cell has been visited and the result is a **perfect maze** (exactly one path between any two cells).

Because backtracking is handled by a Python `list` used as a stack, the implementation is fully iterative and avoids Python's recursion limit.

---

## Data Structure

Two 2-D boolean arrays represent every interior wall exactly **once**:

```
northWall[row][col]   True  ⟹  the NORTH (top) wall of cell (row, col) is solid
eastWall [row][col]   True  ⟹  the EAST (right) wall of cell (row, col) is solid
```

Shared-wall equivalences (no duplication):

| Wall of cell (r, c) | Same physical wall as … |
|---------------------|------------------------|
| South wall          | `northWall[r+1][c]` |
| West wall           | `eastWall[r][c-1]` |

The outer boundary walls are **never stored** in these arrays; they are always drawn separately.

---

## Project Structure

```
Computer-Graphics-Maze/
│
└── main.py     # Maze generation (DFS) + OpenGL rendering
```

---

## Requirements

| Package | Purpose |
|---------|---------|
| Python ≥ 3.8 | Runtime |
| PyOpenGL | OpenGL bindings |
| PyOpenGL_accelerate *(optional)* | Faster rendering |

Install dependencies:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

---

## Running

```bash
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| `R` | Generate a new random maze |
| `Q` or `ESC` | Quit |

---

## Configuration

At the top of `main.py` you can adjust:

| Variable | Default | Description |
|----------|---------|-------------|
| `ROWS` | 15 | Number of maze rows |
| `COLS` | 20 | Number of maze columns |
| `SEED` | `None` | Fixed integer → reproducible maze |
| `WINDOW_W` | 800 | Window width (px) |
| `WINDOW_H` | 600 | Window height (px) |

---

## Visual Layout

- 🟢 **Green cell** – start `(0, 0)`  
- 🔴 **Red cell** – end `(ROWS-1, COLS-1)`  
- 🔵 **Blue lines** – maze walls  
- ⬛ **Dark background**

---

*Assignment: Computer Graphics – Maze Generator*  
