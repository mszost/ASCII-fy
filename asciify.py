import os, cv2, time
import curses as c
from textwrap import dedent

cx = 640                    # webcam pixels x 
cy = 480                    # webcam pixels y 
density = " .:-=+*#%@"
dmap = len(density)
win = c.initscr()
rfile = open('theme.txt', 'r+')


def init_themes(line = int(rfile.readline())):
    global theme
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

    if line in range(1,9): 
        theme = c.color_pair(line)
    rfile.close()


def theme_menu():
    global theme
    win.addstr(dedent('''
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
    '''))
    win.refresh()

    key = int(win.getkey())
    
    try: 
        theme = c.color_pair(key)
        wfile = open('theme.txt', 'w+')
        wfile.write(str(key))

    except ValueError: return None



def get_abs_path(path): 
    # Determine if absolute, cv2 does not work with relative
    if 'Users' in path or ':' in path: pass 

    else: # path is relative
        dirname = os.path.dirname(__file__)        # gets path of this file, merges it with 
        path = os.path.join(dirname, path)         # provided relative path to get abs path of desired image

    return path



def convert_img():    # Does not convert image yet. Only displays the provided image in a new window
    c.echo()
    while True:
        try:
            win.addstr(dedent('''
            Not fully implemented
            Sample image: "cat.jpg"

            Enter the path to the desired image, or "q" to go back:   '''), theme)
            win.refresh()

            img_path = win.getstr().decode('utf-8')
            if img_path == 'q': return None

            img = cv2.imread(get_abs_path(img_path))
            cv2.imshow('Image', img)
            break

        except: 
            c.beep()
            win.clear()
            win.addstr('\nError converting image! Try again or enter "q" to go back\n', theme)
            win.refresh()


    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()



def convert_vid():
    win.addstr('\nNot yet implemented')
    win.refresh()
    time.sleep(1)



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

        frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (cx, cy), interpolation=cv2.INTER_AREA) 
        # convert feed to grayscale and 640x480

        asciify(frame)
        win.refresh()

        if win.getch() == 27: 
            run_webcam = False 
    cv2.destroyAllWindows()



def asciify(frame):
    max_brightness = max(max(row) for row in frame)
    height, width = win.getmaxyx()          # Image resolution is determined by the size of the terminal. 
                                            # Try using CTRL - or  CTRL + (must be prior to running, though.
    for row in range(height-1):             # It will not work during execution.)
        for column in range(width-1):
            
            y = frame[int(row / float(height) * cy)]                # to get brightness of each pixel, first find the terminal window indicies (x, y) corresponding to camera frame indicies (cx, cy)
            x = y[int(column / float(width) * cx)]                  # !!! the camera/frame and window are most likely different dimensions so they must be scaled w/ the equation:
                                                                    # win index = frame index / win dimensions * frame dimensions
            pixel_brightness = x / max_brightness

            win.addstr(row, column, density[int(pixel_brightness * (dmap - 1))], theme)
            # displays the appropriate ASCII character at the current coordinate



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
        ################################
        #      Welcome to ASCII-fy!    #
        #                              #
        #          Controls:           #
        #         1  =  Image          #
        #         2  =  Video          #
        #         3  =  Webcam         #
        #         4  =  Themes         #
        #         ESC = Exit           #
        #                              #
        ################################
        '''), theme)

        mode = win.getch()

        if mode == int(ord('1')):     
            convert_img()

        elif mode == int(ord('2')):     
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