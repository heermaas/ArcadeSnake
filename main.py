from game_objects import *
from background_music import *

import re
import time
import threading
import pyglet.input

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
SNAKE_SIZE = BLOCK_SIZE
ITEM_TO_EAT_SIZE = BLOCK_SIZE
SNAKE_LENGTH = 3
SCOREBOARD_HEIGHT = BLOCK_SIZE * 2
GAME_TITLE = "Snake Game"
CAPTION = "Navigiere, Wachse, Überlebe!"
SUB_HEADING = "Ein Projekt von Abdelrhman Hassan, Adrian Birlin, Christian Ambs & Manuel Heer"


class StartView(arcade.View):
    def __init__(self, controller, bgm=None):
        super().__init__()
        self.current_option = 0
        self.menu_items = [
            "Spiel starten",
            "Anleitung",
            "Bestenliste",
            "Beenden",
        ]
        self.hovered_item = None
        self.current_option = 0
        self.bgm = bgm
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    if self.current_option > 0:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option -= 1
                elif dpdown:
                    if self.current_option < len(self.menu_items) - 1:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option += 1
                elif dpleft:
                    pass
                elif dpright:
                    pass
                self.hovered_item = self.current_option

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    self.menu()
                elif button == "b":  # Assuming "A" button is similar to 'Enter' action
                    pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AO)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            GAME_TITLE,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            CAPTION,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 10,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        arcade.draw_text(
            SUB_HEADING,
            SCREEN_WIDTH / 2 - 140,
            SCREEN_HEIGHT / 2 - 295,
            arcade.color.WHITE,
            font_size=10,
            anchor_x="center",
        )
        arcade.draw_text(
            "Spiel starten",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            self.get_item_color(0),  # Color of the second menu item
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Bestenliste",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            self.get_item_color(1),  # Color of the third menu item
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Anleitung",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            self.get_item_color(2),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Beenden",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 250,
            self.get_item_color(3),
            font_size=22,
            anchor_x="center",

        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 88 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y + 10, cursor_x - 10, cursor_y - 10, cursor_color
        )

    def get_item_color(self, item_index):
        if self.current_option == item_index or self.hovered_item == item_index:
            return 96, 124, 252
        else:
            return arcade.color.WHITE

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < len(self.menu_items) - 1:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            self.menu()

        self.hovered_item = self.current_option

    def on_mouse_motion(self, x, y, dx, dy):
        for i, _ in enumerate(self.menu_items):
            item_x = SCREEN_WIDTH / 2
            item_y = SCREEN_HEIGHT / 2 - 100 - i * 40
            item_width = 200
            item_height = 30

            # Adjust hitbox size for the second menu item
            if i == 1:
                item_height = 25  # Decrease the height of the hitbox for the second item

            if (
                    item_x - item_width / 2 < x < item_x + item_width / 2
                    and item_y - item_height / 2 < y < item_y + item_height / 2
            ):
                if self.hovered_item != i:
                    self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = i
                self.current_option = i
                break
        else:
            self.hovered_item = None

    def on_mouse_press(self, x, y, button, modifiers):
        if self.hovered_item is not None:
            self.menu()

    def menu(self):
        self.click_effect_menu.play_music(volume=0.1, loop=False)
        if self.current_option == 0:
            mode_selection_view = ModeSelectionView("GameView", self.controller, self.bgm)
            self.window.show_view(mode_selection_view)
        elif self.current_option == 1:
            mode_selection_view = ModeSelectionView("HighScoreView", self.controller)
            self.window.show_view(mode_selection_view)
        elif self.current_option == 2:
            instruction_view = InstructionsView(self.controller)
            self.window.show_view(instruction_view)
        elif self.current_option == 3:
            self.exit_game()

    def exit_game(self):
        self.window.close()


