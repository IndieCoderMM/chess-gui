from game.gui import ChessGUI
import PySimpleGUI as sg


def main():
    sg.theme('Python')
    sg.set_options(font="Cambria 15")

    window = ChessGUI('Chess')

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
