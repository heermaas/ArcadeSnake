import arcade
import random
import time
import re

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
SNAKE_SIZE = BLOCK_SIZE
APPLE_SIZE = BLOCK_SIZE
SNAKE_LENGTH = 3
GAME_TITLE = "Snake Game"
scoreboard_height = BLOCK_SIZE * 2


class BGM:
    def __init__(self, song_index):
        self.music_list = ["bgm/MainMenu.mp3", "bgm/Battle.mp3", "bgm/GameOver.mp3", "bgm/Chomp.mp3" , "bgm/Wall.mp3"]
        self.current_song_index = song_index
        self.player = None
        self.music = None

    def play_music(self, volume, loop):
        if self.player:
            self.player.pause()
            time.sleep(0.03)
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
        self.bgm = BGM(0)
        self.sound_effect_menu = BGM(3)
        self.bgm.play_music(volume=0.5, loop=True)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.bgm.stop_audio()


    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            GAME_TITLE,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            "Start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "High Score",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Exit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 80 - self.current_option * 50
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, arcade.color.WHITE
        )

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.current_option == 1:
                high_scores_view = HighScoresView()
                self.window.show_view(high_scores_view)
            elif self.current_option == 2:
                self.exit_game()

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50
                and SCREEN_HEIGHT / 2 - 130 < y < SCREEN_HEIGHT / 2 - 70
        ):
            game_view = GameView()
            self.window.show_view(game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 120
        ):
            high_scores_view = HighScoresView()
            self.window.show_view(high_scores_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            self.exit_game()

    def exit_game(self):
        self.window.close()  # Close the window to exit the game


class GameOverView(arcade.View):
    def __init__(self, score, bgm):
        super().__init__()
        self.score = score
        self.current_option = 0
        self.bgm = bgm
        self.sound_effect_menu = BGM(3)

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
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Score: {self.score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Main Menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Exit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 250,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 130 - self.current_option * 50
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, arcade.color.WHITE
        )

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.current_option == 1:
                start_view = StartView()
                self.window.show_view(start_view)
            elif self.current_option == 2:
                self.window.close()  # Close the window to exit the game

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 60 < x < SCREEN_WIDTH / 2 + 60
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 120
        ):
            game_view = GameView()
            self.window.show_view(game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            start_view = StartView()
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 280 < y < SCREEN_HEIGHT / 2 - 220
        ):
            self.window.close()  # Close the window to exit the game


class SaveScoreNameView(arcade.View):
    def __init__(self, score, bgm):
        super().__init__()
        self.score = score
        self.player_name = ""
        self.error_message = ""
        self.bgm = bgm

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Save Score",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Do you want to save your score of {self.score}?",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Enter your name:",
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
            game_over_view = GameOverView(self.score, self.bgm)
            self.window.show_view(game_over_view)
        elif re.match(r"^[a-zA-Z0-9]$", chr(key)):
            if len(self.player_name) < 8:
                self.player_name += chr(key)
            else:
                self.error_message = "Name must be at most 8 characters long."

    def save_score_with_name(self):
        if not self.player_name:
            self.player_name = "Player"
        with open("Hiscore.txt", "a") as file:
            file.write(f"{self.player_name},{self.score}\n")

    def on_mouse_press(self, x, y, button, modifiers):
        self.save_score_with_name()
        game_over_view = GameOverView(self.score, self.bgm)
        self.window.show_view(game_over_view)


class SaveScoreView(arcade.View):
    def __init__(self, score, game_bgm):
        super().__init__()
        self.score = score
        self.current_option = 0
        self.bgm = BGM(2)
        self.sound_effect_menu = BGM(3)
        self.bgm.play_music(volume=0.5, loop=True)
        self.game_bgm = game_bgm
        self.game_bgm.stop_audio()


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Save Score",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Do you want to save your score of {self.score}?",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Yes",
            SCREEN_WIDTH / 2 - 75,  # Adjust the horizontal position here
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "No",
            SCREEN_WIDTH / 2 + 120,  # Adjust the horizontal position here
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 120 if self.current_option == 0 else SCREEN_WIDTH / 2 + 80
        cursor_y = SCREEN_HEIGHT / 2 - 180
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, arcade.color.WHITE
        )

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.current_option != 0:
                self.current_option = 0
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.current_option != 1:
                self.current_option = 1
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                save_name_view = SaveScoreNameView(self.score, self.bgm)
                self.window.show_view(save_name_view)
            else:
                game_over_view = GameOverView(self.score, self.bgm)
                self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 120 < x < SCREEN_WIDTH / 2 - 80
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 130
        ):
            save_name_view = SaveScoreNameView(self.score, self.bgm)
            self.window.show_view(save_name_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 280 < y < SCREEN_HEIGHT / 2 - 220
        ):
            game_over_view = GameOverView(self.score, self.bgm)
            self.window.show_view(game_over_view)


