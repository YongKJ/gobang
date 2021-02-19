# coding=gbk

import copy


# ----------------------------------------------------------------------
# evaluation: ���������࣬����ǰ���̴����
# ----------------------------------------------------------------------

class evalution(object):

    def __init__(self):
        self.POS = []  # λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        for i in range(15):
            row = [(7 - max(abs(i - 7), abs(j - 7))) for j in range(15)]
            self.POS.append(tuple(row))
        self.POS = tuple(self.POS)
        self.STWO = 1  # ���
        self.STHREE = 2  # ����
        self.SFOUR = 3  # ����
        self.TWO = 4  # ���
        self.THREE = 5  # ����
        self.FOUR = 6  # ����
        self.FIVE = 7  # ����
        self.ANALYSED = 255  # �Ѿ�������
        self.TODO = 0  # û�з�����
        self.result = [0 for i in range(30)]  # ���浱ǰֱ�߷���ֵ
        self.line = [0 for i in range(30)]
        self.record = []  # ȫ�̷������ [row][col][����]
        for i in range(15):
            self.record.append([])
            self.record[i] = []
            for j in range(15):
                self.record[i].append([0, 0, 0, 0])
        self.count = []  # ÿ����ֵĸ�����count[����/����][ģʽ]
        for i in range(3):
            data = [0 for i in range(20)]
            self.count.append(data)

    # �����������̣����ش��
    def evaluate(self, board, turn):
        score = self._evaluate(board, turn)
        count = self.count
        if score < -9000:
            stone = turn == 1 and 2 or 1
            for i in range(20):
                if count[stone][i] > 0:
                    score -= i
        elif score > 9000:
            for i in range(20):
                if count[turn][i] > 0:
                    score += i
        return score

    # �ĸ�����ˮƽ����ֱ����б����б�������������̣�Ȼ����ݷ���������
    def _evaluate(self, board, turn):
        record, count = self.record, self.count
        TODO, ANALYSED = self.TODO, self.ANALYSED
        # self.reset()

        # �ĸ��������
        for i in range(15):
            boardrow = board[i]
            recordrow = record[i]
            for j in range(15):
                if boardrow[j] != 0:
                    if recordrow[j][0] == TODO:  # ˮƽ��û�з�������
                        self._analysis_horizon(board, i, j)
                    if recordrow[j][1] == TODO:  # ��ֱ��û�з�������
                        self._analysis_vertical(board, i, j)
                    if recordrow[j][2] == TODO:  # ��б��û�з�������
                        self._analysis_left(board, i, j)
                    if recordrow[j][3] == TODO:  # ��б��û�з�������
                        self._analysis_right(board, i, j)

        FIVE, FOUR, THREE, TWO = self.FIVE, self.FOUR, self.THREE, self.TWO
        SFOUR, STHREE, STWO = self.SFOUR, self.STHREE, self.STWO
        check = {}

        # �ֱ�԰��������㣺FIVE, FOUR, THREE, TWO�ȳ��ֵĴ���
        for c in (FIVE, FOUR, SFOUR, THREE, STHREE, TWO, STWO):
            check[c] = 1
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    for k in range(4):
                        ch = record[i][j][k]
                        if ch in check:
                            count[stone][ch] += 1

        # ��������������Ϸ��ط���
        BLACK, WHITE = 1, 2
        if turn == WHITE:  # ��ǰ���ǰ���
            if count[BLACK][FIVE] > 0:
                return -9999
            if count[WHITE][FIVE] > 0:
                return 9999
        else:  # ��ǰ���Ǻ���
            if count[WHITE][FIVE] > 0:
                return -9999
            if count[BLACK][FIVE] > 0:
                return 9999

        # ��������������ģ����൱����һ������
        if count[WHITE][SFOUR] >= 2:
            count[WHITE][FOUR] += 1
        if count[BLACK][SFOUR] >= 2:
            count[BLACK][FOUR] += 1

        # ������
        wvalue, bvalue = 0, 0
        if turn == WHITE:
            if count[WHITE][FOUR] > 0:
                return 9990
            if count[WHITE][SFOUR] > 0:
                return 9980
            if count[BLACK][FOUR] > 0:
                return -9970
            if count[BLACK][SFOUR] and count[BLACK][THREE]:
                return -9960
            if count[WHITE][THREE] and count[BLACK][SFOUR] == 0:
                return 9950
            if count[BLACK][THREE] > 1 and \
                    count[WHITE][SFOUR] == 0 and \
                    count[WHITE][THREE] == 0 and \
                    count[WHITE][STHREE] == 0:
                return -9940

            if count[WHITE][THREE] > 1:
                wvalue += 2000
            elif count[WHITE][THREE]:
                wvalue += 200
            if count[BLACK][THREE] > 1:
                bvalue += 500
            elif count[BLACK][THREE]:
                bvalue += 100

            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]

        else:

            if count[BLACK][FOUR] > 0:
                return 9990
            if count[BLACK][SFOUR] > 0:
                return 9980
            if count[WHITE][FOUR] > 0:
                return -9970
            if count[WHITE][SFOUR] and count[WHITE][THREE]:
                return -9960
            if count[BLACK][THREE] and count[WHITE][SFOUR] == 0:
                return 9950
            if count[WHITE][THREE] > 1 and \
                    count[BLACK][SFOUR] == 0 and \
                    count[BLACK][THREE] == 0 and \
                    count[BLACK][STHREE] == 0:
                return -9940

            if count[BLACK][THREE] > 1:
                bvalue += 2000
            elif count[BLACK][THREE]:
                bvalue += 200
            if count[WHITE][THREE] > 1:
                wvalue += 500
            elif count[WHITE][THREE]:
                wvalue += 100

            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]

        # ����λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        wc, bc = 0, 0
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    if stone == WHITE:
                        wc += self.POS[i][j]
                    else:
                        bc += self.POS[i][j]
        wvalue += wc
        bvalue += bc

        if turn == WHITE:
            return wvalue - bvalue

        return bvalue - wvalue

    # ��������
    def _analysis_horizon(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        for y in range(15):
            line[y] = board[i][y]
        self.analysis_line(line, result, 15, j)
        for y in range(15):
            if result[y] != TODO:
                record[i][y][0] = result[y]
        return record[i][j][0]

    # ��������
    def _analysis_vertical(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        for x in range(15):
            line[x] = board[x][j]
        self.analysis_line(line, result, 15, i)
        for x in range(15):
            if result[x] != TODO:
                record[x][j][1] = result[x]
        return record[i][j][1]

    # ������б
    def _analysis_left(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        if i < j:
            x, y = j - i, 0
        else:
            x, y = 0, i - j
        k = 0
        while k < 15:
            if x + k > 14 or y + k > 14:
                break
            line[k] = board[y + k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != TODO:
                record[y + s][x + s][2] = result[s]
        return record[i][j][2]

    # ������б
    def _analysis_right(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        if 14 < i + j:
            x, y, realnum = j - 14 + i, 14, 14 - i
        else:
            x, y, realnum = 0, i + j, j
        k = 0
        while k < 15:
            if x + k > 14 or y - k < 0:
                break
            line[k] = board[y - k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != TODO:
                record[y - s][x + s][3] = result[s]
        return record[i][j][3]

    # ����һ���ߣ���������������
    def analysis_line(self, line, record, num, pos):
        TODO, ANALYSED = self.TODO, self.ANALYSED
        THREE, STHREE = self.THREE, self.STHREE
        FOUR, SFOUR = self.FOUR, self.SFOUR
        while len(line) < 30:
            line.append(0xf)
        while len(record) < 30:
            record.append(TODO)
        for i in range(num, 30):
            line[i] = 0xf
        for i in range(num):
            record[i] = TODO
        if num < 5:
            for i in range(num):
                record[i] = ANALYSED
            return 0

        stone = line[pos]
        inverse = (0, 1, 2)[stone]
        num -= 1

        # ��ͬ���ӵ����ұ߽�
        xl = pos
        xr = pos
        while xl > 0:  # ̽����߽�
            if line[xl - 1] != stone:
                break
            xl -= 1
        while xr < num:  # ̽���ұ߽�
            if line[xr + 1] != stone:
                break
            xr += 1

        # ��ͬ�����������ߵķ�Χ�����Ҳ���ͬ�����ӣ��ո���෴ɫ���ӣ�
        left_range = xl
        right_range = xr
        while left_range > 0:  # ̽����߷�Χ���ǶԷ����ӵĸ������꣩
            if line[left_range - 1] == inverse:
                break
            left_range -= 1
        while right_range < num:  # ̽����߷�Χ���ǶԷ����ӵĸ������꣩
            if line[right_range + 1] == inverse:
                break
            right_range += 1

        # �����ֱ�߷�ΧС��5����ֱ�ӷ���
        if right_range - left_range < 4:
            for k in range(left_range, right_range + 1):
                record[k] = ANALYSED
            return 0

        # �����Ѿ�������
        for k in range(xl, xr + 1):
            record[k] = ANALYSED

        srange = xr - xl

        # �����5��
        if srange >= 4:
            record[pos] = self.FIVE  # ������XXXXX��
            return self.FIVE

        # �����4��
        if srange == 3:
            left4 = False
            if xl > 0:
                if line[xl - 1] == 0:  # ����Ƿ��ǿո�
                    left4 = True
            if xr < num:
                if line[xr + 1] == 0:  # �ұ��ǿո�
                    if left4:
                        record[pos] = self.FOUR  # ���ģ�.XXXX.��
                    else:
                        record[pos] = self.SFOUR  # ���ģ�OXXXX.��
                else:
                    if left4:
                        record[pos] = self.SFOUR  # ���ģ�.XXXXO��
            else:
                if left4:
                    record[pos] = self.SFOUR  # ���ģ�.XXXX|��
            return record[pos]

        # �����3��
        if srange == 2:
            left3 = False  # ����Ƿ��пո�
            if xl > 0:
                if line[xl - 1] == 0:  # �������
                    if xl > 1 and line[xl - 2] == stone:
                        record[xl] = SFOUR  # ���ģ�X.XXX��
                        record[xl - 2] = ANALYSED
                    else:
                        left3 = True  # ����пո�
                elif xr == num or line[xr + 1] != 0:  # ����(OXXX|)��(OXXXO)
                    return 0
            if xr < num:
                if line[xr + 1] == 0:  # �ұ�����
                    if xr < num - 1 and line[xr + 2] == stone:
                        record[xr] = SFOUR  # ���ģ�XXX.X��
                        record[xr + 2] = ANALYSED
                    elif left3:
                        record[xr] = THREE  # ������.XXX.��
                    else:
                        record[xr] = STHREE  # ������OXXX.��
                elif record[xl] == SFOUR:  # �Ѿ��ǳ���
                    return record[xl]
                elif left3:
                    record[pos] = STHREE  # ������.XXXO��
            else:
                if record[xl] == SFOUR:  # �Ѿ��ǳ���
                    return record[xl]
                if left3:
                    record[pos] = STHREE  # ������.XXX|��
            return record[pos]

        # �����2��
        if srange == 1:
            left2 = False
            if xl > 2:
                if line[xl - 1] == 0:  # �������
                    if line[xl - 2] == stone:
                        if line[xl - 3] == stone:
                            record[xl] = SFOUR  # ���ģ�XX.XX��
                            record[xl - 2] = ANALYSED
                            record[xl - 3] = ANALYSED
                        elif line[xl - 3] == 0:
                            record[xl] = STHREE  # ������.X.XX��
                            record[xl - 2] = ANALYSED
                    else:
                        left2 = True  # ����пո�
            if xr < num:
                if line[xr + 1] == 0:  # �ұ�����
                    if xr < num - 2 and line[xr + 2] == stone:
                        if line[xr + 3] == stone:
                            record[xr] = SFOUR  # ���ģ�XX.XX��
                            record[xr + 2] = ANALYSED
                            record[xr + 3] = ANALYSED
                        elif line[xr + 3] == 0:
                            record[xr] = left2 and THREE or STHREE  # ������.XX.X.���������OXX.X.��
                            record[xr + 2] = ANALYSED
                    else:
                        if record[xl] == SFOUR:  # ����Ѿ��ǳ���
                            return record[xl]
                        if record[xl] == STHREE:  # ����Ѿ��ǳ���
                            record[xl] = THREE  # ����ɳ�����Ϊ������.X.XX���䣨.X.XX.��
                            return record[xl]
                        if left2:
                            record[pos] = self.TWO  # �����.XX.��
                        else:
                            record[pos] = self.STWO  # �����OXX.��
                else:
                    if record[xl] == SFOUR:  # ����Ѿ��ǳ���
                        return record[xl]
                    if left2:
                        record[pos] = self.STWO  # �����.XXO��
            return record[pos]
        return 0

