import sys
import random

try:
    from OpenGL.GL   import *
    from OpenGL.GLUT import *
    from OpenGL.GLU  import *
except ImportError:
    sys.exit("Install PyOpenGL first:  pip install PyOpenGL PyOpenGL_accelerate")

# Grid size
ROWS = 15
COLS = 20
SEED = None   # set an integer for a reproducible maze

# Window size
WINDOW_W = 800
WINDOW_H = 600

# Colors (RGB)
WALL_COLOR  = (0.1, 0.4, 0.9)
BG_COLOR    = (0.05, 0.05, 0.1)
START_COLOR = (0.1, 0.9, 0.3)
END_COLOR   = (0.9, 0.2, 0.2)

# --- Wall arrays ---
# northWall[r][c] = True means the top edge of that cell is a wall
# eastWall[r][c]  = True means the right edge of that cell is a wall
# The south wall of (r,c) is northWall[r+1][c]
# The west  wall of (r,c) is eastWall[r][c-1]
northWall = [[True] * COLS for _ in range(ROWS)]
eastWall  = [[True] * COLS for _ in range(ROWS)]
visited   = [[False] * COLS for _ in range(ROWS)]


def generate_maze(start_row=0, start_col=0):
    if SEED is not None:
        random.seed(SEED)

    for r in range(ROWS):
        for c in range(COLS):
            northWall[r][c] = True
            eastWall[r][c]  = True
            visited[r][c]   = False

    stack = [(start_row, start_col)]
    visited[start_row][start_col] = True

    while stack:
        r, c = stack[-1]

        neighbors = []
        if r > 0        and not visited[r - 1][c]: neighbors.append(('N', r - 1, c))
        if r < ROWS - 1 and not visited[r + 1][c]: neighbors.append(('S', r + 1, c))
        if c > 0        and not visited[r][c - 1]: neighbors.append(('W', r, c - 1))
        if c < COLS - 1 and not visited[r][c + 1]: neighbors.append(('E', r, c + 1))

        if neighbors:
            direction, nr, nc = random.choice(neighbors)

            # Remove the shared wall between current cell and the chosen neighbor
            if direction == 'N':
                northWall[r][c]   = False
            elif direction == 'S':
                northWall[nr][nc] = False
            elif direction == 'W':
                eastWall[nr][nc]  = False
            elif direction == 'E':
                eastWall[r][c]    = False

            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()


def cell_bounds(r, c):
    cw = 1.0 / COLS
    ch = 1.0 / ROWS
    x0 = c * cw
    y0 = (ROWS - 1 - r) * ch
    return x0, y0, x0 + cw, y0 + ch


def draw_filled_cell(r, c, color):
    x0, y0, x1, y1 = cell_bounds(r, c)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x0, y0)
    glVertex2f(x1, y0)
    glVertex2f(x1, y1)
    glVertex2f(x0, y1)
    glEnd()


def draw_line(x0, y0, x1, y1):
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
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

    # Outer border
    draw_line(0.0, 0.0, 1.0, 0.0)
    draw_line(0.0, 0.0, 0.0, 1.0)
    draw_line(0.0, 1.0, 1.0, 1.0)
    draw_line(1.0, 0.0, 1.0, 1.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_filled_cell(0, 0, START_COLOR)
    draw_filled_cell(ROWS - 1, COLS - 1, END_COLOR)
    draw_maze()
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
        glutPostRedisplay()


def main():
    generate_maze()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow(b"Maze Generator")   # must be ASCII only

    glClearColor(*BG_COLOR, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    print("R = new maze | Q / ESC = quit")
    glutMainLoop()


if __name__ == "__main__":
    main()