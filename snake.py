import pygame as pg
from pygame.locals import *
from sys import exit
from random import randint

# inicio
pg.init()
pg.font.init()

# background musica
pg.mixer.music.set_volume(0.15)
musica_fundo = pg.mixer.music.load('MidnightRanger.mp3')
pg.mixer.music.play(-1)

# barulho de ponto
pontos_barulho = pg.mixer.Sound('stomp.wav')

# barulho de morte
morte_barulho = pg.mixer.Sound('smw_lost_a_life.wav')

# especificações da tela
largura = 640
altura = 480

# especificações da cobra
velocidade = 10
x_controle = 0
y_controle = 0
x_snake = largura // 2
y_snake = altura // 2

# posição da maçã
x_apple = randint(40, 600)
y_apple = randint(50, 430)

# morte
morreu = False

# texto
fonte = pg.font.SysFont('palatinolinotype', 40, True, True)
pontos = 0

# screen
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Snake Game')
relogio = pg.time.Clock()
snake_body = []
comprimento = 0


# função para aumentara cobra
def more_snake(snake_body):
    for XeY in snake_body:
        pg.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


def reiniciar_jogo():
    global pontos, comprimento, x_snake, y_snake, x_apple, y_apple, snake_body, snake_head, morreu
    pontos = 0
    comprimento = 0
    x_snake = largura // 2
    y_snake = altura // 2
    x_apple = randint(40, 600)
    y_apple = randint(50, 430)
    snake_body = []
    snake_head = []
    morreu = False


# ações
while True:
    relogio.tick(30)
    tela.fill((255, 255, 255))
    mensagem = f'PONTOS: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))

    # verificação de eventos
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade

    x_snake += x_controle
    y_snake += y_controle

    # cobra
    snake = pg.draw.rect(tela, (0, 255, 0), (x_snake, y_snake, 20, 20))

    # maçã
    apple = pg.draw.rect(tela, (255, 0, 0), (x_apple, y_apple, 20, 20))

    # colisão
    if snake.colliderect(apple):
        pontos_barulho.play()
        pontos += 1
        x_apple = randint(40, 600)
        y_apple = randint(50, 430)
        comprimento += 1

    # fazendo o aumento da cobra
    snake_head = [x_snake, y_snake]
    snake_body.append(snake_head)

    if snake_body.count(snake_head) > 1:
        pg.mixer.music.stop()
        morte_barulho.play()
        fonte2 = pg.font.SysFont('palatinolinotype', 20, True, True)
        mensagem2 = 'GAME OVER! Pressione [R] para jogar novamente.'
        textoF2 = fonte2.render(mensagem2, True, (0, 0, 0))
        ret_texto = textoF2.get_rect()

        morreu = True
        while morreu:
            tela.fill((200, 200, 200))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
                        pg.mixer.music.play(-1)

            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(textoF2, ret_texto)
            pg.display.update()

    if x_snake > largura:
        x_snake = 0
    if x_snake < 0:
        x_snake = largura
    if y_snake > altura:
        y_snake = 0
    if y_snake < 0:
        y_snake = altura

    if len(snake_body) > comprimento:
        del snake_body[0]
    more_snake(snake_body)

    tela.blit(texto_formatado, (400, 40))

    pg.display.update()
