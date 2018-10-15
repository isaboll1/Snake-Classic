import os
os.environ["PYSDL2_DLL_PATH"] = os.path.dirname(os.path.abspath(__file__))
from sdl2 import *
from sdl2.sdlttf import *
import ctypes
import random

#Snake by Isa Bolling

#GLOBALS
WIDTH = 800
HEIGHT = 600
WALL = False
global DT

#______________________________MAIN_______________________________________

def main():

    SDL_Init(SDL_INIT_EVENTS | SDL_INIT_VIDEO)

    window = SDL_CreateWindow(b'Snake - By Isa Bolling',SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                              WIDTH, HEIGHT, SDL_WINDOW_SHOWN)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    #VARIABLES
    event = SDL_Event()
    running = True
    direction = None
    Movement = False
    game = True
    Fullscreen = False
    Game_Start = True
    Length = 0
    DT = 10

#_____________________________CLASSES______________________________________

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
            #Head Movement
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

            #Body Movement
            for i in range(1, len(self.Body)):
                self.Body[i].update(self.Body[i-1].last_pos[0],
                                    self.Body[i-1].last_pos[1])

            #EDGE_CASES

            if not WALL:
                if self.Head.Rect.y < 2:
                    self.Head.update(self.Head.Rect.x, HEIGHT-25)
                if self.Head.Rect.y > HEIGHT - 25:
                    self.Head.update(self.Head.Rect.x, 2)
                if self.Head.Rect.x < 2:
                    self.Head.update(WIDTH - 25, self.Head.Rect.y)
                if self.Head.Rect.x > WIDTH - 25:
                    self.Head.update(2, self.Head.Rect.y)

        def Timing_Process(self):

            if self.limit == 8 :
                self.Factor += 1

                self.limit = 0
            if self.Factor >= 3:
                self.Factor = 3

        def Increase(self, rate = 6):
            dl = 0
            for i in range(2, rate):
                self.Body.append(Node(self.Body[len(self.Body)-1].last_pos[0],
                                      self.Body[len(self.Body)-1].last_pos[1],
                                      self.size,self.size, (0, 208, 0)))

            self.limit += 1


        def Render(self):
            self.Head = self.Body[0]
            SDL_SetRenderDrawColor(renderer, self.head_color[0], self.head_color[1], self.head_color[2], 255)
            SDL_RenderFillRect(renderer, self.Head.Rect)
            for i in range (1, len(self.Body)):
                SDL_SetRenderDrawColor(renderer, self.body_color[0], self.body_color[1], self.body_color[2], 255)
                SDL_RenderFillRect(renderer, self.Body[i].Rect)

        def Is_Touching_Body(self):
            if len(self.Body) > 2:
                for i in range(2, len(self.Body)):
                    if SDL_HasIntersection(self.Head.Rect, self.Body[i].Rect):
                        return True
            return False

    class Fruit:
        def __init__(self, size = 10, x = 320, y = 400 ):
            self.Color = (255, 0, 0)
            self.Rect = SDL_Rect(x, y, size, size)
            SDL_SetRenderDrawColor(renderer,self.Color[0]
                                           ,self.Color[1],
                                            self.Color[2], 255)

        def update(self, x, y):
            self.Rect.x = x
            self.Rect.y = y

        def Render(self):
            SDL_SetRenderDrawColor(renderer, self.Color[0]
                                           , self.Color[1],
                                             self.Color[2], 255)
            SDL_RenderFillRect(renderer, self.Rect)

# __________________________OBJECTS____________________________________
    BG = Node(0, 0,WIDTH, HEIGHT, (255,255,255))
    SNAKE = Snake(20)
    APPLE = Fruit(20)
#__________________________FUNCTIONS___________________________________

    def Touching_Apple(snake, fruit):
        return SDL_HasIntersection(snake.Head.Rect, fruit.Rect)

    def WindowState(window,renderer, fs):
        if fs == False:
            SDL_SetWindowFullscreen(window, 0)

        elif fs == True:
            SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN_DESKTOP)
            SDL_RenderSetLogicalSize(renderer, WIDTH, HEIGHT)

#__________________________GAME_LOOP_________________________________________

    P_FPS = True
    PerfCountFrequency = SDL_GetPerformanceFrequency()
    LastCounter = SDL_GetPerformanceCounter()

    while(running):
        #print(len(SNAKE.Body))

        if (Movement):
            SNAKE.Movement(direction)
            SNAKE.Timing_Process()

        if  (WALL):
            if (SNAKE.Head.Rect.y < 2):
                Movement = False
                game = False

            if (SNAKE.Head.Rect.y > HEIGHT - 25):
                Movement = False
                game = False

            if (SNAKE.Head.Rect.x < 2):
                Movement = False
                game = False

            if (SNAKE.Head.Rect.x > WIDTH - 25):
                Movement = False
                game = False


        if (SNAKE.Is_Touching_Body()):
            Movement = False
            game = False


        if (Touching_Apple(SNAKE, APPLE)):
            SNAKE.Increase()

            APPLE.update(random.randint(30, WIDTH-30),
                         random.randint(30, HEIGHT-30))
            for i in SNAKE.Body:
                if APPLE.Rect.x - i.Rect.x < 15 and APPLE.Rect.y - i.Rect.y < 15:
                    APPLE.update(random.randint(30, WIDTH - 30),
                                 random.randint(30, HEIGHT - 30))


            Length = len(SNAKE.Body)

    #_____________________RENDER LOOP_____________________________
        SDL_SetRenderDrawColor(renderer, 239, 239, 239, 255)
        SDL_RenderClear(renderer)


        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        SDL_RenderFillRect(renderer, BG.Rect)

        APPLE.Render()
        SNAKE.Render()

        SDL_RenderPresent(renderer)

        if (P_FPS == True):
            EndCounter = SDL_GetPerformanceCounter()
            CounterElapsed = EndCounter - LastCounter
            MSPerFrame = 1000.0 * (CounterElapsed) / (PerfCountFrequency)
            FPS = PerfCountFrequency // CounterElapsed
            print('FPS: ',FPS, 'FRAMETIME: ', MSPerFrame)
            LastCounter = EndCounter

    #____________________EVENT_LOOP_________________________________
        while(SDL_PollEvent(ctypes.byref(event))):

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
                    if Fullscreen == False:
                        Fullscreen = True
                        WindowState(window, renderer, Fullscreen)
                    else:
                        Fullscreen = False
                        WindowState(window, renderer, Fullscreen )

        SDL_Delay(DT)

    SDL_DestroyWindow(window)
    SDL_DestroyRenderer(renderer)
#____________________________________________________________________________
main()