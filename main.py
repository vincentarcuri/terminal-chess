from cli import *

def main():
    window = Window()
    controller = CLIController()
    while True:
        window_event = window.get_input()
        game_info = controller.handle_event_and_return_info(window_event, window)
        window.update_board(game_info)
        window.update()

if __name__ == "__main__":
    main()
