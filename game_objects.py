import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
SNAKE_SIZE = BLOCK_SIZE
ITEM_TO_EAT_SIZE = BLOCK_SIZE
SNAKE_LENGTH = 3
SCOREBOARD_HEIGHT = BLOCK_SIZE * 2


class Snake:
    def __init__(self):
        self.x = random.randint(2, (SCREEN_WIDTH - BLOCK_SIZE * 2) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.y = random.randint(2, (
                SCREEN_HEIGHT - BLOCK_SIZE * 2 - SCOREBOARD_HEIGHT) // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.direction = "right"
        self.body = []
        self.body.append((self.x, self.y))  # Füge erstes Segment hinzu
        self.body.append((self.x - BLOCK_SIZE, self.y))  # Zweites Segment
        self.body.append((self.x - 2 * BLOCK_SIZE, self.y))  # Drittes Segment
        self.score = 0  # Setze Score auf 0
        self.is_snake_moving = False
        self.apple_count = 0  # Setze die Apfelanzahl auf 0

        # Ordne Schlangenteile den Texturen zu
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

    # Ändere Richtung zur neuen, wenn diese nicht entgegen der alten ist
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
        # Überprüfe ob Schlange außerhalb des Spielfelds ist
        if (
                self.x < 0
                or self.x >= SCREEN_WIDTH
                or self.y < 0
                or self.y >= SCREEN_HEIGHT - SCOREBOARD_HEIGHT
        ):
            return True
        # Überprüfe ob Schlange mit sich selbst kollidiert
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

    def eat_item(self, snake):
        # Überprüfe ob die Schlange auf einem Item ist (und dieses essen kann)
        if (
                self.x < snake.x + SNAKE_SIZE
                and self.x + ITEM_TO_EAT_SIZE > snake.x
                and self.y < snake.y + SNAKE_SIZE
                and self.y + ITEM_TO_EAT_SIZE > snake.y
        ):
            return True
        return False

    def draw(self):
        # Zeichne den Kopf
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

        # Zeichne die Körpersegmente
        for index in range(1, len(self.body)):
            segment = self.body[index]
            segment_x, segment_y = segment

            if index == len(self.body) - 1:
                # Schwanzsegment
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
                # Restliche Körpersegmente
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
    def __init__(self, snake, item_name="apple", diamond_position=None, mushroom_position=None, mirror_position=None, apple_position=None, previous_position=None):
        self.snake = snake
        self.previous_position = previous_position
        # Speichere aktuelle Itempositionen
        self.current_positions = {
            "diamond": diamond_position,
            "mushroom": mushroom_position,
            "mirror": mirror_position,
            "apple": apple_position
        }
        self.spawn()
        self.Item_to_eat = arcade.load_texture(f'images/{item_name}.png')

    def spawn(self):
        valid_positions = []
        # Iteriere durch alle möglichen Itempositionen
        for x in range(BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE):
            for y in range(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE * 3, BLOCK_SIZE):
                position = (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
                # Üperprüfe ob die Itemposition bereits mit der Schlange oder anderen Items besetzt ist
                if position not in self.snake.body and position != self.previous_position \
                        and not any(position == p for p in self.current_positions.values() if p is not None):
                    valid_positions.append(position)

        # Wenn eine Position frei ist, wähle eine zufällige unter den freien aus
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
