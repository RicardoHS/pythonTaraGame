from random import randint
import sys
import pygame
import math
from time import sleep

blank = "-"
PAWN_PLAYER = "X"
PAWN_IA = "O"

class Graphics():
    
    def initGraphics(self):
        self.scorePanel=pygame.image.load("img/score_panel.png")
        self.greenCircle=pygame.image.load("img/greenindicator1.png")
        self.redCircle=pygame.image.load("img/redindicator1.png")
        self.lineV=pygame.image.load("img/line.png")
        self.lineH=pygame.transform.rotate(pygame.image.load("img/line.png"),-90)
        self.separators=pygame.image.load("img/separators.png")
        self.arrow=pygame.transform.scale(pygame.image.load("img/arrow.png"),(20,20))
        self.button = pygame.image.load("img/button.png")
        pass


    def __init__(self,board):
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TARA - Your turn")
        self.board = board
        self.myTurn = True
        self.clock=pygame.time.Clock()
        self.initGraphics()
        pass
   
    def update(self,board):
        self.myTurn = True
        self.board = board
        self.clock.tick(60)
        self.screen.fill(0)
        self.updateMouseThings()
        self.drawHUD()
        self.drawBoard()
        self.drawPieces()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

        pygame.display.flip()
        return self.board, self.myTurn

    def updateMouseThings(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] >= 34 and mouse[0] <= 354 and mouse[1] < 370:
            actualBox = (int(mouse[0])-34)/64
            self.screen.blit(self.arrow, (64*(actualBox+1)-10,10))
            pygame.event.get()
            if pygame.mouse.get_pressed()[0] :
                self.board = next_state(self.board, PAWN_PLAYER, (actualBox,0))
                self.myTurn = False
                pass
        if pygame.mouse.get_pressed()[0] :
            if mouse[0] > 300 and mouse [0] < 360 and mouse[1] <470 and mouse[1] >410:
                exit()
        pass

    def drawBoard(self):
        for x in range(5):
            for y in range(6):
                self.screen.blit(self.lineH, [32+(x)*64+5, 32+(y)*64])
        for x in range(6):
            for y in range(5):
                self.screen.blit(self.lineV, [32+(x)*64, 32+(y)*64+5])
        for x in range(6):
            for y in range(6):
                self.screen.blit(self.separators, [32+x*64, 32+y*64])

        pass

    def drawPieces(self):
        for x in range(5):
            for y in range(5):
                if self.board[x][y] != blank:
                    if self.board[x][y] == PAWN_PLAYER:
                        self.screen.blit(self.greenCircle,[50+64*(x),50+64*(y)])
                    else:
                        self.screen.blit(self.redCircle,[50+64*(x),50+64*(y)])

    def drawHUD(self):
        self.screen.blit(self.scorePanel, [0, 389])
        label = pygame.font.SysFont(None,32).render(str("Try to beat the AI"),2,(255,255,255))
        self.screen.blit(label, (10,440))
        self.screen.blit(self.button, [300,410])
        label2 = pygame.font.SysFont(None,32).render(str("Exit"),1,(0,0,0))
        self.screen.blit(label2, (310,427))
        self.testMousePos()
        pass

    def testMousePos(self):
        label = pygame.font.SysFont(None,32).render(str(pygame.mouse.get_pos()),1,(255,255,255))
        self.screen.blit(label, (10,400))
        pass


def make_board(width):
    return [[blank] * width for _ in xrange(width)]
              
def possible_moves(board, curr):  
    return [(0,y) for y in reversed(xrange(len(board)))]if curr == PAWN_IA else [(x,0) for x in xrange(len(board))]

def moveXr(board, col, current,old_piece):
    if len(board) != (current+1) :
        if board[col][current] != blank :
            moveXr(board,col,current+1,board[col][current])
            board[col][current] = old_piece
        else :
            board[col][current] = old_piece
    else :
        board[col][current] = old_piece

def moveYr(board, row, current,old_piece):
    if len(board) != (current+1) :
        if board[current][row] != blank :
            moveYr(board,row,current+1,board[current][row])
            board[current][row] = old_piece
        else :
            board[current][row] = old_piece
    else :
        board[current][row] = old_piece

def moveX(board, col):
    import copy
    new = copy.deepcopy(board)
    moveXr(new,col,0,PAWN_PLAYER)
    return new

