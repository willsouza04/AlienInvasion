class Settings():
    """Classe responsável por armazenar todas as configurações do jogo."""

    def __init__(self):
        """Inicializa as as confingurações do jogo."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Configurações da Ship.
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Configurações do Bullet.
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 100, 100, 100
        self.bullets_allowed = 3
        
        # Configurações do Aliens.
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # movimento da frota: 1 representa para direita; -1 representa para esquerda.
        self.fleet_direction = 1
