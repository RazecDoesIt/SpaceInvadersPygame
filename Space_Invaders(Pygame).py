# SPACE INVANDERS BY RAZECDOESIT
import random
import pygame
import os

# pygame window setting
pygame.init()
WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")
BORDER = pygame.Rect(WIDTH // 2, 0, 10, HEIGHT)

# pygame sound engine
# pygame.mixer.init()

# pygame load sound assets

# BULLET_FIRE_SOUND = pygame.mixer.Sound
# BULLET_HIT_SOUND = pygame.mixer.Sound


# game caracteristics
FPS = 60
VEL = 5
ENEMY_VEL = 1
BULLET_VEL = 8
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
HEALTH_FONT = pygame.font.SysFont('arial', 30)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# player spaceship loading assets and transforming into correct size
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'pixel_ship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,
                                                                                           SPACESHIP_HEIGHT)), 0)

# enemy loading assets and transforming into correct size

RED_ENEMY_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'pixel_ship_red_small.png'))
RED_ENEMY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_ENEMY_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,
                                                                                                 SPACESHIP_HEIGHT)), 0)

# GREEN_ENEMY_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'pixel_ship_green_small.png'))
# GREEN_ENEMY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_ENEMY_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,
#                                                                                                 SPACESHIP_HEIGHT)), 0)

# BLUE_ENEMY_SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'pixel_ship_blue_small.png'))
# BLUE_ENEMY_SPACE = pygame.transform.rotate(pygame.transform.scale(BLUE_ENEMY_SPACE_IMAGE, (SPACESHIP_WIDTH,
#                                                                                           SPACESHIP_HEIGHT)), 180)

# shot from player

# BLUE_PLAYER_SHOT_IMAGE = pygame.image.load(os.path.join('Assets', 'pixel_laser_blue.png'))
# BLUE_PLAYER_SHOT = pygame.transform.scale(BLUE_PLAYER_SHOT_IMAGE, (10, 10))

# space load assets
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))

# define event of hit
PLAYER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2


def draw_win(yellow, enemy, yellow_shot_bullets, player_health, enemy_health, score, enemy_shot):
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(SPACE, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_ENEMY_SPACESHIP, (enemy.x, enemy.y))

    player_health_text = HEALTH_FONT.render('Health:' + str(player_health), True, WHITE)
    WIN.blit(player_health_text, (10, 10))
    enemy_health_text = HEALTH_FONT.render('Health:' + str(enemy_health), True, WHITE)
    WIN.blit(enemy_health_text, (WIDTH - 150, HEIGHT - 50))
    score_text = HEALTH_FONT.render('Score:' + str(score), True, WHITE)
    WIN.blit(score_text, (50, HEIGHT - 50))

    for shot in yellow_shot_bullets:
        pygame.draw.rect(WIN, YELLOW, shot)

    for shot in enemy_shot:
        pygame.draw.rect(WIN, RED, shot)
    pygame.display.update()


def handle_player_mov(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x <= WIDTH - SPACESHIP_WIDTH:
        yellow.x += VEL


def handle_enemy(enemy):
    enemy.y += ENEMY_VEL
    pygame.Rect.move(enemy, enemy.x, enemy.y)


def shots(yellow_shot, enemy, enemy_shot, yellow):
    for shot in yellow_shot:
        shot.y -= BULLET_VEL
        if enemy.colliderect(shot):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            yellow_shot.remove(shot)
        elif shot.y > HEIGHT:
            yellow_shot.remove(shot)

    for shot in enemy_shot:
        shot.y += BULLET_VEL
        if yellow.colliderect(shot):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            enemy_shot.remove(shot)
        elif shot.y > HEIGHT:
            enemy_shot.remove(shot)


def draw_win_lose(text):
    draw_text = HEALTH_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() / 2, HEIGHT /2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    run = True
    clock = pygame.time.Clock()
    yellow = pygame.Rect(WIDTH // 2 - SPACESHIP_WIDTH // 2, HEIGHT - 2 * SPACESHIP_HEIGHT, SPACESHIP_WIDTH,
                         SPACESHIP_HEIGHT)
    enemy = pygame.Rect(225, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # list index of shots
    yellow_shot = []
    enemy_shot = []

    # healths? duh
    player_health = 10
    enemy_health = 3
    # counts it based on new enemy loop
    score = 0
    # generate new enemy once the first one is dead
    new_enemy = 0

    while run:
        clock.tick(FPS)
        draw_win(yellow, enemy, yellow_shot, player_health, enemy_health, score, enemy_shot)
        # enemy shot generator
        enemy_prob_shot = random.randrange(1, 21)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot = pygame.Rect(yellow.x + SPACESHIP_WIDTH // 2 - 5, yellow.y + SPACESHIP_HEIGHT // 2 - 25, 10,
                                       10)
                    yellow_shot.append(shot)
            if event.type == ENEMY_HIT:
                enemy_health -= 1
            if event.type == PLAYER_HIT:
                player_health -= 1
            # new enemy structure
            if enemy_health <= 0:
                enemy.x = 0
                new_enemy += 1
            if new_enemy == 1:
                enemy.x += random.randrange(100, 800)
                enemy.y = 0
                enemy = WIN.blit(RED_ENEMY_SPACESHIP, (enemy.x, enemy.y))
                enemy_health = 3
                new_enemy -= 1
                score += 1
            if enemy.y > HEIGHT:
                score -= 1
                enemy.x += random.randrange(100, 800)
                enemy.y = 0
                enemy = WIN.blit(RED_ENEMY_SPACESHIP, (enemy.x, enemy.y))
            # get harder as score increases
            if score:
                if score >= 20:
                    enemy_prob_shot = random.randrange(1, 11)
                if score >= 30:
                    enemy_prob_shot = random.randrange(1, 6)

            # handle enemy shots
            if enemy_prob_shot == 1:
                shot = pygame.Rect(enemy.x + SPACESHIP_WIDTH // 2 - 5, enemy.y + SPACESHIP_HEIGHT // 2 - 25, 10,
                                   10)
                enemy_shot.append(shot)

            # winner / lose
            text = ""
            if score >= 50:
                text = "You WIN!"
                draw_win_lose(text)
            if player_health <= 0:
                text = "You lost!"
                draw_win_lose(text)
                break

        keys_pressed = pygame.key.get_pressed()
        handle_player_mov(keys_pressed, yellow)
        shots(yellow_shot, enemy, enemy_shot, yellow)
        handle_enemy(enemy)


main()

