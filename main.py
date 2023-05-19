import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_WIDTH = 15
SNAKE_HEIGHT = 15
APPLE_WIDTH = 15
APPLE_HEIGHT = 15
SNAKE_SPEED = 5
GRID = 15

class Snake(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.snake_list = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.apple_list = []
        self.snake_speed = SNAKE_SPEED
        self.change_x = GRID
        self.change_y = 0
        self.frame_count = 0
        self.score = 0

    def on_draw(self):
        arcade.start_render()
        for coordinate in self.snake_list:
            arcade.draw_rectangle_filled(coordinate[0], coordinate[1], SNAKE_WIDTH, SNAKE_HEIGHT, arcade.color.GREEN)
        for apple in self.apple_list:
            arcade.draw_rectangle_filled(apple[0], apple[1], APPLE_WIDTH, APPLE_HEIGHT, arcade.color.RED)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        self.frame_count += 1
        if self.frame_count % self.snake_speed == 0:
            self.snake_list.append([self.snake_list[-1][0] + self.change_x, self.snake_list[-1][1] + self.change_y])
            if len(self.snake_list) > 3:
                self.snake_list.pop(0)

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
    Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
