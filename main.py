import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1080//2, 1420/2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

CHAR_SIZE = 90
SIZE = (CHAR_SIZE, CHAR_SIZE)
SPEED = 9
FPS = 60
SPEED_OF_RECTANGLE = 8

FONT = pygame.font.Font('spacemono.ttf', 60)
FONT_SMALLER = pygame.font.Font('spacemono.ttf', 30)

CHARACTER = pygame.image.load('character.png')
CHARACTER = pygame.transform.scale(CHARACTER, SIZE)

def handle_movement(char, key_pressed, FAILED):
    if (key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]) and char.x > 0 and FAILED == False:
        char.x -= SPEED
    if (key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]) and char.x < WIDTH - char.width and FAILED == False:
        char.x += SPEED

def draw_window():
    SCREEN.fill((75, 100, 200))

def draw_char(char):
    SCREEN.blit(CHARACTER, (char.x, char.y))

def draw_txt(level, FAILED):
    if FAILED == False:
        game_name = FONT.render("BlockRain", True, (255, 255, 255))
        game_name_rect = game_name.get_rect(center = (WIDTH//2, HEIGHT//2))
        SCREEN.blit(game_name, game_name_rect)
    else:
        failed = FONT.render("You Lost\nPress R\nTo Restart", True, (255, 0,0))
        failed_rect = failed.get_rect(center = (WIDTH//2, HEIGHT//2))
        SCREEN.blit(failed, failed_rect)

    level_txt = FONT_SMALLER.render(f"Level {level}", True, (255,255, 255))
    level_txt_name = level_txt.get_rect(topleft = (20, 50))
    SCREEN.blit(level_txt, level_txt_name)

def handle_rectangles(rectangles, FAILED):
    for rectangle in rectangles:
        if rectangle.y < 1000 and FAILED == False:
            rectangle.y += SPEED_OF_RECTANGLE
        if rectangle.y >= 1000 and FAILED == False:
            rectangles.remove(rectangle)
        if FAILED == True:
            rectangles.remove(rectangle)

def draw_rectangles(rectangles):
    for rectangle in rectangles:
        block = pygame.draw.rect(SCREEN, (255, 255, 255), (rectangle.x, rectangle.y, 10, 50))

def respawn_tick_fn(frame_count, FPS):
    time = frame_count/FPS
    if time == 0.0:
        return FPS, 1
    if time >= 8.0 and time < 23.0:
        return FPS - 15, 2
    if time >= 23.0 and time < 43.0:
        return FPS - 25, 3
    if time >= 43.0 and time < 60.0:
        return FPS - 38, 4
    if time >= 60.0 and time < 80.0:
        return FPS - 45, 5
    if time >= 80.0:
        return FPS - 50, 6
    else:
        return FPS, 1

def handle_restart(key_pressed, char, FAILED):
    if key_pressed[pygame.K_r] and FAILED == True:
        char.x = WIDTH/2 - 75
        return False
    return True

def main():
    running = True
    char = pygame.Rect(WIDTH/2 - CHAR_SIZE/2, HEIGHT - CHAR_SIZE, CHAR_SIZE, CHAR_SIZE)
    clock = pygame.time.Clock()
    frame_count = 0
    rectangles = []
    factor = 90
    FAILED = False
    while running:
        clock.tick(FPS)
        respawn_tick, level = respawn_tick_fn(frame_count, FPS)
        frame_count +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_count % respawn_tick == 0:
            random_base = random.randint(0, WIDTH - 75)
            rectangle = pygame.Rect(random_base, -50, 10, 50)
            rectangles.append(rectangle)

        for rectangle in rectangles:
            if char.colliderect(rectangle):
                FAILED = True
                print(FAILED)

        key_pressed = pygame.key.get_pressed()
        draw_window()
        draw_txt(level, FAILED) 
        handle_rectangles(rectangles, FAILED)
        draw_rectangles(rectangles)
        draw_char(char)
        handle_movement(char, key_pressed, FAILED)
        if FAILED == True:
            FAILED = handle_restart(key_pressed, char, FAILED)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
