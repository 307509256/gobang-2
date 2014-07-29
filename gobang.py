# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, json, request, redirect, make_response
import time, os, random, re

app = Flask(__name__)


class Gobang():
    def __init__(self):
        self.gb_board = [[0 for j in range(0, 15)] for i in range(15)]
        for i in range(0, 15):
            for j in range(0, 15):
                self.gb_board[i][j] = 0
        self.gb_board[6][6] = -1
        self.gb_board[8][8] = 1

    def joinList2str(self, list):
        for i in range(0, len(list)):
            list[i] = str(list[i])
        return ''.join(list)

    def play_chess(self, pos, num):
        self.gb_board[pos[0]][pos[1]] = num


    def horiztal_analy(self, gb_board_copy = None, pos = None, type = None):
        tmp = []
        centerPoint = -1
        ver_index = pos[0]
        hor_index = pos[1]  # include itself
        while hor_index > -1:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            hor_index = hor_index - 1
        centerPoint = len(tmp) - 1
        hor_index = pos[1] + 1  # not include itself
        while hor_index < 15:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            hor_index = hor_index + 1
        return self.scoring(tmp, centerPoint, type)


    def vertical_analy(self, gb_board_copy = None, pos = None, type = None):
        tmp = []
        centerPoint = -1
        ver_index = pos[0]
        hor_index = pos[1]  # include itself
        while ver_index > -1:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index - 1
        centerPoint = len(tmp) - 1
        ver_index = pos[0] + 1  # not include itself
        while ver_index < 15:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index + 1
        return self.scoring(tmp, centerPoint, type)


    def dw_slant_analy(self, gb_board_copy = None, pos = None, type = None):
        tmp = []
        centerPoint = -1
        ver_index = pos[0]
        hor_index = pos[1]
        while ver_index > -1 and hor_index > -1:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index - 1
            hor_index = hor_index - 1
        centerPoint = len(tmp) - 1
        ver_index = pos[0] + 1
        hor_index = pos[1] + 1
        while ver_index < 15 and hor_index < 15:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index + 1
            hor_index = hor_index + 1
        return self.scoring(tmp, centerPoint, type)


    def up_slant_analy(self, gb_board_copy = None, pos = None, type = None):
        tmp = []
        centerPoint = -1
        ver_index = pos[0]
        hor_index = pos[1]

        while ver_index > -1 and hor_index < 15:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.insert(0, gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index - 1
            hor_index = hor_index + 1
        centerPoint = len(tmp) - 1
        ver_index = pos[0] + 1
        hor_index = pos[1] - 1

        while ver_index < 15 and hor_index > -1:
            if type == 'b':
                if gb_board_copy[ver_index][hor_index] > -1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            elif type == 'w':
                if gb_board_copy[ver_index][hor_index] < 1:
                    tmp.append(gb_board_copy[ver_index][hor_index])
                else:
                    break
            ver_index = ver_index + 1
            hor_index = hor_index - 1
        return self.scoring(tmp, centerPoint, type)


    # make a score for one step
    def scoring(self, chess_pieces, index, type):
        if len(chess_pieces) < 5:
            return 0
        chess_pieces[index] = 1

        for i in range(0, len(chess_pieces)):
            if chess_pieces[i] == -1:
                chess_pieces[i] = 1

        chess_pieces_str = self.joinList2str(chess_pieces)
        if re.findall(r'$0*(1{5})0*$', chess_pieces_str) and type == 'w':
            return 10000

        tmp_max = 0
        for i in range(0, len(chess_pieces) - 4):
            chess_pieces_str = self.joinList2str(chess_pieces[i:i + 5])
            if type == 'b':
                if chess_pieces_str == '11000':
                    if tmp_max < 9: tmp_max = 10
                if chess_pieces_str == '10100':
                    if tmp_max < 8: tmp_max = 9
                if chess_pieces_str == '10010':
                    if tmp_max < 7: tmp_max = 8
                if chess_pieces_str == '10001':
                    if tmp_max < 6: tmp_max = 7
                if chess_pieces_str == '01100':
                    if tmp_max < 10: tmp_max = 10
                if chess_pieces_str == '01010':
                    if tmp_max < 8: tmp_max = 8
                if chess_pieces_str == '01001':
                    if tmp_max < 7: tmp_max = 7
                if chess_pieces_str == '00110':
                    if tmp_max < 10: tmp_max = 10
                if chess_pieces_str == '00101':
                    if tmp_max < 8: tmp_max = 9
                if chess_pieces_str == '00011':
                    if tmp_max < 9: tmp_max = 10

            if chess_pieces_str == '11100':
                if tmp_max < 45: tmp_max = 45
            if chess_pieces_str == '11010':
                if tmp_max < 40: tmp_max = 40
            if chess_pieces_str == '11001':
                if tmp_max < 35: tmp_max = 35
            if chess_pieces_str == '10110':
                if tmp_max < 40: tmp_max = 40
            if chess_pieces_str == '10101':
                if tmp_max < 35: tmp_max = 35
            if chess_pieces_str == '10011':
                if tmp_max < 35: tmp_max = 35
            if chess_pieces_str == '01110':
                if tmp_max < 50: tmp_max = 50
            if chess_pieces_str == '01101':
                if tmp_max < 40: tmp_max = 40
            if chess_pieces_str == '01011':
                if tmp_max < 40: tmp_max = 40
            if chess_pieces_str == '00111':
                if tmp_max < 45: tmp_max = 45

            if chess_pieces_str == '11110':
                if tmp_max < 400: tmp_max = 400
            if chess_pieces_str == '11101':
                if tmp_max < 200: tmp_max = 200
            if chess_pieces_str == '11011':
                if tmp_max < 200: tmp_max = 200
            if chess_pieces_str == '10111':
                if tmp_max < 200: tmp_max = 200
            if chess_pieces_str == '01111':
                if tmp_max < 400: tmp_max = 400
            if chess_pieces_str == '11111':
                tmp_max = 5000
        return tmp_max


    # anlay the board use iteration
    def analy_board(self, gb_board_copy = None, times = None):
        if not gb_board_copy:
            gb_board_copy = self.gb_board[:]
            times = 1
        optimal_value = 0
        optimal_pos = None
        for i in range(0, 15):
            for j in range(0, 15):
                pos = i, j
                if (gb_board_copy[i][j] != 0):
                    continue
                # anlay the black value
                b_hor_score = self.horiztal_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'b')
                b_ver_score = self.vertical_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'b')
                b_dws_score = self.dw_slant_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'b')
                b_ups_score = self.up_slant_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'b')
                # analy the white value
                w_hor_score = self.horiztal_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'w')
                w_ver_score = self.vertical_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'w')
                w_dws_score = self.dw_slant_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'w')
                w_ups_score = self.up_slant_analy(gb_board_copy = gb_board_copy, pos = pos, type = 'w')
                # compare the white value and black value
                b_total_value = b_hor_score + b_ver_score + b_dws_score + b_ups_score
                w_total_value = w_hor_score + w_ver_score + w_dws_score + w_ups_score
                # bigger_value = sorted([b_total_value, w_total_value])[-1]
                if b_total_value > w_total_value:
                    bigger_value = b_total_value
                    position = 'attack'
                else:
                    bigger_value = w_total_value
                    position = 'defense'
                if bigger_value > optimal_value:
                    optimal_value = bigger_value
                    optimal_pos = pos
        return optimal_pos, optimal_value, position


