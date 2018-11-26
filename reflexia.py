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
        self.symbols = [0,1,2,3,4,5,6,7,8,9,'/']
        self.items_on_board = {
                               1: (1, 'STR','./items/star.png'),   # ID: 1
                               2: (2, 'ORB','./items/orb.png'),    # ID: 2
                               3: (3, 'PTN','./items/potion.png'), # ID: 3
                               4: (4, 'SWD','./items/sword.png'),  # ID: 4
                               5: (5, 'DMD','./items/diamond.png') # ID: 5
                              }
        self.turns_dimensions = {
                                 'top_corner':    (42, 18),
                                 'bottom_corner': (130, 38)
                                }
        self.board_dimensions = {
                                 'top_corner':    (233, 144),
                                 'bottom_corner': (708, 557),
                                }
        self.health_dimensions = {
                                 'top_corner':    (38, 671),
                                 'bottom_corner': (87, 690)
                                }
        self.board_positions = np.array([[265, 175], [325, 175], [380, 175], [445, 175], [500, 175], [560, 175], [620, 175], [680, 175],
                                         [265, 235], [325, 235], [380, 235], [445, 235], [500, 235], [560, 235], [620, 235], [680, 235],
                                         [265, 290], [325, 290], [380, 290], [445, 290], [500, 290], [560, 290], [620, 290], [680, 290],
                                         [265, 350], [325, 350], [380, 350], [445, 350], [500, 350], [560, 350], [620, 350], [680, 350],
                                         [265, 410], [325, 410], [380, 410], [445, 410], [500, 410], [560, 410], [620, 410], [680, 410],
                                         [265, 470], [325, 470], [380, 470], [445, 470], [500, 470], [560, 470], [620, 470], [680, 470],
                                         [265, 530], [325, 530], [380, 530], [445, 530], [500, 530], [560, 530], [620, 530], [680, 530]])
        # self.board = np.zeros(7*8)
        self.board = np.zeros((8,7))

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
            self.detect_items_on_board(game_board_frame)
            #########################################################
            ################# Reflexia Interpretation ###############
            #########################################################
            game_frame = self.locate_items_on_board(game_frame)
            game_frame = self.detect_turns(game_frame)
            game_frame = self.detect_health(game_frame)
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

    def detect_items_on_board(self, game_board_frame):
        """
        Returns height, width of the maching template & location of the boxes
        """
        top_corner_x, top_corner_y = 0, 0
        SQUARE_SIDE_LENGTH = 59
        for row in range(1,9):
            for column in range(1,8):
                bottom_corner_x, bottom_corner_y = top_corner_x + SQUARE_SIDE_LENGTH, \
                                                   top_corner_y + SQUARE_SIDE_LENGTH
                item = self.get_most_similar_item(game_board_frame,
                                                    top_corner_x,
                                                    top_corner_y,
                                                    bottom_corner_x,
                                                    bottom_corner_y)
                self.board[row-1][column-1] = item
                top_corner_x += SQUARE_SIDE_LENGTH
            top_corner_x = 0
            top_corner_y = row*SQUARE_SIDE_LENGTH

    def locate_items_on_board(self, game_frame):
        for index, position in enumerate(self.board_positions):
            item_id = self.board.T.flatten()[index]
            try:
                iD, item_name, path = self.items_on_board[item_id]
            except:
                item_name = 'UNK'
            cv2.putText(game_frame, item_name,(position[0]-15,position[1]+2),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=2)
            cv2.putText(game_frame, item_name,(position[0]-15,position[1]+2),cv2.FONT_HERSHEY_PLAIN,0.8, (255,0,0), thickness=1)
        return game_frame

    def get_most_similar_item(self, game_board_frame, top_corner_x, top_corner_y, bottom_corner_x, bottom_corner_y):
        cropped_item =  game_board_frame[top_corner_x:bottom_corner_x, top_corner_y:bottom_corner_y]
        img_gray = cv2.cvtColor(cropped_item, cv2.COLOR_BGR2GRAY)
        for item in self.items_on_board:
            iD, name, item_path = self.items_on_board[item]
            template = cv2.imread(item_path, 0)
            width, height = template.shape[::-1]
            maching_locations = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(maching_locations >= 0.6)
            _, _ = locations
            if len(_):
                return iD
        return -1
        
    def detect_turns(self, game_frame):
        lhs = str(1)
        rhs = str(1)
        cv2.putText(game_frame, 'Turns: '+lhs+'/'+rhs,(50,60),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=1)
        return game_frame
    
    def detect_health(self, game_frame):
        hp = str(1)
        cv2.putText(game_frame, 'Health: '+hp+'%',(50,80),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=1)
        return game_frame

if __name__ == '__main__':
    print('> > > Start')
    reflexia = Reflexia()
    reflexia.capture_screen()
    print('< < < End')