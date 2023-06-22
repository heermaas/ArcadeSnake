import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
SNAKE_SIZE = BLOCK_SIZE
APPLE_SIZE = BLOCK_SIZE
SNAKE_SPEED = 1
GAME_TITLE = "Snake Game"
scoreboard_height = BLOCK_SIZE * 2
class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

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
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.current_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

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
        self.is_snake_moving = False
        self.input_cooldown = False

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        # Draw the scoreboard area
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - scoreboard_height // 2, SCREEN_WIDTH, scoreboard_height,
            arcade.color.DARK_GRAY
        )
        arcade.draw_text(
            f"Score: {self.snake.score}",
            10,
            SCREEN_HEIGHT - scoreboard_height // 2 - 25 ,
            arcade.color.WHITE,
            font_size=36,
        )

        # Draw the game area
        game_height = SCREEN_HEIGHT - scoreboard_height
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, game_height // 2, SCREEN_WIDTH, game_height, arcade.color.BLACK
        )

        # Draw grid lines
        for x in range(BLOCK_SIZE, SCREEN_WIDTH, BLOCK_SIZE):
            arcade.draw_line(x, 0, x, game_height, arcade.color.GRAY + (128,), 1)
        for y in range(BLOCK_SIZE, game_height, BLOCK_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.GRAY + (128,), 1)

        self.snake.draw()
        self.apple.draw()

    def on_key_press(self, key, modifiers):
        if not self.paused and not self.is_snake_moving and not self.input_cooldown:
            if key in (arcade.key.RIGHT, arcade.key.D):
                self.snake.change_direction("right")
                self.input_cooldown = True
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.snake.change_direction("left")
                self.input_cooldown = True
            elif key in (arcade.key.UP, arcade.key.W):
                self.snake.change_direction("up")
                self.input_cooldown = True
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.snake.change_direction("down")
                self.input_cooldown = True
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
        if not self.paused:
            self.movement_timer += delta_time
            if self.movement_timer >= 0.2:
                self.is_snake_moving = True
                self.snake.move()
                if self.snake.check_collision():
                    save_score_view = SaveScoreView(self.snake.score)
                    self.window.show_view(save_score_view)

                try:
                    if self.snake.eat_apple(self.apple):
                        self.snake.score += 100
                        self.previous_apple_position = (self.apple.x, self.apple.y)
                        self.apple = Apple(self.snake, self.previous_apple_position)
                except NoValidApplePositionError:
                    game_over_view = GameOverView(self.snake.score)
                    self.window.show_view(game_over_view)

                self.snake.body.insert(0, (self.snake.x, self.snake.y))
                if len(self.snake.body) > self.snake.score // 100 + 1:
                    self.snake.body.pop()

                self.movement_timer = 0
                self.is_snake_moving = False
                self.input_cooldown = False

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


class Snake:
    def __init__(self):
        self.x = (SCREEN_WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.y = (SCREEN_HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.direction = ""
        self.body = []
        self.body.append((self.x, self.y))
        self.score = 0


    def move(self):
        if self.direction == "right":
            self.x += BLOCK_SIZE
        elif self.direction == "left":
            self.x -= BLOCK_SIZE
        elif self.direction == "up":
            self.y += BLOCK_SIZE
        elif self.direction == "down":
            self.y -= BLOCK_SIZE

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
            return True
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

    def eat_apple(self, snake):
        if (
                self.x < snake.x + SNAKE_SIZE
                and self.x + APPLE_SIZE > snake.x
                and self.y < snake.y + SNAKE_SIZE
                and self.y + APPLE_SIZE > snake.y
        ):
            return True
        return False

    def draw(self):
        for segment in self.body:
            arcade.draw_rectangle_filled(
                segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE, arcade.color.GREEN
            )


class NoValidApplePositionError(Exception):
    pass


class Apple:
    def __init__(self, snake, previous_position=None):
        self.snake = snake
        self.previous_position = previous_position
        self.spawn()

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
        arcade.draw_rectangle_filled(
            self.x, self.y, APPLE_SIZE, APPLE_SIZE, arcade.color.RED
        )





def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()