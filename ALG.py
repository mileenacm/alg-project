import pygame
import sys
import os


class Jogo:
    def __init__(self):
        # --------------- INICIALIZAÇÃO -------------------#
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.LARGURA, self.ALTURA = 800, 600
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Dream Wardrobe")
        self.relogio = pygame.time.Clock()
        self.rodando = True

        # Caminho base dinâmico do projeto
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # ------------------ CORES ----------------------#
        self.COR_CARD = (255, 255, 255)
        self.COR_DOURADA = (212, 175, 55)
        self.COR_TEXTO = (0, 0, 0)
        self.COR_TEXTO_CLARO = (255, 255, 255)
        self.COR_BOTAO = (223, 203, 236)
        self.COR_BOTAO_HOVER = (247, 206, 221)
        self.COR_PRONTO = (160, 210, 180)
        self.COR_DESTAQUE = (255, 105, 180)
        self.COR_FUNDO_PADRAO = (245, 230, 240)

        # ------------------ FONTES -----------------#
        self.fonte_titulo = pygame.font.Font(os.path.join(self.BASE_DIR, "assets", "font", "Midnight Angel.ttf"), 55)
        self.fonte_subtitulo = pygame.font.Font(os.path.join(self.BASE_DIR, "assets", "font", "Retrochips.otf"), 32)

        self.fonte_comum = pygame.font.SysFont("arial", 22, bold=True)
        self.fonte_pontos = pygame.font.SysFont("arial", 28, bold=True) 

        # ------------- VARIÁVEIS DE ESTADO E GAMEPLAY --------------#
        self.estado_atual = "MENU"
        self.modelos_nomes = ["Aisha", "Chloe"]
        self.modelo_selecionado = 0
        self.eventos = ["Show", "Faculdade", "Academia"]
        self.evento_atual_idx = 0
        self.pontuacao_total = 0
        self.acessorio_bonus_desbloqueado = False

        self.blusa_equipada = None
        self.calca_equipada = None
        self.vestido_equipado = None

        # ----------------------- DADOS DAS ROUPAS -------------------------------- #
        self.roupas = [
            # Peça de cima
            {"nome": "blusa azul", "tipo": "blusa", "arquivo": "blusaazul.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 50, "Faculdade": 20, "Academia": 10}},
            {"nome": "blusa branca", "tipo": "blusa", "arquivo": "blusabranca.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
            {"nome": "blusa branca 2", "tipo": "blusa", "arquivo": "blusabranca2.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
            {"nome": "regata branca ", "tipo": "blusa", "arquivo": "regatabranca.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},
            {"nome": "blusa verde", "tipo": "blusa", "arquivo": "blusaverde.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 50, "Faculdade": 20, "Academia": 10}},
            {"nome": "Top Esportivo ", "tipo": "blusa", "arquivo": "topbranco.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},

            # Peça de baixo
            {"nome": "Shorts Tactel", "tipo": "calca", "arquivo": "shortpreto.png", "offset_x": 0, "offset_y": 140,
             "pontos": {"Show": 10, "Faculdade": 20, "Academia": 50}},
            {"nome": "Saia", "tipo": "calca", "arquivo": "saiapreta.png", "offset_x": 0, "offset_y": 140,
             "pontos": {"Show": 50, "Faculdade": 30, "Academia": 10}},
            {"nome": "saião", "tipo": "calca", "arquivo": "saiaobranco.png", "offset_x": 0, "offset_y": 140,
             "pontos": {"Show": 30, "Faculdade": 50, "Academia": 0}},
            {"nome": "calça alfaiataria", "tipo": "calca", "arquivo": "calça.png", "offset_x": 0, "offset_y": 140,
             "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
            {"nome": "Jeans Largo Baggy", "tipo": "calca", "arquivo": "calça.png", "offset_x": 0, "offset_y": 140,
             "pontos": {"Show": 35, "Faculdade": 50, "Academia": 10}},

            # Vestido
            {"nome": "vestido azul ", "tipo": "vestido", "arquivo": "vestidoazul.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 0, "Faculdade": 0, "Academia": 0}},
            {"nome": "vestido verde", "tipo": "vestido", "arquivo": "vestidoverde.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 50, "Faculdade": 20, "Academia": 0}},
            {"nome": "vestido marrom", "tipo": "vestido", "arquivo": "vestidomarrom.png", "offset_x": 0, "offset_y": 40,
             "pontos": {"Show": 50, "Faculdade": 50, "Academia": 0}},
        ]

        # Carrega imagens e som
        self.carregar_assets()

    def carregar_assets(self):
        # Áudio
            pygame.mixer.music.load(os.path.join(self.BASE_DIR, "assets", "sons", "trilha.mp3"))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        
        # Fundo do Jogo
            fundo = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "imagens", "fundo.png"))
            self.imagem_fundo_jogo = pygame.transform.scale(fundo, (self.LARGURA, self.ALTURA))

        # Fundo do Menu
            fundo_m = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "imagens", "fundo.menu.png"))
            self.imagem_fundo_menu = pygame.transform.scale(fundo_m, (self.LARGURA, self.ALTURA))
        
        # Botão Start do Menu
            img_original = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "imagens", "botao.png"))
            largura_nova = int(img_original.get_width() * 0.6)
            altura_nova = int(img_original.get_height() * 0.6)
            self.img_botao_start = pygame.transform.scale(img_original, (largura_nova, altura_nova))
            self.rect_botao_start = self.img_botao_start.get_rect(center=(self.LARGURA // 2, 600 - 240))
        
        # Modelos
            self.img_modelos = [
                pygame.image.load(os.path.join(self.BASE_DIR, "assets", "imagens", "boneca01.png")),
                pygame.image.load(os.path.join(self.BASE_DIR, "assets", "imagens", "boneca02.png")),
            ]
            self.img_modelos = [pygame.transform.scale(img, (320, 530)) for img in self.img_modelos]
       
        # Roupas
            self.imagens_roupas = {}
            fator_escala = 0.47

            for r in self.roupas:
                    caminho_completo = os.path.join(self.BASE_DIR, "assets", "imagens", r["arquivo"])
                    img_original = pygame.image.load(caminho_completo).convert_alpha()

                    bbox = img_original.get_bounding_rect()
                    if bbox.width > 0 and bbox.height > 0:
                        img_original = img_original.subsurface(bbox).copy()

                    nova_largura = int(img_original.get_width() * fator_escala)
                    nova_altura = int(img_original.get_height() * fator_escala)
                    img_redimensionada = pygame.transform.smoothscale(img_original, (nova_largura, nova_altura))

                    self.imagens_roupas[r["arquivo"]] = img_redimensionada
           
    def desenhar_botao_icone(self, imagem_original, x, y, largura, altura, esta_selecionada, cor_hover):
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, largura, altura)
        retorno = False

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.tela, cor_hover, rect, border_radius=12)
            if clique[0] == 1:
                retorno = True
        elif esta_selecionada:
            pygame.draw.rect(self.tela, self.COR_DESTAQUE, rect, border_radius=12)
        else:
            pygame.draw.rect(self.tela, (255, 255, 255), rect, width=3, border_radius=12)

        if imagem_original:
            rect_conteudo = imagem_original.get_bounding_rect()

            if rect_conteudo.width > 0 and rect_conteudo.height > 0:
                imagem_recortada = imagem_original.subsurface(rect_conteudo)

                escala_w = (largura - 14) / rect_conteudo.width
                escala_h = (altura - 14) / rect_conteudo.height
                escala_final = min(escala_w, escala_h)

                tamanho_novo = (int(rect_conteudo.width * escala_final), int(rect_conteudo.height * escala_final))
                img_miniatura = pygame.transform.scale(imagem_recortada, tamanho_novo)
            else:
                img_miniatura = pygame.transform.scale(imagem_original, (largura - 14, altura - 14))

            img_rect = img_miniatura.get_rect(center=rect.center)
            self.tela.blit(img_miniatura, img_rect)

        return retorno

    def desenhar_botao(self, texto, x, y, largura, altura, cor_base, cor_hover):
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, largura, altura)
        retorno = False

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.tela, cor_hover, rect, border_radius=6)
            if clique[0] == 1:
                retorno = True
        else:
            pygame.draw.rect(self.tela, cor_base, rect, border_radius=6)

        txt = self.fonte_comum.render(texto, True, (0, 0, 0))
        self.tela.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
        return retorno

    def gerenciar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.estado_atual == "MENU" and self.rect_botao_start.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.estado_atual == "MENU":
                    if self.rect_botao_start.collidepoint(event.pos):
                        pygame.time.delay(150)
                        self.estado_atual = "SELECAO"

    def resetar_gameplay(self):
        self.blusa_equipada = None
        self.calca_equipada = None
        self.vestido_equipado = None
        self.acessorio_bonus_desbloqueado = False

# ---- Encaixando a roupa na modelo ---- #
    def desenhar_roupa_ajustada(self, item, rect_modelo):
        if not item:
            return

        nome_arq = item.get("arquivo")
        img = self.imagens_roupas.get(nome_arq)
        if not img:
            return

        offset_x = item.get("offset_x", 0)
        offset_y = item.get("offset_y", 0)
        tipo = item.get("tipo")

        if tipo == "blusa":
            x = rect_modelo.centerx + offset_x
            y = rect_modelo.top + 73 + offset_y
            rect_roupa = img.get_rect(midtop=(x, y))

        elif tipo == "calca":
            x = rect_modelo.centerx + offset_x
            y = rect_modelo.top + 64.5 + offset_y
            rect_roupa = img.get_rect(midtop=(x, y))

        elif tipo == "vestido":
            x = rect_modelo.centerx + offset_x
            y = rect_modelo.top + 69 + offset_y
            rect_roupa = img.get_rect(midtop=(x, y))

        else:
            rect_roupa = img.get_rect(center=rect_modelo.center)

        self.tela.blit(img, rect_roupa)

    def tela_menu(self):
        if self.img_botao_start:
            self.tela.blit(self.img_botao_start, self.rect_botao_start)
        else:
            if self.desenhar_botao("JOGAR", self.LARGURA // 2 - 100, 350, 200, 50, self.COR_BOTAO,
                                   self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "SELECAO"

    def tela_selecao(self):
        txt_sel = self.fonte_titulo.render("Escolha sua Modelo", True, self.COR_TEXTO)
        self.tela.blit(txt_sel, (self.LARGURA // 2 - txt_sel.get_width() // 2, 50))

        for i in range(2):
            x_pos = 180 + i * 260
            pygame.draw.rect(self.tela, self.COR_CARD, (x_pos, 130, 180, 310), border_radius=10)
            if i < len(self.img_modelos):
                img_miniatura = pygame.transform.scale(self.img_modelos[i], (140, 220))
                self.tela.blit(img_miniatura, (x_pos + 20, 150))

            if self.desenhar_botao(self.modelos_nomes[i], x_pos + 15, 390, 150, 35, self.COR_BOTAO,
                                   self.COR_BOTAO_HOVER):
                self.modelo_selecionado = i
                self.evento_atual_idx = 0
                self.pontuacao_total = 0
                self.resetar_gameplay()
                pygame.time.delay(150)
                self.estado_atual = "GAMEPLAY"

    def tela_gameplay(self):
        txt_titulo = self.fonte_titulo.render("Monte o seu Look", True, (255, 255, 255))
        self.tela.blit(txt_titulo, (self.LARGURA // 2 - txt_titulo.get_width() // 2, 20))

        evento_nome = self.eventos[self.evento_atual_idx]
        txt_evento = self.fonte_subtitulo.render(f"Tema: {evento_nome}", True, (255, 255, 0))
        self.tela.blit(txt_evento, (self.LARGURA // 2 - txt_evento.get_width() // 2, 75))

        pos_modelo = (100, 100)

        if self.modelo_selecionado is not None and self.modelo_selecionado < len(self.img_modelos):
            modelo_img = self.img_modelos[self.modelo_selecionado]
            rect_modelo = modelo_img.get_rect(topleft=pos_modelo)

            self.tela.blit(modelo_img, rect_modelo)

            for item in [self.blusa_equipada, self.calca_equipada, self.vestido_equipado]:
                self.desenhar_roupa_ajustada(item, rect_modelo)

        # --- SISTEMA DO GUARDA-ROUPA --- #
        x_inicial = 440
        y_inicial = 140
        colunas = 3
        largura_icone = 95
        altura_icone = 95
        espacamento = 15

        for indice, roupa in enumerate(self.roupas):
            col = indice % colunas
            lin = indice // colunas

            x_pos = x_inicial + col * (largura_icone + espacamento)
            y_pos = y_inicial + lin * (altura_icone + espacamento)

            img_roupa = self.imagens_roupas.get(roupa["arquivo"])

            if img_roupa:
                esta_equipada = (
                            roupa == self.blusa_equipada or roupa == self.calca_equipada or roupa == self.vestido_equipado)

                if self.desenhar_botao_icone(img_roupa, x_pos, y_pos, largura_icone, altura_icone, esta_equipada,
                                             self.COR_BOTAO_HOVER):
                    tipo_roupa = roupa.get("tipo")
                    if tipo_roupa == "blusa":
                        self.blusa_equipada = roupa
                        self.vestido_equipado = None
                    elif tipo_roupa == "calca":
                        self.calca_equipada = roupa
                        self.vestido_equipado = None
                    elif tipo_roupa == "vestido":
                        self.vestido_equipado = roupa
                        self.blusa_equipada = None
                        self.calca_equipada = None
                    pygame.time.delay(120)

        if (self.blusa_equipada and self.calca_equipada) or self.vestido_equipado:
            if self.desenhar_botao("AVALIAR LOOK", 450, 525, 320, 45, self.COR_PRONTO, self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "AVALIACAO"

    def tela_avaliacao(self):
        # 1. Título principal da tela
        txt_av = self.fonte_titulo.render("Avaliação do Look", True, (255, 255, 255))
        self.tela.blit(txt_av, (self.LARGURA // 2 - txt_av.get_width() // 2, 40))

        evento_nome = self.eventos[self.evento_atual_idx]
        pontos_ultimo = 0
        if self.vestido_equipado:
            pontos_ultimo = self.vestido_equipado["pontos"][evento_nome]
        else:
            if self.blusa_equipada:
                pontos_ultimo += self.blusa_equipada["pontos"][evento_nome]
            if self.calca_equipada:
                pontos_ultimo += self.calca_equipada["pontos"][evento_nome]

        # --- NOVO CARD DE PONTUAÇÃO PARA GARANTIR LEITURA ---
        # Desenha uma caixa escura arredondada no centro da tela para contrastar
        largura_card, altura_card = 500, 100
        x_card = self.LARGURA // 2 - largura_card // 2
        y_card = 130
        pygame.draw.rect(self.tela, (40, 20, 45), (x_card, y_card, largura_card, altura_card), border_radius=15)
        pygame.draw.rect(self.tela, self.COR_DESTAQUE, (x_card, y_card, largura_card, altura_card), width=3,
                         border_radius=15)

        # Texto dos pontos em amarelo marcante dentro da caixa escura
        txt_pontos = self.fonte_pontos.render(f"Você fez {pontos_ultimo} pontos em: {evento_nome}!", True,
                                              (255, 255, 0))
        self.tela.blit(txt_pontos, (self.LARGURA // 2 - txt_pontos.get_width() // 2, y_card + 35))

        # 2. Sistema de Feedback
        if pontos_ultimo >= 80:
            feedback = "Perfeito! Você domina completamente o Streetwear Y2K!"
            self.acessorio_bonus_desbloqueado = True
        elif pontos_ultimo >= 50:
            feedback = "Bom look, mas faltou um pouco mais de vibe anos 2000."
        else:
            feedback = "Hum... este look não combinou muito bem com o local."

        # Caixa menor para o texto de feedback
        pygame.draw.rect(self.tela, (255, 255, 255), (self.LARGURA // 2 - 275, 255, 550, 40), border_radius=8)
        txt_feed = self.fonte_comum.render(feedback, True, (0, 0, 0))
        self.tela.blit(txt_feed, (self.LARGURA // 2 - txt_feed.get_width() // 2, 263))

        if self.acessorio_bonus_desbloqueado:
            pygame.draw.rect(self.tela, self.COR_DESTAQUE, (self.LARGURA // 2 - 180, 315, 360, 40), border_radius=5)
            txt_bonus = self.fonte_comum.render("✨ Óculos Lente Degradê Desbloqueado! ✨", True, (255, 255, 255))
            self.tela.blit(txt_bonus, (self.LARGURA // 2 - txt_bonus.get_width() // 2, 325))

        if self.evento_atual_idx < 2:
            if self.desenhar_botao("PRÓXIMO EVENTO", self.LARGURA // 2 - 120, 420, 240, 50, self.COR_BOTAO,
                                   self.COR_BOTAO_HOVER):
                self.pontuacao_total += pontos_ultimo
                self.evento_atual_idx += 1
                self.resetar_gameplay()
                pygame.time.delay(150)
                self.estado_atual = "GAMEPLAY"
        else:
            final_total = self.pontuacao_total + pontos_ultimo

            # Caixa escura final para mostrar o fim de jogo
            pygame.draw.rect(self.tela, (0, 0, 0), (self.LARGURA // 2 - 250, 380, 500, 45), border_radius=8)
            txt_fim = self.fonte_subtitulo.render(f"Fim do Jogo! Pontuação Total: {final_total} pts", True,
                                                  (255, 255, 255))
            self.tela.blit(txt_fim, (self.LARGURA // 2 - txt_fim.get_width() // 2, 385))

            if self.desenhar_botao("VOLTAR AO MENU", self.LARGURA // 2 - 120, 470, 240, 50, self.COR_BOTAO,
                                   self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "MENU"

    def rodar(self):
        while self.rodando:
            if self.estado_atual == "MENU" and self.imagem_fundo_menu is not None:
                self.tela.blit(self.imagem_fundo_menu, (0, 0))
            elif self.imagem_fundo_jogo is not None:
                self.tela.blit(self.imagem_fundo_jogo, (0, 0))
            else:
                self.tela.fill(self.COR_FUNDO_PADRAO)

            self.gerenciar_eventos()

            if self.estado_atual == "MENU":
                self.tela_menu()
            elif self.estado_atual == "SELECAO":
                self.tela_selecao()
            elif self.estado_atual == "GAMEPLAY":
                self.tela_gameplay()
            elif self.estado_atual == "AVALIACAO":
                self.tela_avaliacao()

            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.rodar()