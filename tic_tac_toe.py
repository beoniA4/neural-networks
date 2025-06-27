import math
board=["   ","   ","   ",
       "   ","   ","   ",
       "   ","   ","   "]
currentPlayer= " X "
winner= None
gameRunning=True

#board for playing
def printBoard(board):
    print("-------------")
    print("|" + board[0] + "|" + board[1] + "|" + board[2] + "|")
    print("-------------")
    print("|" + board[3] + "|" + board[4] + "|" + board[5] + "|")
    print("-------------")
    print("|" + board[6] + "|" + board[7] + "|" + board[8] + "|")
    print("-------------")

#moves 
def moves(board):
    global currentPlayer
    pos= int(input("Enter a number(1-9):"))
    if pos>0 and pos<10 and board[pos-1]=="   " :
        board[pos-1]= currentPlayer
    else:
        print("you cant place there!")
        moves(board)
   

#switch player
def switchPlayer():
    global currentPlayer
    currentPlayer = " O " if currentPlayer == " X " else " X "


#winner 
def cWin(board):
    global winner
    # Horizontal
    if board[0] == board[1] == board[2] and board[0] != "   ":
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != "   ":
        winner = board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != "   ":
        winner = board[6]
        return True
    # Vertical
    elif board[0] == board[3] == board[6] and board[0] != "   ":
        winner = board[0]
        return True
    elif board[1] == board[4] == board[7] and board[1] != "   ":
        winner = board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != "   ":
        winner = board[2]
        return True
    # Diagonal
    elif board[0] == board[4] == board[8] and board[0] != "   ":
        winner = board[0]
        return True
    elif board[2] == board[4] == board[6] and board[2] != "   ":
        winner = board[2]
        return True
    else:
        return False
    
#tie
def tie(board):
    if "   " not in board and not cWin(board):
        print("It is a tie!")
        return True
    return False
  
 # Evaluate the board for minimax
def evaluate(board):
    if cWin(board):
        if winner == " O ":
            return 10
        elif winner == " X ":
            return -10
    return 0

# Minimax algorithm
def minimax(board, depth, isMaximizing):
    score = evaluate(board)
    if score == 10 or score == -10:
        return score
    if "   " not in board:
        return 0

    if isMaximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == "   ":
                board[i] = " O "
                best = max(best, minimax(board, depth + 1, not isMaximizing))
                board[i] = "   "
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "   ":
                board[i] = " X "
                best = min(best, minimax(board, depth + 1, not isMaximizing))
                board[i] = "   "
        return best

# AI move
def aiMove(board):
    bestVal = -math.inf
    bestMove = -1
    for i in range(9):
        if board[i] == "   ":
            board[i] = " O "
            moveVal = minimax(board, 0, False)
            board[i] = "   "
            if moveVal > bestVal:
                bestMove = i
                bestVal = moveVal
    board[bestMove] = " O "
    print("AI chose position", bestMove + 1)

printBoard(board)   
while gameRunning == True:
    if currentPlayer == " X ":
        moves(board)
    else:
        aiMove(board)
    printBoard(board)
    if cWin(board):
        print(f"The winner is {winner.strip()}!")
        gameRunning = False
    elif tie(board):
        gameRunning = False
    switchPlayer()
    
