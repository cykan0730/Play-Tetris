from tkinter import *
import random

def playTetris():
    # Set up the dimensions for the game
    # Calculate the window size and run it
    rows = 15
    cols = 10
    cellSize = 20
    margin = 30
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    run(width, height)

def init(data):
    # Initialize all the data
    data.rows = 15
    data.cols = 10
    data.cellSize = 20
    data.margin = 30
    data.emptyColor = "blue"
    # Create a board with all the cells in blue color initially
    board = []
    for row in range(data.rows): board += [[data.emptyColor] * data.cols]
    data.board = board
    # Define the piece types
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ], [  True,  True,  True ]]
    lPiece = [[ False, False,  True ], [  True,  True,  True ]]
    oPiece = [[  True,  True ], [  True,  True ]]
    sPiece = [[ False,  True,  True ], [  True,  True, False ]]
    tPiece = [[ False,  True, False ], [  True,  True,  True ]]
    zPiece = [[  True,  True, False ], [ False,  True,  True ]]
    # Place all the piece types into a single list
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", \
                          "green", "orange" ]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors
    # Create a new falling piece
    newFallingPiece(data)
    data.isGameOver = False
    data.score = 0

def drawCell(canvas, data, row, col, color):
    # Draw a cell given its row, col and color
    x0 = data.margin + col * data.cellSize
    y0 = data.margin + row * data.cellSize
    x1 = data.margin + (col+1) * data.cellSize
    y1 = data.margin + (row+1) * data.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=4)

def drawBoard(canvas, data):
    # Draw the board
    for row in range(data.rows):
        for col in range(data.cols):
            color = data.board[row][col]
            drawCell(canvas, data, row, col, color)

def newFallingPiece(data):
    # Randomly choosing a new piece, setting its color
    # and positioning it in the middle of the top row
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = int(data.cols/2 - len(data.fallingPiece[0])//2)
    
def drawFallingPiece(canvas, data):
    # Draw the falling piece over the board
    # in the color of the falling piece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, row+data.fallingPieceRow, \
                         col+data.fallingPieceCol, data.fallingPieceColor)

def fallingPieceIsLegal(data):
    # Check whether the move in a given direction is legal
    # the falling piece cannot go beyond the board
    # and collide with a non-empty cell on the board
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                if 0 <= row+data.fallingPieceRow <= data.rows-1 and \
                   0 <= col+data.fallingPieceCol <= data.cols-1 and \
                   data.board[row+data.fallingPieceRow]\
                   [col+data.fallingPieceCol] == data.emptyColor:
                    continue
                else:
                    return False
    return True

def moveFallingPiece(data, drow, dcol):
    # Move the falling piece a given number of rows and cols
    # Fist, modify the location of the falling piece
    # Second, test whether the new location is legal
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if fallingPieceIsLegal(data) != True:
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    else:
        return True

def rotateFallingPiece(data):
    # Store the old piece, its location and its dimensions
    numOldCols = len(data.fallingPiece[0])
    numOldRows = len(data.fallingPiece)
    numNewCols, numNewRows = numOldRows, numOldCols
    newFallingPiece = []
    for row in range(numNewRows): newFallingPiece += [[False] * numNewCols]
    # Compute the new dimensions by reversing the old one
    for row in range(numOldRows):
        for col in range(numOldCols):
            if data.fallingPiece[row][col] == True:
                newFallingPiece[numOldCols-1-col][row] = True
    # Compute the new location by keeping the center of
    # the falling piece constant
    oldCenterRow = data.fallingPieceRow + int(numOldRows/2)
    newFallingPieceRow = oldCenterRow - int(numNewRows/2)
    oldCenterCol = data.fallingPieceCol + int(numOldCols/2)
    newFallingPieceCol = oldCenterCol - int(numNewCols/2)
    # Check if the rotation makes the falling piece go off
    # the board or collide with a non-empty cell on the board
    # If not, restore the piece, its location and dimension
    copyOriginalPiece = data.fallingPiece
    copyPieceRow = data.fallingPieceRow
    copyPieceCol = data.fallingPieceCol
    data.fallingPiece = newFallingPiece
    data.fallingPieceRow = newFallingPieceRow
    data.fallingPieceCol = newFallingPieceCol
    if fallingPieceIsLegal(data) != True :
        data.fallingPiece = copyOriginalPiece
        data.fallingPieceRow = copyPieceRow
        data.fallingPieceCol = copyPieceCol

def placeFallingPiece(data):
    # When the falling piece gets to the bottom
    # load the corresponding positions on the board
    # with the falling piece color
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                data.board[row+data.fallingPieceRow]\
                   [col+data.fallingPieceCol] = data.fallingPieceColor
    removeFullRows(data)
    
def removeFullRows(data):
    # Check whether there is a full row or not
    # If not, just copy over the rows
    fullRows = 0
    newboard = []
    addboard = []
    for row in range(data.rows):
        count = 0
        for col in range(data.cols):
            if data.board[row][col] != data.emptyColor:
                count += 1
        if count != data.cols:
            newboard += [data.board[row]]
        else:
            fullRows += 1
    # If there are full rows, remove them and add back the new board
    # with the blue color
    if fullRows != 0:
        for row in range(fullRows):
            addboard += [[data.emptyColor] * data.cols]
        newboard = addboard + newboard
        data.board = newboard
    # score will be incremented by the square of total number of
    # full rows removed at once
    data.score += fullRows ** 2

def drawScore(canvas, data):
    # Update the score
    canvas.create_text(data.width/2, data.margin/2, text="Score: "+\
                       str(data.score), fill="brown", \
                       font="Calibri 18 bold")

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # Press "r" to restart when game is over
    if (data.isGameOver == True):
        if (event.keysym == "r"): init(data)
    # Modify the keyPressed handler to move left, right, down
    # or rotate the falling piece
    if (event.keysym == "Left"): moveFallingPiece(data, 0, -1)
    elif (event.keysym == "Right"): moveFallingPiece(data, 0, +1)
    elif (event.keysym == "Down"): moveFallingPiece(data, +1, 0)
    elif (event.keysym == "Up"): rotateFallingPiece(data)

def timerFired(data):
    # When game is not over
    # continue to generate new piece and place them on board
    # If the falling piece is placed against the top of the board
    # then game is over
    if data.isGameOver == False:
        if moveFallingPiece(data, +1, 0) == False:
            placeFallingPiece(data)
            for col in range(data.cols):
                if data.board[0][col] != data.emptyColor:
                    data.isGameOver = True
            if data.isGameOver == False:
                newFallingPiece(data)
                if fallingPieceIsLegal(data) == False:
                    data.isGameOver = True

def redrawAll(canvas, data):
    # Draw the background, board and the falling piece
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    # If game is over, stop and draw the text
    # any key pressed or operations after will be ignored
    # except for the restart
    if data.isGameOver == True:
        canvas.create_rectangle(data.margin, data.margin+data.cellSize,\
                                data.width-data.margin, data.margin+\
                                3*data.cellSize, fill="black")
        canvas.create_text(data.margin+data.cellSize*data.cols/2, \
                           data.margin+2*data.cellSize, text="Game Over!", \
                           fill="yellow", font="Calibri 24 bold")
    # Draw the score
    drawScore(canvas, data)

####################################
# run function
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 400 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()
