# Bricks
# By Nick, 2018.
# needed: Python3.5, pygame1.3

import pygame, sys, time, random
from pygame.locals import *
from pygame.color import THECOLORS

# 定义宽高
WINDOW_WIDTH, WINDOW_HEIGHT       = 640, 480
BACKGROUND_COLOR                  = (0, 0, 0)
BALL_SIZE                         = 4
BALL_COLOR                        = (255, 0, 0)
GAME_STATE_INIT                   = 0
GAME_STATE_START_LEVEL            = 1
GAME_STATE_RUN                    = 2
GAME_STATE_SHUTDOWN               = 3
GAME_STATE_EXIT                   = 4
PADDLE_START_X, PADDLE_START_Y    = 300, WINDOW_HEIGHT - 50
PADDLE_WIDTH, PADDLE_HEIGHT       = 80, 5
NUM_BLOCK_COLUMNS, NUM_BLOCK_ROWS = 6, 4
BLOCK_ORIGIN_X, BLOCK_ORIGIN_Y    = 50, 10
BLOCK_COLOR                       = (9, 250, 88)
BLOCK_WIDTH, BLOCK_HEIGHT         = 50, 10
BLOCK_X_GAP, BLOCK_Y_GAP          = 100, 40

# 初始化
pygame.init()
mainClock = pygame.time.Clock()
paddle = {"rect":pygame.Rect(PADDLE_START_X, PADDLE_START_Y, PADDLE_WIDTH, PADDLE_HEIGHT),
          "color":(108, 79, 80)}
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
iconSurface   = pygame.image.load("block.ico")
pygame.display.set_caption("Block Breaker")
pygame.display.set_icon(iconSurface)
game_state = 0
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(paddle['rect'].centerx, paddle['rect'].centery)

# 初始化砖块数组
def InitBlocks():
    #blocks = [[1] * NUM_BLOCK_COLUMNS] * NUM_BLOCK_ROWS
    blocks = []
    for i in range(NUM_BLOCK_ROWS):             #@UnusedVarialbe
        blocks.append([1] * NUM_BLOCK_COLUMNS)
    return blocks

# game main loop
while True:
    # 事件监听
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                paddle_move_left = True
            if event.key == K_RIGHT:
                paddle_move_right = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                paddle_move_left = False
            if event.key == K_RIGHT:
                paddle_move_right = False
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == MOUSEMOTION:
            paddle['rect'].move_ip(event.pos[0] - paddle['rect'].centerx, 0)
    
    if game_state == GAME_STATE_INIT:
        # 初始化游戏
        ball_x  = random.randint(10, WINDOW_WIDTH-10)
        ball_y  = random.randint(200, WINDOW_HEIGHT-10)
        ball_dx = random.randint(-5, 10)
        ball_dy = random.randint(-10, 2)
		
        paddle['rect'].left = PADDLE_START_X
        paddle['rect'].top  = PADDLE_START_Y
        
        paddle_move_left  = False
        paddle_move_right = False
        
        game_state = GAME_STATE_START_LEVEL
    elif game_state == GAME_STATE_START_LEVEL:
        # 新的一关
        blocks = InitBlocks()
        game_state = GAME_STATE_RUN
    elif game_state == GAME_STATE_RUN:
        # 游戏运行
        
        # 球的运动
        ball_x += ball_dx;
        ball_y += ball_dy;
        
        if ball_x > (WINDOW_WIDTH-BALL_SIZE) or ball_x < BALL_SIZE:
            ball_dx = -ball_dx
            ball_x  += ball_dx;
        elif ball_y > (WINDOW_HEIGHT-BALL_SIZE) or ball_y < BALL_SIZE:
            ball_dy = -ball_dy
            ball_y  += ball_dy
            
        # 球碰挡板后弹开
        if ( (ball_x + BALL_SIZE) <= (paddle['rect'].left + paddle['rect'].width) \
              and (ball_x >= paddle['rect'].left) \
              and ((ball_y + BALL_SIZE) >= paddle['rect'].top) \
              and (ball_y <= paddle['rect'].top + paddle['rect'].height) ):
            ball_dy = -ball_dy
            ball_x += ball_dx
            ball_y += ball_dy
            ball_dx += random.randint(-3, 2)
                
        # 球碰砖块后弹开
        cur_x = BLOCK_ORIGIN_X
        cur_y = BLOCK_ORIGIN_Y
        for row in range(NUM_BLOCK_ROWS):
            cur_x = BLOCK_ORIGIN_X
            for col in range(NUM_BLOCK_COLUMNS):
                if blocks[row][col] != 0:
                    if (ball_x+BALL_SIZE >= cur_x and \
                        ball_x-BALL_SIZE <= cur_x+BLOCK_WIDTH and \
                        ball_y+BALL_SIZE >= cur_y and \
                        ball_y-BALL_SIZE <= cur_y+BLOCK_HEIGHT):
                        blocks[row][col] = 0
                        ball_dy = -ball_dy
                        ball_dx += random.randint(-2, 2) 
                cur_x += BLOCK_X_GAP
            cur_y += BLOCK_Y_GAP
        
        # 挡板的运动and随鼠标运动
        if paddle_move_left:
            paddle['rect'].left -= 8
            if paddle['rect'].left < 0:
                paddle['rect'].left = 0
        if paddle_move_right:
            paddle['rect'].left += 8
            if paddle['rect'].left > WINDOW_WIDTH-PADDLE_WIDTH:
                paddle['rect'].left = WINDOW_WIDTH-PADDLE_WIDTH
        
        game_state = GAME_STATE_RUN
		
        #绘制过程		
        windowSurface.fill(BACKGROUND_COLOR)
		
        pygame.draw.rect(windowSurface, paddle['color'], paddle['rect'])
        pygame.draw.circle(windowSurface, BALL_COLOR, (ball_x, ball_y), BALL_SIZE, 0)
		# 绘制砖块
        cur_x = BLOCK_ORIGIN_X
        cur_y = BLOCK_ORIGIN_Y
        for row in range(NUM_BLOCK_ROWS):
            cur_x = BLOCK_ORIGIN_X
            for col in range(NUM_BLOCK_COLUMNS):
                if blocks[row][col] != 0:
                    pygame.draw.rect(windowSurface, BLOCK_COLOR, 
                                     (cur_x, cur_y, BLOCK_WIDTH, BLOCK_HEIGHT))
                cur_x += BLOCK_X_GAP
            cur_y += BLOCK_Y_GAP
			
    elif game_state == GAME_STATE_SHUTDOWN:
        game_state = GAME_STATE_EXIT
    
    pygame.display.update()
    mainClock.tick(60)
