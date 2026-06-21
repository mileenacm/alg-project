import pygame
import sys

pygame.init()
pygame.mixer.init()
pygame.font.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dream Wardrobe")
relogio = pygame.time.Clock()

try:
    pygame.mixer.music.load("assets/sons/trilha.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
except pygame.error:
    som_clique = None

img_modelos = []

try:
    imagem_fundo_jogo = pygame.image.load("assets/imagens/fundo.png")
    imagem_fundo_jogo = pygame.transform.scale(imagem_fundo_jogo, (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Não consegui carregar o fundo: {e}")
    imagem_fundo_jogo = None

try:
    img_modelos = [
        pygame.image.load("assets/imagens/boneca01.png"),  # Aisha
        pygame.image.load("assets/imagens/boneca02.png"),  # Chloe
    ]
except pygame.error as e:
    print(f"Aviso: Criando superfícies temporárias para as bonecas: {e}")
    img_modelos = [pygame.Surface((200, 400), pygame.SRCALPHA) for _ in range(2)]
    img_modelos[0].fill((200, 150, 150))
    img_modelos[1].fill((150, 150, 200))

COR_CARD = (255, 255, 255)
COR_DOURADA= (184,134,11)
COR_TEXTO = (65, 43, 21)
COR_BOTAO = (223, 203, 236)
COR_BOTAO_HOVER = (247, 206, 221)
COR_PRONTO = (160, 210, 180)
COR_DESTAQUE = (255, 105, 180)

fonte_titulo = pygame.font.Font("assets/font/fonte.ttf", 60)
fonte_subtitulo = pygame.font.SysFont(None, 36)
fonte_comum = pygame.font.SysFont(None, 24)

ESTADO_MENU = "MENU"
ESTADO_SELECAO = "SELECAO"
ESTADO_GAMEPLAY = "GAMEPLAY"
ESTADO_AVALIACAO = "AVALIACAO"

estado_atual = "MENU"
modelos_nomes = ["Aisha", "Chloe"]
modelo_selecionado = 0
eventos = ["Show", "Faculdade", "Academia"]
evento_atual_idx = 0


roupas = [
    {"nome": "blusa azul", "tipo": "blusa", "arquivo": "blusaazul.png",
     "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
    {"nome": "blusa branca", "tipo": "blusa", "arquivo": "blusabranca.png",
     "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
    {"nome": "Top Esportivo ", "tipo": "blusa", "arquivo": "topbranco.png",
     "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},
    {"nome": "Saia", "tipo": "calca", "arquivo": "saiapreta.png",
     "pontos": {"Show": 50, "Faculdade": 30, "Academia": 10}},
    {"nome": "Jeans Largo Baggy", "tipo": "calca", "arquivo": "calça.png",
     "pontos": {"Show": 35, "Faculdade": 50, "Academia": 10}},
    {"nome": "Shorts Tactel", "tipo": "calca", "arquivo": "shortpreto.png",
     "pontos": {"Show": 10, "Faculdade": 20, "Academia": 50}},
    {"nome": "blusa branca", "tipo": "blusa", "arquivo": "blusabranca2.png",
     "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
    {"nome": "saião", "tipo": "calca", "arquivo": "saiaobranco.png",
     "pontos": {"Show": 30, "Faculdade": 50, "Academia": 0}},
    {"nome": "regata branca ", "tipo": "blusa", "arquivo": "regatabranca.png",
     "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},
    {"nome": "blusa verde", "tipo": "blusa", "arquivo": "blusaverde.png",
     "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
    {"nome": "calça alfaiataria", "tipo": "calca", "arquivo": "calça.png",
     "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
    {"nome": "vestido azul ", "tipo": "vestido", "arquivo": "vestidoazul.png",
     "pontos": {"Show": 0, "Faculdade": 0, "Academia": 0}},
    {"nome": "vestido verde", "tipo": "vestido", "arquivo": "vestidoverde.png",
     "pontos": {"Show": 50, "Faculdade": 20, "Academia": 0}},
    {"nome": "vestido marrom", "tipo": "vestido", "arquivo": "vestidomarrom.png",
     "pontos": {"Show": 50, "Faculdade": 50, "Academia": 0}},
]

imagens_roupas = {}
for r in roupas:
    try:
        caminho_completo = "assets/imagens/" + r["arquivo"]
        imagens_roupas[r["arquivo"]] = pygame.image.load(caminho_completo)
    except FileNotFoundError:
        imagens_roupas[r["arquivo"]] = pygame.Surface((200, 400), pygame.SRCALPHA)
        imagens_roupas[r["arquivo"]].fill((230, 180, 200, 150))

blusa_equipada = None
calca_equipada = None
vestido_equipado = None
pontuacao_total = 0
acessorio_bonus_desbloqueado = False

def desenhar_botao(texto, x, y, largura, altura, cor_base, cor_hover):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, largura, altura)
    retorno = False

    if rect.collidepoint(mouse):
        pygame.draw.rect(tela, cor_hover, rect, border_radius=10)
        if clique[0] == 1:
            retorno = True
    else:
        pygame.draw.rect(tela, cor_base, rect, border_radius=10)

    texto_surf = fonte_comum.render(texto, True, COR_TEXTO)
    tela.blit(texto_surf, texto_surf.get_rect(center=rect.center))
    return retorno

rodando = True

while rodando:
    if imagem_fundo_jogo is not None:
        tela.blit(imagem_fundo_jogo, (0, 0))
    else:
        tela.fill((245, 230, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if estado_atual == "MENU":
        txt_titulo = fonte_titulo.render("Dream Wardrobe", True, COR_DOURADA)
        txt_sub = fonte_subtitulo.render("Estilo Urbano Anos 2000", True, COR_TEXTO)
        tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 150))
        tela.blit(txt_sub, (LARGURA // 2 - txt_sub.get_width() // 2, 220))

        if desenhar_botao("JOGAR", LARGURA // 2 - 100, 350, 200, 50, COR_BOTAO, COR_BOTAO_HOVER):
            pygame.time.delay(150)
            estado_atual = ESTADO_SELECAO

    elif estado_atual == ESTADO_SELECAO:
        txt_sel = fonte_titulo.render("Escolha sua Modelo", True, COR_TEXTO)
        tela.blit(txt_sel, (LARGURA // 2 - txt_sel.get_width() // 2, 50))

        for i in range(2):
            x_pos = 180 + i * 260
            pygame.draw.rect(tela, COR_CARD, (x_pos, 130, 180, 310), border_radius=10)
            if i < len(img_modelos):
                img_miniatura = pygame.transform.scale(img_modelos[i], (140, 220))
                tela.blit(img_miniatura, (x_pos + 20, 150))

            if desenhar_botao(modelos_nomes[i], x_pos + 15, 390, 150, 35, COR_BOTAO, COR_BOTAO_HOVER):
                modelo_selecionado = i
                evento_atual_idx = 0
                pontuacao_total = 0
                blusa_equipada = None
                calca_equipada = None
                vestido_equipado = None
                acessorio_bonus_desbloqueado = False
                pygame.time.delay(150)
                estado_atual = ESTADO_GAMEPLAY

    elif estado_atual == ESTADO_GAMEPLAY:
        txt_titulo = fonte_titulo.render("Monte o seu Look", True, COR_TEXTO)
        tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 25))

        evento_nome = eventos[evento_atual_idx]
        txt_evento = fonte_subtitulo.render(f"Tema: {evento_nome}", True, COR_DESTAQUE)
        tela.blit(txt_evento, (LARGURA // 2 - txt_evento.get_width() // 2, 75))

        pos_modelo = (120, 130)

        if modelo_selecionado is not None and modelo_selecionado < len(img_modelos):
            tela.blit(img_modelos[modelo_selecionado], pos_modelo)

        if blusa_equipada:
            nome_arquivo_blusa = blusa_equipada.get("arquivo")
            if nome_arquivo_blusa in imagens_roupas:
                tela.blit(imagens_roupas[nome_arquivo_blusa], pos_modelo)

        if calca_equipada:
            nome_arquivo_calca = calca_equipada.get("arquivo")
            if nome_arquivo_calca in imagens_roupas:
                tela.blit(imagens_roupas[nome_arquivo_calca], pos_modelo)

        if vestido_equipado:
            nome_arquivo_vestido = vestido_equipado.get("arquivo")
            if nome_arquivo_vestido in imagens_roupas:
                tela.blit(imagens_roupas[nome_arquivo_vestido], pos_modelo)

        y_item = 130
        for roupa in roupas:
            if y_item < 480:
                prefixo = "   "
                if roupa == blusa_equipada or roupa == calca_equipada or roupa == vestido_equipado:
                    prefixo = "[X] "

                if desenhar_botao(prefixo + roupa["nome"], 470, y_item, 280, 25, COR_BOTAO, COR_BOTAO_HOVER):
                    tipo_roupa = roupa.get("tipo")
                    if tipo_roupa == "blusa":
                        blusa_equipada = roupa
                        vestido_equipado = None
                    elif tipo_roupa == "calca":
                        calca_equipada = roupa
                        vestido_equipado = None
                    elif tipo_roupa == "vestido":
                        vestido_equipado = roupa
                        blusa_equipada = None
                        calca_equipada = None
                    pygame.time.delay(100)

                y_item += 32

        if (blusa_equipada and calca_equipada) or vestido_equipado:
            if desenhar_botao("AVALIAR LOOK", 450, 520, 320, 50, COR_PRONTO, COR_BOTAO_HOVER):
                pygame.time.delay(150)
                estado_atual = ESTADO_AVALIACAO

    elif estado_atual == ESTADO_AVALIACAO:
        evento_nome = eventos[evento_atual_idx]
        txt_av = fonte_titulo.render("Avaliação do Look", True, COR_TEXTO)
        tela.blit(txt_av, (LARGURA // 2 - txt_av.get_width() // 2, 50))

        if vestido_equipado:
            vestido_pontos = vestido_equipado["pontos"]
            pontos_ultimo = vestido_pontos[evento_nome]
        else:
            pontos_ultimo = 0
            if blusa_equipada:
                pontos_ultimo += blusa_equipada["pontos"][evento_nome]
            if calca_equipada:
                pontos_ultimo += calca_equipada["pontos"][evento_nome]

        txt_pontos = fonte_subtitulo.render(f"Fizeste {pontos_ultimo} pontos em: {evento_nome}!", True, COR_DESTAQUE)
        tela.blit(txt_pontos, (LARGURA // 2 - txt_pontos.get_width() // 2, 150))

        if pontos_ultimo >= 80:
            feedback = "Perfeito! Dominaste completamente o Streetwear Y2K!"
            acessorio_bonus_desbloqueado = True
        elif pontos_ultimo >= 50:
            feedback = "Bom look, mas faltou um pouco mais de vibe anos 2000."
        else:
            feedback = "Hum... este look não combinou muito bem com o local."

        txt_feed = fonte_comum.render(feedback, True, COR_TEXTO)
        tela.blit(txt_feed, (LARGURA // 2 - txt_feed.get_width() // 2, 210))

        if acessorio_bonus_desbloqueado:
            pygame.draw.rect(tela, COR_DESTAQUE, (LARGURA // 2 - 180, 260, 360, 40), border_radius=5)
            txt_bonus = fonte_comum.render("✨ Óculos Lente Degradê Desbloqueado! ✨", True, COR_CARD)
            tela.blit(txt_bonus, (LARGURA // 2 - txt_bonus.get_width() // 2, 270))

        if evento_atual_idx < 2:
            if desenhar_botao("PRÓXIMO EVENTO", LARGURA // 2 - 120, 400, 240, 50, COR_BOTAO, COR_BOTAO_HOVER):
                pontuacao_total += pontos_ultimo
                evento_atual_idx += 1
                blusa_equipada = None
                calca_equipada = None
                vestido_equipado = None
                acessorio_bonus_desbloqueado = False
                pygame.time.delay(150)
                estado_atual = ESTADO_GAMEPLAY
        else:
            final_total = pontuacao_total + pontos_ultimo
            txt_fim = fonte_subtitulo.render(f"Fim do Jogo! Pontuação Total: {final_total} pts", True, COR_TEXTO)
            tela.blit(txt_fim, (LARGURA // 2 - txt_fim.get_width() // 2, 360))

            if desenhar_botao("VOLTAR AO MENU", LARGURA // 2 - 120, 450, 240, 50, COR_BOTAO, COR_BOTAO_HOVER):
                pygame.time.delay(150)
                estado_atual = ESTADO_MENU

    pygame.display.flip()
    relogio.tick(60)