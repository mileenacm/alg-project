
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
            if self.desenhar_botao("AVALIAR LOOK", 95, 525, 320, 45, self.COR_PRONTO, self.COR_BOTAO_HOVER):
                pygame.time.delay(150)
                self.estado_atual = "AVALIACAO"