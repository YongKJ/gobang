# coding=gbk

import SpecifiedStart
import queue
import ChessBoard
import random
import copy
import SaveInfoToDB
import NoobRobot
import ForbidStep
import time


class CentralControl(object):

    def __init__(self):
        self.Robot_gobang_type = 0  # �����˵����������ͣ��������壩
        self.gobang_step_now = 0  # ��ʱ�ֵ��������������ɫ
        self.Opening_type = 0  # ���ɿ��ֻ�ָ������
        self.free_start_forbid_choice = 0  # ���ɿ����Ƿ����ý��ֵ��ж�
        self.free_three_change = 1  # �����ѡ����ֲ������ɿ���ʱ��Ĭ�Ͽ���ѯ���Ƿ�ѡ�����ֽ���
        self.gobang_board = []  # ����
        self.gobang_board_switch = False  # �Ƿ�ѡ���ֶ����뿪������
        self.gobang_chess_total = 0  # ���������ӵ�����
        self.round = 0  # �ڼ��أ�����������һ��Ϊһ�أ�
        self.Robot_input_stack = queue.LifoQueue()  # �����������ջ
        self.Player_input_stack = queue.LifoQueue()  # ��������ջ
        self.gobang_board_stack = queue.LifoQueue()  # ���̶�ջ������ר�ã�

        # ָ�����ֲ���Ҫ��ʼ��
        self.five_step_switch = False  # �Ƿ�ѡ������N��
        self.five_step_num = 0  # ����N�������
        self.three_step_change = False  # �Ƿ����ֽ���
        self.specified_start_type = ""  # бָ���ֻ�ֱָ����
        self.specified_start_name = ""  # 26��ָ��������ĳ��ֵ�����
        self.specified_start_priority = []  # 26��ָ��������ĳ��ֵ����ȼ�

        self.victory = False

        self.saveToTxt = []

    def gobang_board_quit(self):  # �˳�

        now1 = time.strftime("%H%M%S", time.localtime())
        now2 = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        filePath = "D://fivechess//save" + str(now1) + ".txt"
        with open(filePath, 'w') as f:
            if self.gobang_chess_total != 225:
                if self.gobang_step_now == 1:
                    win = "����ʤ]["
                else:
                    win = "����ʤ]["
            else:
                win = "����]["
            if self.Robot_gobang_type == 1:
                name = "[�˵������������][���ֶ�������]["
            else:
                name = "[���ֶ�������][�˵������������]["

            out = "{[C5]" + name + win + str(now2) + " ���������ѧ][2019 CCGC];"

            num = 1
            l = len(self.saveToTxt)
            for row, col in self.saveToTxt:
                if num % 2 == 1:
                    out += "B"
                else:
                    out += "W"
                x = chr(ord("A") + col)
                y = 14 - row + 1
                out += "(" + str(x) + "," + str(y) + ")"
                if num != l:
                    out += ";"
                num += 1

            out += "}"
            f.write(out)

        self.operation()

        # exit()

    def quit(self):
        Save = SaveInfoToDB.SaveInfoToDB()
        if self.Opening_type == 1:  # ��������Ϣ���浽���ݿ�
            Save.Save_regular_start_info_to_db(self.Robot_gobang_type, self.Opening_type, self.five_step_switch,
                                               self.five_step_num, self.three_step_change,
                                               self.specified_start_type,
                                               self.specified_start_name, self.specified_start_priority,
                                               self.Robot_input_stack, self.Player_input_stack,
                                               self.gobang_board_stack)
        else:
            Save.Save_free_start_info_to_db(self.Robot_gobang_type, self.Opening_type, self.Robot_input_stack,
                                            self.Player_input_stack, self.gobang_board_stack)
        exit()

    def operation(self):
        now, robot = self.gobang_step_now, self.Robot_gobang_type
        choose = input("����������Ҫ�Ĳ���(U:����, Q:�˳�):")
        if choose.upper() == "Q":
            self.quit()
        else:
            self.gobang_board_undo_second()  # ����
            self.show_the_gobang_board_now(self.gobang_board)  # ��ʾ���̾���
            if now == 1:
                if robot == 1:
                    self.robot_move()
                else:
                    self.player_move()
            else:
                if robot == 2:
                    self.robot_move()
                else:
                    self.player_move()

    def gobang_board_undo(self):  # ����
        self.gobang_chess_total -= 2  # ���������ӵ���������
        # ������ջ
        self.Robot_input_stack.get()
        self.Player_input_stack.get()
        for i in range(2):
            self.gobang_board_stack.get()
        self.saveToTxt.pop()
        self.saveToTxt.pop()
        self.gobang_board = self.gobang_board_stack.get()
        self.gobang_board_stack.put(copy.deepcopy(self.gobang_board))

    def gobang_board_undo_second(self):  # ����
        robot, now = self.Robot_gobang_type, self.gobang_step_now
        self.gobang_chess_total -= 3  # ���������ӵ���������
        # ������ջ
        if now == 1 and robot == 1 or (now == 2 and robot == 2):
            self.Robot_input_stack.get()
            self.Player_input_stack.get()
            self.Robot_input_stack.get()
        else:
            self.Player_input_stack.get()
            self.Robot_input_stack.get()
            self.Player_input_stack.get()

        for i in range(3):
            self.gobang_board_stack.get()
        self.saveToTxt.pop()
        self.saveToTxt.pop()
        self.saveToTxt.pop()
        self.gobang_board = self.gobang_board_stack.get()
        self.gobang_board_stack.put(copy.deepcopy(self.gobang_board))

    def show_the_gobang_board_now(self, board):  # ��ʾ��ʱ�����̾���
        # _board, open, robot = copy.deepcopy(board), self.Opening_type, self.Robot_gobang_type
        # turn, free_forbid = self.gobang_step_now, self.free_start_forbid_choice
        _board, turn = copy.deepcopy(board), self.gobang_step_now
        total = self.gobang_chess_total

        # if (open == 1 or (open == 2 and free_forbid == 1)) and robot == 1:
        if total != 0:
            noobrobot = NoobRobot.NoobRobot()  # ��������˳�ʼ��
            noobrobot.board = board  # ��������˵����̾����ʼ��
            moves = noobrobot.genmove_second(turn)

            forbid_step = ForbidStep.ForbidStep()
            forbid_step.board = board
            for score, row, col in moves:
                if forbid_step.deal_noobrobot_move(row, col):
                    _board[row][col] = -1

        self.update_round()
        UI = ChessBoard.ChessBoard()
        UI.out_gobang_board(self.round, _board)

    def update_round(self):  # ���µڼ���
        if self.gobang_chess_total % 2 == 1:
            self.round = self.gobang_chess_total // 2 + 1
        else:
            self.round = self.gobang_chess_total // 2

    def gobang_type_choose(self):  # ѡ���Ⱥ���
        print("��ѡ�����ֻ��ߺ���(����Bѡ�����֣�����Wѡ�����):")
        gobang_type = input()
        if gobang_type.upper() == "B":
            self.Robot_gobang_type = 2
        else:
            self.Robot_gobang_type = 1

    def free_board_handle_input(self):
        board = [[0 for n in range(15)] for m in range(15)]  # ���̾����ʼ��
        pos = []
        print("�������������ӵ�����(����һ�����ݣ��ո����)��")
        pos = input().split()
        if len(pos) == 3:
            for i in range(3):
                x = ord(pos[i][0].upper()) - ord("A")
                y = ord(pos[i][1].upper()) - ord("A")
                if 0 <= x < 15 and 0 <= y < 15:
                    if i == 1:
                        board[x][y] = 2
                        move_list = [x, y]
                        self.saveToTxt.append(move_list)
                    else:
                        board[x][y] = 1
                        move_list = [x, y]
                        self.saveToTxt.append(move_list)
                else:
                    print("���ӵ����������������������ӵ����ꡣ")
                    board = self.free_board_handle_input()
        else:
            print("����������������������������������ӵ����ꡣ")
            board = self.free_board_handle_input()

        return board

    def free_gobang_start_init(self):  # ���ɿ��ֳ�ʼ��
        robot, switch = self.Robot_gobang_type, self.five_step_switch

        open = 2  # ���ɿ���
        round = 1  # ��һ��
        five = 0

        print("��ѡ���Ƿ���Ҫ����N��(����Y/N):")  # �Ƿ�ѡ���ʼ������N��
        five_str = input()
        if five_str.upper() == "Y":
            switch = True  # ѡ������N��

        if robot == 1:  # �����ת����
            now = 2  # �ֵ��������

            if switch:
                # five = random.randint(2, 5)  # �����������N�������
                five = 2
                print("���������ѡ�������N�������Ϊ%d" % five)

            board = [[0 for n in range(15)] for m in range(15)]  # ���̾����ʼ��
            board[7][7] = 1  # ��������������ֵ�һ������
            total = 1  # ��������������Ϊ1
            step_list = [7, 7]
            self.stack_push(step_list)  # ����������ջ
        else:  # �����ת����
            now = 1  # �ֵ��������

            if switch:
                print("��ѡ������N�����������ɷ�ʽ(����Aѡ���Զ����ɣ�����Hѡ���ֶ�����):")  # ����N���ʼ��
                choose_type = input()
                if choose_type.upper().upper() == "A":
                    five = random.randint(2, 5)  # �����������N�������
                    print("������ɵ�����N������Ϊ%d" % five)
                else:
                    print("����������N�������(������һ������):")
                    five = int(input())  # �ֶ���������N�������

            print("��ѡ���Ƿ���Ҫ�ֶ����뿪������(����Y/N):")
            choose_type = input()
            if choose_type.upper().upper() == "Y":
                self.gobang_board_switch = True
                now = 2
                board = self.free_board_handle_input()
                total = 3
            else:
                board = [[0 for n in range(15)] for m in range(15)]  # ���̾����ʼ��
                total = 0  # ��������������Ϊ0

        self.Opening_type, self.gobang_step_now, self.five_step_switch = open, now, switch
        self.gobang_board, self.gobang_chess_total, self.round = copy.deepcopy(board), total, round
        self.five_step_num = five
        self.show_the_gobang_board_now(board)  # ��ʾ��ʱ�����̾���

    def regular_start_gobang_toTxt(self):
        board = self.gobang_board

        x1, y1 = 7, 7
        x2, y2 = 0, 0
        x3, y3 = 0, 0

        for i in range(15):
            for j in range(15):
                if board[i][j] == 2:
                    x2, y2 = i, j
                elif board[i][j] == 1 and not (i == 7 and j == 7):
                    x3, y3 = i, j

        self.saveToTxt.append([x1, y1])
        self.saveToTxt.append([x2, y2])
        self.saveToTxt.append([x3, y3])

    def regular_gobang_start_init(self):  # ָ�����ֳ�ʼ��
        switch, five, type = self.five_step_switch, 0, ""
        robot, black, white = self.Robot_gobang_type, 1, 2

        open = 1  # ָ������
        round = 2  # �ڶ���
        total = 3  # ��������������Ϊ3
        specified_start = SpecifiedStart.SpecifiedStart()

        print("��ѡ���Ƿ���Ҫ����N��(����Y/N):")  # �Ƿ�ѡ���ʼ������N��
        five_str = input()
        if five_str.upper() == "Y":
            switch = True  # ѡ������N��

        if robot == black:  # ��������ѡ�����ʱ�ĳ�ʼ��
            now = white  # �ֵ��°���
            if switch:
                # five = random.randint(2, 5)  # �����������N�������
                five = 2
                print("���������ѡ�������N�������Ϊ%d" % five)
            board = specified_start.random_read_db(robot)  # �������ֱ�ӿ����е����̾���
        else:  # ��������ѡ�����ʱ�ĳ�ʼ��
            now = white  # �ֵ��°���
            if switch:
                print("��ѡ������N�����������ɷ�ʽ(����Aѡ���Զ����ɣ�����Hѡ���ֶ�����):")  # ����N���ʼ��
                choose_type = input()
                if choose_type.upper().upper() == "A":
                    five = random.randint(2, 5)  # �����������N�������
                    print("������ɵ�����N������Ϊ%d" % five)
                else:
                    print("����������N�������(������һ������):")
                    five = int(input())  # �ֶ���������N�������

            print("��ѡ�񿪾ֵ����ɷ�ʽ(����Aѡ���Զ����ɣ�����Hѡ���ֶ�����):")  # ָ���������ͳ�ʼ��
            start_type = input()
            if start_type.upper() == "A":
                board = specified_start.random_read_db(robot)  # �������26��ָ�������е�һ��
            else:
                board = specified_start.hand_read_db()  # �ֶ�ѡ��26��ָ�������е�һ��

        if specified_start.get_start_type() == "inclined":  # �����Ϣ��ʼ��
            type = "бָ����"
        else:
            type = "ֱָ����"
        name = specified_start.get_start_name()  # ���ָ����������
        priority = specified_start.get_priority()  # ���ָ���������ȼ�

        out_str = ""
        if priority[0] == '0':
            out_str += "(ƽ��)"
        elif priority[0] == '1':
            out_str += "(����"
        else:
            out_str += "(����"

        if priority[1] == '1':
            out_str += "ƫ�ţ�"
        elif priority[1] == '2':
            out_str += "���ƣ�"
        elif priority[1] == '3':
            out_str += "��ʤ��"

        print(type + ":" + name + "��" + out_str)

        self.gobang_board_stack.put(copy.deepcopy(board))  # ���̾�����ջ
        self.Opening_type, self.round, self.gobang_chess_total = open, round, total
        self.gobang_board, self.gobang_step_now, self.five_step_num = copy.deepcopy(board), now, five
        self.specified_start_type, self.specified_start_name, self.specified_start_priority = type, name, priority
        self.five_step_switch = switch
        self.regular_start_gobang_toTxt()
        self.show_the_gobang_board_now(board)  # ��ʾ���̾���

    def opening_type_choose(self):  # ѡ�񿪾ַ�ʽ
        print("��ѡ�񿪾ַ�ʽ(����Rѡ��ָ�����֣�����Fѡ�����ɿ���):")
        opening_type = input()
        if opening_type.upper().upper() == "F":
            print("��ѡ���Ƿ����ý��ֵ��ж�(����Y/N):")
            choice = input()  # ѡ���Ƿ������ֵ��ж�
            if choice.upper() == "Y":
                self.free_start_forbid_choice = 1
            self.free_gobang_start_init()  # �������ɿ��ֳ�ʼ������
        else:
            self.regular_gobang_start_init()  # ����ָ�����ֳ�ʼ������

    def get(self, row, col):  # ���ص�ǰλ�õ�����
        board = self.gobang_board

        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return board[row][col]

    # �ж���Ӯ������0������Ӯ����1������Ӯ����2������Ӯ��
    def check(self):
        board = self.gobang_board
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))  # �ĸ�������б����ֱ����б��ˮƽ
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    continue
                id = board[i][j]  # ���������ɫ
                for d in dirs:  # �����ĸ�����
                    x, y = j, i
                    count = 0
                    for k in range(5):
                        if self.get(y, x) != id:  # �������Ƿ񹹳�5��ͬɫ��������һ��
                            break
                        y += d[0]
                        x += d[1]
                        count += 1
                    if count == 5:
                        return id
        return 0

    def player_move(self):  # ����ƶ�����
        open, total, robot = self.Opening_type, self.gobang_chess_total, self.Robot_gobang_type
        now, board, switch = self.gobang_step_now, self.gobang_board, self.five_step_switch
        round, black, white = self.round, 1, 2

        # if open == 1 and total == 4 and switch:
        # print(total, switch,"$$$$$$$$$$$$$")
        if total == 4 and switch:
            self.deal_five_step()  # ָ�����֣�������������4������ʱ��ʼ��������N����

        if open == 2 and total == 3 and now == white and self.free_three_change == 1 and not self.gobang_board_switch:
            print("��ѡ���Ƿ����ֽ���(����Y/N)��")
            choose = input()  # ���ɿ��֣���������3�����ӣ���ʱ�ֵ��°��壬���ɿ��ֵ����ֽ���ѡ����Ϊһ
            if choose.upper() == "Y":
                self.Robot_gobang_type = 2  # ���ֽ���������ɺ��ֱ�Ϊ����
                self.robot_move()  # �ֵ�����������°���
            else:
                self.free_three_change = 0  # ���û�н������ֽ������������Ϊ0�����´β���ѯ������Ƿ�ѡ�����ֽ���
                self.player_move()  # �ֵ�����°���

        player_input = input("�����������ƶ���λ��(U:����, Q:�˳�):")  # ����������������
        if len(player_input) > 2:
            print("��������ݲ��Ϸ������������룡")
            self.player_move()  # ���������������
        elif len(player_input) == 2:  # ����Ƿ�������������ĸ���ɵ�����
            x = ord(player_input[0].upper()) - ord("A")  # ת������
            y = ord(player_input[1].upper()) - ord("A")

            if now == black:  # ��ʱ�º���
                if 0 <= x <= 14 and 0 <= y <= 14:  # �����Ƿ�Ϸ�
                    if board[x][y] == 0:  # �жϵ�ǰ�����Ƿ�Ϊ��
                        board[x][y] = black  # ���Ϊ����
                    else:  # ��ǰ���겻Ϊ��
                        print("�����ƶ�������")
                        self.player_move()  # ���������������
                        return 0
                else:  # ���겻�Ϸ�
                    print("�����߽�")
                    self.player_move()  # ���������������
                    return 0

                self.judge_victory(x, y)
                now = white  # �ֵ��°���

            else:  # ��ʱ�°���
                if 0 <= x <= 14 and 0 <= y <= 14:  # �����Ƿ�Ϸ�
                    if board[x][y] == 0:  # �жϵ�ǰ�����Ƿ�Ϊ��
                        board[x][y] = white  # ���Ϊ����
                    else:  # ��ǰ���겻Ϊ��
                        print("�����ƶ�������")
                        self.player_move()  # ���������������
                        return 0
                else:  # ���겻�Ϸ�
                    print("�����߽�")
                    self.player_move()  # ���������������
                    return 0

                self.judge_victory(x, y)
                now = black  # �ֵ��º���

            player_move_list = [x, y]
            self.saveToTxt.append(player_move_list)
            self.stack_push(player_move_list)  # ������ջ

            total += 1  # ����������������1

        elif player_input.upper() == "U":  # ��������д��ĸU���л������
            if open == 2:  # �Ƿ����ɿ���
                if round < 3:  # С��3�ֲ��û���
                    print("\nָ�����ֵ�����غϵ���3�أ���������壡")
                    self.show_the_gobang_board_now(board)  # ��ʾ���̾���
                    self.player_move()  # �����������
                else:
                    self.gobang_board_undo()  # ����
                    self.show_the_gobang_board_now(self.gobang_board)  # ��ʾ���̾���
                    self.player_move()  # ����������ֵ��������
            else:  # ָ������
                if round < 5:  # С��5�ֲ��û���
                    print("\nָ�����ֵ�����غϵ���5�أ���������壡")
                    self.show_the_gobang_board_now(board)  # ��ʾ���̾���
                    self.player_move()  # �����������
                else:
                    self.gobang_board_undo()  # ����
                    self.show_the_gobang_board_now(self.gobang_board)  # ��ʾ���̾���
                    self.player_move()  # ����������ֵ��������
        else:  # ���������ĸQ�����˳�����
            self.quit()  # ��������Ϣ�������ݿⲢ�˳�

        self.gobang_step_now, self.Robot_gobang_type, self.gobang_chess_total = now, robot, total
        self.show_the_gobang_board_now(board)  # ��ʾ���̾���
        self.robot_move()  # �ֵ��������������

    def robot_move(self):  # �������ƶ�����
        open, total, board = self.Opening_type, self.gobang_chess_total, self.gobang_board
        now, choice, switch = self.gobang_step_now, self.free_start_forbid_choice, self.five_step_switch
        robot, free_fobid = self.Robot_gobang_type, self.free_start_forbid_choice

        # if open == 1 and total == 4 and switch:
        # print(total, switch,"$$$$$$$$$$$$$")
        if total == 4 and switch:
            self.deal_five_step()  # ָ�����֣�������������4������ʱ��ʼ��������N����

        print("�������������˼��...")
        DEPTH = 4  # ��������ȳ�ʼ��
        noobrobot = NoobRobot.NoobRobot()  # ��������˳�ʼ��
        noobrobot.board = board  # ��������˵����̾����ʼ��
        noobrobot.Opening_type = open  # ��������˵Ŀ������;����ʼ��
        noobrobot.Robot = self.Robot_gobang_type
        noobrobot.free_fobid = self.free_start_forbid_choice

        start = time.time()
        score, row, col = noobrobot.search(now, DEPTH)  # �������������ֺ�����ƶ�λ������

        end = time.time()

        second = int(end - start)
        min = second // 60
        sec = second % 60

        x = chr(ord("A") + row)
        y = chr(ord("A") + col)
        out_str = ""
        # out_str += "����������ƶ���  " + x + y + " (" + str(score) + ") (" + str(min) + "min" + str(sec) + "sec)"
        if min != 0:
            out_str += "����������ƶ���  " + x + y + " (" + str(min) + " min " + str(sec) + " sec)"
        else:
            out_str += "����������ƶ���  " + x + y + " (" + str(sec) + " sec)"

        if now == 1:  # ��ʱ�Ƿ��º���
            board[row][col] = 1  # ���Ϊ����

            if (open == 1 or choice == 1) and robot != 1:  # ָ�����ֻ����ɿ��ֽ��ֵ��ʾΪ1����н��ֵ��ж�
                self.check_forbid_step()  # ���ֵ��ж�

            print(out_str)  # �����������˵��ƶ�λ������

            self.judge_victory(row, col)
            now = 2  # �ֵ��°���
        else:  # ��ʱ�°���
            board[row][col] = 2  # ���Ϊ����

            if open == 1 or choice == 1:  # ָ�����ֻ����ɿ��ֽ��ֵ��ʾΪ1����н��ֵ��ж�
                self.check_forbid_step()  # ���ֵ��ж�

            print(out_str)  # �����������˵��ƶ�λ������

            self.judge_victory(row, col)
            now = 1  # �ֵ��º���

        robot_move_list = [row, col]
        self.saveToTxt.append(robot_move_list)
        self.stack_push(robot_move_list)  # ������ջ

        total += 1  # ����������������1

        self.gobang_step_now, self.gobang_chess_total = now, total
        self.show_the_gobang_board_now(board)  # ��ʾ���̾���
        self.player_move()  # �ֵ��������

    def judge_victory(self, row, col):
        open, choice, board = self.Opening_type, self.free_start_forbid_choice, self.gobang_board
        total, robot = self.gobang_chess_total, self.Robot_gobang_type
        black, white = 1, 2

        if (self.check() == black and robot == black) or (self.check() == white and robot == white):  # �жϰ����Ƿ񹹳�����
            self.show_the_gobang_board_now(board)  # ��ʾ���̾���
            print("���ź��������ˣ�")
            self.saveToTxt.append([row, col])
            self.stack_push([row, col])
            self.victory = True
            self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�
        elif (self.check() == black and robot == white) or (self.check() == white and robot == black):  # �жϺ����Ƿ񹹳�����
            self.show_the_gobang_board_now(board)  # ��ʾ���̾���
            # print(self.check(), robot)
            print("��ϲ�ˣ���Ӯ�ˣ�")
            self.saveToTxt.append([row, col])
            self.stack_push([row, col])
            self.victory = True
            self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�
        elif self.check() == 0 and total == 225:  # �ж��Ƿ����
            print("WOW!��������")
            self.saveToTxt.append([row, col])
            self.stack_push([row, col])
            self.victory = True
            self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�

    def stack_push(self, move_input):  # �����ˣ�����µ����Լ���ǰ�����ջ
        now, robot, board = self.gobang_step_now, self.Robot_gobang_type, self.gobang_board

        if now != robot:  # ��ʱ�µ��岻�ǲ��������ѡ�����������
            self.Robot_input_stack.put(copy.deepcopy(move_input))  # �������������������ջ
        else:  # ��ʱ�µ��岻�����ѡ�����������
            self.Player_input_stack.put(copy.deepcopy(move_input))  # �������������ջ
        self.gobang_board_stack.put(copy.deepcopy(board))  # ���̾�����ջ

    def deal_five_step(self):  # ����N��
        robot, five, now = self.Robot_gobang_type, self.five_step_num, self.gobang_step_now
        board, total = self.gobang_board, self.gobang_chess_total

        noobrobot = NoobRobot.NoobRobot()  # ��������˳�ʼ��
        noobrobot.board = board  # ��������˵����̾����ʼ��

        if robot == 1:  # ��ʱ����������Ƿ�Ϊ����
            pos = noobrobot.deal_robot_five_step(five, now)  # ��ò��������ѡ�������N���λ������POS����
            num = 1  # ���λ������POS����
            out_str = ""
            for score, i, j in pos:
                x = chr(ord("A") + i)
                y = chr(ord("A") + j)
                out_str += str(num) + "." + x + y
                if num == five:
                    out_str += "\n"
                else:
                    out_str += " "
                num += 1
            out_str += "\n" + "��ѡ���������˵�����" + str(five) + "���ƶ�λ�õı��:"
            print(out_str)

            pos_num = int(input())  # ��Ҵ�POS������ѡ����ʵ�λ������
            score, row, col = pos[pos_num - 1]
            board[row][col] = 1  # ���Ϊ����
            robot_move_list = [row, col]
            self.saveToTxt.append(robot_move_list)
            self.stack_push(robot_move_list)  # ������ջ

            now = 2  # �ֵ��°���
            total += 1  # ����������������1

            self.gobang_step_now, self.gobang_chess_total = now, total
            self.show_the_gobang_board_now(board)  # ��ʾ���̾���
            self.player_move()  # �ֵ��������

        else:  # ��ʱ���Ϊ����
            print("�������������%d��(����һ�����ݣ��ո����)��" % five)
            pos = []
            pos = input().split()  # �����������N���λ������
            moves = []
            if len(pos) != five:  # �ж�λ�����������Ƿ��㹻
                print("���������������%d����ƶ�λ�������������������룡" % five)
                self.deal_five_step()  # ��������
                return 0
            for i in range(five):
                x = ord(pos[i][0].upper()) - ord("A")
                y = ord(pos[i][1].upper()) - ord("A")
                if 0 <= x <= 14 and 0 <= y <= 14:  # �ж������Ƿ�Ϸ�
                    if board[x][y] == 0:  # �ж������Ƿ�Ϊ��
                        moves.append((x, y))  # ������moves����
                    else:  # ���겻Ϊ��
                        print("����������������ƶ�λ�ã��������룡")
                        self.deal_five_step()  # ��������
                        return 0
                else:  # ����λ�ò��Ϸ�
                    print("������������ƶ�λ���д������������룡")
                    self.deal_five_step()  # ��������
                    return 0

            row, col = noobrobot.deal_player_five_step(moves, now)  # ����������������N��moves����
            x = chr(ord("A") + row)
            y = chr(ord("A") + col)
            s = ""
            s += x + y
            print("���������ѡ���������%d����ƶ�λ��Ϊ (%s)" % (five, s))
            board[row][col] = 1  # ���Ϊ����
            player_move_list = [row, col]
            self.saveToTxt.append(player_move_list)
            self.stack_push(player_move_list)  # ������ջ

            now = 2  # �ֵ��°���
            total += 1  # ����������������1

            self.gobang_step_now, self.gobang_chess_total = now, total
            self.show_the_gobang_board_now(board)  # ��ʾ���̾���
            self.robot_move()  # �ֵ��������������

    def check_forbid_step(self):  # ���ֵ���жϣ������������֣����Ľ��֣���������
        board = self.gobang_board
        CheckStep = ForbidStep.ForbidStep()
        CheckStep.board = board  # �����жϽ��ֵ�����̾����ʼ��
        for i in range(15):
            for j in range(15):
                if board[i][j] == 1:  # �ж��Ƿ�Ϊ����
                    flag = CheckStep.charge_three_forbid(i, j)
                    if flag:  # �ж��Ƿ�Ϊ�������ֵ�
                        row = chr(ord("A") + i)
                        col = chr(ord("A") + j)
                        s = ""
                        s += row + col
                        print("�ܲ��Ұ���������˵��װ�Ľ��ֵ㣡����е��������ֵ�Ϊ (%s) �������ˣ�" % (s))
                        self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�

                    flag = CheckStep.charge_four_forbid(i, j)
                    if flag:  # �ж��Ƿ�Ϊ���Ľ���
                        row = chr(ord("A") + i)
                        col = chr(ord("A") + j)
                        s = ""
                        s += row + col
                        print("�ܲ��Ұ���������˵��װ�Ľ��ֵ㣡����е����Ľ��ֵ�Ϊ (%s) �������ˣ�" % (s))
                        self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�

                    flag = CheckStep.charge_long_forbid(i, j)
                    if flag:  # �ж��Ƿ�Ϊ��������
                        board = self.gobang_board_stack.get()
                        self.gobang_board_stack.put(copy.deepcopy(board))
                        if board[i][j] == 0:
                            row = chr(ord("A") + i)
                            col = chr(ord("A") + j)
                            s = ""
                            s += row + col
                            print("�ܲ��Ұ���������˵��װ�Ľ��ֵ㣡����еĳ������ֵ�Ϊ (%s) �������ˣ�" % (s))
                            self.gobang_board_quit()  # ��������Ϣ�������ݿⲢ�˳�
        return 0

    def gobang_go(self):  # ��ֳ�ʼ����ʼ����
        robot, open, priority = self.Robot_gobang_type, self.Opening_type, self.specified_start_priority,
        total, now, board = self.gobang_chess_total, self.gobang_step_now, self.gobang_board

        if robot == 1 and open == 1:  # ����������Ƿ�Ϊ���ֲ��ҿ�������Ϊָ������
            print("��ѡ���Ƿ����ֽ���(����Y/N)��")
            choose = input()  # ��������Ƿ����ֽ���
            if choose.upper() == "Y":
                self.Robot_gobang_type = 2  # ��������˱�Ϊ����
                self.robot_move()  # �ֵ��������������
            else:  # ��Ҳ�ѡ�����ֽ���
                self.player_move()  # �ֵ��������

        elif robot == 2 and open == 1:  # ����������Ƿ�Ϊ���ֲ��ҿ�������Ϊָ������
            print("���������˼���Ƿ����ֽ���...")
            if priority[0] == "1":  # �ж�ָ�������е�������ȼ��Ƿ�Ϊ��������
                print("���������ѡ�񽻻��Ⱥ���")
                self.Robot_gobang_type = 1  # ��������˱�Ϊ����
                self.player_move()  # �ֵ��������
            else:  # ָ�������е�������ȼ�Ϊ��������
                print("��������˾����������Ⱥ���")
                self.robot_move()  # �ֵ��������������

        elif robot == 1 and open == 2:  # ����������Ƿ�Ϊ���ֲ��ҿ�������Ϊ���ɿ���
            self.player_move()  # �ֵ��������

        elif robot == 2 and open == 2:  # ����������Ƿ�Ϊ���ֲ��ҿ�������Ϊ���ɿ���
            if total == 3:
                print("���������˼���Ƿ����ֽ���...")
                noobrobot = NoobRobot.NoobRobot()  # ��������˳�ʼ��
                noobrobot.board = board  # ��������˵����̾����ʼ��
                if noobrobot.judge_free_three_change(now):
                    print("���������ѡ�񽻻��Ⱥ���")
                    self.Robot_gobang_type = 1
                    self.player_move()
                else:
                    print("��������˾����������Ⱥ���")
                    self.robot_move()
            else:
                self.player_move()  # �ֵ��������

        self.Robot_gobang_type = robot

if __name__ == "__main__":
    s = CentralControl()
    s.gobang_type_choose()
    s.opening_type_choose()
    s.gobang_go()
