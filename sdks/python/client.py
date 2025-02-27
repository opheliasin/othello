#!/usr/bin/python

import sys
import json
import socket

#questions:
# 1. client only checks the board and makes moves, it doesn't have to worry about anything else
# 2. a piece can only be placed in an empty space adjacent to an existing piece (vertical, horizontal, or diagonal)
# 3. if we use a greedy algorithm, each potential placement should be adjacent to an existing piece
#    - we calculate the number of pieces we can flip by placing the piece there 
# first check if cell is adjacent to any piece – if it is, the we can calculate 
# finally we select the move that flips the most pieces

# every time we receive the new board, not just the move that's just being made, so we can't just check the last move
# we need to check the entire board 

DIRECTION_MAP = {
  'up': [1, 0],
  'down': [-1, 0],
  'left': [0, -1],
  'right': [0, 1],
  'left-up-diagonal': [-1, -1],
  'right-up-diagonal': [-1, 1],
  'left-down-diagonal': [1, -1],
  'right-down-diagonal': [1, 1]
}

def get_move(player, board):
  # TODO determine valid moves 

  max_flips = 0
  move_row, move_col = -1, -1

  # check if the empty space is adjacent to any pieces
  for row in range(len(board)):
    for col in range(len(board[row])):
      if board[row][col] == 0: 
          # print("row, col: ", row, col)
          total_flips = 0
          if row != 0 and row != 7: # if not top or bottom row
            # print("if not top and not bottom row")
            if board[row+1][col] != 0: #down
              total_flips += check_valid_move((row+1, col), 'down', player)
            if board[row-1][col] != 0: #up
              total_flips += check_valid_move((row-1, col), 'up', player)
            if col != 0 and col != 7:
              if board[row][col-1] != 0: # left
                total_flips += check_valid_move((row, col-1), 'left', player)
              if board[row][col+1] != 0: # right
                total_flips += check_valid_move((row, col+1), 'right', player)
              if board[row+1][col+1] != 0: # right down diagonal
                total_flips += check_valid_move((row+1, col+1), 'right-down-diagonal', player)
              if board[row+1][col-1] != 0: # left down diagonal
                total_flips += check_valid_move((row+1, col-1), 'left-down-diagonal', player)
              if board[row-1][col+1] != 0: # right up diagonal
                total_flips += check_valid_move((row-1, col+1), 'right-up-diagonal', player)
              if board[row-1][col-1] != 0: # left up diagonal
                total_flips += check_valid_move((row-1, col-1), 'left-up-diagonal', player)
          if row == 0: # if top row
            # print("if top row")
            if board[row+1][col] != 0: # down
              total_flips += check_valid_move((row+1, col), 'down', player)
            if col != 0: # if not the left-most column
              if board[row][col-1] != 0: # left
                total_flips += check_valid_move((row, col-1), 'left', player)
              if board[row+1][col-1] != 0: # left-diagonal down
                total_flips += check_valid_move((row+1, col-1), 'left-down-diagonal', player)
            if col != 7: # if not the right most column
              if board[row][col+1] != 0: # right
                total_flips += check_valid_move((row, col+1), 'right', player)
              if board[row+1][col+1] != 0: # right-diagonal down
                total_flips += check_valid_move((row+1, col+1), 'right-down-diagonal', player)
          if row == 7: # if bottom row
            # print("if bottom row")
            if board[row-1][col] != 0: # up
              total_flips += check_valid_move((row-1, col), 'up', player)
            if col != 0: # if not left most column
              if board[row][col-1] != 0: # left
                total_flips += check_valid_move((row, col-1), 'left', player)
              if board[row-1][col-1] != 0: # left-diagonal up
                total_flips += check_valid_move((row-1, col-1), 'left-up-diagonal', player)
            if col != 7: # if not right most column 
              if board[row][col+1] != 0: # right
                total_flips += check_valid_move((row, col+1), 'right', player)
              if board[row-1][col+1] != 0: # right-diagonal up
                total_flips += check_valid_move((row-1, col+1), 'right-up-diagonal', player)
          
          # TODO determine best move
          if total_flips >= max_flips:
            max_flips = total_flips
            move_row, move_col = row, col

            
            # print("total_flips: ", total_flips)
            # print("move_row, move_col: ", move_row, move_col)
            # print("----------------------------------------------")
      #print(row, col)
  # move should be a JSON array, followed by a newline (e.g. "[1,2]\n")
  return json.dumps([move_row, move_col]) # returns the coordinate of the piece placed on the board

def check_valid_move(coord, direction, player):
  row, col = coord[0], coord[1]
  running_total = 0 # total number of opponent's pieces on the line
  temp_total = 0

  # print(" row, col: ", row, col)
  # print(" value: ", board[row][col])
  # print(" direction: ", direction)
  while row <= 7 and col <= 7 and board[row][col] != 0: # while we're in bounds and pieces exist
    # we count how many opponent pieces there are on the line 
    # if the 
    if board[row][col] != player: # if opponent piece
      temp_total += 1
    else: # encounter player's piece 
      running_total += temp_total 
      temp_total = 0 # reset temp_total 
    
    # increment according to the direction 
    row += DIRECTION_MAP[direction][0]
    col += DIRECTION_MAP[direction][1]
  # print(" running_total: ", running_total)
  return running_total

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
