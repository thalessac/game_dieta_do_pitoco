import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen

    def draw_start_menu(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 40)
        title = font.render("Dieta do Pitoco", True, (255, 255, 255))
        start_button = font.render("Start", True, (255, 255, 255))
        self.screen.blit(
            title,
            (
                self.screen.get_width() / 2 - title.get_width() / 2,
                self.screen.get_height() / 2 - title.get_height() / 2,
            ),
        )
        self.screen.blit(
            start_button,
            (
                self.screen.get_width() / 2 - start_button.get_width() / 2,
                self.screen.get_height() / 2 + start_button.get_height() / 2,
            ),
        )
        pygame.display.update()

    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 40)
        title = font.render(
            "Salada? DÚVIDO! Você comeu salada e perdeu o jogo, tente novamente...CADEIA!", True, (255, 255, 255)
        )
        restart_button = font.render("R - Restart", True, (255, 255, 255))
        quit_button = font.render("Q - Quit", True, (255, 255, 255))
        self.screen.blit(
            title,
            (
                self.screen.get_width() / 2 - title.get_width() / 2,
                self.screen.get_height() / 2 - title.get_height() / 3,
            ),
        )
        self.screen.blit(
            restart_button,
            (
                self.screen.get_width() / 2 - restart_button.get_width() / 2,
                self.screen.get_height() / 1.9 + restart_button.get_height(),
            ),
        )
        self.screen.blit(
            quit_button,
            (
                self.screen.get_width() / 2 - quit_button.get_width() / 2,
                self.screen.get_height() / 2 + quit_button.get_height() / 2,
            ),
        )
        pygame.display.update()
