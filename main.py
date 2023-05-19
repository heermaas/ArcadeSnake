import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SIZE = 15
SNAKE_SPEED = 5
GRID = 15

class SnakeSprite(arcade.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(SPRITE_SIZE, arcade.color.GREEN, outer_alpha=255)
        self.center_x, self.center_y = pos

class AppleSprite(arcade.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(SPRITE_SIZE, arcade.color.RED, outer_alpha=255)
        self.center_x, self.center_y = pos

class StartView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.selected_option = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Snake Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, arcade.color.BLACK, font_size=30, anchor_x="center")
        if self.selected_option == 0:
            arcade.draw_text("> Start <", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, arcade.color.BLACK, font_size=20, anchor_x="center")
        else:
            arcade.draw_text("Start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("> Exit <", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_option = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_option = 1
        elif key == arcade.key.ENTER:
            if self.selected_option == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.selected_option == 1:
                arcade.window_commands.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if SCREEN_WIDTH // 2 - 60 <= x <= SCREEN_WIDTH // 2 + 60:
            if SCREEN_HEIGHT // 2 - 10 <= y <= SCREEN_HEIGHT // 2 + 10:
                game_view = GameView()
                self.window.show_view(game_view)
            elif SCREEN_HEIGHT // 2 - 40 <= y <= SCREEN_HEIGHT // 2 - 20:
                arcade.window_commands.close_window()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.snake_list = arcade.SpriteList()
        self.snake_list.append(SnakeSprite([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]))
        self.apple_list = arcade.SpriteList()
        self.snake_speed = SNAKE_SPEED
        self.change_x = GRID
        self.change_y = 0
        self.frame_count = 0
        self.score = 0
        self.generate_apple()  # Generate the first apple

    def generate_apple(self):
        while True:
            apple_x = random.randint(1, (SCREEN_WIDTH-GRID)//GRID - 1) * GRID
            apple_y = random.randint(1, (SCREEN_HEIGHT - GRID - SPRITE_SIZE - 30)//GRID - 1) * GRID
            if not arcade.check_for_collision_with_list(AppleSprite([apple_x, apple_y]), self.snake_list):
                self.apple_list = arcade.SpriteList()
                self.apple_list.append(AppleSprite([apple_x, apple_y]))
                break

    def on_draw(self):
        arcade.start_render()
        self.snake_list.draw()
        self.apple_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, SCREEN_HEIGHT - 20, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        self.frame_count += 1
        if self.frame_count % self.snake_speed == 0:
            next_x = (self.snake_list[-1].center_x + self.change_x) % SCREEN_WIDTH
            next_y = (self.snake_list[-1].center_y + self.change_y) % (SCREEN_HEIGHT - 30)
            self.snake_list.append(SnakeSprite([next_x, next_y]))

            # Check for collision with apple
            if arcade.check_for_collision_with_list(self.snake_list[-1], self.apple_list):
                self.score += 100
                self.generate_apple()
            else:  # Only pop when not eating to avoid growth
                self.snake_list[0].kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.change_y != -GRID:
            self.change_x = 0
            self.change_y = GRID
        elif key == arcade.key.DOWN and self.change_y != GRID:
            self.change_x = 0
            self.change_y = -GRID
        elif key == arcade.key.LEFT and self.change_x != GRID:
            self.change_x = -GRID
            self.change_y = 0
        elif key == arcade.key.RIGHT and self.change_x != -GRID:
            self.change_x = GRID
            self.change_y = 0

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game")
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
