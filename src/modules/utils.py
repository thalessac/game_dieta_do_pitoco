import random
import os
import pygame
from pygame import Rect
from pygame import mixer


def detect_border(width: float, height: float, x: float, y: float) -> bool:
    if x >= 0 and x <= width and y >= 0 and y <= height:
        return True
    return False


def random_throw_item(pakeka_weight: int, salada_weight: int, level: int, bomb_flag: bool, freeze_flag: bool) -> str:
    if level <= 5:
        extra_life_weight = 0
        speed_up_weight = 1
        freeze_weight = 0
        bomb_weight = 1
    elif level > 5 and level <= 10:
        extra_life_weight = 1
        speed_up_weight = 3
        freeze_weight = 1
        bomb_weight = 2
    elif level > 10 and level <= 20:
        extra_life_weight = 3
        speed_up_weight = 5
        freeze_weight = 3
        bomb_weight = 3
    elif level > 20 and level <= 30:
        extra_life_weight = 5
        speed_up_weight = 7
        freeze_weight = 5
        bomb_weight = 3
    elif level > 30 and level <= 50:
        extra_life_weight = 5
        speed_up_weight = 10
        freeze_weight = 7
        bomb_weight = 5
    elif level > 50 and level <= 100:
        extra_life_weight = 3
        speed_up_weight = 5
        freeze_weight = 3
        bomb_weight = 2
    elif level > 100:
        extra_life_weight = 2
        speed_up_weight = 2
        freeze_weight = 2
        bomb_weight = 2
    if bomb_flag:
        salada_weight = 0
        extra_life_weight = 1 if level >= 10 else 0
        speed_up_weight = 1
        freeze_weight = 1
        bomb_weight = 0
    if freeze_flag:
        freeze_weight = 0
        extra_life_weight = 1 if level >= 15 else 0
        speed_up_weight = 1 if level >= 15 else 0
    if freeze_flag and bomb_flag:
        speed_up_weight = 0

    item_list = (
        ["pakeka"] * pakeka_weight
        + ["salada"] * salada_weight
        + ["extra_life"] * extra_life_weight
        + ["speed_up"] * speed_up_weight
        + ["freeze"] * freeze_weight
        + ["bomb"] * bomb_weight
    )
    random.shuffle(item_list)
    item_name = random.choice(item_list)
    return item_name


def play_collision_sound_effect(item_name: str) -> None:
    if item_name == "pakeka":
        audio_file = random.choice(["pakeka-success.wav", "eating_1.wav", "eating_2.wav", "eating_3.wav"])
        sound = mixer.Sound(f"../audios/sound_effect/{audio_file}")
    elif item_name == "salada":
        sound = mixer.Sound("../audios/sound_effect/duvido.wav")
    else:
        sound = mixer.Sound("../audios/sound_effect/power_up.wav")
    mixer.find_channel().play(sound)


def draw_collision(img_size: float, name: str):
    image = pygame.image.load(f"../images/{name}.png")
    scale_factor = img_size / image.get_width()
    image = pygame.transform.scale_by(image, scale_factor)
    return image


def draw_mute_button(screen: pygame.surface.Surface, img_size: float, muted: bool):
    if muted:
        image = pygame.image.load("../images/muted-icon.png")
    else:
        image = pygame.image.load("../images/unmuted-icon.png")
    scale_factor = img_size / image.get_width()
    position = pygame.Vector2(screen.get_width() / 2, 0)
    image = pygame.transform.scale_by(image, scale_factor)
    screen.blit(image, position)
    return image, position


def get_mute_state(event: pygame.event, button: pygame.image, position: pygame.Vector2, muted: bool) -> bool:
    if event.button == 1:
        x, y = event.pos
        buttom_rect = Rect(
            position.x,
            position.y,
            button.get_width(),
            button.get_height(),
        )
        if buttom_rect.collidepoint(x, y):
            pygame.time.wait(100)
            return not muted


def write_score(screen: pygame.surface.Surface, font: pygame.font.Font, score: int, level: int) -> None:
    score_text = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def write_lifes(screen: pygame.surface.Surface, font: pygame.font.Font, lifes: list) -> None:
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


def get_level(level: int, reset: bool = False) -> dict:
    level = level - 1
    score_increment = 6

    initial_pitoco_speed = 1000
    initial_item_frequency = 150
    initial_items_speed = 200
    initial_score_goal = score_increment
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
    min_item_frequency = 15
    max_items_speed = 1000
    min_pakeka_weight = 20

    pitoco_speed = max(initial_pitoco_speed - level * 50, min_pitoco_speed)
    if level <= 20:
        item_frequency = max(initial_item_frequency - level * 15, min_item_frequency)
    else:
        min_item_frequency = 5
        max_items_speed = 1200
        initial_item_frequency = 15
        item_frequency = max(initial_item_frequency - (level - 20) * 1, min_item_frequency)
    items_speed = (
        initial_items_speed + level * 50 if initial_items_speed + level * 50 < max_items_speed else max_items_speed
    )
    score_goal = initial_score_goal + level * score_increment
    pakeka_weight = max(int(initial_pakeka_weight - level * 8), min_pakeka_weight)
    salada_weight = int(100 - pakeka_weight)

    return pitoco_speed, item_frequency, items_speed, score_goal, pakeka_weight, salada_weight


def play_music(audio_file: str = None, previous_song: str = None) -> str:
    mixer.init()
    dir = "../audios"
    audios_list = os.listdir(dir)
    audios_list = [audio for audio in audios_list if audio.endswith(".wav")]
    if not audio_file:
        audio_file = random.choice(audios_list)
        if previous_song:
            while audio_file == previous_song:
                audio_file = random.choice(audios_list)
    filename = os.path.join(dir, audio_file)
    mixer.music.load(filename)
    mixer.music.play()
    return audio_file
