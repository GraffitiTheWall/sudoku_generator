import random
from reportlab.pdfgen import canvas

ans_board = []

is_done = False


def generate_a_valid_board(board, curr_i, curr_j):
    '''
    This program fills in the empty cells of the sudoku board (an empty cell will have a value of 0). It needs to fill out an entire valid
    sudoku board before picking out 'k' cells to empty them, just to make sure that the sudoku board is solvable. It does this by iterating
    through each cell in the sudoku board, using 'curr_i' and 'curr_j'. It then finds which sector of the board the two points are in 
    (since it is a 9 x 9 celled - sudoku - board, which 9 sectors) using 'trackings',

    It then creates a list of all numbers from one to 10 (not - inclusive), and finds a number to fill a cell, given that is satisfies the
    given contraints: the number is not repeated in its sector, row, or column. Once a number is found, it goes to the next cell in the row,
    or, if that row has already been filled out, the first cell in the next column. It keeps on recursing until a valid board is found, 
    where then the valid board will be appended to 'ans_board'. All recursion call stacks will stop, then.
    '''
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
    #If a valid board is found, stop all recursion calls.
    if is_done == True:
        return

    #If a valid board is found, stop all recursion calls.
    if curr_i == 9:
        for i in range(len(board)):
            ans_board.append(board[i].copy())
        is_done = True
        return
    sub_grid = -1
    
    #Finding which sector the two points are in (in the board).
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


#Once we have gotten our valid board, the program then proceeds to picking out 'k' random points off the board for the user to fill in. You
#may change the value of 'k', but, as default, I have left it as 30. Thus, 30 cells will be unfilled, and must be filled in by the user.
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
    '''
    This program is used to carve out the sudoku board in the blank pdf file. I have basically just combined a bunch of math and logic to
    to carve out the board, and I have forgotten the magic behind it. You can just ignore this. 
    '''
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
