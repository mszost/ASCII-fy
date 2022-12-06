import os, sys, cv2, curses
from textwrap import dedent

# img_path = 'C:\\Users\\msz\\Lewis\\cpsc\\sprint-08\\ASCII-Text-Converter\\assets\\cat.jpg'
# C:\Users\msz\Lewis\cpsc\sprint-08\ASCII-Text-Converter\cat.jpg

# x = 640
# y = 480
# density = " .:'\"</~+=§#■╠@▓"



def get_absolute_path(path): # checks whether a file is likely to be absolute or relative, if relative finds the absolute version, and returns it
    if 'Users' in path or ':' in path: pass 
    
    else: # path is relative
        dirname = os.path.dirname(__file__) # gets absolute path of ascii-webcam.py
        path = os.path.join(dirname, path) # merges directory tree of this file and the provided relative path to find absolute path of the desired file

    return path



def convert_img(img_path, theme=None):
    img = get_absolute_path(img_path)

    img_ascii = cv2.imread(img)
    cv2.imshow('Image', img_ascii)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_vid(vid_path, theme=None):
    vid = get_absolute_path(vid_path)
    print('\nLoading video ...')
    # TODO: Implement video conversion



def show_webcam(mirror=True, theme=None):
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
    ###############################
    #                             #
    #        Controls Menu        #
    #                             #
    #         0  =  QUIT          #
    #         1  =  Image         #
    #         2  =  Video         #
    #         3  =  Webcam        #
    #         4  =  Theme         #       
    #                             #
    ###############################
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


    elif mode == '4':
        pass
    # TODO: implement theme changer (green on black), (white on black), (black on white), (blue on red)


    else: print('INVALID INPUT')