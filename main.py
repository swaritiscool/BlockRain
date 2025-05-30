import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1080//2, 1420/2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

SIZE = (120, 120)
SPEED = 7
FPS = 60
SPEED_OF_RECTANGLE = 3

FONT = pygame.font.Font('spacemono.ttf', 60)
FONT_SMALLER = pygame.font.Font('spacemono.ttf', 30)

CHARACTER = pygame.image.load('character.png')
CHARACTER = pygame.transform.scale(CHARACTER, SIZE)

def handle_movement(char, key_pressed):
    if key_pressed[pygame.K_a] and char.x > 0:
        char.x -= SPEED
    if key_pressed[pygame.K_d] and char.x < WIDTH - char.width:
        char.x += SPEED

def draw_window():
    SCREEN.fill((75, 100, 200))

def draw_char(char):
    SCREEN.blit(CHARACTER, (char.x, char.y))

def draw_txt(level):
    game_name = FONT.render("BlockRain", True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center = (WIDTH//2, HEIGHT//2))
    SCREEN.blit(game_name, game_name_rect)

    level_txt = FONT_SMALLER.render(f"Level {level}", True, (255,255, 255))
    level_txt_name = level_txt.get_rect(topleft = (20, 50))
    SCREEN.blit(level_txt, level_txt_name)

def handle_rectangles(rectangles):
    for rectangle in rectangles:
        if rectangle.y < 1000:
            rectangle.y += SPEED_OF_RECTANGLE
        if rectangle.y >= 1000:
            rectangles.remove(rectangle)

def draw_rectangles(rectangles):
    for rectangle in rectangles:
        block = pygame.draw.rect(SCREEN, (255, 255, 255), (rectangle.x, rectangle.y, 10, 50))

def respawn_tick_fn(frame_count, FPS):
    time = frame_count/FPS
    
    if time == 0.0:
        return FPS, 1
    if time >= 8.0 and time < 23.0:
        return FPS - 10, 2
    if time >= 23.0 and time < 43.0:
        return FPS - 15, 3
    if time >= 43.0:
        return FPS - 20, 4
    else:
        return FPS, 1

def main():
    running = True
    char = pygame.Rect(WIDTH/2 - 75, HEIGHT - 150, 150, 100)
    clock = pygame.time.Clock()
    frame_count = 0
    rectangles = []
    random_base = random.randint(0, WIDTH - 75)
    factor = 90
    while running:
        clock.tick(FPS)
        respawn_tick, level = respawn_tick_fn(frame_count, FPS)
        frame_count +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_count % 60 == 0:
            selector = random.randint(0, 101)
            if selector % 2 == 0:
                rectangle = pygame.Rect(random_base+factor, -50, 10, 50)
                random_base += factor
                if random_base >= WIDTH - 75:
                    random_base = random.randint(0, WIDTH - 75)
            else:
                rectangle = pygame.Rect(random_base-factor, -50, 10, 50)
                random_base -= factor
                if random_base <= 0:
                    random_base = random.randint(0, WIDTH - 75)

            rectangles.append(rectangle)

        key_pressed = pygame.key.get_pressed()
        draw_window()
        draw_txt(level)
        handle_rectangles(rectangles)
        draw_rectangles(rectangles)
        draw_char(char)
        handle_movement(char, key_pressed)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
