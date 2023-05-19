
# Importieren der notwendigen Bibliotheken
import arcade
import random
import re

# Setzen der Konstanten für das Spiel
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_WIDTH = 20
APPLE_SIZE = 20
MOVEMENT_SPEED = 18
SPEED_INCREASE = 0.5

# Regulärer Ausdruck zur Überprüfung der Gültigkeit des Spielernamens
VALID_NAME_REGEX = re.compile(r'^\w{1,15}$')


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        # Ausgewählte Option, default ist 0
        self.selected_option = 0
        # Optionen für das Menü
        self.options = ["Spiel Starten", "Highscores", "Beenden"]

    def on_show(self):
        # Setzt die Hintergrundfarbe
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        # Startet das Zeichnen des Bildschirms
        arcade.start_render()
        # Zeichnet den Titel
        arcade.draw_text("Snake Spiel", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        # Zeichnet die Optionen
        for i, option in enumerate(self.options):
            # Die ausgewählte Option wird blau hervorgehoben
            color = arcade.color.BLUE if i == self.selected_option else arcade.color.BLACK
            y_position = SCREEN_HEIGHT / 2 - (i * 40)
            arcade.draw_text(option, SCREEN_WIDTH / 2, y_position, color, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        # Bewegt die Auswahl nach oben oder unten
        if key in [arcade.key.UP, arcade.key.W]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == arcade.key.ENTER:
            # Führt die ausgewählte Option aus
            if self.selected_option == 0:
                game_view = Game()
                self.window.show_view(game_view)
            elif self.selected_option == 1:
                highscores_view = HighScoresView()
                self.window.show_view(highscores_view)
            elif self.selected_option == 2:
                arcade.close_window()


class HighScoresView(arcade.View):
    def on_show(self):
        # Setzt die Hintergrundfarbe
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        # Startet das Zeichnen des Bildschirms
        arcade.start_render()
        # Zeichnet den Highscores-Titel
        arcade.draw_text("Highscores:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        try:
            # Zeigt die gespeicherten Highscores an
            with open("hiscores.txt", "r") as file:
                for i, line in enumerate(file.readlines()):
                    arcade.draw_text(line.strip(), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40 - 30 * i,
                                     arcade.color.BLACK, font_size=20, anchor_x="center")
        except FileNotFoundError:
            arcade.draw_text("Noch keine Highscores.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                             arcade.color.BLACK, font_size=20, anchor_x="center")

        # Zeigt die Nachricht zum Zurückkehren an
        arcade.draw_text("Drücken Sie ESC zum Zurückkehren", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 220,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            # Bei Drücken von ESC, zurück zum Menü
            menu_view = MenuView()
            self.window.show_view(menu_view)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.change_x = 0
        self.change_y = 0
        self.snake_head = [100, 100]
        self.snake_body_list = []
        self.apple = [random.randint(20, SCREEN_WIDTH - 20),
                      random.randint(20, SCREEN_HEIGHT - 20)]
        self.frame_count = 0
        self.is_game_over = False
        self.name_prompted = False

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        # Zeichnet den Apfel
        arcade.draw_rectangle_filled(self.apple[0], self.apple[1], APPLE_SIZE, APPLE_SIZE,
                                     arcade.color.RED)
        # Zeichnet den Kopf der Schlange
        arcade.draw_rectangle_filled(self.snake_head[0], self.snake_head[1], SNAKE_WIDTH, SNAKE_WIDTH,
                                     arcade.color.GREEN)
        # Zeichnet den Körper der Schlange
        for body in self.snake_body_list:
            arcade.draw_rectangle_filled(body[0], body[1], SNAKE_WIDTH, SNAKE_WIDTH,
                                         arcade.color.GREEN)
        # Zeichnet den aktuellen Punktestand
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20)

        # Wenn das Spiel vorbei ist, zeige den Game Over-Bildschirm
        if self.is_game_over:
            self.draw_game_over()

    def draw_game_over(self):
        # Zeichnet den Game Over-Text und den Punktestand
        arcade.draw_text(f"Game Over\nScore: {self.score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, 30, anchor_x="center")

        if not self.name_prompted:
            # Fordert den Namen des Spielers an
            self.prompt_name()
        else:
            # Zeigt die Nachricht zum Zurückkehren an
            arcade.draw_text("Drücken Sie ESC zum Zurückkehren", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                             arcade.color.BLACK, 20, anchor_x="center")

    def prompt_name(self):
        # Fordert den Namen des Spielers an
        self.name_prompted = True
        name = arcade.gui.UIInputBox(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 50,
                                     width=200)
        name.text = "Name"
        button = arcade.gui.UIFlatButton(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 100,
                                         width=100, height=40, text="Speichern")
        button.set_style_attrs(font_color=arcade.color.BLACK)

        def on_click(_):
            if VALID_NAME_REGEX.match(name.text):
                # Speichert den Namen und den Punktestand des Spielers
                with open("hiscores.txt", "a") as file:
                    file.write(f"{name.text}: {self.score}\n")
            else:
                # Zeigt eine Fehlermeldung an, wenn der Name ungültig ist
                name.text = "Ungültiger Name!"

        button.on_click = on_click
        self.add_ui_element(name)
        self.add_ui_element(button)

    def on_key_press(self, key, _modifiers):
        # Ändert die Richtung der Schlange
        if key in [arcade.key.UP, arcade.key.W]:
            self.change_x = 0
            self.change_y = 1
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.change_x = 0
            self.change_y = -1
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.change_x = -1
            self.change_y = 0
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.change_x = 1
            self.change_y = 0
        elif key == arcade.key.ESCAPE and self.is_game_over:
            # Bei Drücken von ESC, zurück zum Menü
            self.window.show_view(MenuView())

    def update(self, delta_time):
        self.frame_count += 1

        # Bewegt die Schlange
        if self.frame_count % max(1, 60 - self.score // 100) == 0 and not self.is_game_over:
            self.snake_body_list.insert(0, self.snake_head.copy())
            if len(self.snake_body_list) > self.score // 100 + 5:
                self.snake_body_list.pop()

            self.snake_head[0] += self.change_x * MOVEMENT_SPEED
            self.snake_head[1] += self.change_y * MOVEMENT_SPEED

            # Handhabung der Bildschirm-Wraparound für die Schlange
            if self.snake_head[0] < 0:
                self.snake_head[0] = SCREEN_WIDTH
            elif self.snake_head[0] > SCREEN_WIDTH:
                self.snake_head[0] = 0
            if self.snake_head[1] < 0:
                self.snake_head[1] = SCREEN_HEIGHT
            elif self.snake_head[1] > SCREEN_HEIGHT:
                self.snake_head[1] = 0

            # Überprüft, ob die Schlange einen Apfel gefressen hat
            if abs(self.snake_head[0] - self.apple[0]) < SNAKE_WIDTH and abs(
                    self.snake_head[1] - self.apple[1]) < SNAKE_WIDTH:
                self.score += 100
                self.apple = [random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)]

            # Überprüft, ob die Schlange sich selbst gebissen hat
            for body in self.snake_body_list[1:]:
                if body[0] == self.snake_head[0] and body[1] == self.snake_head[1]:
                    self.is_game_over = True


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Spiel")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
