import pygame, os, ctypes
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats #18
from ship import Ship
import game_functions as gf

def run_game():
    # Inicializa a pygame, settings, e o objeto screen.
    pygame.init()    
    
    user32 = ctypes.windll.user32
    screenSize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    screen = pygame.display.set_mode((screenSize) , pygame.FULLSCREEN)
    
    pygame.display.set_caption("Invasão Alienígena")
    
    ai_settings = Settings()
    
    # Cria uma instância do GameStats para armazenas as estatísticas do jogo..
    stats = GameStats(ai_settings) # 19
    
    # Cria uma nave, um grupo de bullets (tiros) e um grupo de aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group() #04
    
    # Cria uma frota de alienígenas.
    gf.create_fleet(ai_settings, screen, ship, aliens) #05

    # Laço principal do jogo para ficar capturando os eventos.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        
        if stats.game_active: # 20
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets) #11
        
        gf.update_screen(ai_settings, screen, ship, aliens, bullets) #02 

run_game()
