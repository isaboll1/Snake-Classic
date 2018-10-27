import os
os.environ["PYSDL2_DLL_PATH"] = os.path.dirname(os.path.abspath(__file__))
from sdl2 import *
from sdl2.sdlttf import *
import ctypes
import random


# Snake by Isa Bolling

# GLOBALS
WIDTH = 800
HEIGHT = 600
BOUNDS_W = WIDTH
BOUNDS_H = HEIGHT - 60

WALL = True
global DT

# ______________________________MAIN_______________________________________

def main():
    if (TTF_Init() < 0):
        print(TTF_GetError())

    if(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) < 0):
        print(SDL_GetError())

    window = SDL_CreateWindow(b'Snake Classic - By Isa Bolling', SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                              WIDTH, HEIGHT, SDL_WINDOW_SHOWN)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    # VARIABLES
    event = SDL_Event()
    running = True
    direction = None
    Movement = False
    menu = True
    game = False
    Fullscreen = False
    Length = 0
    DT = 10

# _____________________________CLASSES______________________________________
    class Pointer:
        def __init__(self):
            self.pointer = SDL_Rect(0,0,10,10)
            self.clicking = False

        def Compute(self):
            if(event.type == SDL_MOUSEBUTTONDOWN):
                if(event.button.button == SDL_BUTTON_LEFT):
                    self.clicking = True
            if(event.type == SDL_MOUSEBUTTONUP):
                self.clicking = False

            if(event.type == SDL_MOUSEMOTION):
                self.pointer.x = event.motion.x
                self.pointer.y = event.motion.y

        def Is_Touching(self, item):
            return SDL_HasIntersection(self.pointer, item.rect)

        def Is_Clicking(self, item):
            return self.Is_Touching(item) and self.clicking



    class TextObject:
        fonts = dict()
        def __init__(self, text, width, height, font_name,color = (0,0,0), location = (0, 0),
                                                                            font_size = 36):
            if len(font_name) > 1:
                TextObject.fonts[font_name[0]] = TTF_OpenFont(font_name[1], font_size)
            self.color = SDL_Color(color[0], color[1], color[2])
            self.surface = TTF_RenderText_Solid(TextObject.fonts[font_name[0]], text.encode('utf-8'), self.color)
            self.message = SDL_CreateTextureFromSurface(renderer, self.surface)
            SDL_FreeSurface(self.surface)
            self.rect = SDL_Rect(location[0], location[1], width, height)
            self.highlight = False

        def Render(self, x = None, y = None):
            if self.highlight:
                SDL_SetRenderDrawColor(renderer, self.color.r, self.color.g, self.color.b, self.color.a)
                SDL_RenderDrawRect(renderer, self.rect)
            if x is None and y:
                self.rect.y = y
            elif x and y is None:
                self.rect.x = x
            elif x and y:
                self.rect.x = x
                self.rect.y = y
            SDL_RenderCopy(renderer, self.message, None, self.rect)

        def __del__(self):
            SDL_DestroyTexture(self.message)
            for key in TextObject.fonts:
                TTF_CloseFont(TextObject.fonts[key])


    class Node:
        def __init__(self, x, y, w, h, color):
            self.current_pos = (x, y)
            self.last_pos = (x, y)
            self.Rect = SDL_Rect(x, y, w, h)
            SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], 255)
            SDL_RenderFillRect(renderer, self.Rect)

        def update(self, x, y):
            self.last_pos = (self.current_pos[0], self.current_pos[1])
            self.current_pos = (x, y)
            self.Rect.x = x
            self.Rect.y = y

    class Snake:
        def __init__(self, size = 20, x = 100, y = 100, headcolor = (0, 255, 0)):
            self.size = size
            self.Body = [Node(x, y, self.size, self.size, (0, 240, 0)),
                         Node(x-size, y, self.size, self.size, (0, 255, 0))]
            self.Head = self.Body[0]
            self.Timer = 0
            self.limit = 0
            self.Factor = 2
            self.head_color = headcolor
            self.body_color = [0, 0, 0]
            for i in range(len(headcolor)):
                if headcolor[i] == 255:
                    self.body_color[i] = 208

        def Movement(self, direction):
            # Head Movement
            self.Timer += self.Factor
            if direction == 'Left' :
                if self.Timer >= 10:
                    self.Head.update(self.Head.Rect.x - self.size, self.Head.Rect.y)
                    self.Timer = 0
            elif direction == 'Right':
                if self.Timer >= 10:
                    self.Head.update(self.Head.Rect.x + self.size, self.Head.Rect.y)
                    self.Timer = 0
            elif direction == 'Up':
                if self.Timer >= 10:
                    self.Head.update(self.Head.Rect.x, self.Head.Rect.y - self.size)
                    self.Timer = 0
            elif direction == 'Down':
                if self.Timer >= 10:
                    self.Head.update(self.Head.Rect.x, self.Head.Rect.y + self.size)
                    self.Timer = 0

            # Body Movement
            for i in range(1, len(self.Body)):
                self.Body[i].update(self.Body[i-1].last_pos[0],
                                    self.Body[i-1].last_pos[1])

            # EDGE_CASES

            if not WALL:
                if self.Head.Rect.y < 2:
                    self.Head.update(self.Head.Rect.x, BOUNDS_H-25)
                if self.Head.Rect.y > BOUNDS_H - 25:
                    self.Head.update(self.Head.Rect.x, 2)
                if self.Head.Rect.x < 2:
                    self.Head.update(BOUNDS_W - 25, self.Head.Rect.y)
                if self.Head.Rect.x > BOUNDS_W - 25:
                    self.Head.update(2, self.Head.Rect.y)

        def Timing_Process(self):

            if self.limit == 8:
                self.Factor += 1

                self.limit = 0
            if self.Factor >= 3:
                self.Factor = 3

        def Increase(self, rate = 6):
            dl = 0
            for i in range(2, rate):
                self.Body.append(Node(self.Body[len(self.Body)-1].last_pos[0],
                                      self.Body[len(self.Body)-1].last_pos[1],
                                      self.size, self.size, (0, 208, 0)))

            self.limit += 1


        def Render(self):
            self.Head = self.Body[0]
            SDL_SetRenderDrawColor(renderer, self.head_color[0], self.head_color[1], self.head_color[2], 255)
            SDL_RenderFillRect(renderer, self.Head.Rect)
            for i in range(1, len(self.Body)):
                SDL_SetRenderDrawColor(renderer, self.body_color[0], self.body_color[1], self.body_color[2], 255)
                SDL_RenderFillRect(renderer, self.Body[i].Rect)

        def Is_Touching_Body(self):
            if len(self.Body) > 2:
                for i in range(2, len(self.Body)):
                    if SDL_HasIntersection(self.Head.Rect, self.Body[i].Rect):
                        return True
            return False

        def __del__(self):
            for node in self.Body:
                SDL_free(node)

    class Fruit:
        def __init__(self, size = 10, x = 320, y = 400 ):
            self.Color = (255, 0, 0)
            self.Rect = SDL_Rect(x, y, size, size)
            SDL_SetRenderDrawColor(renderer, self.Color[0], self.Color[1], self.Color[2], 255)

        def update(self, x, y):
            self.Rect.x = x
            self.Rect.y = y

        def Render(self):
            SDL_SetRenderDrawColor(renderer, self.Color[0]
                                           , self.Color[1],
                                             self.Color[2], 255)
            SDL_RenderFillRect(renderer, self.Rect)

