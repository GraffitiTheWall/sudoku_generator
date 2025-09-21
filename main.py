import random
from reportlab.pdfgen import canvas

ans_board = []

is_done = False


def generate_a_valid_board(board, curr_i, curr_j):
    trackings = {
        1: ((0, 3), (0, 3)),
        2: ((0, 3), (3, 6)),
        3: ((0, 3), (6, 9)),
        4: ((3, 6), (0, 3)),
        5: ((3, 6), (3, 6)),
        6: ((3, 6), (6, 9)),
        7: ((6, 9), (0, 3)),
        8: ((6, 9), (3, 6)),
        9: ((6, 9), (6, 9)),
    }
    global is_done, ans_board
    if is_done == True:
        return
    if curr_i == 9:
        for i in range(len(board)):
            ans_board.append(board[i].copy())
        is_done = True
        return
    sub_grid = -1
    for key in trackings:
        i_ranges = trackings[key][0]
        j_ranges = trackings[key][1]
        if i_ranges[0] <= curr_i < i_ranges[1] and j_ranges[0] <= curr_j < j_ranges[1]:
            sub_grid = key
            break
    l = list(range(1, 10))
    random.shuffle(l)
    for curr_n in l:
        is_valid = True
        for n_i in range(trackings[sub_grid][0][0], (trackings[sub_grid][0][1])):
            for n_j in range(trackings[sub_grid][1][0], (trackings[sub_grid][1][1])):
                if board[n_i][n_j] == curr_n:
                    is_valid = False
                    break
        for n_i in range(len(board)):
            if board[n_i][curr_j] == curr_n:
                is_valid = False
                break
        for n_j in range(len(board[0])):
            if board[curr_i][n_j] == curr_n:
                is_valid = False
                break
        if is_valid == True:
            board[curr_i][curr_j] = curr_n
            if curr_j == len(board[0]) - 1:
                generate_a_valid_board(board, curr_i + 1, 0)
            else:
                generate_a_valid_board(board, curr_i, curr_j + 1)
            board[curr_i][curr_j] = -1


board = [[0 for _ in range(9)] for _ in range(9)]
generate_a_valid_board(board, 0, 0)


board = ans_board
k = 30
while k > 0:
    i = random.randint(0, 8)
    j = random.randint(0, 8)
    if board[i][j] == 0:
        continue
    else:
        k -= 1
        board[i][j] = 0
my_canvas = canvas.Canvas("sudoku_board.pdf", pagesize=(255, 255))
my_canvas.setFont("Times-Bold", 25)
my_canvas.setFont("Times-Roman", 12)
my_canvas.setLineWidth(1)


def draw_out_board(board):
    starting_x = 15
    starting_y = 240
    for row in board:
        for char in row:
            if starting_y in [240, 165, 90, 40]:
                if starting_y == 40:
                    starting_y -= 25
                my_canvas.setLineWidth(5)
                my_canvas.line(starting_x, starting_y, starting_x + 25, starting_y)
                my_canvas.setLineWidth(1)
                if starting_y == 15:
                    starting_y += 25
                my_canvas.line(starting_x, starting_y, starting_x + 25, starting_y)
            else:
                my_canvas.line(starting_x, starting_y, starting_x + 25, starting_y)
            if starting_x in [15, 90, 165, 215]:
                if starting_x == 215:
                    starting_x += 25
                my_canvas.setLineWidth(5)
                my_canvas.line(starting_x, starting_y, starting_x, starting_y - 25)
                my_canvas.setLineWidth(1)
                if starting_x == 240:
                    starting_x -= 25
                my_canvas.line(starting_x, starting_y, starting_x, starting_y - 25)
            else:
                my_canvas.line(starting_x, starting_y, starting_x, starting_y - 25)
            my_canvas.setFont("Times-Bold", 12)
            if char != 0:
                my_canvas.drawString(
                    int((starting_x + starting_x + 25) / 2) - 3,
                    int((starting_y + starting_y - 25) / 2) - 3,
                    str(char),
                )
            my_canvas.setFont("Times-Roman", 12)
            starting_x += 25
        starting_y -= 25
        starting_x = 15
    my_canvas.line(
        starting_x + (25 * len(board[0])),
        240,
        starting_x + (25 * len(board[0])),
        starting_y,
    )
    my_canvas.line(
        starting_x, starting_y, starting_x + (25 * len(board[0])), starting_y
    )


draw_out_board(board)
my_canvas.save()
