import arcade
import random
import re
import time
import threading

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
SNAKE_SIZE = BLOCK_SIZE
ITEM_TO_EAT_SIZE = BLOCK_SIZE
SNAKE_LENGTH = 3
GAME_TITLE = "Snake Game"
CAPTION = "Navigiere, Wachse, Überlebe!"
SUB_HEADING = "Ein Projekt von Abdelrhman Hassan, Adrian Birlin, Christian Ambs & Manuel Heer"
SCOREBOARD_HEIGHT = BLOCK_SIZE * 2


class BGM:
    def __init__(self, song_index):
        self.music_list = ["bgm/MainMenu2.mp3", "bgm/GameMusic2.mp3", "bgm/GameOver.mp3", "bgm/Chomp.mp3",
                           "bgm/Death.mp3", "bgm/Switch.mp3", "bgm/mirror.mp3", "bgm/diamond.mp3", "bgm/Click.wav"]
        self.current_song_index = song_index
        self.player = None
        self.music = None

    def play_music(self, volume, loop):
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True)
        self.player = self.music.play(volume=volume, loop=loop)
        time.sleep(0.03)

    def stop_audio(self):
        if self.player:
            self.player.pause()


class StartView(arcade.View):
    def __init__(self):
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
        self.bgm = BGM(0)
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.bgm.play_music(volume=0.3, loop=True)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AO)

    def on_hide_view(self):
        self.bgm.stop_audio()

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
        cursor_y = SCREEN_HEIGHT / 2 - 80 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, cursor_color
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
            mode_selection_view = ModeSelectionView()
            self.window.show_view(mode_selection_view)
        elif self.current_option == 1:
            high_scores_view = HighScoresView()
            self.window.show_view(high_scores_view)
        elif self.current_option == 2:
            instruction_view = InstructionsView()
            self.window.show_view(instruction_view)
        elif self.current_option == 3:
            self.exit_game()

    def exit_game(self):
        self.window.close()


class InstructionsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0
        self.arrow_keys = arcade.load_texture("images/ArrowKeys.png")
        self.wasd_keys = arcade.load_texture("images/WASDKeys.png")
        self.sound_effect_menu = BGM(3)
        self.click_effect_menu = BGM(8)

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
            SCREEN_HEIGHT // 2 + 50,
            self.wasd_keys.width // 2,
            self.wasd_keys.height // 2,
            self.wasd_keys,
        )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 + 45,
            self.arrow_keys.width // 2,
            self.arrow_keys.height // 2,
            self.arrow_keys,
        )
        arcade.draw_text(
            "Benutze die Pfeilasten oder WASD um die Schlange zu bewegen.",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )
        arcade.draw_text(
            "Sammel so viele Äpfel wie es geht und berühre nicht die Wand oder dich selber!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_text(
            "Drücke Enter oder klicke die Maus um zurückzukehren",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 230,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            start_view = StartView()
            self.window.show_view(start_view)

    def on_mouse_press(self, x, y, button, modifiers):
        self.click_effect_menu.play_music(volume=0.1, loop=False)
        start_view = StartView()
        self.window.show_view(start_view)


class ModeSelectionView(arcade.View):
    def __init__(self):
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
        cursor_y = SCREEN_HEIGHT / 2 - 80 - self.current_option * 60
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, cursor_color
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
                game_view = GameView(party_mode=self.party_mode)
                self.window.show_view(game_view)
            elif self.current_option == 1:
                self.party_mode = True
                game_view = GameView(party_mode=self.party_mode)
                self.window.show_view(game_view)
            elif self.current_option == 2:
                start_view = StartView()
                self.window.show_view(start_view)

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
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            if self.hovered_item == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.hovered_item == 1:
                self.party_mode = True
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.hovered_item == 2:
                start_view = StartView()
                self.window.show_view(start_view)


class GameView(arcade.View):
    def __init__(self, party_mode=False):
        super().__init__()
        self.snake = Snake()
        self.Item_to_eat = ItemToEat(self.snake, "Apple")
        self.previous_Item_to_eat_position = (self.Item_to_eat.x, self.Item_to_eat.y)
        if party_mode:
            self.mushroom = ItemToEat(self.snake, "Mushroom")
            self.previous_mushroom_position = (self.mushroom.x, self.mushroom.y)
            self.mushroom = None
            self.mirror = ItemToEat(self.snake, "mirror")
            self.previous_mirror_position = (self.mirror.x, self.mirror.y)
            self.mirror = None
            self.diamond = ItemToEat(self.snake, "diamond")
            self.previous_diamond_position = (self.diamond.x, self.diamond.y)
            self.diamond = None
        self.paused = False
        self.current_option = 0
        self.movement_timer = 0
        self.move_border = 0.15
        self.mirrored_control = False
        self.input_cooldown = False
        self.bgm = BGM(1)
        self.sound_effect_apple = BGM(3)
        self.sound_effect_mirror = BGM(6)
        self.sound_effect_diamond = BGM(7)
        self.sound_effect_wall = BGM(4)
        self.bgm.play_music(volume=0.3, loop=True)
        self.party_mode = party_mode
        self.star = arcade.load_texture("images/star.png")
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=SCREEN_WIDTH // 2,
            start_y=SCREEN_HEIGHT // 2 - 50,
            color=arcade.color.WHITE,
            font_size=100,
            anchor_x="center",
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def draw_apple_count(self):
        # Set the font style, size, and color
        arcade.draw_texture_rectangle(460, SCREEN_HEIGHT - SCOREBOARD_HEIGHT // 2, 50, 50, self.Item_to_eat.Item_to_eat)
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
        self.timer_text.draw()

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
        self.Item_to_eat.draw()
        if self.party_mode and self.mushroom is not None:
            self.mushroom.draw()
        if self.party_mode and self.mirror is not None:
            self.mirror.draw()
        if self.party_mode and self.diamond is not None:
            self.diamond.draw()

    def on_key_press(self, key, modifiers):
        if self.paused:
            pause_view = self.window.current_view
            if isinstance(pause_view, PauseView):  # Check if current view is PauseView
                if key == arcade.key.UP or key == arcade.key.W:
                    pause_view.update_option(pause_view.current_option - 1)
                elif key == arcade.key.DOWN or key == arcade.key.S:
                    pause_view.update_option(pause_view.current_option + 1)
                elif key == arcade.key.ENTER:
                    if pause_view.current_option == 0:
                        self.paused = False
                        self.window.show_view(self)
                    elif pause_view.current_option == 1:
                        start_view = StartView()
                        self.window.show_view(start_view)
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
                    self.snake.change_direction(directions[key])
                    self.snake.is_snake_moving = True
                self.input_cooldown = True

    def update(self, delta_time):
        if not self.paused and self.snake.is_snake_moving:
            self.movement_timer += delta_time
            if self.movement_timer >= self.move_border:
                self.snake.is_snake_moving = True
                self.snake.move()

                if self.party_mode and random.randint(1, 4) == 2:
                    self.mushroom = ItemToEat(self.snake, "mushroom", self.previous_mushroom_position)
                    mushroom_timer = threading.Timer(20.0, lambda: self.delete_item("mushroom"))
                    mushroom_timer.start()

                if self.party_mode and random.randint(1, 8) == 2:
                    self.mirror = ItemToEat(self.snake, "mirror", self.previous_mushroom_position)
                    mirror_timer = threading.Timer(20.0, lambda: self.delete_item("mirror"))
                    mirror_timer.start()

                if self.party_mode and random.randint(1, 12) == 2:
                    self.diamond = ItemToEat(self.snake, "diamond", self.previous_mushroom_position)
                    diamond_timer = threading.Timer(20.0, lambda: self.delete_item("diamond"))
                    diamond_timer.start()

                if self.party_mode and self.mushroom is not None:
                    if self.snake.eat_item(self.mushroom):
                        factor = 1 - (2.5 * self.move_border)
                        border_timer = threading.Timer(10, self.higher_border, args=[factor])
                        border_timer.start()
                        self.move_border *= factor
                        self.previous_mushroom_position = (self.mushroom.x, self.mushroom.y)
                        self.mushroom = None

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
                    save_score_view = SaveScoreView(self.snake.score, self.party_mode, self.bgm, self.snake.apple_count)
                    self.window.show_view(save_score_view)

                try:
                    if self.snake.eat_item(self.Item_to_eat):
                        self.sound_effect_apple.play_music(volume=0.5, loop=False)
                        self.snake.score += 100
                        self.snake.apple_count += 1
                        self.previous_Item_to_eat_position = (self.Item_to_eat.x, self.Item_to_eat.y)
                        self.Item_to_eat = ItemToEat(self.snake, "Apple", self.previous_Item_to_eat_position)

                except NoValidItemToEatPositionError:
                    save_score_view = SaveScoreView(self.snake.score, self.bgm, self.snake.apple_count)
                    self.window.show_view(save_score_view)

                self.snake.body.insert(0, (self.snake.x, self.snake.y))
                if len(self.snake.body) > self.snake.score // 100 + SNAKE_LENGTH:
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
        cursor_y = SCREEN_HEIGHT / 2 - 80 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, cursor_color
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
                start_view = StartView()
                self.window.show_view(start_view)
            elif self.current_option == 2:
                game_over_view = GameOverView(self.game_view.snake.score, self.game_view.party_mode, self.game_over_bgm,
                                              self.game_view.snake.apple_count)
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
            start_view = StartView()
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            game_over_view = GameOverView(self.game_view.snake.score, self.game_view.party_mode, self.game_over_bgm, self.game_view.snake.apple_count)
            self.game_over_bgm.play_music(volume=0.1, loop=True)
            self.window.show_view(game_over_view)


class SaveScoreView(arcade.View):
    def __init__(self, score, party_mode, game_view_bgm, apple_count):
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
        cursor_y = SCREEN_HEIGHT / 2 - 180
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, cursor_color
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
                save_name_view = SaveScoreNameView(self.score, self.party_mode, self.bgm, self.apple_count)
                self.window.show_view(save_name_view)
            else:
                game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count)
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
            save_name_view = SaveScoreNameView(self.score, self.party_mode, self.bgm, self.apple_count)
            self.window.show_view(save_name_view)
        elif (
                SCREEN_WIDTH / 2 + 80 < x < SCREEN_WIDTH / 2 + 130
                and SCREEN_HEIGHT / 2 - 200 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count)
            self.window.show_view(game_over_view)


class SaveScoreNameView(arcade.View):
    def __init__(self, score, party_mode, bgm, apple_count):
        super().__init__()
        self.score = score
        self.player_name = ""
        self.error_message = ""
        self.party_mode = party_mode
        self.apple_count = apple_count
        self.bgm = bgm

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
            self.save_score_with_name()
            game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count)
            self.window.show_view(game_over_view)
        elif re.match(r"^[a-zA-Z0-9]$", chr(key)):
            if len(self.player_name) < 8:
                self.player_name += chr(key)
            else:
                self.error_message = "Name kann maximal 8 Zeichen lang sein!"

    def save_score_with_name(self):
        if not self.player_name:
            self.player_name = "Spieler"
        with open("Hiscore.txt", "a") as file:
            file.write(f"{self.player_name},{self.score}\n")

    def on_mouse_press(self, x, y, button, modifiers):
        self.save_score_with_name()
        game_over_view = GameOverView(self.score, self.party_mode, self.bgm, self.apple_count)
        self.window.show_view(game_over_view)


