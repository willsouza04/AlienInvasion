import pygame

class Ship():

    def __init__(self, ai_settings, screen):
        """Inicializa a nave e coloca em sua posição inicial."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem da nave e cria o rec da figura carregada.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Inicializa cada nave nem baixo e no centro da tela.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Armazena o valor decimal da posição central x da nave.
        self.center = float(self.rect.centerx)
        
        # Flags para dizer se a nave deve se mover (se tecla ainda está pressionada).
        self.moving_right = False
        self.moving_left = False
        
    def center_ship(self): #22
        """Centraliza nave com o screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Atualizar a posição da nave com base nas flags."""
        # Atuzalizar o x da nave com base no fator velocidade.
        # se estiver precissonado direita e esquerta a nave vai permanecer parada, pois o valor de x final será o mesmo
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Atualizar o retangulo da nave para o valor devido.
        self.rect.centerx = self.center

    def blitme(self):
        """Desenha a nave em seu local devido."""
        self.screen.blit(self.image, self.rect)
