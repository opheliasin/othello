#!/usr/bin/python

import sys
import json
import socket

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

  max_flips = 0
  move_row, move_col = -1, -1

  # check if the empty space is adjacent to an opponent's piece
  for row in range(len(board)):
    for col in range(len(board[row])):

      if board[row][col] == 0: 
          total_flips = 0

          for direction, (dr, dc) in DIRECTION_MAP.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] not in [0, player]:
              total_flips += check_valid_move((new_row, new_col), direction, player, board)

          # Best move is move that can flip the most pieces
          if total_flips > max_flips:
            max_flips = total_flips
            move_row, move_col = row, col

  # did not account for invalid results, as instruction stated that the player 
  # would only be prompted if there's a valid move
  # returns the coordinate of the piece placed on the board
  return json.dumps([move_row, move_col]) 

def check_valid_move(coord, direction, player, board):
  row, col = coord[0], coord[1]
  running_total = 0 # total number of opponent's pieces on the line

  while 0 <= row < 8 and 0 <= col < 8: # while in bounds 
    if board[row][col] == 0:
      break
    elif board[row][col] != player: 
      # count how many opponent pieces there are before we encounter our own  
      running_total += 1 
    else:
      return running_total
    
    # increment according to the direction 
    row += DIRECTION_MAP[direction][0]
    col += DIRECTION_MAP[direction][1]

  return 0 #when last piece is opponent's piece

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
