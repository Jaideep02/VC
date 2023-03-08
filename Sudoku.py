#This code creates a graphical user interface (GUI) for a Sudoku game using the Tkinter library. 
# The root window of the GUI is created and its size and background color are set.
#  The title of the window is also set to "Sudoku Puzzle". An instance of the GUI class, called "Game", 
# is created and passed the root window. The "generate_sudoku_board()" and "right_side_option_block"
#  methods of the "Game" object are called to create the Sudoku board and the options block on the right 
# side of the window, respectively. Finally, the "mainloop()" function is called to display the window and
#  allow for user interaction.
import tkinter as tk
from src.gui.sudoku_gui import GUI

def main():
    root = tk.Tk()
    root.geometry("1690x845")
    root.configure(background='#c6c8df')
    root.title("Sudoku Puzzle")

    Game = GUI(root)
    Game.generate_sudoku_board()
    Game.right_side_option_block()

    root.mainloop()

if __name__ == '__main__':
    main()