# __________________________OBJECTS____________________________________
    mouse = Pointer()
    BG = Node(0, 0, BOUNDS_W, BOUNDS_H, (255, 255, 255))
    Title = TextObject('Snake  Classic', 400, 220, ['arcade',b'font/arcade.ttf'], (239,239,239))
    MenuItems = {
        'Fullscreen':TextObject('Fullscreen', 150, 100, ['arcade'],(239,239,239),(100, 350)),
        'Start'     :TextObject('Start', 100, 100, ['arcade'], (239, 239, 239), (350, 350)),
        'Quit'      :TextObject('Quit', 100, 100, ['arcade'], (239,239,239), (550, 350))
    }

    SNAKE = Snake(20)
    APPLE = Fruit(20)
# __________________________FUNCTIONS___________________________________

    def Touching_Apple(snake, fruit):
        return SDL_HasIntersection(snake.Head.Rect, fruit.Rect)

    def WindowState(window,renderer, fs):
        if not fs:
            SDL_SetWindowFullscreen(window, 0)

        elif fs:
            SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN_DESKTOP)
            SDL_RenderSetLogicalSize(renderer, WIDTH, HEIGHT)

# __________________________GAME_LOOP_________________________________________

    P_FPS = True
    PerfCountFrequency = SDL_GetPerformanceFrequency()
    LastCounter = SDL_GetPerformanceCounter()

    while(running):
        #print(len(SNAKE.Body))
        if menu:
            BG.Rect.y = 30

            for item in MenuItems:
                if mouse.Is_Touching(MenuItems[item]):
                    MenuItems[item].highlight = True
                else:
                    MenuItems[item].highlight = False

            if mouse.Is_Clicking(MenuItems['Start']):

                menu = False
                game = True
                BG.Rect.y = 0

            if mouse.Is_Clicking(MenuItems['Fullscreen']):
                if Fullscreen is False:
                    Fullscreen = True
                    WindowState(window, renderer, Fullscreen)
                else:
                    Fullscreen = False
                    WindowState(window, renderer, Fullscreen)

            if mouse.Is_Clicking(MenuItems['Quit']):
                running = False
                break

            SDL_SetRenderDrawColor(renderer, 239, 239, 239, 255)
            SDL_RenderClear(renderer)

            SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
            SDL_RenderFillRect(renderer, BG.Rect)
            for key in MenuItems:
                MenuItems[key].Render()
            Title.Render(200, 100)

            SDL_RenderPresent(renderer)

        if game:
            if (Movement):
                SNAKE.Movement(direction)
                SNAKE.Timing_Process()

            if (WALL):
                if (SNAKE.Head.Rect.y < 2):
                    Movement = False
                    game = False

                if (SNAKE.Head.Rect.y > BOUNDS_H - 25):
                    Movement = False
                    game = False

                if (SNAKE.Head.Rect.x < 2):
                    Movement = False
                    game = False

                if (SNAKE.Head.Rect.x > BOUNDS_W - 25):
                    Movement = False
                    game = False


            if (SNAKE.Is_Touching_Body()):
                Movement = False
                game = False


            if (Touching_Apple(SNAKE, APPLE)):
                SNAKE.Increase()

                APPLE.update(random.randint(30, BOUNDS_W-60),
                             random.randint(30, BOUNDS_H-30))
                for i in SNAKE.Body:
                    if APPLE.Rect.x - i.Rect.x < 15 and APPLE.Rect.y - i.Rect.y < 15:
                        APPLE.update(random.randint(30, BOUNDS_W - 60),
                                     random.randint(30, BOUNDS_H - 30))


                Length = len(SNAKE.Body)

        # _____________________RENDER LOOP_____________________________
            SDL_SetRenderDrawColor(renderer, 239, 239, 239, 255)
            SDL_RenderClear(renderer)

            SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
            SDL_RenderFillRect(renderer, BG.Rect)

            APPLE.Render()
            SNAKE.Render()

            SDL_RenderPresent(renderer)

        if (P_FPS):
            EndCounter = SDL_GetPerformanceCounter()
            CounterElapsed = EndCounter - LastCounter
            MSPerFrame = 1000.0 * (CounterElapsed) / (PerfCountFrequency)
            FPS = PerfCountFrequency // CounterElapsed
            print('FPS: ', FPS, 'FRAMETIME: ', MSPerFrame)
            LastCounter = EndCounter

    # ____________________EVENT_LOOP_________________________________
        while(SDL_PollEvent(ctypes.byref(event))):
            mouse.Compute()

            if(event.type == SDL_QUIT):
                running = False
                break

            if(event.type == SDL_KEYDOWN):
                if game:
                    Movement = True

                    if(event.key.keysym.scancode == SDL_SCANCODE_LEFT):
                        if direction != "Right":
                            direction = "Left"
                    elif(event.key.keysym.scancode == SDL_SCANCODE_RIGHT):
                        if direction != "Left":
                            direction = "Right"
                    elif (event.key.keysym.scancode == SDL_SCANCODE_UP):
                        if direction != "Down":
                            direction = "Up"
                    elif (event.key.keysym.scancode == SDL_SCANCODE_DOWN):
                        if direction != "Up":
                            direction = "Down"

                if (event.key.keysym.scancode == SDL_SCANCODE_ESCAPE):
                    running = False
                    break

                if(event.key.keysym.scancode == SDL_SCANCODE_F12):
                    if Fullscreen is False:
                        Fullscreen = True
                        WindowState(window, renderer, Fullscreen)
                    else:
                        Fullscreen = False
                        WindowState(window, renderer, Fullscreen)

        SDL_Delay(DT)

    SDL_DestroyWindow(window)
    SDL_DestroyRenderer(renderer)
    SDL_Quit()
    TTF_Quit()

    return 0
# ____________________________________________________________________________

main()