def moveY(board, row):
    import copy
    new = copy.deepcopy(board)
    moveYr(new,row,0,PAWN_IA)
    return new

# create a new board but with position @(col, row) changed to @player
def next_state(old, player, (col,row)):
    if player == PAWN_PLAYER:
        new = moveX(old, col)
        new[col][0] = player
    else :
        new = moveY(old,row)
        new[0][row] = player
    
    #print_board(new)

    return new

def checkNeighborXnodes(board, x, y):
    if x > 0 and x < (len(board)-1):
        if board[x-1][y]  == PAWN_PLAYER or board[x][y] == PAWN_PLAYER or board[x+1][y] == PAWN_PLAYER  :
            return True
    elif x == 0:
        if board[x][y] == PAWN_PLAYER  or board[x+1][y] == PAWN_PLAYER :
            return True
    else : #x == len(board)-1
        if board[x-1][y] == PAWN_PLAYER  or board[x][y] == PAWN_PLAYER :
            return True
    return False

def checkPathXr(board, x, y):
    if y == (len(board)-1):
        return checkNeighborXnodes(board, x, y)
    else:
        temp = False
        if x > 0 and x < (len(board)-1):
            if board[x-1][y] == PAWN_PLAYER :
                temp = checkPathXr(board,x-1,y+1)
            if temp == False and board[x][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x,y+1)
            if temp == False and board[x+1][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x+1,y+1)
            return temp
        elif x == 0:
            if board[x][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x,y+1)
            if temp == False and board[x+1][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x+1,y+1)
            return temp
        else : #x == len(board)-1
            if board[x-1][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x-1,y+1)
            if temp == False and board[x][y] == PAWN_PLAYER:
                temp = checkPathXr(board,x,y+1)
            return temp

def checkNeighborYnodes(board, x, y):
    if y > 0 and y < (len(board)-1):
        if board[x][y-1]== PAWN_IA or board[x][y]== PAWN_IA or board[x][y+1] == PAWN_IA :
            return True
    elif y == 0:
        if board[x][y]== PAWN_IA or board[x][y+1] == PAWN_IA :
            return True
    else : #y == len(board)-1
        if board[x][y-1]== PAWN_IA or board[x][y] == PAWN_IA :
            return True
    return False

def checkPathYr(board, x, y):
    if x == (len(board)-1):
        return checkNeighborYnodes(board, x, y)
    else:
        temp = False
        if y > 0 and y < (len(board)-1):
            if board[x][y-1] == PAWN_IA :
                temp = checkPathYr(board,x+1,y-1)
            if temp == False and board[x][y] == PAWN_IA:
                temp = checkPathYr(board,x+1,y)
            if temp == False and board[x][y+1] == PAWN_IA:
                temp = checkPathYr(board,x+1,y+1)
            return temp
        elif y == 0:
            if board[x][y] == PAWN_IA:
                temp = checkPathYr(board,x+1,y)
            if temp == False and board[x][y+1] == PAWN_IA:
                temp = checkPathYr(board,x+1,y+1)
            return temp
        else : #y == len(board)-1
            if board[x][y-1] == PAWN_IA:
                temp = checkPathYr(board,x+1,y-1)
            if temp == False and board[x][y] == PAWN_IA:
                temp = checkPathYr(board,x+1,y)
            return temp

def get_winner(board):
    verticalWinner, horizontalWinner, draw = False, False, False
    
    #check vertical path
    for i in range(len(board)):
        if checkPathXr(board, i, 0) :
            verticalWinner = True
            break
    
    #check orizontal path
    for i in range(len(board)):
        if checkPathYr(board, 0, i) :
            horizontalWinner = True
            break

    if verticalWinner and horizontalWinner :
        draw = True

    return verticalWinner, horizontalWinner, draw
    

def game_over(board, player, opp):
    vW, hW, draw = get_winner(board)

    if vW or hW :
        return True
    else:
        return False

# returns 10 if @you is the winner, -10 if @you is the loser
# and 0 otherwise (tie, or game not over)
def evaluate(board, you, _):
    vW, hW, draw = get_winner(board)
    if you == PAWN_PLAYER :
        if vW :
            return 10 
        if hW :
            return -10

    if you == PAWN_IA :
        if vW :
            return -10 
        if hW :
            return 10
    
    return randint(-3,3)

                

