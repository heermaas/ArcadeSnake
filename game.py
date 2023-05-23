import arcade
import random
# import vectormath as vmath

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SIZE = 40
APPLE_SIZE = 30
SNAKE_SPEED = 5
NUM_ROWS = 15
NUM_COLS = 20
CELL_HEIGHT = SCREEN_HEIGHT // 15
CELL_WIDTH = SCREEN_WIDTH // 20


class Snake:
    def __init__(self, border_wrapping=False):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
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
        # Get the position of the snake's head and tail
        head_x, head_y = self.body[0]
        tail_x, tail_y = self.body[-1]

        # Assign a default texture to head_texture
        head_texture = self.head_up

        # Assign a default texture to tail_texture
        tail_texture = self.tail_down

        # Calculate the direction of the snake's head
        if self.direction == "up":
            head_texture = self.head_up
            tail_texture = self.tail_up
        elif self.direction == "down":
            head_texture = self.head_down
            tail_texture = self.tail_down
        elif self.direction == "right":
            head_texture = self.head_right
            tail_texture = self.tail_right
        elif self.direction == "left":
            head_texture = self.head_left
            tail_texture = self.tail_left

        # Draw the snake's body segments with the appropriate texture
        for i in range(1, len(self.body) - 1):
            segment_x, segment_y = self.body[i]
            prev_segment_x, prev_segment_y = self.body[i - 1]
            next_segment_x, next_segment_y = self.body[i + 1]

            texture = self.body_vertical  # Assign a default texture

            if segment_x == prev_segment_x == next_segment_x:
                texture = self.body_vertical
            elif segment_y == prev_segment_y == next_segment_y:
                texture = self.body_horizontal
            elif (segment_x < prev_segment_x and segment_x < next_segment_x) or (
                    segment_x > prev_segment_x and segment_x > next_segment_x):
                texture = self.body_horizontal
            elif (segment_y < prev_segment_y and segment_y < next_segment_y) or (
                    segment_y > prev_segment_y and segment_y > next_segment_y):
                texture = self.body_vertical
            elif (segment_x < prev_segment_x and segment_y > next_segment_y) or (
                    segment_x > prev_segment_x and segment_y < next_segment_y):
                texture = self.body_br
            elif (segment_x > prev_segment_x and segment_y > next_segment_y) or (
                    segment_x < prev_segment_x and segment_y < next_segment_y):
                texture = self.body_bl
            elif (segment_x < prev_segment_x and segment_y < next_segment_y) or (
                    segment_x > prev_segment_x and segment_y > next_segment_y):
                texture = self.body_tl
            elif (segment_x > prev_segment_x and segment_y < next_segment_y) or (
                    segment_x < prev_segment_x and segment_y > next_segment_y):
                texture = self.body_tr

            arcade.draw_texture_rectangle(segment_x, segment_y, SNAKE_SIZE, SNAKE_SIZE, texture)

        # Draw the snake's tail with the appropriate texture
        arcade.draw_texture_rectangle(tail_x, tail_y, SNAKE_SIZE, SNAKE_SIZE, tail_texture)

        # Draw the snake's head with the appropriate texture
        arcade.draw_texture_rectangle(head_x, head_y, SNAKE_SIZE, SNAKE_SIZE, head_texture)


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
