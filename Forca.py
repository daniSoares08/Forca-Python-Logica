import pygame as pg  # Importa a biblioteca Pygame e a renomeia como 'pg' para facilitar o uso
import random  # Importa a biblioteca random, que permite gerar números aleatórios

# Cores do jogo definidas em formato RGB (Red, Green, Blue)
branco = (255, 255, 255)  # Branco puro
preto = (0, 0, 0)  # Preto puro

# Setup da tela do Jogo com dimensões 1000x600
window = pg.display.set_mode((1000, 600))  # Cria a janela do jogo com largura de 1000 pixels e altura de 600 pixels

# Inicializando o sistema de fontes do Pygame para exibir textos
pg.font.init()  # Inicializa as funções de fontes no Pygame

# Escolhendo a fonte "Courier New" com tamanho 50 para exibir a palavra camuflada no jogo
fonte = pg.font.SysFont("Courier New", 50)

# Escolhendo a mesma fonte, porém com tamanho 30, para o botão "Restart"
fonte_rb = pg.font.SysFont("Courier New", 30)

# Lista de palavras que podem ser sorteadas aleatoriamente no jogo da forca
palavras = ['PARALELEPIPEDO', 'ORNITORINCO', 'APARTAMENTO', 'XICARA DE CHA']

# Variáveis iniciais
tentativas_de_letras = [' ', '-']  # Lista que contém as letras já tentadas, iniciando com espaço e hífen
palavra_escolhida = ''  # Armazena a palavra sorteada, inicialmente vazia
palavra_camuflada = ''  # Armazena a palavra camuflada (com letras ocultas), inicialmente vazia
end_game = True  # Indica se o jogo terminou ou não, inicia como verdadeiro para sortear uma nova palavra
chance = 0  # Contador de chances/erros do jogador
letra = ' '  # Armazena a última letra tentada, inicialmente vazia
click_last_status = False  # Armazena o estado anterior do clique do mouse

# Função para desenhar a forca e partes do corpo conforme o número de erros (chance)
def Desenho_da_Forca(window, chance):
    # Preenche o fundo da tela com a cor branca
    pg.draw.rect(window, branco, (0, 0, 1000, 600))
    # Desenha a base e a estrutura da forca
    pg.draw.line(window, preto, (100, 500), (100, 100), 10)  # Linha vertical da base
    pg.draw.line(window, preto, (50, 500), (150, 500), 10)  # Linha horizontal da base
    pg.draw.line(window, preto, (100, 100), (300, 100), 10)  # Linha horizontal do topo
    pg.draw.line(window, preto, (300, 100), (300, 150), 10)  # Linha vertical do topo
    # Desenho das partes do corpo conforme o número de erros
    if chance >= 1:  # Cabeça é desenhada se o jogador erra 1 vez ou mais
        pg.draw.circle(window, preto, (300, 200), 50, 10)  # Desenha a cabeça
    if chance >= 2:  # Tronco é desenhado se o jogador erra 2 vezes ou mais
        pg.draw.line(window, preto, (300, 250), (300, 350), 10)  # Desenha o tronco
    if chance >= 3:  # Braço direito é desenhado se o jogador erra 3 vezes ou mais
        pg.draw.line(window, preto, (300, 260), (225, 350), 10)  # Desenha o braço direito
    if chance >= 4:  # Braço esquerdo é desenhado se o jogador erra 4 vezes ou mais
        pg.draw.line(window, preto, (300, 260), (375, 350), 10)  # Desenha o braço esquerdo
    if chance >= 5:  # Perna direita é desenhada se o jogador erra 5 vezes ou mais
        pg.draw.line(window, preto, (300, 350), (375, 450), 10)  # Desenha a perna direita
    if chance >= 6:  # Perna esquerda é desenhada se o jogador erra 6 vezes ou mais (fim de jogo)
        pg.draw.line(window, preto, (300, 350), (225, 450), 10)  # Desenha a perna esquerda

# Função para desenhar o botão de "Restart" na tela
def Desenho_Restart_Button(window):
    pg.draw.rect(window, preto, (700, 100, 200, 65))  # Desenha um retângulo preto para o botão
    texto = fonte_rb.render('Restart', 1, branco)  # Renderiza o texto "Restart" na cor branca
    window.blit(texto, (740, 120))  # Exibe o texto na posição especificada dentro do botão

