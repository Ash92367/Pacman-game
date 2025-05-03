
import pygame
import sys
from heapq import heappop, heappush

CELL_SIZE = 20
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 3, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
WIDTH = len(maze[0]) * CELL_SIZE
HEIGHT = len(maze) * CELL_SIZE

BLACK = (0, 0, 0)
WALL = "blue"
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FOOD_COLOR = "pink"
BIG_FOOD_COLOR = "purple"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man AI")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

pacman_pos = (1, 1)
ghost_pos = (9, 6)
score = 0

food_positions = {(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 0}
big_food_positions = {(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3}
ghost_img = pygame.image.load("ghostt.jpg")
ghost_img = pygame.transform.scale(ghost_img, (CELL_SIZE, CELL_SIZE))
pacman_img = pygame.image.load("pacman.jpg")
pacman_img = pygame.transform.scale(pacman_img, (CELL_SIZE, CELL_SIZE))

def is_valid_move(pos):
    return 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(maze[0]) and maze[pos[0]][pos[1]] != 1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(ghost_pos, pacman_pos):
    open_list = []
    heappush(open_list, (heuristic(ghost_pos, pacman_pos), ghost_pos))
    
    g_score = {ghost_pos: 0}
    came_from = {}
    
    while open_list:
        current_f_score, current = heappop(open_list)
        
        if current == pacman_pos:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if is_valid_move(neighbor):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, pacman_pos)
                    heappush(open_list, (f_score, neighbor))
    
    return []

def ghost_movement(ghost_pos, pacman_pos):
    path = a_star(ghost_pos, pacman_pos)
    print("Heuristic Path:", path)

    if path:
        if len(path) > 0 and path[0] == pacman_pos:
            return pacman_pos

        steps_to_take = min(len(path), ghost_speed)
        for _ in range(steps_to_take):
            ghost_pos = path.pop(0)

    return ghost_pos

def check_collision(pacman_pos, ghost_pos):
    return pacman_pos == ghost_pos

def display_game_over():
    font = pygame.font.SysFont("Times New Roman", 24, bold=True)
    game_over_text = font.render("Game Over! The Ghost ate Pac-Man!", True, "red")
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)

running = True
ghost_move_counter = 0
ghost_speed = 3

while running:
    screen.fill(BLACK)
    
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, WALL, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (row, col) in food_positions:
                pygame.draw.circle(screen, FOOD_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 4)
            elif (row, col) in big_food_positions:
                pygame.draw.circle(screen, BIG_FOOD_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 6)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_pos = list(pacman_pos)
    if keys[pygame.K_UP]:
        new_pos[0] -= 1
    if keys[pygame.K_DOWN]:
        new_pos[0] += 1
    if keys[pygame.K_LEFT]:
        new_pos[1] -= 1
    if keys[pygame.K_RIGHT]:
        new_pos[1] += 1
    
    if is_valid_move(tuple(new_pos)):
        pacman_pos = tuple(new_pos)

    if pacman_pos in food_positions:
        food_positions.remove(pacman_pos)
        score += 1
    if pacman_pos in big_food_positions:
        big_food_positions.remove(pacman_pos)
        score += 5
    
    ghost_move_counter += 1
    if ghost_move_counter >= ghost_speed:
        ghost_pos = ghost_movement(ghost_pos, pacman_pos)
        ghost_move_counter = 0
    
    if check_collision(pacman_pos, ghost_pos):
        display_game_over()  
        pygame.display.update()
        pygame.time.delay(10000)  
        running = False 
    
    screen.blit(pacman_img, (pacman_pos[1] * CELL_SIZE, pacman_pos[0] * CELL_SIZE))
    screen.blit(ghost_img, (ghost_pos[1] * CELL_SIZE, ghost_pos[0] * CELL_SIZE))
    
    score_text = font.render(f"Score: {score}", True, "red")
    screen.blit(score_text, (5, -4))

    pygame.display.update()
    
    clock.tick(10)

pygame.quit()
sys.exit()
