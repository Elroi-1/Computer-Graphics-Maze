# Computer Graphics – Maze Generator
# name: Elroi Tesfaye
# id: UGR/1293/16
# section: 1


import sys
import random

try:
    from OpenGL.GL   import *
    from OpenGL.GLUT import *
    from OpenGL.GLU  import *
except ImportError:
    sys.exit("Install PyOpenGL first:  pip install PyOpenGL PyOpenGL_accelerate")

# grid size
ROWS     = 15
COLS     = 20
SEED     = None   # fixed seed for repeatable maze

WINDOW_W = 800
WINDOW_H = 600

STEP_MS  = 40     # ms per animation frame

# interior start/end so shoulder-to-wall trick fails
START = (ROWS // 4,     COLS // 4)
END   = (3 * ROWS // 4, 3 * COLS // 4)

# colors
BG_COLOR      = (0.05, 0.05, 0.10)
WALL_COLOR    = (0.20, 0.45, 0.90)
START_COLOR   = (0.10, 0.90, 0.30)
END_COLOR     = (0.90, 0.20, 0.20)
VISITED_COLOR = (0.15, 0.15, 0.30)  # visited path
DEAD_COLOR    = (0.10, 0.20, 0.60)  # dead end
MOUSE_COLOR   = (1.00, 0.20, 0.20)  # mouse dot
DONE_COLOR    = (1.00, 0.85, 0.10)  # solved



# walls of the maze

northWall = [[True] * COLS for _ in range(ROWS)]
eastWall  = [[True] * COLS for _ in range(ROWS)]

cell_state = [[None] * COLS for _ in range(ROWS)]  # None / 'visited' / 'dead'

solve_stack = []   # DFS stack for the mouse
solve_seen  = set()
solved      = False


# maze generation – stack-based DFS
def generate_maze():
    global solved, solve_stack, solve_seen

    if SEED is not None:
        random.seed(SEED)

    for r in range(ROWS):
        for c in range(COLS):
            northWall[r][c] = True
            eastWall[r][c]  = True
            cell_state[r][c] = None

    visited = [[False] * COLS for _ in range(ROWS)]
    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        r, c = stack[-1]
        neighbors = []
        if r > 0        and not visited[r-1][c]: neighbors.append(('N', r-1, c))
        if r < ROWS - 1 and not visited[r+1][c]: neighbors.append(('S', r+1, c))
        if c > 0        and not visited[r][c-1]: neighbors.append(('W', r, c-1))
        if c < COLS - 1 and not visited[r][c+1]: neighbors.append(('E', r, c+1))

        if neighbors:
            direction, nr, nc = random.choice(neighbors)
            carve_wall(r, c, direction, nr, nc)
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    # eat extra walls (~1 in 20) to create cycles that break shoulder-to-wall
    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.05:
                candidates = []
                if r > 0:        candidates.append(('N', r-1, c))
                if r < ROWS - 1: candidates.append(('S', r+1, c))
                if c > 0:        candidates.append(('W', r, c-1))
                if c < COLS - 1: candidates.append(('E', r, c+1))
                if candidates:
                    direction, nr, nc = random.choice(candidates)
                    carve_wall(r, c, direction, nr, nc)

    # reset solver
    solved = False
    solve_stack = [START]
    solve_seen  = {START}
    cell_state[START[0]][START[1]] = 'visited'


def carve_wall(r, c, direction, nr, nc):
    if direction == 'N':
        northWall[r][c]   = False
    elif direction == 'S':
        northWall[nr][nc] = False
    elif direction == 'W':
        eastWall[nr][nc]  = False
    elif direction == 'E':
        eastWall[r][c]    = False


# animated solver – one step per timer tick
def can_move(r, c, direction):
    if direction == 'N': return r > 0        and not northWall[r][c]
    if direction == 'S': return r < ROWS - 1 and not northWall[r+1][c]
    if direction == 'W': return c > 0        and not eastWall[r][c-1]
    if direction == 'E': return c < COLS - 1 and not eastWall[r][c]


def neighbor_of(r, c, direction):
    if direction == 'N': return r-1, c
    if direction == 'S': return r+1, c
    if direction == 'W': return r, c-1
    if direction == 'E': return r, c+1


def solver_step(value):
    global solved

    if solved or not solve_stack:
        return

    r, c = solve_stack[-1]

    if (r, c) == END:
        solved = True
        glutPostRedisplay()
        return

    # move to first unvisited neighbor
    moved = False
    for direction in ('N', 'S', 'W', 'E'):
        if can_move(r, c, direction):
            nr, nc = neighbor_of(r, c, direction)
            if (nr, nc) not in solve_seen:
                solve_seen.add((nr, nc))
                solve_stack.append((nr, nc))
                cell_state[nr][nc] = 'visited'
                moved = True
                break

    if not moved:
        # dead end – mark blue and backtrack
        cell_state[r][c] = 'dead'
        solve_stack.pop()

    glutPostRedisplay()
    glutTimerFunc(STEP_MS, solver_step, 0)


# rendering
def cell_bounds(r, c):
    cw = 1.0 / COLS
    ch = 1.0 / ROWS
    x0 = c * cw
    y0 = (ROWS - 1 - r) * ch
    return x0, y0, x0 + cw, y0 + ch


def fill_cell(r, c, color):
    x0, y0, x1, y1 = cell_bounds(r, c)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x0, y0); glVertex2f(x1, y0)
    glVertex2f(x1, y1); glVertex2f(x0, y1)
    glEnd()


def draw_circle(r, c, color, radius=0.35):
    x0, y0, x1, y1 = cell_bounds(r, c)
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    rx = (x1 - x0) * radius
    ry = (y1 - y0) * radius
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    steps = 20
    for i in range(steps + 1):
        angle = 2 * 3.14159 * i / steps
        import math
        glVertex2f(cx + rx * math.cos(angle), cy + ry * math.sin(angle))
    glEnd()


def draw_line(x0, y0, x1, y1):
    glBegin(GL_LINES)
    glVertex2f(x0, y0); glVertex2f(x1, y1)
    glEnd()


def draw_maze():
    glColor3f(*WALL_COLOR)
    glLineWidth(2.0)
    for r in range(ROWS):
        for c in range(COLS):
            x0, y0, x1, y1 = cell_bounds(r, c)
            if northWall[r][c]:
                draw_line(x0, y1, x1, y1)
            if eastWall[r][c]:
                draw_line(x1, y0, x1, y1)
    # outer border
    draw_line(0, 0, 1, 0); draw_line(0, 0, 0, 1)
    draw_line(0, 1, 1, 1); draw_line(1, 0, 1, 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # cell backgrounds
    for r in range(ROWS):
        for c in range(COLS):
            state = cell_state[r][c]
            if (r, c) == START:
                fill_cell(r, c, START_COLOR)
            elif (r, c) == END:
                fill_cell(r, c, END_COLOR)
            elif state == 'dead':
                fill_cell(r, c, DEAD_COLOR)
            elif state == 'visited':
                fill_cell(r, c, VISITED_COLOR)

    draw_maze()

    # mouse dot at current position
    if solve_stack:
        mr, mc = solve_stack[-1]
        if solved:
            draw_circle(mr, mc, DONE_COLOR)
        else:
            draw_circle(mr, mc, MOUSE_COLOR)

    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = w / h if h else 1.0
    if aspect >= 1.0:
        gluOrtho2D(-0.05 * aspect, 1.05 * aspect, -0.05, 1.05)
    else:
        gluOrtho2D(-0.05, 1.05, -0.05 / aspect, 1.05 / aspect)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard(key, x, y):
    if key in (b'\x1b', b'q', b'Q'):
        sys.exit(0)
    elif key in (b'r', b'R'):
        generate_maze()
        glutTimerFunc(STEP_MS, solver_step, 0)
        glutPostRedisplay()


# entry point
def main():
    generate_maze()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow(b"Maze Generator")

    glClearColor(*BG_COLOR, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    # start animation
    glutTimerFunc(STEP_MS, solver_step, 0)

    print("R = new maze | Q / ESC = quit")
    print(f"Start: {START}  |  End: {END}")
    glutMainLoop()


if __name__ == "__main__":
    main()