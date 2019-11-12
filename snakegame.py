##### SNAKE GAME ####
import pygame, random
from pygame.locals import *

pygame.init() #INICIA O PYGAME
'''Carrega os arquivos'''
crunch_sound = pygame.mixer.Sound("crunch.wav")
direction_sound = pygame.mixer.Sound("game_bump.wav")
apple_img = pygame.image.load("apple.png")
menu_img = pygame.image.load("menu1.png")

def on_grid_random(): #FUNÇÃO PARA MAÇA FICAR ALINHADA
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10) #SÓ PODERÁ SER VALORES MULTIPLOS DE 10 PARA FICAR ALINHADA E NÃO APARECER FORA DA TELA

def collision(c1, c2): #FUNÇÃO QUE TESTA CONDIÇÃO SE INICIO DA SNAKE ESTÁ NO MESMO LUGAR DA MAÇA
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# ATRIBUIÇÃO DE VARIAVEIS PARA MOVIMENTAÇÃO DA SNAKE
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

screen = pygame.display.set_mode((600, 600)) #TAMANHO DA TELA DO JOGO
pygame.display.set_caption("Snake Game ") #NOME QUE APARECE NA TELA DO JOGO

snake = [(200, 200), (210, 200), (220, 200)] #TAMANHO DA SNAKE E LUGAR QUE ELA VAI COMEÇAR NA TELA
snake_skin = pygame.Surface((10, 10)) #TAMANHO DE CADA QUADRADO DA SNAKE
snake_skin.fill((107, 142, 35))  #COR DA SNAKE EM RBG

apple_pos = on_grid_random() #POSIÇÃO DA MAÇA, ESTÁ CHAMANDO A FUNÇÃO QUE CRIARÁ UMA MAÇA EM ALGUM LUGAR ALEATÓRIO

my_direction = LEFT #SNAKE INICIA ANDANDO PARA ESQUERDA

clock = pygame.time.Clock() #CLOCK PARA PODER TER MOVIMENTAÇÃO DA SNAKE

font = pygame.font.Font('freesansbold.ttf', 17)
score = 0

screen_menu = True

while screen_menu:
    screen.blit(menu_img, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():  #TIPOS DE POSSIVEIS EVENTOS NO GAME:
        if event.type == QUIT: # EM CASO DE QUIT
            pygame.quit()
            exit() # IRA FECHAR O JOGO
        if event.type == KEYDOWN: #EVENTOS EM QUE ALGUMA TECLA É PRESSIONADA:
            if event.key == K_s: # SE APERTAR A TECLA "S"
                screen_menu = False # VAI FECHAR O MENU E IR PRO JOGO

game_over = False #GAME OVER
while True: #ENQUANTO NAO DER GAME OVER VAI RODAR:
    ''' NIVEIS DE VELOCIDADE CONFORME SCORE'''
    clock.tick(score+5)

    for event in pygame.event.get():  #TIPOS DE POSSIVEIS EVENTOS NO GAME:
        if event.type == QUIT: # EM CASO DE QUIT
            pygame.quit()
            exit() # IRA FECHAR O JOGO

        if event.type == KEYDOWN: #EVENTOS EM QUE ALGUMA TECLA É PRESSIONADA:
            if event.key == K_UP and my_direction != DOWN: # SE APERTAR *CIMA* E A SNAKE NÃO ESTIVER ANDANDO PRA BAIXO:
                my_direction = UP # A SNAKE IRA EM DIREÇÃO PARA CIMA
                pygame.mixer.Sound.play(direction_sound)
            elif event.key == K_DOWN and my_direction != UP: # SE APERTAR *BAIXO* E A SNAKE NÃO ESTIVER ANDANDO PRA CIMA:
                my_direction = DOWN # A SNAKE IRA PARA BAIXO
                pygame.mixer.Sound.play(direction_sound)
            elif event.key == K_LEFT and my_direction != RIGHT: # SE APERTAR *ESQUERDA* E A SNAKE NÃO ESTIVER ANDANDO PRA DIREITA:
                my_direction = LEFT # A SNAKE IRA PARA ESQUERDA
                pygame.mixer.Sound.play(direction_sound)
            elif event.key == K_RIGHT and my_direction != LEFT: # SE APERTAR *DIREITA* E A SNAKE NÃO ESTIVER ANDANDO PRA ESQUERDA:
                my_direction = RIGHT # A SNAKE IRA PARA DIREITA
                pygame.mixer.Sound.play(direction_sound)

    if collision(snake[0], apple_pos): # TESTA SE OCORRE COLISÃO CHAMANDO A FUNÇÃO
        apple_pos = on_grid_random() # MAÇA IRA SE REPOSIONAR EM ALGUM LUGAR ALEATÓRIO
        snake.append((0, 0)) # SERA ADICIONADO UM PEDAÇO A MAIS NA SNAKE
        score = score + 1 #PONTUAÇÃO IRA AUMENTAR EM 1
        pygame.mixer.Sound.play(crunch_sound) #EFEITO SONORO DE COMER A MAÇA
    # VERIFICA SE SNAKE VAI COLIDIR COM AS BORDAS
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True

    # VERIFICA SE SNAKE COLIDE EM SI PRÓPRIA
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    # MOVIMENTAÇÃO DA SNAKE:
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((238, 232, 170)) # COR FUNDO DA TELA
    screen.blit(apple_img, apple_pos) #COLOCANDO MAÇA NA TELA

    for x in range(0, 600, 10):  # DESENHA LINHAS VERTICAIS
        pygame.draw.line(screen, (255, 250, 205), (x, 0), (x, 600)) # LINHAS VERTICAIS
    for y in range(0, 600, 10):  # DESENHA LINHAS HORIZONTAIS
        pygame.draw.line(screen, (255, 250, 205), (0, y), (600, y)) # LINHAS HORIZONTAIS

    score_font = font.render("Score: %s" % (score), True, (0, 0, 0)) # SCORE LAYOUT
    score_rect = score_font.get_rect()
    score_rect.topleft = (500, 10) # POSIÇÃO DO SCORE LAYOUT
    screen.blit(score_font, score_rect) # MOSTRA NA TELA O SCORE

    for pos in snake: # MOSTRA NA TELA A SNAKE
        screen.blit(snake_skin, pos)

    pygame.display.update() # ATUALIZA O DISPLAY

    while game_over:
        game_over_font = pygame.font.Font("freesansbold.ttf", 80)
        game_over_screen = game_over_font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (300, 200)
        screen.blit(game_over_screen, game_over_rect)

        restart_font = pygame.font.Font("freesansbold.ttf", 40)
        restart_font_screen = restart_font.render('Press "r" to restart', True, (0, 0, 0))
        screen.blit(restart_font_screen, (120, 300))
        pygame.display.update()
        pygame.time.wait(20)

        if event.type == KEYDOWN:  # EVENTOS EM QUE ALGUMA TECLA É PRESSIONADA:
            if event.key == K_r:
                game_over = False
                score = 0
                snake = [(200, 200), (210, 200), (220, 200)]  # TAMANHO DA SNAKE E LUGAR QUE ELA VAI COMEÇAR NA TELA
                my_direction = LEFT  # SNAKE INICIA ANDANDO PARA ESQUERDA

        for event in pygame.event.get():  # TIPOS DE POSSIVEIS EVENTOS NO GAME:
            if event.type == QUIT:  # EM CASO DE QUIT
                pygame.quit()
                exit()  # IRA FECHAR O JOGO


