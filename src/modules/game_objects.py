from random import randrange
import pygame
from pygame import Rect
from pygame.surface import Surface
from modules.utils import detect_border


class Player:
    def __init__(self, screen: Surface, position: pygame.Vector2, img_size: float, name: str):
        self.img_size = img_size
        self.name = name
        self.screen = screen
        image = pygame.image.load(f"../images/{name}.png")
        scale_factor = img_size / image.get_width()
        self.player = pygame.transform.scale_by(image, scale_factor)
        self.position = position

    def draw(self):
        pos_x = self.position.x - self.img_size / 2
        pos_y = self.position.y - self.img_size / 2
        self.screen.blit(self.player, (pos_x, pos_y))

    def move(self, speed: float, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and detect_border(
            self.screen.get_width(), self.screen.get_height(), self.position.x, self.position.y - speed * dt
        ):
            self.position.y -= speed * dt
        if keys[pygame.K_DOWN] and detect_border(
            self.screen.get_width(), self.screen.get_height(), self.position.x, self.position.y + speed * dt
        ):
            self.position.y += speed * dt
        if keys[pygame.K_LEFT] and detect_border(
            self.screen.get_width(), self.screen.get_height(), self.position.x - speed * dt, self.position.y
        ):
            self.position.x -= speed * dt
        if keys[pygame.K_RIGHT] and detect_border(
            self.screen.get_width(), self.screen.get_height(), self.position.x + speed * dt, self.position.y
        ):
            self.position.x += speed * dt


class Item:
    def __init__(self, screen: Surface, img_size: float, name: str):
        self.img_size = img_size
        self.screen = screen
        self.name = name
        image = pygame.image.load(f"../images/{name}.png")
        scale_factor = img_size / image.get_width()
        self.item = pygame.transform.scale_by(image, scale_factor)
        self.position = pygame.Vector2(randrange(screen.get_width() - img_size // 2), 0)
        self.removed = False

    def draw(self):
        if not self.removed:
            self.screen.blit(self.item, self.position)

    def move(self, speed: float, dt: float):
        self.position.y += speed * dt


def detect_collision(player_object: Player, item_object: Item) -> bool:
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
