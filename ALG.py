import pygame
import sys

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

        # ------------------ CORES ----------------------#
        self.COR_CARD = (255, 255, 255)
        self.COR_DOURADA = (255, 225, 100)
        self.COR_TEXTO = (255, 250, 200)
        self.COR_BOTAO = (223, 203, 236)
        self.COR_BOTAO_HOVER = (247, 206, 221)
        self.COR_PRONTO = (160, 210, 180)
        self.COR_DESTAQUE = (255, 105, 180)
        self.COR_FUNDO_PADRAO = (245, 230, 240)

        # ------------------ FONTES -----------------#
        self.fonte_titulo = pygame.font.Font("alg-project/assets/font/Midnight Angel.ttf", 60)
        self.fonte_subtitulo = pygame.font.SysFont("alg-project/assets/font/Retrochips.otf", 36)
        self.fonte_comum = pygame.font.SysFont(None, 24)

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
            #Peça de cima
            {"nome": "blusa azul", "tipo": "blusa", "arquivo": "blusaazul.png", "offset_x": 95, "offset_y": 140, "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
            {"nome": "blusa branca", "tipo": "blusa", "arquivo": "blusabranca.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
            {"nome": "blusa branca 2", "tipo": "blusa", "arquivo": "blusabranca2.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}}, 
            {"nome": "regata branca ", "tipo": "blusa", "arquivo": "regatabranca.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},
            {"nome": "blusa verde", "tipo": "blusa", "arquivo": "blusaverde.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 15, "Faculdade": 20, "Academia": 10}},
            {"nome": "Top Esportivo ", "tipo": "blusa", "arquivo": "topbranco.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 15, "Faculdade": 10, "Academia": 50}},

            #Peça de baixo
            {"nome": "Shorts Tactel", "tipo": "calca", "arquivo": "shortpreto.png","offset_x": 0, "offset_y": 80, "pontos": {"Show": 10, "Faculdade": 20, "Academia": 50}},
            {"nome": "Saia", "tipo": "calca", "arquivo": "saiapreta.png","offset_x": 0, "offset_y": 80, "pontos": {"Show": 50, "Faculdade": 30, "Academia": 10}}, 
            {"nome": "saião", "tipo": "calca", "arquivo": "saiaobranco.png","offset_x": 0, "offset_y": 80, "pontos": {"Show": 30, "Faculdade": 50, "Academia": 0}}, 
            {"nome": "calça alfaiataria", "tipo": "calca", "arquivo": "calça.png","offset_x":-390, "offset_y": -220, "pontos": {"Show": 30, "Faculdade": 50, "Academia": 25}},
             {"nome": "Jeans Largo Baggy", "tipo": "calca", "arquivo": "calça.png","offset_x": 0, "offset_y": 80, "pontos": {"Show": 35, "Faculdade": 50, "Academia": 10}},  

             #Vestido
            {"nome": "vestido azul ", "tipo": "vestido", "arquivo": "vestidoazul.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 0, "Faculdade": 0, "Academia": 0}},
            {"nome": "vestido verde", "tipo": "vestido", "arquivo": "vestidoverde.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 50, "Faculdade": 20, "Academia": 0}},
            {"nome": "vestido marrom", "tipo": "vestido", "arquivo": "vestidomarrom.png","offset_x": -390, "offset_y": -220, "pontos": {"Show": 50, "Faculdade": 50, "Academia": 0}},
        ]

        # Carrega imagens e som
        self.carregar_assets()

    def carregar_assets(self):
        # Áudio
        try:
            pygame.mixer.music.load("alg-project/assets/sons/trilha.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass # Ignora se não achar a música

        # Fundo
        try:
            fundo = pygame.image.load("alg-project/assets/imagens/fundo.png")
            self.imagem_fundo_jogo = pygame.transform.scale(fundo, (self.LARGURA, self.ALTURA))
        except pygame.error as e:
            print(f"Não consegui carregar o fundo: {e}")
            self.imagem_fundo_jogo = None

        # Modelos
        try:
            self.img_modelos = [
                pygame.image.load("alg-project/assets/imagens/boneca01.png"),  # Aisha
                pygame.image.load("alg-project/assets/imagens/boneca02.png"),  # Chloe
            ]
            
            # Alterar largura e altura das modelos
            self.img_modelos = [pygame.transform.scale(img, (320, 530)) for img in self.img_modelos]

        except pygame.error as e:
            print(f"Aviso: Criando superfícies temporárias para as bonecas: {e}")
            # Altere aqui também:
            self.img_modelos = [pygame.Surface((320, 530), pygame.SRCALPHA) for _ in range(2)]
            self.img_modelos[0].fill((200, 150, 150))
            self.img_modelos[1].fill((150, 150, 200))

        # Roupas
        self.imagens_roupas = {}

        fator_escala = 1.5 

        for r in self.roupas:
            try:
                caminho_completo = "alg-project/assets/imagens/" + r["arquivo"]
                img_original = pygame.image.load(caminho_completo)
                
                # 🟢 ALTERAÇÃO: Redimensiona mantendo a proporção original da própria imagem
                nova_largura = int(img_original.get_width() * fator_escala)
                nova_altura = int(img_original.get_height() * fator_escala)
                img_redimensionada = pygame.transform.scale(img_original, (nova_largura, nova_altura))
                
                self.imagens_roupas[r["arquivo"]] = img_redimensionada
                
            except (FileNotFoundError, pygame.error):
                img_temp = pygame.Surface((100, 100), pygame.SRCALPHA)
                img_temp.fill((230, 180, 200, 150))
                self.imagens_roupas[r["arquivo"]] = img_temp


    def desenhar_botao(self, texto, x, y, largura, altura, cor_base, cor_hover):
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, largura, altura)
        retorno = False

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.tela, cor_hover, rect, border_radius=10)
            if clique[0] == 1:
                retorno = True
        else:
            pygame.draw.rect(self.tela, cor_base, rect, border_radius=10)

        texto_surf = self.fonte_comum.render(texto, True, self.COR_TEXTO)
        self.tela.blit(texto_surf, texto_surf.get_rect(center=rect.center))
        return retorno

    def gerenciar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

    def resetar_gameplay(self):
        self.blusa_equipada = None
        self.calca_equipada = None
        self.vestido_equipado = None
        self.acessorio_bonus_desbloqueado = False

    def desenhar_roupa_ajustada(self, item, pos_base):
        """
        Calcula a posição final da roupa baseada na posição da boneca 
        somada aos ajustes (offsets) de ancoragem.
        """
        if not item:
            return
            
        nome_arq = item.get("arquivo")
        if nome_arq in self.imagens_roupas:
            # 🟢 ALTERAÇÃO: Volta a ler o offset específico definido na lista de roupas
            offset_x = item.get("offset_x", 0)
            offset_y = item.get("offset_y", 0)
            
            # Soma a posição da boneca com o ajuste da peça
            pos_final_x = pos_base[0] + offset_x
            pos_final_y = pos_base[1] + offset_y
            
            # Desenha a peça na tela na posição calculada
            self.tela.blit(self.imagens_roupas[nome_arq], (pos_final_x, pos_final_y))

    # ------------ MÁQUINA DE ESTADOS (TELAS) ------------- #
    def tela_menu(self):
        txt_titulo = self.fonte_titulo.render("Dream Wardrobe", True, self.COR_DOURADA)
        txt_sub = self.fonte_subtitulo.render("Estilo Urbano Anos 2000", True, self.COR_TEXTO)
        self.tela.blit(txt_titulo, (self.LARGURA // 2 - txt_titulo.get_width() // 2, 150))
        self.tela.blit(txt_sub, (self.LARGURA // 2 - txt_sub.get_width() // 2, 220))

        if self.desenhar_botao("JOGAR", self.LARGURA // 2 - 100, 350, 200, 50, self.COR_BOTAO, self.COR_BOTAO_HOVER):
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

            if self.desenhar_botao(self.modelos_nomes[i], x_pos + 15, 390, 150, 35, self.COR_BOTAO, self.COR_BOTAO_HOVER):
                self.modelo_selecionado = i
                self.evento_atual_idx = 0
                self.pontuacao_total = 0
                self.resetar_gameplay()
                pygame.time.delay(150)
                self.estado_atual = "GAMEPLAY"

    def tela_gameplay(self):
        txt_titulo = self.fonte_titulo.render("Monte o seu Look", True, self.COR_TEXTO)
        self.tela.blit(txt_titulo, (self.LARGURA // 2 - txt_titulo.get_width() // 2, 25))

        evento_nome = self.eventos[self.evento_atual_idx]
        txt_evento = self.fonte_subtitulo.render(f"Tema: {evento_nome}", True, self.COR_DESTAQUE)
        self.tela.blit(txt_evento, (self.LARGURA // 2 - txt_evento.get_width() // 2, 75))

        pos_modelo = (220, 130)

        # Desenha a modelo e as roupas equipadas
        if self.modelo_selecionado is not None and self.modelo_selecionado < len(self.img_modelos):
            self.tela.blit(self.img_modelos[self.modelo_selecionado], pos_modelo)

        # Desenha as roupas equipadas usando o novo sistema de ancoragem
        for item in [self.blusa_equipada, self.calca_equipada, self.vestido_equipado]:
            self.desenhar_roupa_ajustada(item, pos_modelo)

        # Lista de botões do guarda-roupa
        y_item = 130
        for roupa in self.roupas:
            if y_item < 480:
                prefixo = "   "
                if roupa in [self.blusa_equipada, self.calca_equipada, self.vestido_equipado]:
                    prefixo = "[X] "

                if self.desenhar_botao(prefixo + roupa["nome"], 600, y_item, 145, 25, self.COR_BOTAO, self.COR_BOTAO_HOVER):
                    tipo = roupa.get("tipo")
                    if tipo == "blusa":
                        self.blusa_equipada = roupa
                        self.vestido_equipado = None
                    elif tipo == "calca":
                        self.calca_equipada = roupa
                        self.vestido_equipado = None
                    elif tipo == "vestido":
                        self.vestido_equipado = roupa
                        self.blusa_equipada = None
                        self.calca_equipada = None
                    pygame.time.delay(100)

                y_item += 32

        # Botão de avaliar look
        if (self.blusa_equipada and self.calca_equipada) or self.vestido_equipado:
            if self.desenhar_botao("AVALIAR LOOK", 450, 520, 320, 50, self.COR_PRONTO, self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "AVALIACAO"

    def tela_avaliacao(self):
        evento_nome = self.eventos[self.evento_atual_idx]
        txt_av = self.fonte_titulo.render("Avaliação do Look", True, self.COR_TEXTO)
        self.tela.blit(txt_av, (self.LARGURA // 2 - txt_av.get_width() // 2, 50))

        # Calcula os pontos
        pontos_ultimo = 0
        if self.vestido_equipado:
            pontos_ultimo = self.vestido_equipado["pontos"][evento_nome]
        else:
            if self.blusa_equipada:
                pontos_ultimo += self.blusa_equipada["pontos"][evento_nome]
            if self.calca_equipada:
                pontos_ultimo += self.calca_equipada["pontos"][evento_nome]

        # Mensagens de Feedback
        txt_pontos = self.fonte_subtitulo.render(f"Fizeste {pontos_ultimo} pontos em: {evento_nome}!", True, self.COR_DESTAQUE)
        self.tela.blit(txt_pontos, (self.LARGURA // 2 - txt_pontos.get_width() // 2, 150))

        if pontos_ultimo >= 80:
            feedback = "Perfeito! Você domina completamente o Streetwear Y2K!"
            self.acessorio_bonus_desbloqueado = True
        elif pontos_ultimo >= 50:
            feedback = "Bom look, mas faltou um pouco mais de vibe anos 2000."
        else:
            feedback = "Hum... este look não combinou muito bem com o local."

        txt_feed = self.fonte_comum.render(feedback, True, self.COR_TEXTO)
        self.tela.blit(txt_feed, (self.LARGURA // 2 - txt_feed.get_width() // 2, 210))

        if self.acessorio_bonus_desbloqueado:
            pygame.draw.rect(self.tela, self.COR_DESTAQUE, (self.LARGURA // 2 - 180, 260, 360, 40), border_radius=5)
            txt_bonus = self.fonte_comum.render("✨ Óculos Lente Degradê Desbloqueado! ✨", True, self.COR_CARD)
            self.tela.blit(txt_bonus, (self.LARGURA // 2 - txt_bonus.get_width() // 2, 270))

        # Controle de progressão do jogo
        if self.evento_atual_idx < 2:
            if self.desenhar_botao("PRÓXIMO EVENTO", self.LARGURA // 2 - 120, 400, 240, 50, self.COR_BOTAO, self.COR_BOTAO_HOVER):
                self.pontuacao_total += pontos_ultimo
                self.evento_atual_idx += 1
                self.resetar_gameplay()
                pygame.time.delay(150)
                self.estado_atual = "GAMEPLAY"
        else:
            final_total = self.pontuacao_total + pontos_ultimo
            txt_fim = self.fonte_subtitulo.render(f"Fim do Jogo! Pontuação Total: {final_total} pts", True, self.COR_TEXTO)
            self.tela.blit(txt_fim, (self.LARGURA // 2 - txt_fim.get_width() // 2, 360))

            if self.desenhar_botao("VOLTAR AO MENU", self.LARGURA // 2 - 120, 450, 240, 50, self.COR_BOTAO, self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "MENU"

    # ------------------ LOOP PRINCIPAL ------------------ #
    def rodar(self):
        while self.rodando:
            # Desenha o fundo
            if self.imagem_fundo_jogo is not None:
                self.tela.blit(self.imagem_fundo_jogo, (0, 0))
            else:
                self.tela.fill(self.COR_FUNDO_PADRAO)

            # Verifica eventos (Fechar janela)
            self.gerenciar_eventos()

            # Chama o método de desenho e lógica com base no estado atual
            if self.estado_atual == "MENU":
                self.tela_menu()
            elif self.estado_atual == "SELECAO":
                self.tela_selecao()
            elif self.estado_atual == "GAMEPLAY":
                self.tela_gameplay()
            elif self.estado_atual == "AVALIACAO":
                self.tela_avaliacao()

            # Atualiza a tela
            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.rodar()