class HighScoresView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0
        self.scores = []

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AO)
        self.load_scores()

    def load_scores(self):
        try:
            with open("Hiscore.txt", "r") as file:
                scores = file.readlines()
                self.scores = [score.strip().split(",") for score in scores]
                self.scores.sort(key=lambda x: int(x[1]), reverse=True)
        except FileNotFoundError:
            self.scores = []

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Bestenliste",
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
            start_view = StartView()
            self.window.show_view(start_view)

    def on_mouse_press(self, x, y, button, modifiers):
        start_view = StartView()
        self.window.show_view(start_view)


class GameOverView(arcade.View):
    def __init__(self, score, party_mode, bgm, apple_count):
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
        self.sound_effect_menu = BGM(5)
        self.click_effect_menu = BGM(8)
        self.star = arcade.load_texture("images/star.png")

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
        cursor_y = SCREEN_HEIGHT / 2 - 130 - self.current_option * 50
        cursor_color = self.get_item_color(self.current_option)
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, cursor_color
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
                game_view = GameView(party_mode=self.party_mode)
                self.window.show_view(game_view)
            elif self.current_option == 1:
                start_view = StartView()
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
            game_view = GameView(party_mode=self.party_mode)
            self.window.show_view(game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            start_view = StartView()
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 280 < y < SCREEN_HEIGHT / 2 - 220
        ):
            self.click_effect_menu.play_music(volume=0.1, loop=False)
            self.window.close()  # Close the window to exit the game


