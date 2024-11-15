import pygame as pg
import random

# Inicializa os módulos do Pygame
pg.init()

# Definindo cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Configurando a janela
window = pg.display.set_mode((1000, 600))
pg.display.set_caption("Jogo da Forca - Lógica Matemática")

# Fontes para textos
fonte = pg.font.SysFont("Courier New", 50)
fonte_rb = pg.font.SysFont("Courier New", 30)
fonte_grande = pg.font.SysFont("Courier New", 50)

# Lista de palavras e dicas relacionadas à lógica matemática
palavras_e_dicas = [
    ('PROPOSICAO', 'Conjunto de palavras que pode ser verdadeira ou falsa, mas nunca ambas.'),
    ('CONJUNCAO', 'Operação lógica onde ambas as proposições precisam ser verdadeiras.'),
    ('DISJUNCAO', 'Operação lógica verdadeira quando pelo menos uma proposição é verdadeira.'),
    ('NEGACAO', 'Operação lógica que inverte o valor da proposição.'),
    ('IMPLICACAO', 'Se P, então Q. Relação lógica onde a verdade de P implica a verdade de Q.'),
    ('BICONDICIONAL', 'Operação verdadeira somente se ambas as proposições têm o mesmo valor.'),
    ('TAUTOLOGIA', 'Proposição que sempre resulta em verdadeiro.'),
    ('CONTRADICAO', 'Proposição que sempre resulta em falso.'),
    ('QUANTIFICADOR', 'Expressão que indica a quantidade dos elementos envolvidos, como "para todo" ou "existe".'),
    ('PREDICADO', 'Expressão lógica que depende de uma ou mais variáveis.')
]

# Variáveis do jogo
tentativas_de_letras = [' ', '-']
palavra_escolhida = ''
palavra_camuflada = ''
dica = ''
end_game = True
vidas = 6
letra = ' '
click_last_status = False
jogo_ganho = False
jogo_perdido = False

# Função que desenha a forca e o boneco conforme as vidas
def Desenho_da_Forca(window, vidas):
    pg.draw.rect(window, branco, (0, 0, 1000, 600))
    pg.draw.line(window, preto, (100, 500), (100, 100), 10)
    pg.draw.line(window, preto, (50, 500), (150, 500), 10)
    pg.draw.line(window, preto, (100, 100), (300, 100), 10)
    pg.draw.line(window, preto, (300, 100), (300, 150), 10)
    if vidas <= 5:
        pg.draw.circle(window, preto, (300, 200), 50, 10)  # Cabeça
    if vidas <= 4:
        pg.draw.line(window, preto, (300, 250), (300, 350), 10)  # Corpo
    if vidas <= 3:
        pg.draw.line(window, preto, (300, 260), (225, 350), 10)  # Braço esquerdo
    if vidas <= 2:
        pg.draw.line(window, preto, (300, 260), (375, 350), 10)  # Braço direito
    if vidas <= 1:
        pg.draw.line(window, preto, (300, 350), (375, 450), 10)  # Perna direita
    if vidas == 0:
        pg.draw.line(window, preto, (300, 350), (225, 450), 10)  # Perna esquerda

# Função que desenha o botão de reiniciar centralizado na parte inferior da tela
def Desenho_Restart_Button(window):
    button_width = 200
    button_height = 65
    x = (1000 - button_width) // 2  # Centralizado horizontalmente
    y = 500  # Perto da parte inferior da tela
    pg.draw.rect(window, preto, (x, y, button_width, button_height))
    texto = fonte_rb.render('Restart', 1, branco)
    window.blit(texto, (x + 40, y + 15))

# Função para quebrar o texto em várias linhas
def Quebrar_Texto(texto, fonte, largura_max):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if fonte.size(linha_atual + palavra)[0] < largura_max:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    
    linhas.append(linha_atual)  # Adiciona a última linha
    return linhas

# Função para sortear uma palavra e dica
def Sorteando_Palavra(palavras_e_dicas, end_game, palavra_atual, dica_atual):
    if end_game:
        palavra_n = random.randint(0, len(palavras_e_dicas) - 1)
        palavra_escolhida, dica = palavras_e_dicas[palavra_n]
    else:
        palavra_escolhida = palavra_atual
        dica = dica_atual
    end_game = False
    return palavra_escolhida, dica, end_game

