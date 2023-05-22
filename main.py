from game import *
import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SIZE = 15
APPLE_SIZE = BLOCK_SIZE
SNAKE_SPEED = 5
GAME_TITLE = "Snake Game"
NUM_ROWS = 15
NUM_COLS = 20
CELL_HEIGHT = SCREEN_HEIGHT // 15
CELL_WIDTH = SCREEN_WIDTH // 20


def draw_chessboard():
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            # Calculate the coordinates of the current cell
            x = column * CELL_WIDTH
            y = row * CELL_HEIGHT

            # Alternate the color of the cells
            if (row + column) % 2 == 0:
                color = arcade.color.GREEN_YELLOW
            else:
                color = arcade.color.GREEN

            # Draw the cell
            arcade.draw_rectangle_filled(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2, CELL_WIDTH, CELL_HEIGHT, color)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)

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
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                game_mode_view = GameModeView()
                self.window.show_view(game_mode_view)
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
            game_mode_view = GameModeView()
            self.window.show_view(game_mode_view)
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


class GameModeView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Select Game Mode",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
        )
        arcade.draw_text(
            "Easy",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        arcade.draw_text(
            "Normal",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
        )
        self.draw_cursor()

    def draw_cursor(self):
        cursor_x = SCREEN_WIDTH / 2 - 75
        cursor_y = SCREEN_HEIGHT / 2 + 10 - self.current_option * 50
        arcade.draw_triangle_filled(
            cursor_x, cursor_y, cursor_x - 10, cursor_y - 10, cursor_x + 10, cursor_y - 10, arcade.color.WHITE
        )

    def update_option(self, option):
        self.current_option = option

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.current_option > 0:
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 1:
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                game_view = GameView(border_wrapping=True)
                self.window.show_view(game_view)
            elif self.current_option == 1:
                game_view = GameView(border_wrapping=False)
                self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)

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
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                game_mode_view = GameModeView()
                self.window.show_view(game_mode_view)
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
            game_mode_view = GameModeView()
            self.window.show_view(game_mode_view)
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


class SaveScoreView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.current_option = 0

    def on_show(self):
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
            self.current_option = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.current_option = 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                self.save_score()
            game_over_view = GameOverView(self.score)
            self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if (
            SCREEN_WIDTH / 2 - 120 < x < SCREEN_WIDTH / 2 - 80
            and SCREEN_HEIGHT / 2 - 180 < y < SCREEN_HEIGHT / 2 - 130
        ):
            self.save_score()
        game_over_view = GameOverView(self.score)
        self.window.show_view(game_over_view)

    def save_score(self):
        with open("Hiscore.txt", "a") as file:
            file.write(f"Player,{self.score}\n")


class HighScoresView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0
        self.scores = []

    def on_show(self):
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
                    f"{i+1}. {score[0]} - {score[1]}",
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
    def __init__(self, border_wrapping=False):
        super().__init__()
        self.snake = Snake(border_wrapping)
        self.apple = Apple(self.snake)
        self.paused = False
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        arcade.start_render()
        draw_chessboard()
        self.snake.draw()
        self.apple.draw()
        arcade.draw_text(
            f"Score: {self.snake.score}",
            10,
            SCREEN_HEIGHT - 20,
            arcade.color.WHITE,
            font_size=18,
        )

    def on_key_press(self, key, modifiers):
        if not self.paused:
            if key in (arcade.key.RIGHT, arcade.key.D):
                self.snake.change_direction("right")
                self.snake.start_moving()
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.snake.change_direction("left")
                self.snake.start_moving()
            elif key in (arcade.key.UP, arcade.key.W):
                self.snake.change_direction("up")
                self.snake.start_moving()
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.snake.change_direction("down")
                self.snake.start_moving()
            elif key == arcade.key.ESCAPE:
                self.paused = True
                pause_view = PauseView(self)  # Pass the current instance of GameView to PauseView
                self.window.show_view(pause_view)
            elif key == arcade.key.RETURN:
                self.paused = True
                pause_view = PauseView(self)
                self.window.show_view(pause_view)
        else:
            if key == arcade.key.UP or key == arcade.key.W:
                pause_view = self.window.current_view
                if isinstance(pause_view, PauseView):  # Check if current view is PauseView
                    pause_view.update_option(pause_view.current_option - 1)
            elif key == arcade.key.DOWN or key == arcade.key.S:
                pause_view = self.window.current_view
                if isinstance(pause_view, PauseView):  # Check if current view is PauseView
                    pause_view.update_option(pause_view.current_option + 1)
            elif key == arcade.key.ENTER:
                pause_view = self.window.current_view
                if isinstance(pause_view, PauseView):  # Check if current view is PauseView
                    if pause_view.current_option == 0:
                        self.paused = False
                        self.window.show_view(self)
                    elif pause_view.current_option == 1:
                        start_view = StartView()
                        self.window.show_view(start_view)

    def update(self, delta_time):
        if not self.paused and self.snake.moving:
            self.snake.move()
            if self.snake.check_collision():
                save_score_view = SaveScoreView(self.snake.score)
                self.window.show_view(save_score_view)

            if self.snake.eat_apple(self.apple):
                self.snake.score += 100
                self.apple = Apple(self.snake)
                self.snake.body.append((self.snake.x, self.snake.y))

            self.snake.body.insert(0, (self.snake.x, self.snake.y))
            if len(self.snake.body) > self.snake.score // 100 + 1:
                self.snake.body.pop()

    def update_option(self, option):
        pass  # This is here because PauseView inherits from GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.current_option = 0

    def on_show(self):
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
                self.current_option -= 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_option < 2:
                self.current_option += 1
        elif key == arcade.key.ENTER:
            if self.current_option == 0:
                self.game_view.paused = False
                self.window.show_view(self.game_view)  # Show the stored GameView
            elif self.current_option == 1:
                start_view = StartView()
                self.window.show_view(start_view)
            elif self.current_option == 2:
                game_over_view = GameOverView(self.game_view.snake.score)
                self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if (
            SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50
            and SCREEN_HEIGHT / 2 - 130 < y < SCREEN_HEIGHT / 2 - 70
        ):
            self.game_view.paused = False
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
            game_over_view = GameOverView(self.game_view.snake.score)
            self.window.show_view(game_over_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
