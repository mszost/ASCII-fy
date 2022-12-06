import os, sys, cv2, curses
from textwrap import dedent

# x = 640
# y = 480
density = " .:'\"</~+=§#■╠@▓" # if lightmode: density.reverse()
mode = None
img_path = None
vid_path = None


def convert_img(img_path):
    # img_path = 'C:\\Users\\msz\\Lewis\\cpsc\\sprint-08\\ASCII-Text-Converter\\assets\\cat.jpg'
    # C:\Users\msz\Lewis\cpsc\sprint-08\ASCII-Text-Converter\assets\cat.jpg

    if ':' in img_path: # path is absolute
       filename = img_path

    else: # path is relative
        dirname = os.path.dirname(__file__) # gets absolute path of this file
        filename = os.path.join(dirname, img_path) # merges directory tree of this file to find absolute path of the given relative img_path

    img_ascii = cv2.imread(filename)
    cv2.imshow('Image', img_ascii)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_vid(vid_path):
    print('\nLoading video ...')
    # TODO: Implement video conversion


def show_webcam(mirror=True):
    print('\nLoading camera ...')
    cap = cv2.VideoCapture(0)
    print('Press ESC on focused window to close')

    while True:
        ret, frame = cap.read()

        if mirror: frame = cv2.flip(frame, 1)

        cv2.imshow('Camera view', frame)

        if cv2.waitKey(1) == 27: break  # esc to quit
    cv2.destroyAllWindows()



while True:
    mode = input(dedent('''
    ############################
    #                           #
    #        0 = QUIT           #
    #        1 = Image          #
    #        2 = Video          #
    #        3 = Webcam         #
    #                           #
    #############################
    '''))

    if mode == '0': break

    if mode == '1':
        while True:
            img_path = input('\nEnter the path to the desired image: ')# At least 2 of the images I tested didn't work, but all of the others did. I couldn't figure out what was causing issues with the ones that didn't, as they had no noticeable differences from the ones that did work.
            if img_path == '0': break

            try:
                convert_img(img_path)
                break
            except:
                print('\nError converting image! Double check file path, or enter "0" to go back.')

    elif mode == '2':
        while True:
            vid_path = input('\nEnter the path to the desired video: ')
            if vid_path == '0': break

            try:
                convert_vid(vid_path)
                break
            except:
                print('\nError converting video! Double check file path, or enter "0" to go back.')

    elif mode == '3':
        show_webcam()

    else: print('INVALID INPUT')