# doesn't do any error handling of bad input
def repl():
    d = 5
    if len(sys.argv) == 2:
        d = int(sys.argv[1])
    board = make_board(5)
    graphics = Graphics(board)
    player = PAWN_PLAYER
    opp = PAWN_IA
    myTurn=True

    ai = AI(ai_piece=opp,
            opp=player,
            depth=d,
            game_over_fun=game_over,
            eval_fun=evaluate,
            moves_fun=possible_moves,
            next_state_fun=next_state)

    turn = 0
    
    board = next_state(board, player, (0,0))
    print_board(board)
    graphics.update(board) 
    print "You are X"
    
    while(True):
        if myTurn :
            board, myTurn = graphics.update(board)
        else:
            pygame.display.set_caption("TARA - His turn, AI thinking...")
            print_board(board)
            vW,hW,draw = get_winner(board)    
            if game_over(board, player, opp):
                if vW :
                    print "The real player wins!"
                    message = "The real player wins!"
                elif hW:
                    print "The IA wins!"
                    message = "The IA wins!"
                else:
                    print "Draw!"
                    message = "Draw!"
                break
            print 
            #AI controls
            sys.stdout.write('The AI is thinking and the move is ')
            sys.stdout.flush()
            if turn == 0 :
                print "(0, "+str(4)+")"
                board = next_state(board, opp , (0,4))
                sleep(1)
            else:
                score, ai_move = ai.get_move(board)
                print ai_move
                board = next_state(board, opp, ai_move)
                sleep(1)
            print
            #end AI controls
            print_board(board)
            vW,hW,draw = get_winner(board)    
            if game_over(board, player, opp):
                if vW :
                    print "The real player wins!"
                    message = "The real player wins!"
                elif hW:
                    print "The IA wins!"
                    message = "The IA wins!"
                else:
                    print "Draw!"
                    message = "Draw!"
                break
            print
            print "Your turn"
            myTurn = True
            turn = turn + 1
            pygame.display.set_caption("TARA - Your turn")
        pass
    graphics.update(board)
    while(True):
        graphics.clock.tick(60)
        graphics.screen.fill(0)
        graphics.drawBoard()
        graphics.drawPieces()
        graphics.screen.blit(graphics.scorePanel, [0, 389])
        label = pygame.font.SysFont(None,32).render(message,1,(255,255,255))
        graphics.screen.blit(label, (10,400))
        graphics.screen.blit(graphics.button, [300,410])
        label2 = pygame.font.SysFont(None,32).render(str("Exit"),1,(0,0,0))
        graphics.screen.blit(label2, (310,427))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
        if pygame.mouse.get_pressed()[0] :
            if mouse[0] > 300 and mouse [0] < 360 and mouse[1] <470 and mouse[1] >410:
                exit()
        pygame.display.flip()


class AI:
    def __init__(self, ai_piece, opp, depth,
                 game_over_fun, eval_fun, moves_fun, next_state_fun):
        self.piece = ai_piece
        self.opp = opp
        self.depth = depth
        self.game_over = game_over_fun
        self.evaluate = eval_fun
        self.possible_moves = moves_fun
        self.next_state = next_state_fun
        
    def get_move(self, board):
        return self._minmax(board=board, player=self.piece, opp=self.opp, 
                           curr=self.piece, depth=self.depth,
                           alpha=-float("inf"), beta=float("inf"))
        
    def _minmax(self, board, player, opp, curr, depth, alpha, beta):
        if self.game_over(board, player, opp) or depth < 0:
            score = self.evaluate(board, player, opp)
            return (score, None)

        moves = self.possible_moves(board, curr)
        move_to_return = None
        for move in moves:
            ns = self.next_state(board, curr, move)
            score, _ = self._minmax(ns, 
                                    player,
                                    opp,
                                    curr=opp if curr == player else player,
                                    depth= depth - 1,
                                    alpha=alpha, 
                                    beta=beta)

            # alpha beta pruning
            if curr == player:
                if score > alpha:
                    alpha = score
                    move_to_return = move
                if alpha >= beta:
                    break
            else:
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break
    
        # return either max or min, respectively
        if curr == player:
            return (alpha, move_to_return)
        else:
            return (beta, None)

# prints a rectangular board with "|" separating columns
def print_board(board):
    print
    for i in xrange(len(board[0])):
        row = [board[j][i] for j in xrange(len(board))]
        row = map(str, row)
        print " | ".join(row)

if __name__ == "__main__":
    repl()


