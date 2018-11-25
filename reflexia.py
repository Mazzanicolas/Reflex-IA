from PIL import ImageGrab
import numpy as np
import win32gui
import cv2


class Reflexia():

    def __init__(self, window_name=r'Mirror'):
        """
        * window_name: Name of the window to capture
        +
        """ 
        self.window_position = win32gui.FindWindow(None, window_name)
        self.items_on_board = {
                              'star':  './items/star.png',
                              'orb':   './items/orb.png',
                              'potion':'./items/potion.png',
                              'sword': './items/sword.png'
                             }
        self.turns_dimensions = {
                                 'top_corner':    (42, 18),
                                 'bottom_corner': (130, 38)
                                }
        self.board_dimensions = {
                                 'top_corner':    (233, 140),
                                 'bottom_corner': (708, 557),
                                }
        self.health_dimensions = {
                                 'top_corner':    (38, 671),
                                 'bottom_corner': (87, 690)
                                }                                
    def capture_screen(self):
        while True:
            ##########################################################
            ################# Getting windows frames #################
            ##########################################################
            window_dimensions = win32gui.GetWindowRect(self.window_position)
            distance_left, distance_top, window_width, window_height = window_dimensions
            cropped_window_dimensions = (distance_left+5,
                                         distance_top+26,
                                         window_width-2,
                                         window_height-3)
            game_frame = ImageGrab.grab(cropped_window_dimensions)
            game_frame = np.array(game_frame)
            ################ Getting board dimensions ###############
            x, y = self.board_dimensions['top_corner']
            x2, y2 = self.board_dimensions['bottom_corner']
            game_board_frame = game_frame[y:y2, x:x2]
            ################ Getting turns dimensions ###############
            x, y = self.turns_dimensions['top_corner']
            x2, y2 = self.turns_dimensions['bottom_corner']
            game_turns_frame = game_frame[y:y2, x:x2]
            #########################################################
            ###################### Reflexia View ####################
            #########################################################
            game_frame = self.locate_on_screen(game_frame, self.turns_dimensions, thickness=2)
            game_frame = self.locate_on_screen(game_frame, self.board_dimensions, thickness=2)
            game_frame = self.locate_on_screen(game_frame, self.health_dimensions, thickness=2)
            #########################################################
            ################### Get items on board ##################
            #########################################################
            
            x, y = self.board_dimensions['top_corner']

            potion_w, potion_h, potion_locations = self.detect_item(game_board_frame, 'potion')
            game_frame = self.locate_on_board(game_frame, potion_locations, (0,255,0), 15)

            sword_w, sword_h, sword_locations = self.detect_item(game_board_frame, 'sword')
            game_frame = self.locate_on_board(game_frame, sword_locations, (255,255,0), 15)
            
            star_w, star_h, star_locations = self.detect_item(game_board_frame, 'star')
            game_frame = self.locate_on_board(game_frame, star_locations, (0,255,255), 15)

            orb_w, orb_h, orb_locations = self.detect_item(game_board_frame, 'orb')            
            game_frame = self.locate_on_board(game_frame, orb_locations, (255,0,255), 15)
            #########################################################
            ################### Show window Frames ##################
            #########################################################
            game_frame = cv2.cvtColor(game_frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Reflexia', game_frame)            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def locate_on_screen(self, game_board_frame, dimensions, color=(0,255,0), thickness=1):
        """
        Draw a rectangle with the given dimensions, color & thickness over the given frame
        """
        top_corner    = dimensions['top_corner']
        bottom_corner = dimensions['bottom_corner']
        cv2.rectangle(game_board_frame, top_corner, bottom_corner, color, thickness)
        return game_board_frame

    def locate_on_board(self, game_frame, locations, color=(0,255,0), thickness=10):
        """
        Draw a circle with the given dimensions, color & thickness over the given frame
        """
        x, y = self.board_dimensions['top_corner']
        for point in zip(*locations[::-1]):
            cv2.circle(game_frame, (point[0]+25+x, point[1]+25+y), 10, color, thickness)
        return game_frame

    def detect_item(self, game_frame, item_name, threshold=0.8):
        """
        Returns height, width of the maching template & location of the boxes
        """
        img_gray = cv2.cvtColor(game_frame, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(self.items_on_board[item_name],0)
        width, height = template.shape[::-1]
        maching_locations = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(maching_locations >= threshold)
        return width, height, locations

if __name__ == '__main__':
    print('> > > Start')
    reflexia = Reflexia()
    reflexia.capture_screen()
    print('< < < End')