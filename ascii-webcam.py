import os, sys, cv2
import curses as c
from textwrap import dedent


win = c.initscr()
#C:\Users\msz\Lewis\cpsc\sprint-08\ASCII-Text-Converter\cat.jpg
dx = 640
dy = 480
density = " .:'\"</~+=§#■╠@▓"
dmap = len(density)



def cr_input(row, col, prompt, win=win): #input function for curses
    c.echo() 
    win.addstr(row, col, prompt)
    win.refresh()
    userinput = win.getstr(row + 1, col, 200)

    return userinput.decode('utf-8')  # .decode('utf-8') converts "bytes object" from win.addstr() into a unicode string compatbile with get_abs_path()



def toAscii(pic, win):
    global operating
    m = 0
    for y in pic:
        tm = max(y)
        if tm > m:
            m = tm

    fx = 0
    fy = 0
    h,w = win.getmaxyx()

    #for y in pic:
        #for x in y:
    for _y in range(h-1):
        for _x in range(w-1):
            y = pic[int(_y/float(h) * len(pic))]
            x = y[int(_x/float(w) * len(y))]

            win.addstr(_y, _x, density[int(x/m*(dmap-1))], c.color_pair(1))
            fx += 1
        fy += 1
        fx = 0
    operating = False



def get_abs_path(path): # checks whether a file is likely to be absolute or relative, if relative finds the absolute form, and returns it. Should work on both mac and windows
    if 'Users' in path or ':' in path: pass 

    else: # path is relative
        dirname = os.path.dirname(__file__) # gets absolute path of ascii-webcam.py
        path = os.path.join(dirname, path) # merges directory tree of this file and the provided relative path to find absolute path of the desired file

    return path



def convert_img(img_path, theme=None):
    img = get_abs_path(img_path)

    img_ascii = cv2.imread(img)
    cv2.imshow('Image', img_ascii)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



def convert_vid(vid_path, theme=None):
    vid = get_abs_path(vid_path)
    win.addstr('\nLoading video ...')
    win.refresh()
    # TODO: Implement video conversion



def show_webcam(mirror=True, theme=None):
    win.addstr('\nLoading camera ...')
    win.addstr('\nPress ESC to close')
    win.refresh()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if mirror: frame = cv2.flip(frame, 1)

        c.init_pair(1, c.COLOR_GREEN, c.COLOR_BLACK)
        gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (dx, int(dx*0.75)))

        toAscii(gray, win)
        win.refresh()

        cv2.imshow('Camera view', frame)

        if cv2.waitKey(1) == 27: break  # esc to quit

    cv2.destroyAllWindows()



def main(win):
    while True:
        c.noecho()
        win.keypad(False)
        win.clear()
        win.refresh()

        win.addstr(0,0, dedent('''
        ###############################
        #                             #
        #        Controls Menu        #
        #                             #
        #         1  =  Image         #
        #         2  =  Video         #
        #         3  =  Webcam        #
        #         4  =  Theme         #       
        #                             #
        ###############################
        '''))

        mode = win.getch()

        if mode == 27: break #esc 

        if mode == int(ord('1')):
            while True:
                img_path = cr_input(12, 0, 'Enter the path to the desired image, or "q" to go back:')
                win.refresh()
                if img_path == 'q': break

                try:
                    convert_img(img_path)
                    break
                except:
                    c.beep()
                    win.addstr(13, 0, 'Error converting image! Try again or enter "q" to go back')
                    win.refresh()


        elif mode == ord('2'):
            while True:
                vid_path = win.getstr('\nEnter the path to the desired video: ')
                if vid_path == '0': break

                try:
                    convert_vid(vid_path)
                    break
                except:
                    win.addstr('\nError converting video! Double check file path, or enter "0" to go back.')
                    win.refresh()


        elif mode == int(ord('3')): 
            show_webcam(win)


        elif mode == ord('4'):
            pass
        # TODO: implement theme changer (green on black), (white on black), (black on white), (blue on red)



c.wrapper(main)

c.endwin()