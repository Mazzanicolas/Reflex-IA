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
                               'star':  (1,'./items/star.png'),   # ID: 1
                               'orb':   (2,'./items/orb.png'),    # ID: 2
                               'potion':(3,'./items/potion.png'), # ID: 3
                               'sword': (4,'./items/sword.png')   # ID: 4
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
        self.board_positions = np.array([[265-233, 175-140], [325-233, 175-140], [380-233, 175-140], [445-233, 175-140], [500-233, 175-140], [560-233, 175-140], [620-233, 175-140], [680-233, 175-140],
                                [265-233, 235-140], [325-233, 235-140], [380-233, 235-140], [445-233, 235-140], [500-233, 235-140], [560-233, 235-140], [620-233, 235-140], [680-233, 235-140],
                                [265-233, 290-140], [325-233, 290-140], [380-233, 290-140], [445-233, 290-140], [500-233, 290-140], [560-233, 290-140], [620-233, 290-140], [680-233, 290-140],
                                [265-233, 350-140], [325-233, 350-140], [380-233, 350-140], [445-233, 350-140], [500-233, 350-140], [560-233, 350-140], [620-233, 350-140], [680-233, 350-140],
                                [265-233, 410-140], [325-233, 410-140], [380-233, 410-140], [445-233, 410-140], [500-233, 410-140], [500-233, 410-140], [620-233, 410-140], [680-233, 410-140],
                                [265-233, 470-140], [325-233, 470-140], [380-233, 470-140], [445-233, 470-140], [500-233, 470-140], [500-233, 470-140], [620-233, 470-140], [680-233, 470-140],
                                [265-233, 530-140], [325-233, 530-140], [380-233, 530-140], [445-233, 530-140], [500-233, 530-140], [500-233, 530-140], [620-233, 530-140], [680-233, 530-140]])
        self.board = np.zeros(7*8)

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
            ###################### Find Potions #####################
            potion_w, potion_h, potion_locations = self.detect_item(game_board_frame, 'potion', threshold=0.75)
            game_frame = self.locate_on_board(game_frame, potion_locations, (0,255,0), 1)
            ###################### Find Swords ######################
            sword_w, sword_h, sword_locations = self.detect_item(game_board_frame, 'sword', threshold=0.75)
            game_frame = self.locate_on_board(game_frame, sword_locations, (255,255,0), 1)
            ####################### Find Stars ######################
            star_w, star_h, star_locations = self.detect_item(game_board_frame, 'star', threshold=0.75)
            game_frame = self.locate_on_board(game_frame, star_locations, (0,255,255), 1)
            ######################## Find Orbs ######################
            orb_w, orb_h, orb_locations = self.detect_item(game_board_frame, 'orb', threshold=0.75)
            game_frame = self.locate_on_board(game_frame, orb_locations, (255,0,255), 1)
            #########################################################
            ################# Reflexia Interpretation ###############
            #########################################################
            cv2.putText(game_frame, 'Potions: '+str(len(potion_locations[0])),(50, 160),cv2.FONT_HERSHEY_PLAIN,1.0, (255,255,255), thickness=1)
            # cv2.putText(game_frame, 'Swords: '+str(len(sword_locations[0])),(50, 180),cv2.FONT_HERSHEY_PLAIN,1.0, (255,255,255), thickness=1)
            # cv2.putText(game_frame, 'Stars: '+str(len(star_locations[0])),(50, 200),cv2.FONT_HERSHEY_PLAIN,1.0, (255,255,255), thickness=1)
            # cv2.putText(game_frame, 'Orbs: '+str(len(orb_locations[0])),(50, 220),cv2.FONT_HERSHEY_PLAIN,1.0, (255,255,255), thickness=1)
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
        mask = np.zeros(game_frame.shape[:2], np.uint8)
        prev_point = (-100, -100)
        for point in zip(*locations[::-1]):
            # cv2.putText(game_frame, str(prev_point[0]-18+25+x)+','+str(prev_point[1]-18+25+y),(prev_point[0]-18+25+x, prev_point[1]-18+25+y),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=1)
            # cv2.putText(game_frame, str(prev_point[0]+18+25+x)+','+str(prev_point[1]+18+25+y),(prev_point[0]+18+25+x, prev_point[1]+18+25+y),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=1)
            # if prev_point[0]-25 < point[0] and point[0] < prev_point[0]+25:
                # prev_point = point
            #     continue
            # if prev_point[1]-25 < point[1] and point[1] < prev_point[1]+25:
                # prev_point = point
            #     continue
            # prev_point = point
            cv2.circle(game_frame, (point[0]+25+x, point[1]+25+y), 10, color, thickness)
            # cv2.putText(game_frame, str(point[0]+25+x)+','+str(point[1]+25+y),(point[0]+25+x, point[1]+25+y),cv2.FONT_HERSHEY_PLAIN,0.8, (255,255,255), thickness=1)
        return game_frame

    def detect_item(self, game_frame, item_name, threshold=0.8):
        """
        Returns height, width of the maching template & location of the boxes
        """
        img_gray = cv2.cvtColor(game_frame, cv2.COLOR_BGR2GRAY)
        iD, item_path = self.items_on_board[item_name]
        template = cv2.imread(item_path, 0)
        width, height = template.shape[::-1]
        maching_locations = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(maching_locations >= threshold)
        # Remove next Duplicates TODO: Remove all duplicates
        # > > > > > > > > > > > > > > > > > > > > > > > > > >
        loc_0, loc_1 = locations
        clean_loc_0  = []
        clean_loc_1  = []
        prev_point = [-100, -100]
        for point in zip(*locations[::-1]):
            if (prev_point[0]-10 < point[0] and point[0] < prev_point[0]+10) and \
               (prev_point[1]-10 < point[1] and point[1] < prev_point[1]+10):
                prev_point = point
                continue
            clean_loc_0.append(point[1])
            clean_loc_1.append(point[0])
            prev_point = point
        locations = (np.array(clean_loc_0), np.array(clean_loc_1))
        # < < < < < < < < < < < < < < < < < < < < < < < < < <
        self.set_positions_on_board(locations, iD)
        return width, height, locations

    def set_positions_on_board(self, locations, iD):
    
        unique_points = self.get_position_on_board(locations)
        np.put(self.board, unique_points, iD)
        print(self.board.reshape((7,8)))

    def get_position_on_board(self, locations):
        distances = []
        positions = []
        # TODO: Use numpy broadcasting 
        for point_found in zip(*locations[::-1]):
            for point_on_board in self.board_positions:
                distance = self.euclidean_distance(point_on_board, point_found)
                distances.append(distance)
            positions.append(np.argmin(np.array(distances)))
            distances = []
        unique_points = np.unique(positions)

        return unique_points
            # distances.append(np.argmin(self.euclidean_distance(point)))
        # print(distances)
        # return 
    
    def euclidean_distance(self, point_1, point_2):
        return np.sqrt(np.sum((np.array([point_2[1], point_2[0]]) - np.array([point_1[1], point_1[0]]))**2))

if __name__ == '__main__':
    print('> > > Start')
    reflexia = Reflexia()
    reflexia.capture_screen()
    print('< < < End')