
def sum(a, b, c):
    return a + b + c
def printBoard(xState, zState):
    board = []
    for i in range(9):
        if xState[i]:
            board.append('X')
        elif zState[i]:
            board.append('O')
        else:
            board.append(str(i))
    for row in range(3):
        print(board[row*3],'|',board[row*3+1],'|',board[row*3+2])
        if row < 2:
            print("--|---|---")
def checkWin(xState, zState):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for i in wins:
      if(sum(xState[i[0]],xState[i[1]],xState[i[2]])==3):
        print("X Won the match")
        return 1
      if(sum(zState[i[0]],zState[i[1]],zState[i[2]])==3):
        print("O Won the match")
        return 0
    return -1
def isBoardFull(xState,zState):
  for i in range(len(xState)):
    if xState[i]==0 and zState[i]==0:
      return 0
  return 1

if __name__ == "__main__":
    xState = [0,0,0,0,0,0,0,0,0]
    zState = [0,0,0,0,0,0,0,0,0]
    turn = 1
    print("Welcome to Tic Tac Toe Game")
    while True:
      printBoard(xState,zState)
      if turn == 1:
        print("X's Chance")
      else:
        print("O's Chance")

      try:
        value = int(input("Please enter a value: "))
        if(value<0 and value>8):
          print("Invalid Input")
          continue
        if(xState[value] == 1 or zState[value] == 1):
          print("The Position has been Taken")
          continue

      except ValueError:
        print("Invalid Input")
        continue
      if turn == 1:
          xState[value] = 1
      else:
          zState[value] = 1
      isWin = checkWin(xState,zState)
      if isWin != -1:
        if isWin == 1:
          print("X has Won the Match")
          break;
        else:
          print("O has won the match")
      cBoard = isBoardFull(xState,zState)
      if cBoard:
        print("Match Has Been Drawn")
        break;
      turn = 1 - turn
