# Example file showing a circle moving on screen
import pygame
from modules.game_objects import Player, Item
from modules.utils import detect_collision
from modules.utils import (
    write_score,
    get_level,
    draw_collision,
    write_lifes,
    random_throw_item,
    play_music,
)

from modules.menu import Menu

WIDTH, HEIGHT = 1280, 720
MAX_LIFES = 10

# pygame setup
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

running = True
dt = 0
time_on_level = 0
power_up_duration = 15  # seconds

cron_speed_up = 0
speed_up_flag = False

cron_freeze = 0
freeze_flag = False

cron_bomb = 0
bomb_flag = False

items = []
collision_draws = []
counter = 0
score = 0
level = {1}
lifes = [1, 1, 1]

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
pitoco = Player(screen=screen, position=player_pos, img_size=150, name="pitoco")

background = pygame.image.load("../images/background_2.png")

play_music(audio_file="a-paritr-de-amanhã-dieta.wav")

game_state = "start_menu"
menu = Menu(screen=screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_state == "start_menu":
        menu.draw_start_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "game"
            game_over = False

    if game_state == "game_over":
        menu.draw_game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state = "start_menu"
            score = 0
            level = {1}
            pitoco_speed, item_frequency, items_speed, score_goal, pakeka_weight, salada_weight = get_level(
                1, reset=True
            )
            lifes = [1, 1, 1]
        if keys[pygame.K_q]:
            running = False

    if game_state == "game":
        screen.blit(background, (0, 0))

        if not pygame.mixer.music.get_busy():
            play_music()

        pitoco_speed, item_frequency, items_speed, score_goal, pakeka_weight, salada_weight = get_level(max(level))

        if speed_up_flag:
            pitoco_speed = max(pitoco_speed * 1.5, items_speed)
            cron_speed_up += dt
            if cron_speed_up >= power_up_duration:
                speed_up_flag = False

        if freeze_flag:
            items_speed /= 2
            cron_freeze += dt
            if cron_freeze >= power_up_duration:
                freeze_flag = False

        if bomb_flag:
            cron_bomb += dt
            if cron_bomb >= power_up_duration:
                bomb_flag = False

        pitoco.draw()
        pitoco.move(speed=pitoco_speed, dt=dt)

        if not counter % item_frequency:
            item_name = random_throw_item(
                pakeka_weight=pakeka_weight, salada_weight=salada_weight, level=max(level), bomb_flag=bomb_flag
            )
            items.append(Item(screen=screen, img_size=75, name=item_name))

        for item in items:
            if bomb_flag and item_name == "salada":
                item.removed = True
                items.remove(item)
            item.draw()
            item.move(speed=items_speed, dt=dt)
            if detect_collision(player_object=pitoco, item_object=item):
                item.removed = True
                items.remove(item)
                if item.name == "pakeka":
                    collision_draws.append(
                        {
                            "image": draw_collision(img_size=90, name="success"),
                            "position": pitoco.position,
                            "elapsed_time": 0,
                        }
                    )
                    score += 1
                elif item.name == "salada":
                    collision_draws.append(
                        {
                            "image": draw_collision(img_size=90, name="fail"),
                            "position": pitoco.position,
                            "elapsed_time": 0,
                        }
                    )
                    if len(lifes):
                        lifes.pop(0)
                    else:
                        game_state = "game_over"
                elif item.name == "extra_life":
                    if len(lifes) < MAX_LIFES:
                        lifes = [1] * (len(lifes) + 1)
                elif item.name == "speed_up":
                    cron_speed_up = 0
                    speed_up_flag = True
                elif item.name == "freeze":
                    cron_freeze = 0
                    freeze_flag = True
                elif item.name == "bomb":
                    cron_bomb = 0
                    bomb_flag = True

        for collision in collision_draws:
            collision["elapsed_time"] += dt
            if collision["elapsed_time"] <= 1.5:
                screen.blit(collision.get("image"), collision.get("position"))

        write_score(screen, font, score, max(level))
        write_lifes(screen, font, lifes)

        if score == score_goal or time_on_level >= 60:
            level.add(max(level) + 1)
            time_on_level = 0

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        counter += 1
        time_on_level += dt

pygame.quit()
