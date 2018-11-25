from PIL import ImageGrab
import numpy as np
import win32gui
import cv2


window_position = win32gui.FindWindow(None, r'Mirror')
window_dimensions = win32gui.GetWindowRect(window_position)
distance_left, distance_top, window_width, window_height = window_dimensions
cropped_window_dimensions = (distance_left+5,
                            distance_top+26,
                            window_width-2,
                            window_height-3)
game_frame = ImageGrab.grab(cropped_window_dimensions)
game_frame = np.array(game_frame)
ix,iy = -1,-1
# Mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),1,(255,0,0),2)
        ix,iy = x,y

# Create a black image, a window and bind the function to window
img = game_frame
cv2.namedWindow('Frame Debugger')
cv2.setMouseCallback('Frame Debugger',draw_circle)

while True:
    cv2.imshow('Frame Debugger',img)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('a'):
        print(ix,iy)
cv2.destroyAllWindows()