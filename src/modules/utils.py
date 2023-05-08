# from modules.game_objects import Player, Item
import random
import os
import pygame
from pygame import Rect
from pygame import mixer


def detect_border(width: float, height: float, x: float, y: float) -> bool:
    if x >= 0 and x <= width and y >= 0 and y <= height:
        return True
    return False


def random_throw_item(pakeka_weight, salada_weight, level, bomb_flag):
    extra_life_weight = 0 if level <= 4 else 1 if level > 4 and level < 10 else 3
    speed_up_weight = 3 if level <= 3 else 5 if level > 3 and level < 10 else 7
    freeze_weight = 3 if level > 3 else 1
    bomb_weight = 1 if level <= 3 else 2 if level > 5 and level < 10 else 7
    if bomb_flag:
        salada_weight = 0
        extra_life_weight = 0
        speed_up_weight = 0
        freeze_weight = 0
        bomb_weight = 0

    item_name = random.choice(
        ["pakeka"] * pakeka_weight
        + ["salada"] * salada_weight
        + ["extra_life"] * extra_life_weight
        + ["speed_up"] * speed_up_weight
        + ["freeze"] * freeze_weight
        + ["bomb"] * bomb_weight
    )
    return item_name


def detect_collision(player_object: object, item_object: object) -> bool:
    player_rect = Rect(
        player_object.position.x - player_object.img_size / 4,
        player_object.position.y - player_object.img_size / 4,
        player_object.player.get_width() / 2.5,
        player_object.player.get_height() / 2.5,
    )
    item_rect = Rect(
        item_object.position.x,
        item_object.position.y,
        item_object.item.get_width(),
        item_object.item.get_height(),
    )

    return player_rect.colliderect(item_rect)


def draw_collision(img_size, name):
    image = pygame.image.load(f"../images/{name}.png")
    scale_factor = img_size / image.get_width()
    image = pygame.transform.scale_by(image, scale_factor)
    return image


def write_score(screen: object, font: object, score: str, level: int):
    score_text = font.render(f"Score: {score} | Level: {str(level)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def write_lifes(screen: object, font: object, lifes: list):
    heart_image = pygame.image.load("../images/extra_life.png")
    scale_factor = 36 / heart_image.get_width()
    heart_image = pygame.transform.scale_by(heart_image, scale_factor)
    heart_image_rect = heart_image.get_rect()

    for i in range(len(lifes)):
        heart_image_rect.right = screen.get_width() - i * heart_image.get_width()
        screen.blit(heart_image, heart_image_rect)
    lifes_text = font.render("Lifes: ", True, (255, 255, 255))
    lifes_text_rect = lifes_text.get_rect()
    lifes_text_rect.right = screen.get_width() - len(lifes) * heart_image.get_width()
    screen.blit(lifes_text, lifes_text_rect)


def get_level(level: int, reset=False) -> dict:
    level = level - 1

    initial_pitoco_speed = 900
    initial_item_frequency = 100
    initial_items_speed = 150
    initial_score_goal = 10
    initial_pakeka_weight = 80
    initial_salada_weight = 20

    if reset:
        return (
            initial_pitoco_speed,
            initial_item_frequency,
            initial_items_speed,
            initial_score_goal,
            initial_pakeka_weight,
            initial_salada_weight,
        )

    min_pitoco_speed = 400
    min_item_frequency = 5 if level >= 20 else 15
    max_items_speed = 1000
    min_pakeka_weight = 20

    pitoco_speed = max(initial_pitoco_speed - level * 50, min_pitoco_speed)
    item_frequency = max(initial_item_frequency - level * 10, min_item_frequency)
    items_speed = (
        initial_items_speed + level * 50 if initial_items_speed + level * 50 < max_items_speed else max_items_speed
    )
    score_goal = initial_score_goal + level * 8
    pakeka_weight = max(int(initial_pakeka_weight - level * 8), min_pakeka_weight)
    salada_weight = int(100 - pakeka_weight)

    return pitoco_speed, item_frequency, items_speed, score_goal, pakeka_weight, salada_weight


def play_music(audio_file=None):
    mixer.init()
    dir = "../audios"
    if not audio_file:
        audio_file = random.choice(os.listdir(dir))
    filename = os.path.join(dir, audio_file)
    mixer.music.load(filename)
    mixer.music.play()
