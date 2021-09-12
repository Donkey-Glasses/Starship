import arcade


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
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list('Walls')
        player_sprite_source = ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite = arcade.Sprite(player_sprite_source, CHARACTER_SCALING)
        self.physics_engine = None
        self.frame_rate = 0
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

    def setup(self):
        self.scene.player_list = arcade.SpriteList()
        self.player_sprite.center_x = SCREEN_X / 2
        self.player_sprite.center_y = SCREEN_Y / 2
        self.scene.add_sprite("Player", self.player_sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))
        # self.camera = arcade.Camera(self.width, self.height)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny2.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        arcade.draw_text(f'FPS: {self.frame_rate}', 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key in BACKWARD_VELOCITY:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key in RIGHT_VELOCITY:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key in LEFT_VELOCITY:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int):
        if key in FORWARD_VELOCITY:
            self.player_sprite.change_y = 0
        elif key in BACKWARD_VELOCITY:
            self.player_sprite.change_y = 0
        elif key in RIGHT_VELOCITY:
            self.player_sprite.change_x = 0
        elif key in LEFT_VELOCITY:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

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
        self.physics_engine.update()
        self.center_camera_to_player()


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
