class GameStats(): #17
    """Armazena as estatísticas do jogo."""
    
    def __init__(self, ai_settings):
        """inicializa as variáveis."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Inicia o jogo com as estatísticas ligadas.
        self.game_active = True
        
    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo."""
        self.ships_left = self.ai_settings.ship_limit