# Função para sortear uma nova palavra quando o jogo começa ou reinicia
def Sorteando_Palavra(palavras, palavra_escolhida, end_game):
    if end_game == True:  # Se o jogo terminou (ou está reiniciando)
        palavra_n = random.randint(0, len(palavras) - 1)  # Escolhe um índice aleatório da lista de palavras
        palavra_escolhida = palavras[palavra_n]  # Seleciona a palavra correspondente ao índice sorteado
        end_game = False  # Sinaliza que o jogo está em andamento
        chance = 0  # Reinicia o contador de erros
    return palavra_escolhida, end_game  # Retorna a palavra sorteada e o estado do jogo

# Função para camuflar a palavra sorteada, ocultando as letras não adivinhadas
def Camuflando_Palavra(palavra_escolhida, palavra_camuflada, tentativas_de_letras):
    palavra_camuflada = palavra_escolhida  # Começa com a palavra inteira
    for n in range(len(palavra_camuflada)):  # Percorre cada letra da palavra
        if palavra_camuflada[n:n + 1] not in tentativas_de_letras:  # Se a letra não foi tentada ainda
            palavra_camuflada = palavra_camuflada.replace(palavra_camuflada[n], '#')  # Substitui a letra por '#'
    return palavra_camuflada  # Retorna a palavra camuflada

# Função para processar uma nova tentativa de letra
def Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, chance):
    if letra not in tentativas_de_letras:  # Se a letra ainda não foi tentada
        tentativas_de_letras.append(letra)  # Adiciona a letra à lista de tentativas
    if letra not in palavra_escolhida:  # Se a letra não está na palavra
        chance += 1  # Incrementa o contador de erros (chance)
    elif letra in tentativas_de_letras:  # Se a letra já foi tentada, não faz nada
        pass
    return tentativas_de_letras, chance  # Retorna as tentativas e o número de erros

# Função para exibir a palavra (camuflada ou completa) na tela
def Palavra_do_Jogo(window, palavra_camuflada):
    palavra = fonte.render(palavra_camuflada, 1, preto)  # Renderiza a palavra camuflada usando a fonte
    window.blit(palavra, (200, 500))  # Exibe a palavra na tela na posição (200, 500)

# Função para reiniciar o jogo se o botão de restart for clicado
def Restart_do_Jogo(palavra_camuflada, end_game, chance, letra, tentativas_de_letras, click_last_status, click, x, y):
    count = 0  # Inicializa o contador de letras adivinhadas
    limite = len(palavra_camuflada)  # Define o limite como o comprimento da palavra
    for n in range(len(palavra_camuflada)):  # Percorre a palavra camuflada
        if palavra_camuflada[n] != '#':  # Conta as letras já reveladas
            count += 1
    if count == limite and click_last_status == False and click[0] == True:  # Se todas as letras foram reveladas e o botão foi clicado
        if x >= 700 and x <= 900 and y >= 100 and y <= 165:  # Verifica se o clique foi na área do botão de restart
            tentativas_de_letras = [' ', '-']  # Reseta as tentativas de letras
            end_game = True  # Marca o fim do jogo para iniciar um novo
            chance = 0  # Reseta o contador de chances
            letra = ' '  # Reseta a última letra
    return end_game, chance, tentativas_de_letras, letra  # Retorna o estado do jogo atualizado

# Loop principal do jogo
while True:
    # Verifica os eventos que estão acontecendo no jogo (teclado, mouse, etc.)
    for event in pg.event.get():
        if event.type == pg.QUIT:  # Se o jogador fechar a janela do jogo
            pg.quit()  # Encerra o Pygame
    # Lê a posição do mouse e o status dos cliques
    x, y = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    # Desenho da forca e botão de restart
    Desenho_da_Forca(window, chance)
    Desenho_Restart_Button(window)
    # Sorteia uma nova palavra se o jogo começou/reiniciou
    palavra_escolhida, end_game = Sorteando_Palavra(palavras, palavra_escolhida, end_game)
    # Atualiza a palavra camuflada conforme as tentativas
    palavra_camuflada = Camuflando_Palavra(palavra_escolhida, palavra_camuflada, tentativas_de_letras)
    # Exibe a palavra camuflada na tela
    Palavra_do_Jogo(window, palavra_camuflada)
    # Reinicia o jogo se o botão de restart for clicado
    end_game, chance, tentativas_de_letras, letra = Restart_do_Jogo(palavra_camuflada, end_game, chance, letra, tentativas_de_letras, click_last_status, click, x, y)
    # Atualiza o status do último clique do mouse
    click_last_status = click[0]
    # Atualiza a tela do jogo
    pg.display.update()