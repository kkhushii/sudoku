import pygame
import requests
import time

bg_color = (102, 102, 153)
WIDTH = 550
og_grid_ele_color = (255, 128, 128)
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y]for y in range(len(grid[0]))]for x in range(len(grid))]

def isEmpty(num):
    if num == 0:
        return True
    return False

def isValid(position, num):
    #checking for row
    for i in range(0, len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    
    #checking  for column
    for i in range(0, len(grid[0])):
        if(grid[i][position[1]] == num):
            return False

    #checking subgrid
    x = position[0]//3*3
    y = position[1]//3*3  
    #gives box number
    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j] == num):
                return False
    return True

solved = 0
def sudoku_solver(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(isEmpty(grid[i][j])):
                for k in range(1,10):
                    if isValid((i,j),k):
                        grid[i][j] = k
                        pygame.draw.rect(win, bg_color,((j+1)*50+buffer, (i+1)*50+buffer, 50-2*buffer, 50-2*buffer))
                        value = myfont.render(str(k), True, (0,0,0))
                        win.blit(value,((j+1)*50 +15, (i+1)*50))
                        pygame.display.update()
                        pygame.time.delay(25)

                        sudoku_solver(win)

                        #exit
                        global solved
                        if(solved == 1):
                            return

                        #if solver returns, there's a mismatch
                        grid[i][j] = 0
                        pygame.draw.rect(win, bg_color, ((j+1)*50+buffer, (i+1)*50+buffer, 50-2*buffer, 50-2*buffer))
                return

    solved = 1
    return


def insert(win, position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        global strikes
        strikes = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != 0):
                    return
                if(event.key == 48):           #checking with zero
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, bg_color,(position[0]*50+buffer,position[1]*50+buffer,50-2*buffer,50-2*buffer))
                if(0 < event.key-48 < 10):     #we are checking for valid input
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    if isValid((i,j), event.key-48):
                        pygame.draw.rect(win, bg_color,(position[0]*50+buffer,position[1]*50+buffer,50-2*buffer,50-2*buffer))
                        win.blit(value,(position[0]*50+15, position[1]*50))
                        grid[i-1][j-1] = event.key - 48
                    else:
                        grid[i-1][j-1] = 48
                        pygame.draw.rect(win, bg_color,(position[0]*50+buffer,position[1]*50+buffer,50-2*buffer,50-2*buffer))
                        strikes += 1
                        #drawing strikes
                        text = myfont.render("X " * strikes, 1, (255, 0, 0))
                        win.blit(text, (50, 500))
                        
                return

def format_time(secs):
    sec = secs%60
    minute = secs//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def draw_board(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0,10):
        if(i%3==0):
            pygame.draw.line(win,(0,0,0),(50+50*i,50),(50+50*i,500),4)
            pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),4)
        pygame.draw.line(win,(0,0,0),(50+50*i,50),(50+50*i,500),2)
        pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),2)


    for i in range(0,len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, og_grid_ele_color)
                win.blit(value, ((j+1)*50+15, (i+1)*50))
    

def redraw(win, play_time, strikes):
    win.fill(bg_color)
    #drawing time
    myfont = pygame.font.SysFont("Comic Sans MS", 35)
    text = myfont.render("Time: " + format_time(play_time), 1, (0,0,0))
    win.blit(text, (330, 500))
    #drawing strikes
    text = myfont.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (50, 500))
    #drawing board
    draw_board(win)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH,WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(bg_color)
    strikes = 0
    start = time.time()

    

    while True:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))          
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_SPACE):
                    sudoku_solver(win)
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        redraw(win, play_time,strikes)
        pygame.display.update()

main()