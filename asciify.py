import os, cv2, time
import curses as c
from textwrap import dedent

#C:\Users\msz\Lewis\cpsc\sprint-08\ASCII-Text-Converter\cat.jpg

cx = 640 # webcam pixels x 
cy = 480 # webcam pixels y 
density = " .:'\"</~+=§#@╠■▓"
dmap = len(density)

win = c.initscr()


# serves as alternative to input() compatible with the curses environment
def cr_input(row, col, prompt, win=win): 
    c.echo() 
    win.addstr(row, col, prompt, theme)
    win.refresh()
    userinput = win.getstr(row + 1, col, 200)
    return userinput.decode('utf-8')  
    # decode('utf-8') converts "bytes object" returned from win.addstr()
    # into a unicode string compatbile with get_abs_path() and other operations



def init_themes():
    # custom color IDs starting at 17. 0-16 are used by curses for basic 8-bit colors 
    c.init_color(17, 875, 790, 670)     # beige
    c.init_color(18, 165, 65, 0)        # brown 
    c.init_color(19, 0, 0, 0)           # black
    c.init_color(20, 1000, 1000, 1000)  # white
    c.init_color(21, 0, 830, 200)       # green
    c.init_color(22, 260, 0, 100)       # maroon
    c.init_color(23, 880, 650, 450)     # pale-orange
    c.init_color(24, 800, 0, 300)       # magenta
    c.init_color(25, 0, 150, 500)       # blue
    c.init_color(26, 350, 250, 0)       # coffee
    c.init_color(27, 150, 1000, 840)    # cyan
    c.init_color(28, 800, 650, 0)       # yelllow-orange
    c.init_color(29, 360, 90, 0)        # red-orange

    # setting up pairs (themes) with the custom color IDs        
    c.init_pair(1, 21, 19)              # matrix
    c.init_pair(2, 26, 19)              # coffee
    c.init_pair(3, 23, 22)              # raspberry
    c.init_pair(4, 17, 18)              # noctua 
    c.init_pair(5, 24, 25)              # vaporwave 
    c.init_pair(6, 28, 29)              # sunset
    c.init_pair(7, 27, 25)              # melange
    c.init_pair(8, 20, 25)              # powershell    



def theme_menu():
    global theme
    win.addstr(dedent(('''
    Enter the number corresponding to the desired terminal theme.

      0  =  Grayscale  ------- ( default       )
      1  =  Matrix  ---------- ( black/green   )
      2  =  Coffee  ---------- ( black/brown   )
      3  =  Raspberry  ------- ( red/pink      )
      4  =  Noctua  ---------- ( brown/beige   )
      5  =  Vaporwave  ------- ( blue/magenta  )
      6  =  Sunset  ---------- ( orange/yellow )
      7  =  Melange  --------- ( blue/cyan     )
      8  =  PowerShell  ------ ( blue/white    )
    ''')))

    win.refresh()
    try: theme = c.color_pair(int(win.getkey()))
    except ValueError: return None
    #TODO: use a text file and the os lib to store theme setting for subsequent program executions



def asciify(frame):
    max_brightness = max(max(row) for row in frame)
    height, width = win.getmaxyx()

    for row in range(height-1):
        for column in range(width-1):

            y = frame[int(row / float(height) * cy)] 
            # y = frame index at [divide row by height, multiply by y camera dimension] 
            # gets current y pixel (the row number that the cursor is at in the frame)

            x = y[int(column / float(width) * cx)]
            # x = row index at [divide column by height, multiply by x camera dimension]
            # gets current x pixel (the column number that the cursor is at in the row y)

            pixel_brightness = x / max_brightness

            win.addstr(row, column, density[int(pixel_brightness * (dmap - 1))], theme)
            # displays the appropriate ASCII character at the current coordinate
            # character is determined by coordinate's brightness



def get_abs_path(path): 
    # Determine if absolute
    if 'Users' in path or ':' in path: pass 

    else: # path is relative
        dirname = os.path.dirname(__file__) 
        path = os.path.join(dirname, path) 
        # gets absolute path of this python file, merges directory tree and
        # the provided relative path to find the absolute path of the desired file
    return path


def convert_img():
    win.addstr('\nSample image: enter "cat.jpg"', theme)

    while True:
        img_path = cr_input(14, 0, 'Enter the path to the desired image, or "q" to go back:')
        win.refresh()
        if img_path == 'q': return None

        try:
            img = get_abs_path(img_path)
            img = cv2.imread(img)
            cv2.imshow('Image', img)
            break
        except: 
            c.beep()
            win.addstr(14, 85, 'Error converting image!', theme)
            win.refresh()


    
        while run_webcam:
            ret, frame = img.read()

            frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (cx, cy)) 
        # convert to grayscale and 640x480

            asciify(frame)

            if win.getch() == 27: 
                run_webcam = False 
    cv2.destroyAllWindows()


    #if cv2.waitKey(0) == 27:
        #cv2.destroyAllWindows()



def convert_vid():
    # TODO: Implement video conversion
    pass



def show_webcam(mirror=True):
    win.nodelay(True)
    win.addstr('\nLoading camera ...', theme)
    win.addstr('\nPress ESC to close', theme)
    win.refresh()

    cap = cv2.VideoCapture(0)
    run_webcam = True

    while run_webcam:
        ret, frame = cap.read()
        if mirror: frame = cv2.flip(frame, 1)

        frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (cx, cy)) 
        # convert to grayscale and 640x480

        asciify(frame)

        if win.getch() == 27: 
            run_webcam = False 
    cv2.destroyAllWindows()



def main(win):
    global theme
    theme = c.color_pair(0)
    init_themes()

    while True:
        c.noecho()
        win.bkgd(' ', theme)
        win.nodelay(False)
        win.keypad(False)
        win.clear()
        win.refresh()

        win.addstr(dedent('''
        ###############################
        #                             #
        #        Controls Menu        #
        #                             #
        #        1  =  Image          #
        #        2  =  Video          #
        #        3  =  Webcam         #
        #        4  =  Themes         #
        #        ESC = Exit           #
        #                             #
        ###############################
        '''), theme)

        mode = win.getch()

        if mode == int(ord('1')):       # TODO
            convert_img()

        elif mode == int(ord('2')):     # TODO
            convert_vid()
        

        elif mode == int(ord('3')): 
            show_webcam()

        elif mode == int(ord('4')):
            theme_menu()

        elif mode == 27: # 27 = esc key 
            break


c.wrapper(main)

win.addstr('\nExiting ...', theme)
win.refresh()
time.sleep(1)
c.endwin()