class ModeSelectionView(arcade.View):
    def __init__(self, next_view, controller, bgm=None):
        super().__init__()
        self.current_option = 0
        self.menu_items = [
            "Normal",
            "Party",
            "Zurück",
        ]
        self.party_mode = False
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.hovered_item = -1
        self.next_view = next_view
        self.bgm = bgm
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    if self.current_option > 0:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option -= 1
                elif dpdown:
                    if self.current_option < len(self.menu_items) - 1:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option += 1
                elif dpleft:
                    pass
                elif dpright:
                    pass
                self.hovered_item = self.current_option

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    self.menu()
                elif button == "b":
                    self.click_effect_menu.play_music(volume=0.1, loop=False)
                    start_view = StartView(self.controller)
                    self.window.show_view(start_view)

    def on_show(self):
        arcade.set_background_color(arcade.color.AO)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Wähle einen Modus",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            "Normal",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            self.get_item_color(0),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "(Klassiches Snake)",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 120,
            self.get_item_color(0),
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_text(
            "Party",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 160,
            self.get_item_color(1),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "(Zusätzliche Items)",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 180,
            self.get_item_color(1),
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_text(
            "Zurück",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 220,
            self.get_item_color(2),
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 110 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y + 10, cursor_x - 10, cursor_y - 10, cursor_color
        )

    def get_item_color(self, item_index):
        if self.current_option == item_index or self.hovered_item == item_index:
            return 96, 124, 252
        else:
            return arcade.color.WHITE

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.hovered_item is not None:
                self.menu()

    def on_mouse_motion(self, x, y, dx, dy):
        for i, _ in enumerate(self.menu_items):
            item_x = SCREEN_WIDTH / 2
            item_y = SCREEN_HEIGHT / 2 - 100 - i * 50
            item_width = 200
            item_height = 30
            if (
                    item_x - item_width / 2 < x < item_x + item_width / 2
                    and item_y - item_height / 2 < y < item_y + item_height / 2
            ):
                if self.hovered_item != i:
                    self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = i
                self.current_option = i  # Update current_option as well
                break
        else:
            self.hovered_item = None

    def on_mouse_press(self, x, y, button, modifiers):
        if self.hovered_item is not None:
            self.menu()

    def menu(self):
        self.click_effect_menu.play_music(volume=0.1, loop=False)
        if self.current_option == 0:
            if self.next_view == "GameView":
                self.bgm.stop_audio()
                game_view = GameView(self.controller, party_mode=self.party_mode)
                self.window.show_view(game_view)
            else:
                high_scores_view = HighScoresView(self.controller, self.party_mode)
                self.window.show_view(high_scores_view)
        elif self.current_option == 1:
            self.party_mode = True
            if self.next_view == "GameView":
                self.bgm.stop_audio()
                game_view = GameView(self.controller, party_mode=self.party_mode)
                self.window.show_view(game_view)
            else:
                high_scores_view = HighScoresView(self.controller, self.party_mode)
                self.window.show_view(high_scores_view)
        elif self.current_option == 2:
            start_view = StartView(self.controller)
            self.window.show_view(start_view)


class InstructionsView(arcade.View):
    def __init__(self, controller):
        super().__init__()
        self.current_option = 0
        self.arrow_keys = arcade.load_texture("images/ArrowKeys.png")
        self.wasd_keys = arcade.load_texture("images/WASDKeys.png")
        self.mushroom = arcade.load_texture("images/mushroom.png")
        self.mirror = arcade.load_texture("images/mirror.png")
        self.diamond = arcade.load_texture("images/diamond.png")
        self.sound_effect_menu = BGM(3)
        self.click_effect_menu = BGM(8)
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    pass
                elif dpdown:
                    pass
                elif dpleft:
                    pass
                elif dpright:
                    pass

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    self.click_effect_menu.play_music(volume=0.1, loop=False)
                    start_view = StartView(self.controller)
                    self.window.show_view(start_view)
                elif button == "b":
                    self.click_effect_menu.play_music(volume=0.1, loop=False)
                    start_view = StartView(self.controller)
                    self.window.show_view(start_view)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AO)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Anleitung",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 200,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 + 200,
            SCREEN_HEIGHT // 2 + 70,
            self.wasd_keys.width // 2.4,
            self.wasd_keys.height // 2.4,
            self.wasd_keys,
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 + 65,
            self.arrow_keys.width // 2.4,
            self.arrow_keys.height // 2.4,
            self.arrow_keys,
        )
        arcade.draw_text(
            "Benutze die Pfeilasten oder WASD um die Schlange zu bewegen.",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 60,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )
        arcade.draw_text(
            "Sammel so viele Äpfel wie es geht und berühre nicht die Wand oder dich selber!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 - 250,
            SCREEN_HEIGHT // 2 - 170,
            self.mushroom.width // 7,
            self.mushroom.height // 7,
            self.mushroom,
        )
        arcade.draw_text(
            "Macht dich schneller!",
            SCREEN_WIDTH / 2 - 250,
            SCREEN_HEIGHT / 2 - 235,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 - 10,
            SCREEN_HEIGHT // 2 - 170,
            self.mirror.width // 8,
            self.mirror.height // 8,
            self.mirror,
        )
        arcade.draw_text(
            "Spiegelt die Steuerung!",
            SCREEN_WIDTH / 2 - 10,
            SCREEN_HEIGHT / 2 - 235,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 + 250,
            SCREEN_HEIGHT // 2 - 165,
            self.diamond.width // 2.5,
            self.diamond.height // 2.5,
            self.diamond,
        )
        arcade.draw_text(
            "Erhalte 500 Extrapunkte!",
            SCREEN_WIDTH / 2 + 250,
            SCREEN_HEIGHT / 2 - 235,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_text(
            "Drücke Enter oder klicke die Maus um zurückzukehren",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 280,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            start_view = StartView(self.controller)
            self.window.show_view(start_view)

    def on_mouse_press(self, x, y, button, modifiers):
        self.click_effect_menu.play_music(volume=0.1, loop=False)
        start_view = StartView(self.controller)
        self.window.show_view(start_view)


class HighScoresView(arcade.View):
    def __init__(self, controller, party_mode):
        super().__init__()
        self.current_option = 0
        self.scores = []
        self.party_mode = party_mode
        if self.party_mode:
            self.game_mode = "Party"
        else:
            self.game_mode = "Normal"
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    pass
                elif dpdown:
                    pass
                elif dpleft:
                    pass
                elif dpright:
                    pass

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    mode_selection_view = ModeSelectionView("HighScoreView", self.controller)
                    self.window.show_view(mode_selection_view)
                elif button == "b":
                    pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AO)
        self.load_scores()

    def load_scores(self):
        try:
            with open(f"{self.game_mode}_Hiscore.txt", "r") as file:
                scores = file.readlines()
                self.scores = [score.strip().split(",") for score in scores]
                self.scores.sort(key=lambda x: int(x[1]), reverse=True)
        except FileNotFoundError:
            self.scores = []

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            f"Bestenliste {self.game_mode}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
        )
        if self.scores:
            max_scores = min(5, len(self.scores))
            for i in range(max_scores):
                score = self.scores[i]
                arcade.draw_text(
                    f"{i + 1}. {score[0]} - {score[1]}",
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2 + 50 - i * 50,
                    arcade.color.WHITE,
                    font_size=22,
                    anchor_x="center",
                )
        else:
            arcade.draw_text(
                "Noch keinen Highscore",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 50,
                arcade.color.WHITE,
                font_size=22,
                anchor_x="center",
            )
        arcade.draw_text(
            "Drücke Enter oder klicke die Maus um zurückzukehren",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,  # Adjust the vertical position here
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            mode_selection_view = ModeSelectionView("HighScoreView", self.controller)
            self.window.show_view(mode_selection_view)

    def on_mouse_press(self, x, y, button, modifiers):
        mode_selection_view = ModeSelectionView("HighScoreView", self.controller)
        self.window.show_view(mode_selection_view)


class GameView(arcade.View):
    def __init__(self, controller, party_mode=False):
        super().__init__()
        self.controller = controller
        self.mushroom_position = None
        self.mirror_position = None
        self.diamond_position = None
        self.apple_position = None
        self.snake = Snake()
        self.apple = ItemToEat(self.snake, "apple", self.diamond_position, self.mushroom_position, self.mirror_position,
                               self.apple_position)
        self.previous_Item_to_eat_position = (self.apple.x, self.apple.y)
        if party_mode:
            self.mushroom = ItemToEat(self.snake, "Mushroom", self.diamond_position, self.mushroom_position,
                                      self.mirror_position, self.apple_position)
            self.previous_mushroom_position = (self.mushroom.x, self.mushroom.y)
            self.mushroom = None
            self.mirror = ItemToEat(self.snake, "mirror", self.diamond_position, self.mushroom_position,
                                    self.mirror_position, self.apple_position)
            self.previous_mirror_position = (self.mirror.x, self.mirror.y)
            self.mirror = None
            self.diamond = ItemToEat(self.snake, "diamond", self.diamond_position, self.mushroom_position,
                                     self.mirror_position, self.apple_position)
            self.previous_diamond_position = (self.diamond.x, self.diamond.y)
            self.diamond = None

        self.paused = False
        self.current_option = 0
        self.movement_timer = 0
        self.move_border = 0.15
        self.mirrored_control = False
        self.input_cooldown = False
        self.main_menu_bgm = BGM(0)
        self.bgm = BGM(1)
        self.sound_effect_apple = BGM(3)
        self.sound_effect_mirror = BGM(6)
        self.sound_effect_diamond = BGM(7)
        self.sound_effect_mushroom = BGM(9)
        self.sound_effect_wall = BGM(4)
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.game_over_bgm = BGM(2)
        self.bgm.play_music(volume=0.3, loop=True)
        self.party_mode = party_mode
        self.star = arcade.load_texture("images/star.png")

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if self.paused:
                    pause_view = self.window.current_view
                    if isinstance(pause_view, PauseView):
                        if dpup:
                            if pause_view.current_option > 0:
                                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                                pause_view.update_option(pause_view.current_option - 1)
                        if dpdown:
                            if pause_view.current_option < 2:
                                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                                pause_view.update_option(pause_view.current_option + 1)
                        if dpleft:
                            pass
                        if dpright:
                            pass
                        self.hovered_item = self.current_option
                else:
                    if not self.input_cooldown:
                        if self.mirrored_control:
                            if dpup:
                                self.snake.change_direction("down")
                                self.snake.is_snake_moving = True
                            elif dpdown:
                                self.snake.change_direction("up")
                                self.snake.is_snake_moving = True
                            elif dpleft:
                                self.snake.change_direction("right")
                                self.snake.is_snake_moving = True
                            elif dpright:
                                self.snake.change_direction("left")
                                self.snake.is_snake_moving = True
                        else:
                            if dpup:
                                self.snake.change_direction("up")
                                self.snake.is_snake_moving = True
                            elif dpdown:
                                self.snake.change_direction("down")
                                self.snake.is_snake_moving = True
                            elif dpleft:
                                self.snake.change_direction("left")
                                self.snake.is_snake_moving = True
                            elif dpright:
                                self.snake.change_direction("right")
                                self.snake.is_snake_moving = True

            @self.controller.event
            def on_button_press(_, button):
                if self.paused:
                    pause_view = self.window.current_view
                    if isinstance(pause_view, PauseView):
                        if button == "a":
                            self.sound_effect_menu.play_music(volume=0.1, loop=False)
                            if pause_view.current_option == 0:
                                self.paused = False
                                self.bgm.play_music(volume=0.3, loop=True)
                                self.window.show_view(self)
                            elif pause_view.current_option == 1:
                                self.main_menu_bgm.play_music(volume=0.3, loop=True)
                                start_view = StartView(self.controller, self.main_menu_bgm)
                                self.window.show_view(start_view)
                            elif pause_view.current_option == 2:
                                game_over_view = GameOverView(self.snake.score, self.party_mode,
                                                              self.game_over_bgm,
                                                              self.snake.apple_count, self.controller)
                                self.game_over_bgm.play_music(volume=0.1, loop=True)
                                self.window.show_view(game_over_view)
                else:
                    if not self.input_cooldown:
                        if button == "b":
                            self.sound_effect_menu.play_music(volume=0.1, loop=False)
                            self.paused = True
                            pause_view = PauseView(self)
                            self.window.show_view(pause_view)
                        elif button == "a":
                            pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def draw_apple_count(self):
        # Set the font style, size, and color
        arcade.draw_texture_rectangle(460, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2, 50, 50, self.apple.Item_to_eat)
        arcade.draw_text(str(self.snake.apple_count), 490, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2 - 20,
                         arcade.color.WHITE, font_size=36)

    def draw_score_count(self):
        arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2, 50, 50, self.star)
        arcade.draw_text(str(self.snake.score), 80, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2 - 20,
                         arcade.color.WHITE, font_size=36, )

    def on_draw(self):
        arcade.start_render()

        # Draw the scoreboard area
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2, SCREEN_WIDTH, SCOREBOARD_HEIGHT,
            arcade.color.AVOCADO)
        self.draw_score_count()
        self.draw_apple_count()

        # Draw the game area
        game_height = SCREEN_HEIGHT - SCOREBOARD_HEIGHT
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, game_height // 2, SCREEN_WIDTH, game_height, arcade.color.GREEN
        )

        # Draw the grid with alternating colors
        for row in range(0, game_height, BLOCK_SIZE):
            for column in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                if (row // BLOCK_SIZE + column // BLOCK_SIZE) % 2 == 0:
                    arcade.draw_rectangle_filled(
                        column + BLOCK_SIZE // 2,
                        row + BLOCK_SIZE // 2,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        arcade.color.APPLE_GREEN
                    )
                else:
                    arcade.draw_rectangle_filled(
                        column + BLOCK_SIZE // 2,
                        row + BLOCK_SIZE // 2,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        arcade.color.ANDROID_GREEN
                    )

        self.snake.draw()
        self.apple.draw()
        if self.party_mode and self.mushroom is not None:
            self.mushroom.draw()
        if self.party_mode and self.mirror is not None:
            self.mirror.draw()
        if self.party_mode and self.diamond is not None:
            self.diamond.draw()

    def on_key_press(self, key, modifiers):
        if self.paused:
            # Handle pause logic
            pass
        else:
            if not self.input_cooldown:
                if key == arcade.key.ESCAPE or key == arcade.key.RETURN:
                    self.paused = True
                    pause_view = PauseView(self)
                    self.window.show_view(pause_view)
                else:
                    if self.mirrored_control:
                        directions = {
                            arcade.key.RIGHT: "left",
                            arcade.key.D: "left",
                            arcade.key.LEFT: "right",
                            arcade.key.A: "right",
                            arcade.key.UP: "down",
                            arcade.key.W: "down",
                            arcade.key.DOWN: "up",
                            arcade.key.S: "up",
                        }
                    else:
                        directions = {
                            arcade.key.RIGHT: "right",
                            arcade.key.D: "right",
                            arcade.key.LEFT: "left",
                            arcade.key.A: "left",
                            arcade.key.UP: "up",
                            arcade.key.W: "up",
                            arcade.key.DOWN: "down",
                            arcade.key.S: "down",
                        }
                    if key in directions:
                        self.snake.change_direction(directions[key])
                        self.snake.is_snake_moving = True
                    else:
                        pass

    def get_position(self, item_name):
        if item_name == "mushroom":
            if self.mushroom:
                return self.mushroom.x, self.mushroom.y
            else:
                return None
        elif item_name == "mirror":
            if self.mirror:
                return self.mirror.x, self.mirror.y
            else:
                return None
        elif item_name == "diamond":
            if self.diamond:
                return self.diamond.x, self.diamond.y
            else:
                return None
        elif item_name == "apple":
            if self.apple:
                return self.apple.x, self.apple.y
            else:
                return None

    def update(self, delta_time):
        if not self.paused and self.snake.is_snake_moving:
            self.movement_timer += delta_time
            if self.movement_timer >= self.move_border:
                self.apple_position = self.get_position("apple")
                self.snake.is_snake_moving = True
                self.snake.move()

                if self.party_mode:
                    self.mushroom_position = self.get_position("mushroom")
                    self.mirror_position = self.get_position("mirror")
                    self.diamond_position = self.get_position("diamond")

                    if not self.mushroom and random.randint(1, 40) == 1:
                        self.mushroom = ItemToEat(self.snake, "mushroom", self.diamond_position, self.mushroom_position,
                                                  self.mirror_position, self.apple_position)
                        mushroom_timer = threading.Timer(random.uniform(6, 18), lambda: self.delete_item("mushroom"))
                        mushroom_timer.start()

                    if not self.mirror and random.randint(1, 80) == 1:
                        self.mirror = ItemToEat(self.snake, "mirror", self.diamond_position, self.mushroom_position,
                                                self.mirror_position, self.apple_position)
                        mirror_timer = threading.Timer(random.uniform(6, 18), lambda: self.delete_item("mirror"))
                        mirror_timer.start()

                    if not self.diamond and random.randint(1, 150) == 1:
                        self.diamond = ItemToEat(self.snake, "diamond", self.diamond_position, self.mushroom_position,
                                                 self.mirror_position, self.apple_position)
                        diamond_timer = threading.Timer(random.uniform(3, 9), lambda: self.delete_item("diamond"))
                        diamond_timer.start()

                if self.party_mode and self.mushroom is not None:
                    if self.snake.eat_item(self.mushroom):
                        self.sound_effect_mushroom.play_music(volume=0.5, loop=False)
                        factor = 1 - (2.5 * self.move_border)
                        border_timer = threading.Timer(10, self.higher_border, args=[factor])
                        border_timer.start()
                        self.move_border *= factor
                        self.previous_mushroom_position = (self.mushroom.x, self.mushroom.y)
                        self.mushroom = None

                try:
                    if self.party_mode and self.mirror is not None:
                        if self.snake.eat_item(self.mirror):
                            self.sound_effect_mirror.play_music(volume=0.5, loop=False)
                            if self.mirrored_control:
                                self.mirrored_control = False
                            else:
                                self.mirrored_control = True
                            self.previous_mirror_position = (self.mirror.x, self.mirror.y)
                            self.mirror = None

                    if self.party_mode and self.diamond is not None:
                        if self.snake.eat_item(self.diamond):
                            self.sound_effect_diamond.play_music(volume=0.5, loop=False)
                            self.snake.score += 500
                            self.previous_diamond_position = (self.diamond.x, self.diamond.y)
                            self.diamond = None

                    if self.snake.check_collision():
                        self.sound_effect_wall.play_music(volume=0.5, loop=False)
                        self.bgm.stop_audio()
                        time.sleep(2)
                        save_score_view = SaveScoreView(self.snake.score, self.party_mode, self.bgm,
                                                        self.snake.apple_count, self.controller)
                        self.window.show_view(save_score_view)

                    if self.snake.eat_item(self.apple):
                        self.sound_effect_apple.play_music(volume=0.5, loop=False)
                        self.snake.score += 100
                        self.snake.apple_count += 1
                        self.previous_Item_to_eat_position = (self.apple.x, self.apple.y)
                        self.apple = ItemToEat(self.snake, "apple", self.diamond_position, self.mushroom_position,
                                               self.mirror_position, self.apple_position)

                except NoValidItemToEatPositionError:
                    save_score_view = SaveScoreView(self.snake.score, self.party_mode, self.bgm, self.snake.apple_count,
                                                    self.controller)
                    self.window.show_view(save_score_view)

                self.snake.body.insert(0, (self.snake.x, self.snake.y))
                if len(self.snake.body) > self.snake.apple_count + SNAKE_LENGTH:
                    self.snake.body.pop()

                self.movement_timer = 0
                self.input_cooldown = False

    def higher_border(self, factor):
        self.move_border /= factor

    def delete_item(self, item):
        if item == "mushroom":
            self.mushroom = None
        elif item == "mirror":
            self.mirror = None
        elif item == "diamond":
            self.diamond = None

    def update_option(self, option):
        pass  # This is here because PauseView inherits from GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.hovered_item = None
        self.current_option = 0
        self.menu_items = [
            "Zurück",
            "Hauptmenü",
            "Aufgeben",
        ]
        self.bgm = game_view.bgm
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.bgm.stop_audio()
        self.game_over_bgm = BGM(2)
        self.main_menu_bgm = BGM(0)
        self.controller = game_view.controller


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # Draw the scoreboard area
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2, SCREEN_WIDTH, SCOREBOARD_HEIGHT,
            arcade.color.AVOCADO)

        # Draw the game area
        game_height = SCREEN_HEIGHT - SCOREBOARD_HEIGHT
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, game_height // 2, SCREEN_WIDTH, game_height, arcade.color.GREEN
        )

        # Draw the grid with alternating colors
        for row in range(0, game_height, BLOCK_SIZE):
            for column in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                if (row // BLOCK_SIZE + column // BLOCK_SIZE) % 2 == 0:
                    arcade.draw_rectangle_filled(
                        column + BLOCK_SIZE // 2,
                        row + BLOCK_SIZE // 2,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        arcade.color.APPLE_GREEN
                    )
                else:
                    arcade.draw_rectangle_filled(
                        column + BLOCK_SIZE // 2,
                        row + BLOCK_SIZE // 2,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        arcade.color.ANDROID_GREEN
                    )
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 260, 480, 440, (0, 0, 0, 50))
        arcade.draw_text(
            "Pausiert",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            "Zurück",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            self.get_item_color(0),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Hauptmenü",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            self.get_item_color(1),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Aufgeben",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            self.get_item_color(2),
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 88 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y + 10, cursor_x - 10, cursor_y - 10, cursor_color
        )

    def get_item_color(self, item_index):
        if self.current_option == item_index or self.hovered_item == item_index:
            return 96, 124, 252
        else:
            return arcade.color.WHITE

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            if self.current_option == 0:
                self.bgm.play_music(volume=0.3, loop=True)
                self.game_view.paused = False
                self.game_view.input_cooldown = False  # Reset input cooldown
                self.window.show_view(self.game_view)
            elif self.current_option == 1:
                self.main_menu_bgm.play_music(volume=0.3, loop=True)
                start_view = StartView(self.controller, self.main_menu_bgm)
                self.window.show_view(start_view)
            elif self.current_option == 2:
                game_over_view = GameOverView(self.game_view.snake.score, self.game_view.party_mode, self.game_over_bgm,
                                              self.game_view.snake.apple_count, self.controller)
                self.game_over_bgm.play_music(volume=0.1, loop=True)
                self.window.show_view(game_over_view)

        self.hovered_item = self.current_option


    def on_mouse_motion(self, x, y, dx, dy):
        for i, _ in enumerate(self.menu_items):
            item_x = SCREEN_WIDTH / 2
            item_y = SCREEN_HEIGHT / 2 - 100 - i * 40
            item_width = 200
            item_height = 30

            # Adjust hitbox size for the second menu item
            if i == 1:
                item_height = 25  # Decrease the height of the hitbox for the second item

            if (
                    item_x - item_width / 2 < x < item_x + item_width / 2
                    and item_y - item_height / 2 < y < item_y + item_height / 2
            ):
                if self.hovered_item != i:
                    self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = i
                self.current_option = i
                break
        else:
            self.hovered_item = None

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50
                and SCREEN_HEIGHT / 2 - 130 < y < SCREEN_HEIGHT / 2 - 70
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            self.bgm.play_music(volume=0.3, loop=True)
            self.game_view.paused = False
            self.game_view.input_cooldown = False  # Reset input cooldown
            self.window.show_view(self.game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 120
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            self.main_menu_bgm.play_music(volume=0.3, loop=True)
            start_view = StartView(self.controller, self.main_menu_bgm)
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            game_over_view = GameOverView(self.game_view.snake.score, self.game_view.party_mode, self.game_over_bgm,
                                          self.game_view.snake.apple_count, self.controller)
            self.game_over_bgm.play_music(volume=0.1, loop=True)
            self.window.show_view(game_over_view)


class SaveScoreView(arcade.View):
    def __init__(self, score, party_mode, game_view_bgm, apple_count, controller):
        super().__init__()
        self.score = score
        self.current_option = 0
        self.apple_count = apple_count
        self.menu_items = [
            "Ja",
            "Nein",
        ]
        self.hovered_item = None
        self.party_mode = party_mode
        self.bgm = BGM(2)
        self.sound_effect_menu = BGM(5)
        self.bgm.play_music(volume=0.1, loop=True)
        self.game_bgm = game_view_bgm
        self.game_bgm.stop_audio()
        self.click_effect_menu = BGM(8)
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    pass
                elif dpdown:
                    pass
                elif dpleft:
                    if self.current_option != 0:
                        self.current_option = 0
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                elif dpright:
                    if self.current_option != 1:
                        self.current_option = 1
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = self.current_option

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    self.click_effect_menu.play_music(volume=0.1, loop=False)
                    if self.current_option == 0:
                        save_name_view = SaveScoreNameView(self.score, self.party_mode, self.bgm, self.apple_count,
                                                           self.controller)
                        self.window.show_view(save_name_view)
                    else:
                        game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count,
                                                      self.controller)
                        self.window.show_view(game_over_view)
                elif button == "b":  # Assuming "A" button is similar to 'Enter' action
                    pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Punktzahl speichern",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Willst du deine folgende Punktzahl speichern: {self.score}?",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Ja",
            SCREEN_WIDTH / 2 - 75,
            SCREEN_HEIGHT / 2 - 200,
            self.get_item_color(0),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Nein",
            SCREEN_WIDTH / 2 + 120,
            SCREEN_HEIGHT / 2 - 200,
            self.get_item_color(1),
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 120 if self.current_option == 0 else SCREEN_WIDTH / 2 + 80
        cursor_y = SCREEN_HEIGHT / 2 - 187
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y + 10, cursor_x - 10, cursor_y - 10, cursor_color
        )

    def get_item_color(self, item_index):
        if self.current_option == item_index or self.hovered_item == item_index:
            return 96, 124, 252
        else:
            return arcade.color.WHITE

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.current_option != 0:
                self.current_option = 0
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.current_option != 1:
                self.current_option = 1
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
        elif key == arcade.key.ENTER:
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            if self.current_option == 0:
                save_name_view = SaveScoreNameView(self.score, self.party_mode, self.bgm, self.apple_count,
                                                   self.controller)
                self.window.show_view(save_name_view)
            else:
                game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count, self.controller)
                self.window.show_view(game_over_view)

        self.hovered_item = self.current_option

    def on_mouse_motion(self, x, y, dx, dy):
        for i, _ in enumerate(self.menu_items):
            item_x = SCREEN_WIDTH / 2 - 75 if i == 0 else SCREEN_WIDTH / 2 + 120
            item_y = SCREEN_HEIGHT / 2 - 200
            item_width = 100
            item_height = 30
            if (
                    item_x - item_width / 2 < x < item_x + item_width / 2
                    and item_y - item_height / 2 < y < item_y + item_height / 2
            ):
                if self.hovered_item != i:
                    self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = i
                self.current_option = i  # Update current_option as well
                break
        else:
            self.hovered_item = None

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 120 < x < SCREEN_WIDTH / 2 - 70
                and SCREEN_HEIGHT / 2 - 200 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            save_name_view = SaveScoreNameView(self.score, self.party_mode, self.bgm, self.apple_count, self.controller)
            self.window.show_view(save_name_view)
        elif (
                SCREEN_WIDTH / 2 + 80 < x < SCREEN_WIDTH / 2 + 130
                and SCREEN_HEIGHT / 2 - 200 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count, self.controller)
            self.window.show_view(game_over_view)


