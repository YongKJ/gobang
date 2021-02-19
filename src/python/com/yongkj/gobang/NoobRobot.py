# coding=gbk

import evaluation
import threading
import ForbidStep


class NoobRobot(object):

    def __init__(self):
        self.POS = []  # λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        for i in range(15):
            row = [(7 - max(abs(i - 7), abs(j - 7))) for j in range(15)]
            self.POS.append(tuple(row))
        self.POS = tuple(self.POS)
        self.board = [[0 for n in range(15)] for i in range(15)]  # ��ǰ���̾���
        self.maxdepth = 3  # �ݹ�������
        self.Opening_type = 0  # ���ɿ��ֻ�ָ������
        self.flag = True
        self.free_fobid = 0
        self.Robot = 1
        self.round = 0
        self.bestmove = None  # ���λ�ó�ʼ��
        self.trap_moves_list = []

    def judge_first(self, moves, turn):
        gos = []
        tos = []
        los = []
        kos = []

        for score, row, col in moves:
            self.board[row][col] = turn
            t = DealScoreWithThread(self.board, turn)
            t.start()
            score = t.score
            if abs(score) >= 9999:
                self.flag = False
            gos.append((score, row, col))
            self.board[row][col] = 0

        nturn = turn == 1 and 2 or 1

        for score, row, col in moves:
            self.board[row][col] = nturn
            t = DealScoreWithThread(self.board, nturn)
            t.start()
            score = t.score
            if abs(score) >= 9999:
                self.flag = False
            tos.append((score, row, col))
            self.board[row][col] = 0

        gos.sort()
        gos.reverse()

        tos.sort()
        tos.reverse()
        if not self.flag:
            node = 5
        else:
            node = 10
            if self.round > 15:
                node = 10
            if self.round > 25:
                node = 10

        k = 1
        for score, row, col in gos:
            los.append((score, row, col))
            if k == node:
                break
            k += 1

        k = 0
        for score, row, col in tos:
            flag = True
            for s, r, c in los:
                if row == r and col == c:
                    flag = False
            if flag:
                los.append((score, row, col))
                k += 1
            if k == node:
                break

        for score, row, col in moves:
            for s, r, c in los:
                if row == r and col == c:
                    kos.append((score, row, col))

        kos.sort()
        kos.reverse()

        return kos

    def judge(self, moves, turn):
        gos = []
        tos = []
        los = []
        kos = []

        for score, row, col in moves:
            self.board[row][col] = turn
            t = DealScoreWithThread(self.board, turn)
            t.start()
            score = t.score
            gos.append((score, row, col))
            self.board[row][col] = 0

        nturn = turn == 1 and 2 or 1

        for score, row, col in moves:
            self.board[row][col] = nturn
            t = DealScoreWithThread(self.board, nturn)
            t.start()
            score = t.score
            tos.append((score, row, col))
            self.board[row][col] = 0

        gos.sort()
        gos.reverse()

        tos.sort()
        tos.reverse()

        if not self.flag:
            node = 5
        else:
            node = 6
            if self.round > 15:
                node = 5
            if self.round > 25:
                node = 4

        k = 1
        for score, row, col in gos:
            los.append((score, row, col))
            if k == node:
                break
            k += 1

        k = 0
        for score, row, col in tos:
            flag = True
            for s, r, c in los:
                if row == r and col == c:
                    flag = False
            if flag:
                los.append((score, row, col))
                k += 1
            if k == node:
                break

        for score, row, col in moves:
            for s, r, c in los:
                if row == r and col == c:
                    kos.append((score, row, col))

        kos.sort()
        kos.reverse()

        return kos

    # ������ǰ��ֵ��߷�
    def genmove(self, turn):
        board = self.board

        # ���¿������������¼�֦��
        gobang_pos_horizon = []  # ���򣺻��ˮƽ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[i][j] != 0:
                    gobang_pos_horizon.append(i)
                    break
        row1 = gobang_pos_horizon[0]
        row2 = gobang_pos_horizon[len(gobang_pos_horizon) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if row1 > 0:
            row1 -= 1
        if row2 < 14:
            row2 += 1

        gobang_pos_vertical = []  # ���򣺻�ô�ֱ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[j][i] != 0:
                    gobang_pos_vertical.append(i)
                    break
        col1 = gobang_pos_vertical[0]
        col2 = gobang_pos_vertical[len(gobang_pos_vertical) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if col1 > 0:
            col1 -= 1
        if col2 < 14:
            col2 += 1

        dir = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]  # ����ڵ�ǰ����İ˸�������ƶ�����
        moves = []
        POSES = self.POS  # λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        for i in range(row1, row2 + 1):  # �������̾���
            for j in range(col1, col2 + 1):
                for k in range(8):  # ÿ��������˸������ƶ�һ��
                    x = dir[k][0]
                    y = dir[k][1]
                    if 0 <= i - y <= 14 and 0 <= j + x <= 14:  # �ж��ƶ���������Ƿ�Ϸ�
                        if board[i][j] == 0 and board[i - y][j + x] != 0:  # �жϵ�ǰ�����Ƿ�Ϊ�գ������ƶ���������Ƿ������ӣ�Ѱ�Ҹ��������ڵĿ�λ�ã�
                            score = POSES[i][j]
                            moves.append((score, i, j))
                            break
        moves.sort()  # moves��������
        moves.reverse()  # moves���дӴ�С����
        return moves  # ����moves����

    def genmove_second(self, turn):
        board = self.board

        # ���¿������������¼�֦��
        gobang_pos_horizon = []  # ���򣺻��ˮƽ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[i][j] != 0:
                    gobang_pos_horizon.append(i)
                    break
        row1 = gobang_pos_horizon[0]
        row2 = gobang_pos_horizon[len(gobang_pos_horizon) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if row1 > 0:
            row1 -= 1
        if row2 < 14:
            row2 += 1

        gobang_pos_vertical = []  # ���򣺻�ô�ֱ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[j][i] != 0:
                    gobang_pos_vertical.append(i)
                    break
        col1 = gobang_pos_vertical[0]
        col2 = gobang_pos_vertical[len(gobang_pos_vertical) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if col1 > 0:
            col1 -= 1
        if col2 < 14:
            col2 += 1

        dir = [[0, 1], [0, 2], [0, -1], [0, -2], [1, 0], [2, 0], [-1, 0], [-2, 0], [1, 1], [2, 2], [-1, -1], [-2, -2],
               [1, -1], [2, -2], [-1, 1], [-2, 2]]  # ����ڵ�ǰ����İ˸�������ƶ�����
        moves = []
        POSES = self.POS  # λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        for i in range(row1, row2 + 1):  # �������̾���
            for j in range(col1, col2 + 1):
                for k in range(16):  # ÿ��������˸������ƶ�һ��
                    x = dir[k][0]
                    y = dir[k][1]
                    if 0 <= i - y <= 14 and 0 <= j + x <= 14:  # �ж��ƶ���������Ƿ�Ϸ�
                        if board[i][j] == 0 and board[i - y][j + x] != 0:  # �жϵ�ǰ�����Ƿ�Ϊ�գ������ƶ���������Ƿ������ӣ�Ѱ�Ҹ��������ڵĿ�λ�ã�
                            score = POSES[i][j]
                            moves.append((score, i, j))
                            break
        moves.sort()  # moves��������
        moves.reverse()  # moves���дӴ�С����
        return moves  # ����moves����

    def genmove_first(self, turn):
        board = self.board

        # ���¿������������¼�֦��
        gobang_pos_horizon = []  # ���򣺻��ˮƽ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[i][j] != 0:
                    gobang_pos_horizon.append(i)
                    break
        row1 = gobang_pos_horizon[0]
        row2 = gobang_pos_horizon[len(gobang_pos_horizon) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if row1 > 1:
            row1 -= 2
        elif row1 > 0:
            row1 -= 1

        if row2 < 13:
            row2 += 2
        elif row2 < 14:
            row2 += 1

        gobang_pos_vertical = []  # ���򣺻�ô�ֱ���������ӵ�����
        for i in range(15):
            for j in range(15):
                if board[j][i] != 0:
                    gobang_pos_vertical.append(i)
                    break
        col1 = gobang_pos_vertical[0]
        col2 = gobang_pos_vertical[len(gobang_pos_vertical) - 1]
        # ��С������1�����������1��Ŀ����ȷ������ǡ�ð����������С������б߽�
        if col1 > 1:
            col1 -= 2
        elif col1 > 0:
            col1 -= 1

        if col2 < 13:
            col2 += 2
        elif col2 < 14:
            col2 += 1

        dir = [[0, 1], [0, 2], [0, -1], [0, -2], [1, 0], [2, 0], [-1, 0], [-2, 0], [1, 1], [2, 2], [-1, -1], [-2, -2],
               [1, -1], [2, -2], [-1, 1], [-2, 2]]  # ����ڵ�ǰ����İ˸�������ƶ�����
        moves = []
        POSES = self.POS  # λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        for i in range(row1, row2 + 1):  # �������̾���
            for j in range(col1, col2 + 1):
                for k in range(16):  # ÿ��������˸������ƶ�һ��
                    x = dir[k][0]
                    y = dir[k][1]
                    if 0 <= i - y <= 14 and 0 <= j + x <= 14:  # �ж��ƶ���������Ƿ�Ϸ�
                        if board[i][j] == 0 and board[i - y][j + x] != 0:  # �жϵ�ǰ�����Ƿ�Ϊ�գ������ƶ���������Ƿ������ӣ�Ѱ�Ҹ��������ڵĿ�λ�ã�
                            if turn == 1:  # ��ǰ�Ƿ����º�����
                                if (self.Opening_type == 1 or (
                                        self.Opening_type == 2 and self.free_fobid == 1)) and self.Robot == 1:  # �����Ƿ�Ϊָ������
                                    forbid_step = ForbidStep.ForbidStep()
                                    forbid_step.board = self.board
                                    if not forbid_step.deal_noobrobot_move(i, j):  # �жϵ�ǰ��λ���Ƿ�Ϊ���ֵ㣬������λ��Ȩֵ��������moves����
                                        score = POSES[i][j]
                                        moves.append((score, i, j))
                                        break
                                else:  # ��Ϊ���ɿ��֣���λ��Ȩֵ������ֱ����moves����
                                    score = POSES[i][j]
                                    moves.append((score, i, j))
                                    break
                            else:  # ����ǰΪ�°����ӣ���λ��Ȩֵ������ֱ����moves����
                                if (self.Opening_type == 1 or (
                                        self.Opening_type == 2 and self.free_fobid == 1)) and self.Robot == 2:  # �����Ƿ�Ϊָ������
                                    forbid_step = ForbidStep.ForbidStep()
                                    forbid_step.board = self.board
                                    if forbid_step.deal_noobrobot_move(i, j):  # �жϵ�ǰ��λ���Ƿ�Ϊ���ֵ㣬������λ��Ȩֵ��������moves����
                                        self.trap_moves_list.append((i, j))

                                score = POSES[i][j]
                                moves.append((score, i, j))
                                break
        moves.sort()  # moves��������
        moves.reverse()  # moves���дӴ�С����
        return moves  # ����moves����

    # �ݹ�������������ѷ����Լ���������߷�
    def _search(self, turn, depth, alpha=-0x7fffffff, beta=0x7fffffff):

        # ���Ϊ�����������̲�����
        if depth <= 0:
            t = DealScoreWithThread(self.board, turn)
            t.start()
            score = t.score
            return score

        # ���������̣߳�������߳��е�ǰ���̵�����
        t = DealScoreWithThread(self.board, turn)
        t.start()
        score = t.score
        # �����Ϸ������������
        if abs(score) >= 9999 and depth < self.maxdepth:
            return score

        # �������߷�
        if self.maxdepth != 1:
            if depth == self.maxdepth:
                moves = self.genmove_first(turn)
                moves = self.judge_first(moves, turn)
            elif depth == 1:
                moves = self.genmove(turn)
            else:
                moves = self.genmove(turn)
                moves = self.judge(moves, turn)
        else:
            moves = self.genmove(turn)

        # ��õ��ƶ�λ�ó�ʼ��
        bestmove = None

        # ö�ٵ�ǰ�����߷�
        for score, row, col in moves:

            # if not self.flag:
            #     continue

            # ��ǵ�ǰ�߷�������
            self.board[row][col] = turn

            # ������һ�غϸ�˭��
            nturn = turn == 1 and 2 or 1
            # ��������������������֣� �ߵ��к��ߵ���
            score = - self._search(nturn, depth - 1, -beta, -alpha)

            if (self.Opening_type == 1 or (
                    self.Opening_type == 2 and self.free_fobid == 1)) and self.Robot == 2:
                if nturn == 1:
                    flag = False
                    for x, y in self.trap_moves_list:
                        if row == x and col == y:
                            flag = True
                    if flag:
                        score = -9999

            # ��������ϵ�ǰ�߷�
            self.board[row][col] = 0

            # ������÷�ֵ���߷�
            # alpha/ beta ��֦
            if score > alpha:
                alpha = score
                bestmove = (row, col)
                if alpha >= beta:
                    break

        # ����ǵ�һ�����¼��õ��߷�
        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        # ���ص�ǰ��õķ����͸÷����Ķ�Ӧ�߷�
        return alpha

    # ������ʼ�������뵱ǰ�Ǹ�˭��(turn=1/2)���Լ��������(depth)
    def search(self, turn, depth=3):
        self.maxdepth = depth  # ������ݹ����
        self.bestmove = None  # ���λ�ó�ʼ��

        score = self._search(turn, depth)  # �����õ���������

        row, col = self.bestmove

        return score, row, col  # ��������������ֺ�����ƶ�λ������

    def robot_five_step_judge(self, moves, five_num, turn):
        gos = []
        tos = []
        los = []

        for score, row, col in moves:
            self.board[row][col] = turn
            t = DealScoreWithThread(self.board, turn)
            t.start()
            score = t.score
            gos.append((score, row, col))
            self.board[row][col] = 0

        nturn = turn == 1 and 2 or 1

        for score, row, col in moves:
            self.board[row][col] = nturn
            t = DealScoreWithThread(self.board, nturn)
            t.start()
            score = t.score
            tos.append((score, row, col))
            self.board[row][col] = 0

        gos.sort()
        gos.reverse()

        tos.sort()
        tos.reverse()

        node_white = five_num // 2
        if node_white * 2 == five_num:
            node_black = node_white
        else:
            node_black = node_white + 1

        k = 1
        for score, row, col in gos:
            los.append((score, row, col))
            if k == node_black:
                break
            k += 1

        k = 0
        l = len(tos) // 2
        while True:
            flag = True
            score = tos[l][0]
            row = tos[l][1]
            col = tos[l][2]
            for s, r, c in los:
                if row == r and col == c:
                    flag = False
            if flag:
                los.append((score, row, col))
                k += 1
            if k == node_white:
                break
            l -= 1

        return los

    def judge_free_three_change(self, turn):

        board = self.board
        x = -1
        y = -1
        flag = False

        dir = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    continue
                if board[i][j] == 1 and x == -1 and y == -1:
                    x = i
                    y = j
                elif board[i][j] == 1:
                    for k in range(8):
                        xx = x + dir[k][0]
                        yy = y + dir[k][1]
                        if xx == i and yy == j:
                            flag = True
                            break

        return flag

    def deal_robot_five_step(self, five_num, turn):  # �����������˵�����N�򣬴�ʱ���������ѡ���������
        moves = self.genmove(turn)  # ��õ�ǰ���п��ƶ���λ��
        moves = self.robot_five_step_judge(moves, five_num, turn)
        return moves

    def deal_player_five_step(self, pos, turn):  # ������ҵ�����N�򣬴�ʱ���ѡ���������
        moves = []
        for row, col in pos:  # ����������������N������
            self.board[row][col] = turn  # �ڵ�ǰλ������
            t = DealScoreWithThread(self.board, turn)  # ���㵱ǰ��ֵ�����
            t.start()
            score = t.score

            moves.append((score, row, col))  # ���֣�������moves����
            self.board[row][col] = 0
        moves.sort()  # ��С��������
        if abs(moves[0][0]) > abs(moves[len(moves) - 1][0]):
            score, row, col = moves[len(moves) - 1]
        else:
            score, row, col = moves[0]
        return row, col  # ���ص�һ��������moves�����еĵ�һ������


class DealScoreWithThread(threading.Thread):  # ��һ���̼߳��㵱ǰ��ֵ�����

    def __init__(self, board, turn):
        super(DealScoreWithThread, self).__init__()
        self.evaluator = evaluation.evalution()
        self.board = board
        self.turn = turn
        self.score = 0

    def run(self):
        self.score = self.evaluator.evaluate(self.board, self.turn)


if __name__ == "__main__":
    N = NoobRobot()