# Função para camuflar a palavra
def Camuflando_Palavra(palavra_escolhida, tentativas_de_letras):
    palavra_camuflada = ''
    for letra in palavra_escolhida:
        if letra in tentativas_de_letras:
            palavra_camuflada += letra
        else:
            palavra_camuflada += '#'
    return palavra_camuflada

# Função para verificar tentativa de letra
def Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, vidas):
    if letra not in tentativas_de_letras:
        tentativas_de_letras.append(letra)
        if letra not in palavra_escolhida:
            vidas -= 1
    return tentativas_de_letras, vidas

# Função para desenhar a palavra camuflada na tela
def Palavra_do_Jogo(window, palavra_camuflada):
    palavra = fonte.render(palavra_camuflada, 1, preto)
    window.blit(palavra, (200, 500))

# Função para mostrar a dica na tela
def Mostra_Dica(window, dica):
    linhas_dica = Quebrar_Texto(f'Dica: {dica}', fonte_rb, 600)
    y = 20
    for linha in linhas_dica:
        dica_renderizada = fonte_rb.render(linha, 1, preto)
        window.blit(dica_renderizada, (400, y))
        y += 40

# Função para reiniciar o jogo quando o botão é pressionado
def Restart_do_Jogo(click_last_status, click, x, y, end_game, tentativas_de_letras, vidas, jogo_ganho, jogo_perdido):
    if click_last_status == False and click[0] == True:
        button_width = 200
        button_height = 65
        button_x = (1000 - button_width) // 2
        button_y = 500
        if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
            tentativas_de_letras = [' ', '-']
            end_game = True
            vidas = 6
            jogo_ganho = False
            jogo_perdido = False
    return end_game, tentativas_de_letras, vidas, jogo_ganho, jogo_perdido

# Função para mostrar mensagem de vitória em destaque
def Mensagem_Vitoria(window, palavra, dica):
    window.fill(verde)
    texto_vitoria = f"Parabéns! A resposta correta é '{palavra}': {dica}"
    linhas_vitoria = Quebrar_Texto(texto_vitoria, fonte_grande, 900)
    y = 100
    for linha in linhas_vitoria:
        texto_renderizado = fonte_grande.render(linha, 1, preto)
        window.blit(texto_renderizado, (50, y))
        y += 80
    Desenho_Restart_Button(window)

# Função para mostrar mensagem de derrota em destaque
def Mensagem_Derrota(window, palavra, dica):
    window.fill(vermelho)
    texto_derrota = f"Você perdeu! A resposta correta é '{palavra}': {dica}. Estude mais!"
    linhas_derrota = Quebrar_Texto(texto_derrota, fonte_grande, 900)
    y = 100
    for linha in linhas_derrota:
        texto_renderizado = fonte_grande.render(linha, 1, preto)
        window.blit(texto_renderizado, (50, y))
        y += 80
    Desenho_Restart_Button(window)

# Loop principal do jogo
rodando = True
while rodando:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            rodando = False
        elif event.type == pg.KEYDOWN and not jogo_ganho and not jogo_perdido and vidas > 0: 
            letra = event.unicode.upper()
            tentativas_de_letras, vidas = Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, vidas)

    x, y = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    palavra_escolhida, dica, end_game = Sorteando_Palavra(palavras_e_dicas, end_game, palavra_escolhida, dica)
    palavra_camuflada = Camuflando_Palavra(palavra_escolhida, tentativas_de_letras)

    if '#' not in palavra_camuflada:
        jogo_ganho = True

    if vidas == 0:
        jogo_perdido = True

    if jogo_ganho:
        Mensagem_Vitoria(window, palavra_escolhida, dica)
    elif jogo_perdido:
        Mensagem_Derrota(window, palavra_escolhida, dica)
    else:
        Desenho_da_Forca(window, vidas)
        Palavra_do_Jogo(window, palavra_camuflada)
        Mostra_Dica(window, dica)

    end_game, tentativas_de_letras, vidas, jogo_ganho, jogo_perdido = Restart_do_Jogo(click_last_status, click, x, y, end_game, tentativas_de_letras, vidas, jogo_ganho, jogo_perdido)

    click_last_status = click[0]
    pg.display.update()

pg.quit()