session = {}


def gen_app_key():
    key = ""
    for i in range(0, 24):
        if i % 2 == 0:
            key += chr(random.randint(97, 122))
        else:
            key += str(random.randint(0, 10))
    return key


@app.route('/gobang')
def index():
    url_for('static', filename = 'index.js')
    url_for('static', filename = 'index.css')
    url_for('static', filename = 'jquery-1.9.1.min.js')
    gobang = Gobang()
    resp = make_response(render_template('index.html'))
    gobang_key = gen_app_key()
    resp.set_cookie('gobang_key', gobang_key)
    session[gobang_key] = gobang
    return resp


@app.route('/gobang/submit.do', methods = ['POST', 'GET'])
def gobang_ai():
    global session
    gobang_key = request.cookies.get('gobang_key', 'nologin')
    gobang = session[gobang_key]
    pos = int(request.args.get('ver_index', '')), int(request.args.get('hor_index', ''))
    gobang.play_chess(pos, -1)
    optimal_pos, optimal_value, position = gobang.analy_board()
    ai_ver_index, ai_hor_index = optimal_pos
    gobang.play_chess(optimal_pos, 1)
    if optimal_value == 5000 and position == 'attack':
        return json.dumps({"success": True, "message": "黑方胜！", "ver_index": ai_ver_index, "hor_index": ai_hor_index})
    if optimal_value == 10000:
        return json.dumps({"success": True, "message": "白方胜！"})
    return json.dumps({"success": True, "ver_index": ai_ver_index, "hor_index": ai_hor_index})


if __name__ == '__main__':
    app.run(debug = True)