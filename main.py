import arcade


# Constants
SCREEN_X = 1000
SCREEN_Y = 650
SCREEN_TITLE = "Arcade"
CHARACTER_SCALING = 0.25
TILE_SCALING = 0.5


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_X, SCREEN_Y, SCREEN_TITLE)
        self.scene = arcade.Scene()
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.scene.add_sprite_list("Player")
        self.player_sprite = None

    def setup(self):
        self.scene.player_list = arcade.SpriteList()
        player_sprite_source = ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite = arcade.Sprite(player_sprite_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_X / 2
        self.player_sprite.center_y = SCREEN_Y / 2
        self.scene.add_sprite("Player", self.player_sprite)

    def on_draw(self):
        arcade.start_render()

        self.scene.draw()


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
