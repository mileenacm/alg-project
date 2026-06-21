import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# --- CONFIGURAÇÕES DA TELA ---
LARGURA, ALTURA = 600, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo: Desvie dos Blocos!")

# --- CORES (RGB) ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)
VERDE = (50, 255, 50)

# --- PROPRIEDADES DO JOGADOR ---
jogador_tam = 50
jogador_x = LARGURA // 2 - jogador_tam // 2
jogador_y = ALTURA - jogador_tam - 20
jogador_velocidade = 7

# --- PROPRIEDADES DOS INIMIGOS (BLOCOS) ---
inimigo_tam = 50
inimigo_x = random.randint(0, LARGURA - inimigo_tam)
inimigo_y = -inimigo_tam
inimigo_velocidade = 5

# --- PONTUAÇÃO ---
pontos = 0
fonte = pygame.font.SysFont("monospace", 30)

# --- LOOP PRINCIPAL ---
relogio = pygame.time.Clock()
jogando = True

while jogando:
    relogio.tick(60)  # Limita a 60 FPS

    # 1. CAPTURA DE EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    # Movimentação do jogador (Seta Esquerda e Direita)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador_x > 0:
        jogador_x -= jogador_velocidade
    if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_tam:
        jogador_x += jogador_velocidade

    # 2. LÓGICA DO JOGO
    # Faz o inimigo cair
    inimigo_y += inimigo_velocidade

    # Se o inimigo passar do final da tela, ele ressurge no topo
    if inimigo_y > ALTURA:
        inimigo_y = -inimigo_tam
        inimigo_x = random.randint(0, LARGURA - inimigo_tam)
        pontos += 1

        # Aumenta a velocidade do jogo a cada 3 pontos
        if pontos % 3 == 0:
            inimigo_velocidade += 1

    # Criando os retângulos para checar colisão
    retangulo_jogador = pygame.Rect(jogador_x, jogador_y, jogador_tam, jogador_tam)
    retangulo_inimigo = pygame.Rect(inimigo_x, inimigo_y, inimigo_tam, inimigo_tam)

    # Checa colisão da forma correta
    if retangulo_jogador.colliderect(retangulo_inimigo):
        print(f"Fim de Jogo! Você fez {pontos} pontos.")
        jogando = False

    # 3. DESENHAR NA TELA
    tela.fill(PRETO)

    # Desenha o jogador e o inimigo
    pygame.draw.rect(tela, VERDE, retangulo_jogador)
    pygame.draw.rect(tela, VERMELHO, retangulo_inimigo)

    # Desenha o placar
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()


