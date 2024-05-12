

class C4():
    def __init__(self):

        # initialize board
        self.rows = 6
        self.cols = 7
        self.board = [["#"] * self.cols for i in range(self.rows)]

        # initialize vars
        self.gamestate = 0
        self.piece = 0
        self.homeMessage = ""
        
        # set pieces
        self.neutralPiece = ":black_square_button:"
        self.zeroPiece = ":red_circle:"
        self.onePiece = ":blue_circle:"
        #self.zeroPiece = "O"
        #self.onePiece = "1"

    # output display, returns {gamestate, board to print}
    def display(self, message=""):
        boarddisplay = ""
        for line in self.board:
            for item in line:
                match str(item):
                    case "#":
                        boarddisplay += f"{self.neutralPiece} "
                    case "1":
                        boarddisplay += f"{self.onePiece} "
                    case "0":
                        boarddisplay += f"{self.zeroPiece} "
            boarddisplay += "\n"
        boarddisplay+=":regional_indicator_a: :regional_indicator_b: :regional_indicator_c: :regional_indicator_d: :regional_indicator_e: :regional_indicator_f: :regional_indicator_g:"
        boarddisplay+="\n"+str(message)

        
        return ([self.gamestate, boarddisplay])

    def droppiece(self, row, player):
        
        try:
            # Convert from letter row to int value 0-6
            numCol = ord(row.lower())-97
            if(numCol>6):
                raise Exception()
        except:
            return self.display("Invalid input")

        # Drop piece
        for i in range(6):
            # If piece found on board, place above it
            if(self.board[i][numCol] != '#'):
                if(i != 0):
                    self.board[i-1][numCol] = self.piece
                # If top slot is filled
                else:
                    return (self.display("Invalid Placement"))
                # invert piece for next turn 
                self.piece = int(not self.piece)

                # Check for win, display board
                return (self.checkwin(player, f"{player} dropped a piece in row {row}"))
            
            # If no piece is found, place in bottom slot
            elif(i == len(self.board)-1):
                self.board[i][numCol] = self.piece 
                # invert piece for next turn 
                self.piece = int(not self.piece)

                # Check for win, display board
                return (self.checkwin(player, f"{player} dropped a piece in row {row}"))
    
    def checkwin(self, player, message):

        # Check rows for a win
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if self.board[i][j] != "#" and self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3]:
                    self.gamestate = 1
                    return self.display(f"{player} WINS!")

        # Check columns for a win
        for i in range(self.rows - 3):
            for j in range(self.cols):
                if self.board[i][j] != "#" and self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j]:
                    self.gamestate = 1
                    return self.display(f"{player} WINS!")

        # Check diagonals (positive slope) for a win
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                if self.board[i][j] != "#" and self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3]:
                    self.gamestate = 1
                    return self.display(f"{player} WINS!")

        # Check diagonals (negative slope) for a win
        for i in range(3, self.rows):
            for j in range(self.cols - 3):
                if self.board[i][j] != "#" and self.board[i][j] == self.board[i-1][j+1] == self.board[i-2][j+2] == self.board[i-3][j+3]:
                    self.gamestate = 1
                    return self.display(f"{player} WINS!")
        
        # Check to make sure all slots aren't filled
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != "#":
                    return self.display(message)
        
        self.gamestate = 2
        return self.display("This shit full, game over nobody wins")
    
    def setHomeMessage(self,messageID):
        self.homeMessage = messageID
    
    def getHomeMessage(self):
        return self.homeMessage
