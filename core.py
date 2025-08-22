import pygame
import time
from coord import tracking_mass, put_on_mass, where_mouse_mass


class othello:
    def __init__(self):
        # setting
        pygame.init()
        self.mass_size = [60, 60]
        self.shift = [120, 30]
        windowX, windowY = 850, 650
        self.font = pygame.font.Font('ipaexg.ttf', 20)
        self.screen = pygame.display.set_mode((windowX, windowY))
        self.RGBdict = {"WHITE": (240, 240, 240), "BLACK": (50, 50, 50), "GREAN": (118, 190, 180)}
        self.evaluation_lst = [
            [ 50, -20, 15, 10, 10, 15, -20, 50],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [15 , -5 , 15,  8,  8, 15,  -5, 15],
            [10 , -5 , 15,  8,  8, 15,  -5, 10],
            [10 , -5 , 15,  8,  8, 15,  -5, 10],
            [15 , -5 , 15,  8,  8, 15,  -5, 15],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 50, -20, 15, 10, 10, 15, -20, 50],
        ]


    def create_board_lst(self):
        board = [
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1 -1 -1 -1],
        ]
        return board


    def set_board(self, board_lst):
        board_lst[3][3] = 1
        board_lst[3][4] = 0
        board_lst[4][3] = 0
        board_lst[4][4] = 1
        return board_lst


    def draw_board_line(self):
        for YC in range(8):
            for XC in range(8):
                put_on_mass(self.screen, self.mass_size, self.shift, XC, YC, (0, 0, 0), "四角")


    def draw_now_board(self, board_lst, search_lst):
        for YC in range(8):
            for XC in range(8):
                if board_lst[YC][XC] == 0:
                    put_on_mass(self.screen, self.mass_size, self.shift, XC, YC, self.RGBdict["BLACK"], "丸")
                elif board_lst[YC][XC] == 1:
                    put_on_mass(self.screen, self.mass_size, self.shift, XC, YC, self.RGBdict["WHITE"], "丸")
                elif board_lst[YC][XC] == -1 and search_lst[YC][XC] > 0:
                    put_on_mass(self.screen, self.mass_size, self.shift, XC, YC, (100, 100, 0), "小四角")


    def put_stone(self, board_lst, color, X, Y):
        putcolor = self.RGBdict["BLACK"] if color == 0 else self.RGBdict["WHITE"]
        if board_lst[Y][X] == -1:
            board_lst[Y][X] = color
            put_on_mass(self.screen, self.mass_size, self.shift, X, Y, putcolor, "丸")
            time.sleep(0.1)
            pass_ = 0
        return board_lst


    def check_change_stone(self, board_lst, color, mode, X, Y):
        opposite_color = self.opposite(color)
        inversion_num = 0
        ng_lst = [-1, 8]
        pies = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        for p in pies:
            check_X,check_Y = X + p[0], Y + p[1]
            if check_X not in ng_lst and check_Y not in ng_lst:
                if board_lst[check_Y][check_X] == opposite_color:
                    while True:
                        check_X += p[0]
                        check_Y += p[1]
                        if check_X in ng_lst or check_Y in ng_lst or board_lst[check_Y][check_X] == -1:
                            break
                        if board_lst[check_Y][check_X] != opposite_color:
                            if mode == "exe":
                                board_lst = self.change_execute(board_lst,color,X,Y,check_X,check_Y,p)
                            elif mode == "cnt":
                                inversion_num += 1
                            break
        return board_lst if mode == "exe" else inversion_num


    def search_can_put_lst(self,board_lst,color):
        result_lst = self.create_board_lst()
        for X in range(8):
            for Y in range(8):
                if board_lst[Y][X] == -1:
                    cnt = self.check_change_stone(board_lst, color, "cnt", X, Y)
                    result_lst[Y][X] = cnt
        return result_lst


    def change_execute(self, board_lst, color, send_X, send_Y, rec_X, rec_Y, direction):
        target_X, target_Y = send_X + direction[0], send_Y + direction[1]
        while (target_X,target_Y) != (rec_X,rec_Y):
            board_lst[target_Y][target_X] = color
            target_X, target_Y = target_X + direction[0], target_Y + direction[1]
        return board_lst


    def opposite(self, color):
        return 0 if color == 1 else 1


    def AI_put_where(self, board_lst, evaluation_lst, color):
        search_lst = self.search_can_put_lst(board_lst, color)
        decide_put = [(-1,-1), -100]
        for Y in range(8):
            for X in range(8):
                if board_lst[Y][X] == -1 and search_lst[Y][X] > 0 and self.check_change_stone(board_lst,color ,"cnt", X, Y) > 0:
                    if decide_put[1] < evaluation_lst[Y][X]:
                        decide_put[0] = (X, Y)
                        decide_put[1] = evaluation_lst[Y][X]

        return decide_put[0]


    def coune_stone(self,board_lst):
        black = 0
        white = 0
        none = 0
        for Y in range(8):
            for X in range(8):
                if board_lst[Y][X] == 0:
                    black += 1
                elif board_lst[Y][X] == 1:
                    white += 1
                else:
                    none += 1
        return black, white, none
    

    def put_judge_num(self, screen, white, black, font, X,Y):
        text1 = font.render(f'YOU: {black}', True, self.RGBdict["BLACK"])
        text2 = font.render(f'COM: {white}', True, self.RGBdict["BLACK"])

        text1 = pygame.transform.scale(text1, (100, 40))
        text2 = pygame.transform.scale(text2, (100, 40))

        screen.blit(text1, (X+40, Y+10))
        screen.blit(text2, (X+40, Y+60))


    def run(self):
        board_lst = self.set_board(self.create_board_lst())
        turn = 0
        player_color = 0
        enemy_color = 1
        now_put_color = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if turn % 2 == 0:
                now_put_color = 0
                search_lst = self.search_can_put_lst(board_lst, now_put_color)
                self.screen.fill(self.RGBdict["GREAN"])
                self.draw_board_line()
                self.draw_now_board(board_lst, search_lst)
                tracking_mass(self.screen, self.mass_size, self.shift)
                X, Y = where_mouse_mass(self.mass_size, self.shift)
                if event.type == pygame.MOUSEBUTTONDOWN and X >= 0 and X < 8 and Y >= 0 and Y < 8 and board_lst[Y][X] == -1:
                    if self.check_change_stone(board_lst, now_put_color, "cnt", X, Y) >= 1:
                        board_lst = self.put_stone(board_lst, now_put_color, X, Y)
                        board_lst = self.check_change_stone(board_lst, now_put_color, "exe", X, Y)
                        turn += 1

                black,white,none = self.coune_stone(board_lst)
                self.put_judge_num(self.screen, white, black, self.font, 600, 30)
                        
                pygame.display.flip()
            else:
                now_put_color = 1
                search_lst = self.search_can_put_lst(board_lst, now_put_color)
                X, Y = self.AI_put_where(board_lst, self.evaluation_lst, enemy_color)
                board_lst = self.put_stone(board_lst, now_put_color, X, Y)
                board_lst = self.check_change_stone(board_lst, now_put_color , "exe", X, Y)
                turn += 1
                pygame.display.flip()


main = othello()
main.run()
