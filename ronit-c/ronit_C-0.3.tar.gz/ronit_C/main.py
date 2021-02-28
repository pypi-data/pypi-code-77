import pygame
import time

pygame.init()
import random
from functools import reduce
import pyautogui

class Ronit:
    class Colors:
        def BLACK(*args):
            if args == ():
                return (0, 0, 0)

        def WHITE(*args):
            if args == ():
                return (255,255,255)

        def RED(*args):
            if args == ():
                return (255, 0, 0)
            else:
                return (70, 0, 0)

        def BLUE(*args):
            if args == ():
                return (0, 0, 255)
            else:
                return (0, 0, 70)

        def GREEN(*args):
            if args == ():
                return (0, 255, 0)
            else:
                return (0, 70, 0)

        def CUSTOM(*args):
            return args

    def write(text):
        return text

    def geo(shape, area_or_circumference, *args):
        if shape == "triangle" and area_or_circumference == "area":
            v = args[0] * args[1] / 2
            return v
        elif shape == "triangle" and area_or_circumference == "circumference":

            v = args[0] + args[1] + args[2]
            return v
        elif shape == "square" and area_or_circumference == "area":
            v = args[0] * args[0]
            return v
        elif shape == "square" and area_or_circumference == "circumference":
            v = args[0] * 4
            return v
        elif shape == "circle" and area_or_circumference == "area":
            v = args[0] * args[0] * 3.14
            return v
        elif shape == "circle" and area_or_circumference == "circumference":
            v = args[0] * 2 * 3.14
            return v

    def Cow(*self):
        Ronit.write("https://www.youtube.com/watch?v=rRPQs_kM_nw&t=86s")

    def LCM(x, y):
        if x > y:
            greater = x
        else:
            greater = y
        while (True):
            if ((greater % x == 0) and (greater % y == 0)):
                lcm = int(greater)
                break
            greater += 1
            return greater



    def GCD(x, y):

        while (y):
            x, y = y, x % y
        return x

    def ND(x, y):
        for nums in range(x, y + 1):
            for nm in range(x, y + 1):
                if nums % nm == 0:
                    print(str(nums) + " is divided by:" + str(nm))

    def rand(*args):

        if args == ():
            b = random.random()
            return b
        else:
            a = random.randint(args[0], args[1])
            return a
    def sqrt(base, multiplayer):
        return base ** multiplayer

    def shoresh(num):
        for i in range(num):
            if i*i == num:
                return i
                break


    def calculate(peoola, *args):

        if peoola == "-":
            return reduce(lambda a, b: a - b, args)

        if peoola == "*":
            return reduce(lambda a, b: a * b, args)

        if peoola == "%":
            return reduce(lambda a, b: a % b, args)

        if peoola == "/":
            return reduce(lambda a, b: a / b, args)

        if peoola == "+":
            return reduce(lambda a, b: a + b, args)

    def play(game):
        if game == "snake":
            print("---- the project was created by: https://github.com/rajatdiptabiswas/snake-pygame ----")
            import sys
            difficulty = 25
            frame_size_x = 720
            frame_size_y = 480
            check_errors = pygame.init()
            if check_errors[1] > 0:
                print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
                sys.exit(-1)
            else:
                print('[+] Game successfully initialised')
            pygame.display.set_caption('Snake Eater')
            game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
            black = pygame.Color(0, 0, 0)
            white = pygame.Color(255, 255, 255)
            red = pygame.Color(255, 0, 0)
            green = pygame.Color(0, 255, 0)
            blue = pygame.Color(0, 0, 255)
            fps_controller = pygame.time.Clock()
            snake_pos = [100, 50]
            snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
            food_spawn = True
            direction = 'RIGHT'
            change_to = direction
            score = 0

            def game_over():
                my_font = pygame.font.SysFont('times new roman', 90)
                game_over_surface = my_font.render('YOU DIED', True, red)
                game_over_rect = game_over_surface.get_rect()
                game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
                game_window.fill(black)
                game_window.blit(game_over_surface, game_over_rect)
                show_score(0, red, 'times', 20)
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                sys.exit()

            def show_score(choice, color, font, size):
                score_font = pygame.font.SysFont(font, size)
                score_surface = score_font.render('Score : ' + str(score), True, color)
                score_rect = score_surface.get_rect()
                if choice == 1:
                    score_rect.midtop = (frame_size_x / 10, 15)
                else:
                    score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
                game_window.blit(score_surface, score_rect)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == ord('w'):
                            change_to = 'UP'
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                            change_to = 'DOWN'
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                            change_to = 'LEFT'
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                            change_to = 'RIGHT'
                        if event.key == pygame.K_ESCAPE:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
                if change_to == 'UP' and direction != 'DOWN':
                    direction = 'UP'
                if change_to == 'DOWN' and direction != 'UP':
                    direction = 'DOWN'
                if change_to == 'LEFT' and direction != 'RIGHT':
                    direction = 'LEFT'
                if change_to == 'RIGHT' and direction != 'LEFT':
                    direction = 'RIGHT'
                if direction == 'UP':
                    snake_pos[1] -= 10
                if direction == 'DOWN':
                    snake_pos[1] += 10
                if direction == 'LEFT':
                    snake_pos[0] -= 10
                if direction == 'RIGHT':
                    snake_pos[0] += 10
                snake_body.insert(0, list(snake_pos))
                if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                    score += 1
                    food_spawn = False
                else:
                    snake_body.pop()
                if not food_spawn:
                    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
                                random.randrange(1, (frame_size_y // 10)) * 10]
                food_spawn = True
                game_window.fill(black)
                for pos in snake_body:
                    pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
                if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
                    game_over()
                if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
                    game_over()
                for block in snake_body[1:]:
                    if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                        game_over()
                show_score(1, white, 'consolas', 20)
                pygame.display.update()
                fps_controller.tick(difficulty)

    def screenshot(path, name, hhhh):
        time.sleep(hhhh)

        myScreenshot = pyautogui.screenshot()

        myScreenshot.save(path + name)

    def sort(the_list, *args):
        if args == ():
            return the_list.sort()
        elif args[0] == "reverse ":
            return the_list.sort(reverse=True)

    def DrawCube(x, y, width, height, color, *args):

        screen = pygame.display.set_mode((800, 600))
        # *args can be (background color)

        run = True
        while run:
            if args != ():
                screen.fill(args[0])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5:
                        run = False

            pygame.draw.rect(screen, color, [x, y, width, height])
            pygame.display.update()




    def TrackMousePosY(*args):
        pygame.display.set_mode((800, 600))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            x, m_y = pygame.mouse.get_pos()
    class draw:
        def screen(width, hight):
            global a
            a = pygame.display.set_mode((width, hight))
        def background_color(color):
            a.fill(color)

        def run(important):
            if important:
                return True
            else:
                return False
        def QUIT(*args):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Ronit.draw.run(False)

    def TrackMousePosX(*args):
        pygame.display.set_mode((800, 600))
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.QUIT:
                    run = False

            m_x, y = pygame.mouse.get_pos()

    def event(*args):
        pygame.event.get()
    def TrackMousePos(*args):
        pygame.display.set_mode((800, 600))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.QUIT:
                    run = False

            x, y = pygame.mouse.get_pos()
    def help(*args):
        if args == ():
            print('all the available functions in "Ronit_C" are: \n Ronit_C.write = write the text that you input \n Ronit_C.geo = calculate the area or the circumference of a shape' )
            print(' Ronit_C.LCM(number, second number) = calculate the least common multiplier')
            print(' Ronit_C.GCD(number, second number) = calculate the greater common divider')
            print(' Ronit_C.sort(list) = returning the list that you input but sorted')
            print(' Ronit_C.ND(number) = Shows all the natural dividers of a range of numbers')
            print(' Ronit_C.rand(number, second number) = generate a random number ')
            print(' Ronit_C.calculate([+,-,*,/], all the numbers)')
            print(' Ronit_C.screenshot = take a screenshot of your screen!')
            Ronit.write(' Ronit_C.DrawCube(x, y, width, height, color) = opens a new window and draws a cube')

        else:
            print("TypeError: when you are typing Ronit_C.help() you cant enter parameters")
    def RIP(*args):
        Ronit.write("thank you!")
    def f(*args):
        Ronit.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    def Rap(*args):
        Ronit.write("https://www.youtube.com/watch?v=47ZSI7nPAqo")


    def ask(text):
        return input(text)


    def make_me_a_coffe(*args):
        if args != ():
            print("ValueError")
        else:
            print("take the coffee!")



# Traceback (most recent call last):
#   File "C:\Users\forec\PycharmProjects\ronit_lang\ronit_testing.py", line 11, in <module>
#     Ronit_C.help()
#   File "C:\Users\forec\PycharmProjects\ronit_lang\main.py", line 346, in help
#     Ronit_C.type("all the functions are:", Ronit_C.Colors.BLACK(), Ronit_C.Colors.WHITE(), screen, 400,300)
# TypeError: type() takes 6 positional arguments but 7 were given