class SaveScoreNameView(arcade.View):
    def __init__(self, score, party_mode, bgm, apple_count, controller):
        super().__init__()
        self.score = score
        self.player_name = ""
        self.error_message = ""
        self.apple_count = apple_count
        self.bgm = bgm
        self.party_mode = party_mode
        self.game_mode = "Normal"
        if party_mode:
            self.game_mode = "Party"
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    pass
                elif dpdown:
                    pass
                elif dpleft:
                    pass
                elif dpright:
                    pass

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    pass
                elif button == "b":  # Assuming "A" button is similar to 'Enter' action
                    pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Punktzahl speichern",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Willst du deine folgende Punktzahl speichern: {self.score}?",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Gebe deinen Namen ein:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            self.player_name,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        if self.error_message:
            arcade.draw_text(
                self.error_message,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 250,
                arcade.color.RED,
                font_size=18,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif key == arcade.key.ENTER:
            self.save_score()
            game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count, self.controller)
            self.window.show_view(game_over_view)
        else:
            character = chr(key)
            if modifiers & arcade.key.MOD_SHIFT:
                character = character.upper()
            if re.match(r"^[a-zA-Z0-9]$", character):
                if len(self.player_name) < 8:
                    self.player_name += character
                else:
                    self.error_message = "Name kann maximal 8 Zeichen lang sein!"

    def save_score(self):
        if not self.player_name:
            self.player_name = "Spieler"
        with open(f"{self.game_mode}_Hiscore.txt", "a") as file:
            file.write(f"{self.player_name},{self.score}\n")

    def on_mouse_press(self, x, y, button, modifiers):
        self.save_score()
        game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count, self.controller)
        self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def __init__(self, score, party_mode, bgm, apple_count, controller):
        super().__init__()
        self.snake = Snake()
        self.Item_to_eat = ItemToEat(self.snake)
        self.score = score
        self.eaten_Item_to_eat = apple_count
        self.menu_items = [
            "Neustarten",
            "Hauptmenü",
            "Beenden",
        ]
        self.hovered_item = None
        self.current_option = 0
        self.party_mode = party_mode
        self.bgm = bgm
        self.main_menu_bgm = BGM(0)
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.star = arcade.load_texture("images/star.png")
        self.controller = controller

        if self.controller:
            @self.controller.event
            def on_dpad_motion(_, dpleft, dpright, dpup, dpdown):
                if dpup:
                    if self.current_option > 0:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option -= 1
                elif dpdown:
                    if self.current_option < 2:
                        self.sound_effect_menu.play_music(volume=0.1, loop=False)
                        self.current_option += 1
                elif dpleft:
                    pass
                elif dpright:
                    pass
                self.hovered_item = self.current_option

            @self.controller.event
            def on_button_press(_, button):
                if button == "a":  # Assuming "A" button is similar to 'Enter' action
                    self.click_effect_menu.play_music(volume=0.1, loop=False)
                    if self.current_option == 0:
                        game_view = GameView(self.controller, party_mode=self.party_mode)
                        self.window.show_view(game_view)
                    elif self.current_option == 1:
                        self.main_menu_bgm.play_music(volume=0.3, loop=True)
                        start_view = StartView(self.controller, self.main_menu_bgm)
                        self.window.show_view(start_view)
                    elif self.current_option == 2:
                        self.window.close()
                elif button == "b":  # Assuming "A" button is similar to 'Enter' action
                    pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.bgm.stop_audio()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Game Over",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.RED,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 - 130,
            SCREEN_HEIGHT // 2 - 70,
            50,
            50,
            self.star
        )
        arcade.draw_text(
            str(self.score),
            SCREEN_WIDTH / 2 - 100,
            SCREEN_HEIGHT / 2 - 87,
            arcade.color.WHITE,
            font_size=30,
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 + 100,
            SCREEN_HEIGHT // 2 - 70,
            50,
            50,
            self.Item_to_eat.Item_to_eat
        )
        arcade.draw_text(
            str(self.eaten_Item_to_eat),
            SCREEN_WIDTH // 2 + 130,
            SCREEN_HEIGHT // 2 - 87,
            arcade.color.WHITE,
            font_size=30)
        arcade.draw_text(
            "Neustarten",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            self.get_item_color(0),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Hauptmenü",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            self.get_item_color(1),
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Beenden",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 250,
            self.get_item_color(2),
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 140 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y + 10, cursor_x - 10, cursor_y - 10, cursor_color
        )

    def get_item_color(self, item_index):
        if self.current_option == item_index or self.hovered_item == item_index:
            return 96, 124, 252
        else:
            return arcade.color.WHITE

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            if self.current_option == 0:
                game_view = GameView(self.controller, party_mode=self.party_mode)
                self.window.show_view(game_view)
            elif self.current_option == 1:
                self.main_menu_bgm.play_music(volume=0.3, loop=True)
                start_view = StartView(self.controller, self.main_menu_bgm)
                self.window.show_view(start_view)
            elif self.current_option == 2:
                self.window.close()  # Close the window to exit the game

            self.hovered_item = self.current_option

    def on_mouse_motion(self, x, y, dx, dy):
        for i, _ in enumerate(self.menu_items):
            item_x = SCREEN_WIDTH / 2
            item_y = SCREEN_HEIGHT / 2 - 150 - i * 50
            item_width = 120
            item_height = 50
            if i == 1:
                item_height = 25  # Decrease the height of the hitbox for the second item

            if (
                    item_x - item_width / 2 < x < item_x + item_width / 2
                    and item_y - item_height / 2 < y < item_y + item_height / 2
            ):
                if self.hovered_item != i:
                    self.sound_effect_menu.play_music(volume=0.1, loop=False)
                self.hovered_item = i
                self.current_option = i
                break
        else:
            self.hovered_item = None

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 60 < x < SCREEN_WIDTH / 2 + 60
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 120
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            game_view = GameView(self.controller, party_mode=self.party_mode)
            self.window.show_view(game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            self.main_menu_bgm.play_music(volume=0.3, loop=True)
            start_view = StartView(self.controller, self.main_menu_bgm)
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 280 < y < SCREEN_HEIGHT / 2 - 220
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            self.window.close()  # Close the window to exit the game


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    controller_man = pyglet.input.ControllerManager()
    controllers = controller_man.get_controllers()
    controller = controllers[0] if controllers else None

    if controller:
        controller.open()
    bgm = BGM(0)
    bgm.play_music(volume=0.3, loop=True)
    start_view = StartView(controller, bgm)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
