import arcade
import random
import vectormath as vmath

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SIZE = 15
APPLE_SIZE = 40
SNAKE_SPEED = 5
NUM_ROWS = 15
NUM_COLS = 20
CELL_HEIGHT = SCREEN_HEIGHT // 15
CELL_WIDTH = SCREEN_WIDTH // 20


class Snake:
    def __init__(self, border_wrapping=False):
        valid_x_range = range(BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        valid_y_range = range(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        self.x = random.choice(valid_x_range)
        self.y = random.choice(valid_y_range)
        self.direction = ""
        self.body = []
        self.body.append((self.x, self.y))
        self.score = 0
        self.moving = False
        self.border_wrapping = border_wrapping

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

    def start_moving(self):
        self.moving = True

    def move(self):
        if self.direction == "right":
            self.x += SNAKE_SPEED
            if self.border_wrapping and self.x >= SCREEN_WIDTH:
                self.x = 0
        elif self.direction == "left":
            self.x -= SNAKE_SPEED
            if self.border_wrapping and self.x < 0:
                self.x = SCREEN_WIDTH - BLOCK_SIZE
        elif self.direction == "up":
            self.y += SNAKE_SPEED
            if self.border_wrapping and self.y >= SCREEN_HEIGHT:
                self.y = 0
        elif self.direction == "down":
            self.y -= SNAKE_SPEED
            if self.border_wrapping and self.y < 0:
                self.y = SCREEN_HEIGHT - BLOCK_SIZE

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
            not self.border_wrapping
            and (self.x < 0 or self.x >= SCREEN_WIDTH or self.y < 0 or self.y >= SCREEN_HEIGHT)
        ):
            return True
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

    def eat_apple(self, apple):
        if (
            self.x < apple.x + APPLE_SIZE
            and self.x + SNAKE_SIZE > apple.x
            and self.y < apple.y + APPLE_SIZE
            and self.y + SNAKE_SIZE > apple.y
        ):
            return True
        return False

    def draw(self):
        for segment in self.body:
            arcade.draw_circle_filled(
                segment[0], segment[1], SNAKE_SIZE, arcade.color.BLUE
            )


class Apple:
    def __init__(self, snake):
        # Calculate the valid cell positions within the chessboard pattern
        valid_cells = []
        for row in range(NUM_ROWS):
            for column in range(NUM_COLS):
                cell_x = column * CELL_WIDTH + CELL_WIDTH // 2
                cell_y = row * CELL_HEIGHT + CELL_HEIGHT // 2
                valid_cells.append((cell_x, cell_y))

        # Filter out cells that collide with the snake's body
        valid_cells = [cell for cell in valid_cells if cell not in snake.body]

        # Choose a random cell position within the valid range
        self.x, self.y = random.choice(valid_cells)
        self.apple = arcade.load_texture("images/apple_snake1.png")

    def draw(self):
        hitbox_width = APPLE_SIZE
        hitbox_height = APPLE_SIZE

        arcade.draw_texture_rectangle(
            self.x, self.y, hitbox_width, hitbox_height, self.apple
        )