class HighScoresView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0
        self.scores = []

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
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
            "High Scores",
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
                "No high scores yet!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 50,
                arcade.color.WHITE,
                font_size=22,
                anchor_x="center",
            )
        arcade.draw_text(
            "Press Enter or Click Mouse to Return",
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


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.snake = Snake()
        self.apple = Apple(self.snake)
        self.previous_apple_position = (self.apple.x, self.apple.y)
        self.paused = False
        self.current_option = 0
        self.movement_timer = 0
        self.input_cooldown = False
        self.bgm = BGM(1)
        self.bgm.play_music(volume=0.5, loop=True)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        # Draw the scoreboard area
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - scoreboard_height // 2, SCREEN_WIDTH, scoreboard_height,
            arcade.color.DARK_GREEN
        )
        arcade.draw_text(
            f"Score: {self.snake.score}",
            10,
            SCREEN_HEIGHT - scoreboard_height // 2 - 25,
            arcade.color.WHITE,
            font_size=36,
        )

        # Draw the game area
        game_height = SCREEN_HEIGHT - scoreboard_height
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
                        arcade.color.GREEN
                    )
                else:
                    arcade.draw_rectangle_filled(
                        column + BLOCK_SIZE // 2,
                        row + BLOCK_SIZE // 2,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        arcade.color.YELLOW
                    )

        self.snake.draw()
        self.apple.draw()

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
            if self.movement_timer >= 0.2:
                self.snake.is_snake_moving = True
                self.snake.move()
                if self.snake.check_collision():
                    self.bgm.stop_audio()
                    time.sleep(1)
                    save_score_view = SaveScoreView(self.snake.score, self.bgm)
                    self.window.show_view(save_score_view)

                try:
                    if self.snake.eat_apple(self.apple):
                        self.snake.score += 100
                        self.previous_apple_position = (self.apple.x, self.apple.y)
                        self.apple = Apple(self.snake, self.previous_apple_position)
                except NoValidApplePositionError:
                    save_score_view = SaveScoreView(self.snake.score, self.bgm)
                    self.window.show_view(save_score_view)

                self.snake.body.insert(0, (self.snake.x, self.snake.y))
                if len(self.snake.body) > self.snake.score // 100 + SNAKE_LENGTH:
                    self.snake.body.pop()

                self.movement_timer = 0
                self.input_cooldown = False

    def update_option(self, option):
        pass  # This is here because PauseView inherits from GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.current_option = 0
        self.bgm = game_view.bgm
        self.bgm.stop_audio()
        self.game_over_bgm = BGM(2)
        self.sound_effect_menu = BGM(3)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Paused",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=64,
            anchor_x="center",
        )
        arcade.draw_text(
            "Return",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Main Menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Give Up",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 100
        cursor_y = SCREEN_HEIGHT / 2 - 80 - self.current_option * 50
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, arcade.color.WHITE
        )

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.sound_effect_menu.play_music(volume=0.5, loop=False)
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                self.game_view.paused = False
                self.game_view.input_cooldown = False  # Reset input cooldown
                self.bgm.play_music(volume=0.5, loop=True)
                self.window.show_view(self.game_view)
            elif self.current_option == 1:
                start_view = StartView()
                self.window.show_view(start_view)
            elif self.current_option == 2:
                game_over_view = GameOverView(self.score, self.game_over_bgm)
                self.self.game_over_bgm.game_over_bgm.play_music(volume=0.5, loop=True)
                self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50
                and SCREEN_HEIGHT / 2 - 130 < y < SCREEN_HEIGHT / 2 - 70
        ):
            self.game_view.paused = False
            self.game_view.input_cooldown = False  # Reset input cooldown
            self.window.show_view(self.game_view)
        elif (
                SCREEN_WIDTH / 2 - 80 < x < SCREEN_WIDTH / 2 + 80
                and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 120
        ):
            start_view = StartView()
            self.window.show_view(start_view)
        elif (
                SCREEN_WIDTH / 2 - 40 < x < SCREEN_WIDTH / 2 + 40
                and SCREEN_HEIGHT / 2 - 230 < y < SCREEN_HEIGHT / 2 - 170
        ):
            game_over_view = GameOverView(self.score, self.game_over_bgm)
            self.self.game_over_bgm.game_over_bgm.play_music(volume=0.5, loop=True)
            self.window.show_view(game_over_view)


class Snake:
    def __init__(self):
        self.x = random.randint(2, (SCREEN_WIDTH - BLOCK_SIZE * 2) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.y = random.randint(2, (SCREEN_HEIGHT - BLOCK_SIZE * 2 - scoreboard_height) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.direction = "right"
        self.body = []
        self.body.append((self.x, self.y))
        self.body.append((self.x - BLOCK_SIZE, self.y))  # Add the second segment
        self.body.append((self.x - 2 * BLOCK_SIZE, self.y))
        self.score = 0
        self.is_snake_moving = False
        self.sound_effect_chomp = BGM(3)
        self.sound_effect_wall = BGM(4)

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
                or self.y >= SCREEN_HEIGHT - scoreboard_height
        ):
            self.sound_effect_wall.play_music(volume=0.5, loop=False)
            return True
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                print(self.x, self.y)
                self.sound_effect_chomp.play_music(volume=0.5, loop=False)
                time.sleep(0.1)
                return True
        return False

    def eat_apple(self, snake):
        if (
                self.x < snake.x + SNAKE_SIZE
                and self.x + APPLE_SIZE > snake.x
                and self.y < snake.y + SNAKE_SIZE
                and self.y + APPLE_SIZE > snake.y
        ):
            self.sound_effect_chomp.play_music(volume=0.5, loop=False)
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


class NoValidApplePositionError(Exception):
    pass


class Apple:
    def __init__(self, snake, previous_position=None):
        self.snake = snake
        self.previous_position = previous_position
        self.spawn()
        self.apple = arcade.load_texture("images/apple.png")

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
            raise NoValidApplePositionError("No valid position for the apple.")

    def draw(self):
        arcade.draw_texture_rectangle(
            self.x, self.y, APPLE_SIZE, APPLE_SIZE, self.apple
        )


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()



if __name__ == "__main__":
    main()
