import random
from turtle import bgcolor

import PySimpleGUI as sg
import chess

PIECES_IMG = {'K': 'wk.png', 'Q': 'wq.png', 'B': 'wb.png', 'R': 'wr.png', 'N': 'wn.png', 'P': 'wp.png', 'k': 'bk.png',
              'q': 'bq.png', 'b': 'bb.png', 'r': 'br.png', 'n': 'bn.png', 'p': 'bp.png'}
BLANK = 'blank.png'

sg.set_options(font="Franklin 15")


class Tile:
    def __init__(self, f, r):
        self.rank = 7 - r
        self.file = f
        self.square = chess.square(self.file, self.rank)
        self.name = chess.square_name(self.square)
        self.key = (self.file, self.rank)
        self.bgcolor = 'light grey' if (
            self.square + self.rank) % 2 else 'skyblue'
        self.button = self.get_button()

    def get_button(self):
        btn = sg.Button(button_color=self.bgcolor, image_filename='assets/' + BLANK, image_size=(64, 64),
                        image_subsample=4, border_width=1, pad=(0, 0), tooltip=self.name.upper(), key=self.key)
        return btn

    def set_image(self, img_path):
        self.button.ImageFilename = 'assets/' + img_path

    def update_image(self, img_path):
        self.button.update(image_filename='assets/' + img_path,
                           image_size=(64, 64), image_subsample=4)

    def change_bg_color(self, color):
        self.button.update(button_color=color)


class ChessBoard(chess.Board):
    def __init__(self):
        super().__init__(chess960=False)
        self.table = [[Tile(file, rank) for file in range(8)]
                      for rank in range(8)]
        self.pending_move = []
        self.available_squares = []
        self.squares_in_danger = []

    def get_layout(self):
        board_layout = []
        for rank in range(8):
            layout_row = [sg.Text(chess.RANK_NAMES[7 - rank])]
            for file in range(8):
                tile = self.table[rank][file]
                if self.piece_at(tile.square) is not None:
                    tile.set_image(PIECES_IMG[str(self.piece_at(tile.square))])
                layout_row.append(tile.button)
            board_layout.append(layout_row)
        file_names = [sg.Text(chess.FILE_NAMES[i].upper(
        ), expand_x=True, justification='center') for i in range(8)]
        board_layout.append(file_names)
        return board_layout

    def get_piece_img(self, tile):
        if self.piece_at(tile.square):
            return PIECES_IMG[str(self.piece_at(tile.square))]
        else:
            return BLANK

    def update_display(self):
        for rank in self.table:
            for tile in rank:
                piece_img = self.get_piece_img(tile)
                self.highlight_tile(tile)
                tile.update_image(piece_img)

    def highlight_tile(self, tile):
        if tile.name in self.pending_move:
            bg_color = 'yellow'
        elif tile.name in self.available_squares:
            if self.piece_at(tile.square) and self.is_attacked_by(self.turn, tile.square):
                bg_color = 'orange'
            else:
                bg_color = 'lime'
        elif tile.name + 'q' in self.available_squares:
            bg_color = 'purple'
        else:
            bg_color = tile.bgcolor
        if self.is_check() and tile.square == self.king(self.turn):
            bg_color = 'red'
        tile.change_bg_color(bg_color)

    def get_available_squares(self, tile):
        legal_moves = [str(move) for move in self.legal_moves]
        for move in legal_moves:
            if move[:2] == tile.name:
                self.available_squares.append(move[2:])

    def handle_move(self, tile):
        if self.color_at(tile.square) == self.turn or len(self.pending_move) == 1:
            self.get_available_squares(tile)
            self.pending_move.append(tile.name)
        if len(self.pending_move) == 2:
            try:
                move = self.parse_uci(''.join(self.pending_move))
                self.push(move)
                # if not self.is_game_over():
                #     engine_move = get_engine_move(self)
                #     self.push(engine_move)
            except ValueError:
                try:
                    self.pending_move.append('q')
                    if self.parse_uci(''.join(self.pending_move)) in self.legal_moves:
                        promote_to = sg.Window("Choose Your Promotion", [[sg.Button('Queen'), sg.Button(
                            'Rook'), sg.Button('Bishop'), sg.Button('Knight')]]).read(close=True)[0]
                        if promote_to == 'Queen':
                            promote = 'q'
                        elif promote_to == 'Rook':
                            promote = 'r'
                        elif promote_to == 'Bishop':
                            promote = 'b'
                        elif promote_to == 'Knight':
                            promote = 'n'
                        self.pending_move[-1] = promote
                        move = self.parse_uci(''.join(self.pending_move))
                        self.push(move)
                except ValueError:
                    sg.PopupQuickMessage('Invalid Move!')
            self.available_squares = []
            self.pending_move = []


def get_engine_move(board):
    rand_move = random.choice(list(board.legal_moves))
    return rand_move


class GameWindow(sg.Window):
    def __init__(self, title):
        self.board = ChessBoard()
        self.status_msg = 'None'
        super().__init__(title, self.get_layout())

    def get_layout(self):
        layout = [[sg.Text('Chess ', auto_size_text=True,
                           key='-STATUS-', font='Default 20')]]
        layout += self.board.get_layout()
        layout += [[sg.Button('Restart', size=(8, 1), key='-RESTART-')]]
        return layout

    def update_status(self):
        msg = f'{"WHITE" if self.board.turn else "BLACK"} to move..'

        if self.board.is_game_over():
            if self.board.is_checkmate():
                winner = 'WHITE' if self.board.outcome().winner else 'BLACK'
                msg = f'CHECKMATE!!! {winner} wins!'
            elif self.board.is_stalemate():
                msg = 'Draw by STALEMATE!'
            elif self.board.is_insufficient_material():
                msg = 'Draw by INSUFFICIENT MATERIAL!'

        self.status_msg = msg
        self['-STATUS-'].update(self.status_msg)

    def update_board(self, event):
        if event == '-RESTART-':
            self.board.reset()
        for rank in self.board.table:
            for tile in rank:
                if tile.key == event:
                    self.board.handle_move(tile)
        self.board.update_display()


def main():
    sg.theme('Python')

    window = GameWindow('Chess')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        window.update_board(event)
        window.update_status()
        window.refresh()

    window.close()


if __name__ == '__main__':
    main()
