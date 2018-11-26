import pyautogui

class Mover():

    def __init__(self):
        self.moves = {'up':(0, -60), 'down':(0, +60), 'right':(60, 0), 'left':(-60, 0)}

    def move(self, x ,y, direction, speed=0.4):
        x_increment, y_increment = self.moves[direction]
        pyautogui.moveTo(x ,y)
        pyautogui.dragTo(x + x_increment,
                        y + y_increment,
                        speed, button='left')
