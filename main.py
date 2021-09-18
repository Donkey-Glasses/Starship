import arcade
import math
import random


# Constants
SCREEN_X = 1000
SCREEN_Y = 650
SCREEN_TITLE = "Arcade"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
FORWARD_VELOCITY = [arcade.key.UP, arcade.key.W]
BACKWARD_VELOCITY = [arcade.key.DOWN, arcade.key.S]
LEFT_VELOCITY = [arcade.key.LEFT, arcade.key.A]
RIGHT_VELOCITY = [arcade.key.RIGHT, arcade.key.D]


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_X, SCREEN_Y, SCREEN_TITLE)
        self.scene = arcade.Scene()
        self.player = Starship(self)
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list('Walls')
        self.physics_engine = None
        self.frame_rate = 0
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.sector_list = []

    def setup(self):
        self.scene.player_list = arcade.SpriteList()
        self.player.sprite.center_x = SCREEN_X / 2
        self.player.sprite.center_y = SCREEN_Y / 2
        self.scene.add_sprite("Player", self.player.sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player.sprite, self.scene.get_sprite_list("Walls"))
        self.sector_list = [Sector(x_mod=1, y_mod=1)]

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny2.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        for line in self.player.scanner.line_list:
            line.draw()
        self.scene.draw()
        self.gui_camera.use()
        arcade.draw_text(f'FPS: {self.frame_rate}', 10, 10, arcade.csscolor.WHITE, 18)
        self.player.on_draw()
        for sector in self.sector_list:
            sector.on_draw()

    def on_key_press(self, key: int, modifiers: int):
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key: int, modifiers: int):
        self.player.on_key_release(key, modifiers)

    def center_camera_to_player(self):
        screen_center_x = self.player.sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        # noinspection PyTypeChecker
        self.camera.move_to(player_centered)

    def on_update(self, delta_time: float):
        try:
            self.frame_rate = round(1 / delta_time)
        except ZeroDivisionError:
            self.frame_rate = 0
        self.player.on_update()
        self.physics_engine.update()
        self.center_camera_to_player()
        # time.sleep(.5)


class Starship:

    def __init__(self, game: Game):
        self.game = game
        player_sprite_source = ":resources:images/space_shooter/playerShip1_blue.png"
        self.sprite = arcade.Sprite(player_sprite_source, CHARACTER_SCALING)
        self.speed_dict = {"Forward": 0.5, "Backwards": -0.5, "Left": 5, "Right": -5, "Slow": -1}
        self.scanner = Sensors(self, scan_range=300, color=(0, 180, 0))
        self.turn_rate = 0
        self.thrust = 0
        self.speed = 0
        self.max_speed = 15

    def on_key_press(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.thrust = self.speed_dict['Forward']
        elif key in BACKWARD_VELOCITY:
            self.thrust = self.speed_dict['Backwards']
        elif key in RIGHT_VELOCITY:
            self.turn_rate += self.speed_dict['Right']
        elif key in LEFT_VELOCITY:
            self.turn_rate += self.speed_dict['Left']

    def on_key_release(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.thrust = 0
        elif key in BACKWARD_VELOCITY:
            self.thrust = 0
        elif key in RIGHT_VELOCITY:
            self.turn_rate -= self.speed_dict['Right']
        elif key in LEFT_VELOCITY:
            self.turn_rate -= self.speed_dict['Left']

    def on_update(self):
        self.sprite.angle += self.turn_rate
        self.fly_forward()

    def on_draw(self):
        self.scanner.update_line_list()

    def fly_forward(self):
        self.speed += self.thrust
        if self.speed < 0:
            self.speed += 0.1
        elif self.speed > 0:
            self.speed -= 0.1
        self.speed = min(self.speed, self.max_speed)
        # This mostly works, don't touch it.
        forward_radians = (self.sprite.angle + 90) * math.pi / 180
        self.sprite.change_x = self.speed * math.cos(forward_radians)
        self.sprite.change_y = self.speed * math.sin(forward_radians)


class Sensors:
    START_ANGLE = 90
    MAX_ANGLES = 5

    def __init__(self, owner: Starship, scan_range: int, color: tuple, line_width: float = 2):
        self.owner = owner
        self.scan_range = scan_range
        self.line_width = line_width
        self.color = color
        self.angle_list = [self.START_ANGLE]
        self.line_list = []

    def update_line_list(self):
        def get_color(base_color: tuple, index: int) -> tuple:
            modifier = index / self.MAX_ANGLES
            return int(base_color[0] * modifier), int(base_color[1] * modifier), int(base_color[2] * modifier)

        for index, angle in enumerate(self.angle_list, 0):
            radians = angle * math.pi / 180
            start_x = self.owner.sprite.center_x
            start_y = self.owner.sprite.center_y
            end_x = (self.scan_range * math.cos(radians)) + start_x
            end_y = (self.scan_range * math.sin(radians)) + start_y
            color = get_color(self.color, index)
            newest_line = arcade.create_line(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y,
                                             color=color, line_width=self.line_width)
            self.line_list.append(newest_line)

        if self.angle_list[-1] >= 360:
            self.angle_list.append(0)
        else:
            self.angle_list.append(self.angle_list[-1] + 1)
        if len(self.angle_list) > self.MAX_ANGLES:
            del self.angle_list[0]
        if len(self.line_list) > len(self.angle_list):
            del self.line_list[:self.MAX_ANGLES]


class Sector:
    STAR_COUNT = 5000

    def __init__(self, x_mod, y_mod):
        self.x_mod = x_mod
        self.y_mod = y_mod
        self.star_list = []
        for i in range(self.STAR_COUNT):
            self.star_list.append(self.add_star())

    def add_star(self):
        x = random.randint(0, 1000) * self.x_mod
        y = random.randint(0, 1000) * self.y_mod
        # color = (200, 200, 200)
        # size = random.uniform(1, 3)
        return [x, y]

    def on_draw(self):
        arcade.draw_points(self.star_list, (200, 200, 200), 1)


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
