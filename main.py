import arcade
import math
import time


# Constants
SCREEN_X = 1000
SCREEN_Y = 650
SCREEN_TITLE = "Arcade"
CHARACTER_SCALING = 0.25
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

    def setup(self):
        self.scene.player_list = arcade.SpriteList()
        self.player.sprite.center_x = SCREEN_X / 2
        self.player.sprite.center_y = SCREEN_Y / 2
        self.scene.add_sprite("Player", self.player.sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player.sprite, self.scene.get_sprite_list("Walls"))
        # self.camera = arcade.Camera(self.width, self.height)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny2.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.player.scanner.update_line()
        try:
            # self.player.scanner.old_line.draw()
            self.player.scanner.new_line.draw()
        except AttributeError:
            print('None type sensors')
        self.scene.draw()
        self.gui_camera.use()
        arcade.draw_text(f'FPS: {self.frame_rate}', 10, 10, arcade.csscolor.WHITE, 18)

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
        self.speed_dict = {"Forward": 5, "Backwards": -5, "Left": -5, "Right": 5}
        self.scanner = Sensors(self, scan_range=300)

    def on_key_press(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.sprite.change_y = self.speed_dict['Forward']
        elif key in BACKWARD_VELOCITY:
            self.sprite.change_y = self.speed_dict['Backwards']
        elif key in RIGHT_VELOCITY:
            self.sprite.change_x = self.speed_dict['Right']
        elif key in LEFT_VELOCITY:
            self.sprite.change_x = self.speed_dict['Left']

    def on_key_release(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.sprite.change_y = 0
        elif key in BACKWARD_VELOCITY:
            self.sprite.change_y = 0
        elif key in RIGHT_VELOCITY:
            self.sprite.change_x = 0
        elif key in LEFT_VELOCITY:
            self.sprite.change_x = 0

    def on_update(self):
        pass


class Sensors:
    def __init__(self, owner: Starship, scan_range: int, color=arcade.csscolor.GREEN, line_width: float = 2):
        self.owner = owner
        self.scan_range = scan_range
        self.line_width = line_width
        self.angle = 90
        self.color = color
        self.old_line = None
        self.new_line = None

    def update_line(self):
        radians = self.angle * math.pi / 180
        self.old_line = self.new_line
        start_x = self.owner.sprite.center_x
        start_y = self.owner.sprite.center_y
        end_x = (self.scan_range * math.cos(radians)) + start_x
        end_y = (self.scan_range * math.sin(radians)) + start_y
        # end_x = start_x + 300
        # end_y = start_y + 300
        self.angle -= 1
        if self.angle == 360:
            self.angle = 0
        # print(f'{start_x}, {start_y} // {end_x}, {end_y} -- {self.angle}')
        # self.new_line = arcade.create_ellipse_filled(center_x=end_x, center_y=end_y,
        #                                              width=100, height=100, color=self.color)
        self.new_line = arcade.create_line(start_x=start_x, start_y=start_y, end_x=end_x,
                                           end_y=end_y, color=self.color, line_width=self.line_width)


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