class Snake:
    def __init__(self):
        self.x = random.randint(2, (SCREEN_WIDTH - BLOCK_SIZE * 2) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.y = random.randint(2, (
                SCREEN_HEIGHT - BLOCK_SIZE * 2 - SCOREBOARD_HEIGHT) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.direction = "right"
        self.body = []
        self.body.append((self.x, self.y))
        self.body.append((self.x - BLOCK_SIZE, self.y))  # Add the second segment
        self.body.append((self.x - 2 * BLOCK_SIZE, self.y))
        self.score = 0
        self.is_snake_moving = False
        self.apple_count = 0

        self.head_up = arcade.load_texture("images/head_up.png")
        self.head_down = arcade.load_texture("images/head_down.png")
        self.head_right = arcade.load_texture("images/head_right.png")
        self.head_left = arcade.load_texture("images/head_left.png")

        self.tail_up = arcade.load_texture("images/tail_up.png")
        self.tail_down = arcade.load_texture("images/tail_down.png")
        self.tail_right = arcade.load_texture("images/tail_right.png")
        self.tail_left = arcade.load_texture("images/tail_left.png")

        self.body_vertical = arcade.load_texture("images/body_vertical.png")
        self.body_horizontal = arcade.load_texture("images/body_horizontal.png")

        self.body_tr = arcade.load_texture("images/body_tr.png")
        self.body_tl = arcade.load_texture("images/body_tl.png")
        self.body_br = arcade.load_texture("images/body_br.png")
        self.body_bl = arcade.load_texture("images/body_bl.png")

    def move(self):
        movements = {
            "right": (BLOCK_SIZE, 0),
            "left": (-BLOCK_SIZE, 0),
            "up": (0, BLOCK_SIZE),
            "down": (0, -BLOCK_SIZE),
        }

        move = movements.get(self.direction, (0, 0))
        self.x += move[0]
        self.y += move[1]

    def change_direction(self, new_direction):
        if new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def check_collision(self):
        if (
                self.x < 0
                or self.x >= SCREEN_WIDTH
                or self.y < 0
                or self.y >= SCREEN_HEIGHT - SCOREBOARD_HEIGHT
        ):
            return True
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

    def eat_item(self, snake):
        if (
                self.x < snake.x + SNAKE_SIZE
                and self.x + ITEM_TO_EAT_SIZE > snake.x
                and self.y < snake.y + SNAKE_SIZE
                and self.y + ITEM_TO_EAT_SIZE > snake.y
        ):
            return True
        return False

    def draw(self):
        # Draw the head
        head_x, head_y = self.body[0]
        segment_x, segment_y = self.body[1]
        tail_x, tail_y = self.body[-1]
        second_segment_x, second_segment_y = self.body[-2]

        head_relation_x = segment_x - head_x
        head_relation_y = segment_y - head_y
        head_texture = None
        if head_relation_x == 0 and head_relation_y == BLOCK_SIZE:
            head_texture = self.head_down
        elif head_relation_x == 0 and head_relation_y == -BLOCK_SIZE:
            head_texture = self.head_up
        elif head_relation_x == BLOCK_SIZE and head_relation_y == 0:
            head_texture = self.head_left
        elif head_relation_x == -BLOCK_SIZE and head_relation_y == 0:
            head_texture = self.head_right
        arcade.draw_texture_rectangle(self.x, self.y, SNAKE_SIZE, SNAKE_SIZE, head_texture)

        # Draw the body segments
        for index in range(1, len(self.body)):
            segment = self.body[index]
            segment_x, segment_y = segment

            if index == len(self.body) - 1:
                # Last segment (tail)
                tail_relation_x = second_segment_x - tail_x
                tail_relation_y = second_segment_y - tail_y
                tail_texture = None
                if tail_relation_x == BLOCK_SIZE and tail_relation_y == 0:
                    tail_texture = self.tail_left
                elif tail_relation_x == -BLOCK_SIZE and tail_relation_y == 0:
                    tail_texture = self.tail_right
                elif tail_relation_x == 0 and tail_relation_y == BLOCK_SIZE:
                    tail_texture = self.tail_down
                elif tail_relation_x == 0 and tail_relation_y == -BLOCK_SIZE:
                    tail_texture = self.tail_up
                arcade.draw_texture_rectangle(segment_x, segment_y, SNAKE_SIZE, SNAKE_SIZE, tail_texture)
            else:
                # Body segment
                next_segment_x, next_segment_y = self.body[index + 1]
                previous_segment_x, previous_segment_y = self.body[index - 1]

                if segment_x == next_segment_x == previous_segment_x:
                    body_texture = self.body_vertical
                elif segment_y == next_segment_y == previous_segment_y:
                    body_texture = self.body_horizontal
                else:
                    if segment_x < previous_segment_x:
                        if segment_y < next_segment_y:
                            body_texture = self.body_tr
                        else:
                            body_texture = self.body_br
                    elif segment_x > previous_segment_x:
                        if segment_y < next_segment_y:
                            body_texture = self.body_tl
                        else:
                            body_texture = self.body_bl
                    else:
                        if segment_y < previous_segment_y:
                            if segment_x < next_segment_x:
                                body_texture = self.body_tr
                            else:
                                body_texture = self.body_tl
                        else:
                            if segment_x < next_segment_x:
                                body_texture = self.body_br
                            else:
                                body_texture = self.body_bl

                arcade.draw_texture_rectangle(segment_x, segment_y, SNAKE_SIZE, SNAKE_SIZE, body_texture)


class ItemToEat:
    def __init__(self, snake, item_name="Apple", previous_position=None):
        self.snake = snake
        self.previous_position = previous_position
        self.spawn()
        self.Item_to_eat = arcade.load_texture(f'images/{item_name}.png')

    def spawn(self):
        valid_positions = []
        for x in range(BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE):
            for y in range(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE * 3, BLOCK_SIZE):
                position = (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
                if position not in self.snake.body and position != self.previous_position:
                    valid_positions.append(position)

        if valid_positions:
            self.x, self.y = random.choice(valid_positions)
        else:
            raise NoValidItemToEatPositionError("No valid position for the Item.")

    def draw(self):
        arcade.draw_texture_rectangle(
            self.x, self.y, ITEM_TO_EAT_SIZE, ITEM_TO_EAT_SIZE, self.Item_to_eat
        )


class NoValidItemToEatPositionError(Exception):
    pass


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
