import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Classe que gerencia os projéteis atirados pela espaçonave."""

    def __init__(self, ai_settings, screen, ship):
        """Cria um porjétil a partir da mesma posição da aeronave."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Cria um rect do projétil na posição (0, 0), então atualiza para a posição certa.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Armazenha o valor decimal da posição y do projétil.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self): 
        """Move os projéteis para cima."""
        # Atualiza a posicção em decimal dos projéteis.
        self.y -= self.speed_factor
        # Atualiza baseado no fator.
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o projétil na tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)
