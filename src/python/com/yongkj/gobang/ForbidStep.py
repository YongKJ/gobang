# coding=gbk

import copy
import ChessBoard


class ForbidStep(object):

    def __init__(self):
        self.board = [[0 for n in range(15)] for i in range(15)]
        self.total = 0

        # ��������
        # ����ͨ��������������
        self.ThreeThree = []
        self.ThreeThree_blank = []

        self.ThreeFirst = []
        self.ThreeSecond = []
        self.ThreeBlank = []

        self.FourFour = []

        self.FourFirst = []
        self.FourSecond = []

        self.produce_position()
        self.produce_threethree()
        self.produce_forufour()

        self.FourFour1 = [[0, 0, 1], [1, 0, 1], [2, 0, 0], [3, 0, 1], [-1, 0, 1], [-2, 0, 0], [-3, 0, 1]]
        self.FourFour.append(self.FourFour1)

        self.FourFour2 = [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 0], [4, 0, 1], [-1, 0, 0], [-2, 0, 1]]
        self.FourFour.append(self.FourFour2)

        self.FourFour3 = [[0, 0, 1], [-1, 0, 1], [-2, 0, 1], [-3, 0, 0], [-4, 0, 1], [1, 0, 0], [2, 0, 1]]
        self.FourFour.append(self.FourFour3)

        self.FourFour4 = [[0, 0, 1], [1, 0, 0], [2, 0, 1], [3, 0, 1], [-1, 0, 1], [-2, 0, 0], [-3, 0, 1], [-4, 0, 1]]
        self.FourFour.append(self.FourFour4)

        self.FourFour5 = [[0, 0, 1], [1, 0, 0], [2, 0, 1], [3, 0, 1], [4, 0, 1], [5, 0, 2],
                          [-1, 0, 0], [-2, 0, 1], [-3, 0, 1], [-4, 0, 1], [-5, 0, 2]]
        self.FourFour.append(self.FourFour5)

        # ��������
        self.LongLong = []
        self.LongLong1 = [[0, 0, 1], [0, 1, 1], [0, -1, 1], [0, -2, 1], [0, -3, 1], [0, -4, 1]]
        self.LongLong.append(self.LongLong1)

        self.LongLong2 = [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1], [-1, 0, 1], [-2, 0, 1]]
        self.LongLong.append(self.LongLong2)

        self.LongLong3 = [[0, 0, 1], [1, 0, 1], [2, 0, 1], [-1, 0, 1], [-2, 0, 1], [-3, 0, 1]]
        self.LongLong.append(self.LongLong3)

        self.LongLong4 = [[0, 0, 1], [-1, 0, 1], [-2, 0, 1], [-3, 0, 1], [-4, 0, 1], [-5, 0, 2], [1, 0, 1]]
        self.LongLong.append(self.LongLong4)

        self.LongLong5 = [[0, 0, 1], [-1, 0, 1], [-2, 0, 1], [-3, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1]]
        self.LongLong.append(self.LongLong5)

    def left_move(self, moves, sum):
        num = 0
        while True:
            turn = 0
            for m in moves:
                m[0] -= 1
                if m[0] == 0 and m[1] == 0:
                    turn = m[2]
            if turn == 1:
                num += 1
            if num == sum:
                break
        return moves

    def bottom_move(self, moves, sum):
        for k in range(2):
            for i in range(len(moves)):
                x = moves[i][0]
                y = moves[i][1]
                x1, y1 = self.get_spin_pos(x, y)
                moves[i][0] = x1
                moves[i][1] = y1
        num = 0
        while True:
            turn = 0
            for m in moves:
                m[1] -= 1
                if m[0] == 0 and m[1] == 0:
                    turn = m[2]
            if turn == 1:
                num += 1
            if num == sum:
                break
        return moves

    def push_three_three(self, row, col):
        ThreeFirst = self.ThreeFirst
        ThreeSecond = self.ThreeSecond
        ThreeBlank = self.ThreeBlank
        TF = []
        TS = []
        TB = []
        for r in range(len(row)):
            if row[r][0] == 0 and row[r][1] == 0:
                continue
            if r == 0 or r == len(row) - 1:
                TB.append(row[r])
            else:
                TF.append(row[r])
        for c in range(len(col)):
            if col[c][0] == 0 and col[c][1] == 0:
                continue
            if c == 0 or c == len(col) - 1:
                TB.append(col[c])
            else:
                TS.append(col[c])
        ThreeFirst.append(TF)
        ThreeSecond.append(TS)
        ThreeBlank.append(TB)

    def push_four_four(self, row, col):
        FourFirst = self.FourFirst
        FourSecond = self.FourSecond
        FF = []
        FS = []
        for r in range(len(row)):
            if row[r][0] == 0 and row[r][1] == 0:
                continue
            FF.append(row[r])
        for c in range(len(col)):
            if col[c][0] == 0 and col[c][1] == 0:
                continue
            FS.append(col[c])
        FourFirst.append(FF)
        FourSecond.append(FS)

    def produce_position(self):
        TheThree = []
        TheThree.append([[-1, 0, 0], [0, 0, 0], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 0], [5, 0, 0]])
        TheThree.append([[0, 0, 0], [1, 0, 1], [2, 0, 1], [3, 0, 0], [4, 0, 1], [5, 0, 0]])
        TheThree.append([[0, 0, 0], [1, 0, 1], [2, 0, 0], [3, 0, 1], [4, 0, 1], [5, 0, 0]])
        TheThreeFour = []
        TheThreeFour.append([[0, 0, 0], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1], [5, 0, 0]])
        TheFour = []
        TheFour.append([[0, 0, 0], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1], [5, 0, 0]])
        TheFour.append([[1, 0, 1], [2, 0, 0], [3, 0, 1], [4, 0, 1], [5, 0, 1]])
        TheFour.append([[1, 0, 1], [2, 0, 1], [3, 0, 0], [4, 0, 1], [5, 0, 1]])
        TheFour.append([[1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 0], [5, 0, 1]])
        for i in range(len(TheThree)):
            for j in range(i, len(TheThree)):
                for n in range(3):
                    row = self.left_move(copy.deepcopy(TheThree[i]), n + 1)
                    for m in range(3):
                        col = self.bottom_move(copy.deepcopy(TheThree[j]), m + 1)
                        self.push_three_three(row, col)
        for i in range(len(TheFour)):
            for j in range(i, len(TheFour)):
                for n in range(4):
                    row = self.left_move(copy.deepcopy(TheFour[i]), n + 1)
                    for m in range(4):
                        col = self.bottom_move(copy.deepcopy(TheFour[j]), m + 1)
                        self.push_four_four(row, col)
        # print()

    def produce_forufour(self):
        FourFour = self.FourFour
        FourFirst = self.FourFirst
        FourSecond = self.FourSecond
        for i in range(len(FourFirst)):
            for k in range(8):
                a1 = FourSecond[i][0][0]
                a2 = FourSecond[i][0][1]
                b1 = FourSecond[i][1][0]
                b2 = FourSecond[i][1][1]
                n1 = b2 - a2
                n2 = b1 - a1
                for j in range(len(FourFirst[i])):
                    x = FourFirst[i][j][0]
                    y = FourFirst[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    FourFirst[i][j][0] = x1
                    FourFirst[i][j][1] = y1
                c1 = FourFirst[i][0][0]
                c2 = FourFirst[i][0][1]
                m1 = c2 - b2
                m2 = c1 - b1
                k1 = n1 * m2
                k2 = n2 * m1
                if k1 != k2:
                    FourFour1 = []
                    for j in range(len(FourFirst[i])):
                        FourFour1.append(FourFirst[i][j])
                    for j in range(len(FourSecond[i])):
                        FourFour1.append(FourSecond[i][j])
                    FourFour1.sort()
                    FourFour1.insert(0, [0, 0, 1])
                    flag = True
                    for j in range(len(FourFour)):
                        if FourFour[j] == FourFour1:
                            flag = False
                    if flag:
                        FourFour.append(copy.deepcopy(FourFour1))

    def produce_threethree(self):
        ThreeThree = self.ThreeThree
        ThreeThree_blank = self.ThreeThree_blank
        ThreeFirst = copy.deepcopy(self.ThreeFirst)
        ThreeSecond = copy.deepcopy(self.ThreeSecond)
        ThreeBlank = copy.deepcopy(self.ThreeBlank)
        for i in range(len(ThreeFirst)):
            for k in range(8):
                a1 = ThreeSecond[i][0][0]
                a2 = ThreeSecond[i][0][1]
                b1 = ThreeSecond[i][1][0]
                b2 = ThreeSecond[i][1][1]
                n1 = b2 - a2
                n2 = b1 - a1
                for j in range(len(ThreeFirst[i])):
                    x = ThreeFirst[i][j][0]
                    y = ThreeFirst[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    ThreeFirst[i][j][0] = x1
                    ThreeFirst[i][j][1] = y1
                for j in range(2):
                    x = ThreeBlank[i][j][0]
                    y = ThreeBlank[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    ThreeBlank[i][j][0] = x1
                    ThreeBlank[i][j][1] = y1
                c1 = ThreeFirst[i][0][0]
                c2 = ThreeFirst[i][0][1]
                m1 = c2 - b2
                m2 = c1 - b1
                k1 = n1 * m2
                k2 = n2 * m1
                if k1 != k2:
                    ThreeThree1 = []
                    ThreeThree1_blank = []
                    for j in range(len(ThreeFirst[i])):
                        ThreeThree1.append(ThreeFirst[i][j])
                    for j in range(len(ThreeSecond[i])):
                        ThreeThree1.append(ThreeSecond[i][j])
                    for j in range(len(ThreeBlank[i])):
                        ThreeThree1_blank.append(ThreeBlank[i][j])
                    ThreeThree1.sort()
                    ThreeThree1.insert(0, [0, 0, 1])
                    flag = True
                    for j in range(len(ThreeThree)):
                        if ThreeThree[j] == ThreeThree1:
                            flag = False
                    if flag:
                        ThreeThree.append(copy.deepcopy(ThreeThree1))
                        ThreeThree_blank.append(copy.deepcopy(ThreeThree1_blank))
                        # l = len(ThreeFirst)
                        # if i == l - 1:
                        #     self.test3(ThreeThree1)

        # print(len(ThreeThree))
        # print()

    def get_spin_pos(self, x, y):  # ������ʱ����ת45�Ⱥ�������
        if x == 0 or y == 0:
            row = x - y
            col = x + y
        else:
            row = (x - y) // 2
            col = (x + y) // 2
        return row, col

    def judge_the_pos(self, row, col, pos):  # �жϵ�ǰλ���Ƿ����Ͻ��ֵ���Ҫ��
        x = row - pos[1]
        y = col + pos[0]
        if 0 <= x <= 14 and 0 <= y <= 14:
            if self.board[x][y] == pos[2]:
                return True
        return False

    def judge_the_pos_blank(self, row, col, pos1, pos2):  # �жϻ������������ߵĿո��Ƿ����Ϲ��ɻ�����Ҫ��
        x1 = row - pos1[1]
        y1 = col + pos1[0]
        x2 = row - pos2[1]
        y2 = col + pos2[0]
        if 0 <= x1 <= 14 and 0 <= y1 <= 14 and 0 <= x2 <= 14 and 0 <= y2 <= 14:
            if self.board[x1][y1] == pos1[2] or self.board[x2][y2] == pos2[2]:
                return True
        elif 0 <= x1 <= 14 and 0 <= y1 <= 14 and not (0 <= x2 <= 14 and 0 <= y2 <= 14):
            if self.board[x1][y1] == pos1[2]:
                return True
        elif not (0 <= x1 <= 14 and 0 <= y1 <= 14) and 0 <= x2 <= 14 and 0 <= y2 <= 14:
            if self.board[x2][y2] == pos2[2]:
                return True
        return False

    def charge_three_forbid(self, row, col):  # �ж���������
        ThreeThree = copy.deepcopy(self.ThreeThree)
        ThreeThree_bank = copy.deepcopy(self.ThreeThree_blank)

        for i in range(len(ThreeThree)):
            for k in range(8):  # ��ת8�Σ�ÿ����ʱ��ѡ��45��

                for j in range(len(ThreeThree[i])):  # �����������ֵ�������ת
                    x = ThreeThree[i][j][0]
                    y = ThreeThree[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    ThreeThree[i][j][0] = x1
                    ThreeThree[i][j][1] = y1

                if i < len(ThreeThree_bank):
                    for j in range(len(ThreeThree_bank[i])):  # ���ֽ����л������˵Ŀո���ת
                        x = ThreeThree_bank[i][j][0]
                        y = ThreeThree_bank[i][j][1]
                        x1, y1 = self.get_spin_pos(x, y)
                        ThreeThree_bank[i][j][0] = x1
                        ThreeThree_bank[i][j][1] = y1

                flag = True

                for j in range(len(ThreeThree[i])):
                    if self.judge_the_pos(row, col, ThreeThree[i][j]):  # �ж�row,col������ת���������Ƿ�������������
                        continue
                    else:
                        flag = False
                        break

                if i < len(ThreeThree_bank):
                    if flag:
                        for j in range(len(ThreeThree_bank) // 2):  # �ж����������л������˵Ŀո��Ƿ����㹹�ɻ���������
                            c = 0
                            if self.judge_the_pos_blank(-col, row, ThreeThree_bank[i][c], ThreeThree_bank[i][c + 1]):
                                c += 2
                                continue
                            else:
                                flag = False
                                break
                        if flag:
                            return True
                else:
                    if flag:
                        return True

        return False

        # print(ThreeThree)

    def charge_four_forbid(self, row, col):  # �ж����Ľ���
        FourFour = copy.deepcopy(self.FourFour)

        for i in range(len(FourFour)):
            for k in range(8):  # ��ת8�Σ�ÿ����ʱ��ѡ��45��

                flag = True

                for j in range(len(FourFour[i])):  # �������Ľ��ֵ�������ת
                    x = FourFour[i][j][0]
                    y = FourFour[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    FourFour[i][j][0] = x1
                    FourFour[i][j][1] = y1

                for j in range(len(FourFour[i])):
                    if self.judge_the_pos(row, col, FourFour[i][j]):  # �ж�row,col������ת���������Ƿ��������Ľ���
                        continue
                    else:
                        flag = False
                        break

                if flag:
                    return True

        return False

        # print(FourFour)

    def charge_long_forbid(self, row, col):  # �жϳ�������
        LongLong = copy.deepcopy(self.LongLong)

        for i in range(len(LongLong)):
            for k in range(8):  # ��ת8�Σ�ÿ����ʱ��ѡ��45��

                for j in range(len(LongLong[i])):  # ���ϳ������ֵ�������ת
                    x = LongLong[i][j][0]
                    y = LongLong[i][j][1]
                    x1, y1 = self.get_spin_pos(x, y)
                    LongLong[i][j][0] = x1
                    LongLong[i][j][1] = y1

                flag = True

                for j in range(len(LongLong[i])):
                    if self.judge_the_pos(row, col, LongLong[i][j]):  # �ж�row,col������ת���������Ƿ����ϳ�������
                        continue
                    else:
                        flag = False
                        break

                if flag == True:
                    return True

        return False

    def change_one_to_zero(self):  # ��[0,0,1]�ĳ�[0,0,0]

        ThreeThree = self.ThreeThree
        FourFour = self.FourFour
        LongLong = self.LongLong

        for i in range(len(ThreeThree)):
            ThreeThree[i][0][2] = 0

        for i in range(len(FourFour)):
            FourFour[i][0][2] = 0

        for i in range(len(LongLong)):
            LongLong[i][0][2] = 0

    def deal_noobrobot_move(self, row, col):  # �жϲ��������˵���һ���ƶ�λ���Ƿ�Ϊ���ֵ�

        self.change_one_to_zero()
        if self.charge_three_forbid(row, col):
            return True
        if self.charge_four_forbid(row, col):
            return True
        if self.charge_long_forbid(row, col):
            return True
        return False

    def test(self):
        UI = ChessBoard.ChessBoard()
        UI.out_gobang_board(self.total, self.board)

        for i in range(15):
            for j in range(15):
                if self.board[i][j] == 1:
                    if self.charge_three_forbid(i, j):
                        row = chr(ord("A") + i)
                        col = chr(ord("A") + j)
                        s = ""
                        s += row + col
                        print("�ܲ��Ұ����������˵��װ��Ľ��ֵ㣡�����е��������ֵ�Ϊ (%s) ��" % (s))

                    if self.charge_four_forbid(i, j):
                        row = chr(ord("A") + i)
                        col = chr(ord("A") + j)
                        s = ""
                        s += row + col
                        print("�ܲ��Ұ����������˵��װ��Ľ��ֵ㣡�����е����Ľ��ֵ�Ϊ (%s) ��" % (s))

                    if self.charge_long_forbid(i, j):
                        row = chr(ord("A") + i)
                        col = chr(ord("A") + j)
                        s = ""
                        s += row + col
                        print("�ܲ��Ұ����������˵��װ��Ľ��ֵ㣡�����еĳ������ֵ�Ϊ (%s) ��" % (s))

        player_input = input("�����������ƶ���λ��:")  # ������������������
        x = ord(player_input[0].upper()) - ord("A")  # ת������
        y = ord(player_input[1].upper()) - ord("A")
        self.board[x][y] = 1  # ����Ϊ����
        self.total += 1

        self.test()

    def test1(self):
        UI = ChessBoard.ChessBoard()

        ThreeThree = copy.deepcopy(self.ThreeThree)
        for i in range(len(ThreeThree)):
            self.total = i + 1
            # print(ThreeThree[i])
            board = [[0 for n in range(15)] for i in range(15)]
            for j in range(len(ThreeThree[i])):
                x = 7 - ThreeThree[i][j][1]
                y = 7 + ThreeThree[i][j][0]
                if ThreeThree[i][j][2] == 1:
                    board[x][y] = 1
            UI.out_gobang_board(self.total, board)
            print()

    def test2(self):
        UI = ChessBoard.ChessBoard()

        FourFour = copy.deepcopy(self.FourFour)
        for i in range(len(FourFour)):
            self.total = i + 1
            # print(FourFour[i])
            board = [[0 for n in range(15)] for k in range(15)]
            for j in range(len(FourFour[i])):
                x = 7 - FourFour[i][j][1]
                y = 7 + FourFour[i][j][0]
                if FourFour[i][j][2] == 1:
                    board[x][y] = 1
            UI.out_gobang_board(self.total, board)
            print()

    def test3(self, ThreeThree1):
        UI = ChessBoard.ChessBoard()
        board = [[0 for n in range(15)] for i in range(15)]
        for i in range(len(ThreeThree1)):
            x = 7 - ThreeThree1[i][1]
            y = 7 + ThreeThree1[i][0]
            if ThreeThree1[i][2] == 1:
                board[x][y] = 1
        UI.out_gobang_board(self.total, board)


if __name__ == "__main__":
    F = ForbidStep()
    F.test1()
    F.test2()
