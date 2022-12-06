import os, sys, cv2, curses
from textwrap import dedent

x = 640
y = 480

def convert_img(img_path):

    #############
    img_path = 'C:\\Users\\msz\\Lewis\\cpsc\\sprint-08\\assets\\cat.jpg'
    #############

    if ':' in img_path: # path is absolute
       filename = img_path

    else: # path is relative
        dirname = os.path.dirname(__file__) # gets parent directory that this file is stored in
        filename = os.path.join(dirname, img_path) # uses parent dir to get absolute path of img

    img_ascii = cv2.imread(filename)
    cv2.imshow('Image', img_ascii)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_webcam(mirror=True):
    print('\nLoading Webcam ...')
    cap = cv2.VideoCapture(0)
    print('Press ESC to exit.')

    while True:
        ret, vid = cap.read()

        if mirror: 
            vid = cv2.flip(vid, 1)

        cv2.imshow('Webcam view', vid)

        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

while True:
    mode = input(dedent('''
    1 = convert_img()
    2 = TODO
    3 = show_webcam()
    '''))

    if mode == '1':
        img_path = input('Enter the path to the desired image: ') # At least 2 of the images I tested didn't work, but all of the others did. I couldn't figure out what was causing issues wiht the ones that didn't, they weren't special in any way compared to the others

        try:
            convert_img(img_path)
            break
        except:
            print('\nError convering image! Double check entered file path.')

    elif mode == '2':
        break
        # TODO: Implement video file option

    elif mode == '3':
        show_webcam()
        break

    else: print('INVALID INPUT')