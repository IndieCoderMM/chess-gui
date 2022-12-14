import chess
import PySimpleGUI as sg

ASSET_PATH = "./assets/"

class Tile:
    PRIMARY = 'light grey'
    SECONDARY = 'skyblue'
    EMPTY = "blank.png"
    def __init__(self, f, r):
        self.rank = 7 - r
        self.file = f
        self.square = chess.square(self.file, self.rank)
        self.name = chess.square_name(self.square)
        self.key = (self.file, self.rank)
        self.bgcolor = self.PRIMARY if (
            self.square + self.rank) % 2 else self.SECONDARY
        self.button = self.get_button()

    def get_button(self):
        return sg.Button(button_color=self.bgcolor, image_filename=ASSET_PATH + self.EMPTY, image_size=(64, 64),
                        image_subsample=4, border_width=1, pad=(0, 0), tooltip=self.name.upper(), key=self.key)

    def set_image(self, img_path):
        self.button.ImageFilename = ASSET_PATH + img_path

    def update_image(self, img_path):
        self.button.update(image_filename=ASSET_PATH + img_path,
                           image_size=(64, 64), image_subsample=4)

    def change_bg_color(self, color):
        self.button.update(button_color=color)