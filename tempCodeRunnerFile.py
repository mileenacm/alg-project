
# ----- Loop principal ----- #
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

 # -- objeto -- #
if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.rodar()