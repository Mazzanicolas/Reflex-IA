from detector import Detector
from mover import Mover

if __name__ == '__main__':

    print('> > > Start > > > ')

    detector = Detector()
    mover = Mover()
    detector.capture_screen(-1)
    board = detector.get_board()
    mover.move(500,500,'up')
    print(board)
    
    print('< < < End < < < ')