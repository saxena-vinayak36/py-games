import pygame
import logic as logic
import constants as const


class Button:
    def __init__(self, text, width, height, pos, color):
        # Core attributes
        self.pressed = False
        self.executed = False
        self.elevation = 4
        self.dynamic_elevation = self.elevation
        self.original_y_pos = pos[1]
        self.text = text
        self.pos = pos

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.TOP_COLOR = color
        self.top_color = color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = const.PURPLE

        # hitbox rectangle
        self.hitbox_rect = pygame.Rect(pos, (width, height))

        # text
        gui_font = pygame.font.SysFont("Arial", 20)
        self.text_surf = gui_font.render(self.text, True, const.PURPLE)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.hitbox_rect.y = self.original_y_pos - self.elevation

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=5)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=5)

        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.hitbox_rect.collidepoint(mouse_pos):
            self.top_color = const.WHITE
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.button_action()
                    self.pressed = False
        else:
            self.pressed = False
            self.dynamic_elevation = self.elevation
            self.top_color = self.TOP_COLOR

    def button_action(self):
        user_input_length = len(const.num_input)
        if user_input_length < 4:
            if const.num_input.find(self.text) == -1:
                const.num_input += self.text


class NumButton(Button):
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if len(const.num_input) <= 0:
            self.executed = False

        if self.executed:
            self.top_color = const.ORANGE
            self.dynamic_elevation = 0
        elif self.hitbox_rect.collidepoint(mouse_pos):
            self.top_color = const.WHITE
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    if len(const.num_input) < 4:
                        self.executed = True
                    else:
                        self.dynamic_elevation = self.elevation
                    self.button_action()
                    self.pressed = False
        else:
            self.pressed = False
            self.dynamic_elevation = self.elevation
            self.top_color = self.TOP_COLOR

    def button_action(self):
        user_input_length = len(const.num_input)
        if user_input_length < 4:
            if const.num_input.find(self.text) == -1:
                const.num_input += self.text


class ConfirmButton(Button):
    def button_action(self):
        self.executed = False

        if len(const.num_input) == 4:
            logic.compare()
            const.num_input = ""

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if len(const.num_input) < 4:
            self.dynamic_elevation = 0
            self.top_color = const.LIME
            self.executed = False
        else:
            if not self.executed:
                self.executed = True
            if self.hitbox_rect.collidepoint(mouse_pos):
                self.top_color = const.WHITE
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.dynamic_elevation = 0
                    self.pressed = True
                else:
                    self.dynamic_elevation = self.elevation
                    if self.pressed:
                        self.button_action()
                        self.pressed = False
            else:
                self.pressed = False
                self.dynamic_elevation = self.elevation
                self.top_color = self.TOP_COLOR


class ResetButton(Button):
    def button_action(self):
        const.num_input = ""


class RestartButton(Button):
    def button_action(self):
        logic.restart()
        const.game_state = 'main_game'
