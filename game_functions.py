import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Resposta ao pressionar uma tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE: 
        sys.exit()
        
def check_keyup_events(event, ship):
    """Resposta ao liberar uma tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """Resposta ao clicar com o mouse e pressinar teclas."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    """Atira um projétil se o limite não foi ultrapassado"""
    # Cria um novo projétil e o adiciona ao grupo.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Atualiza a imagem na tela e repinta ela."""
    # Repinta a tela a cada passagem no loop.
    screen.fill(ai_settings.bg_color)
    
    # Redesenha os projéteis atrás da nave e dos alienígenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme() 
    aliens.draw(screen) # 03

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, ship, aliens, bullets): #15
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
    # Atualiza a posição dos projéteis.
    bullets.update()

    # Elimina os projéteis que passarem do topo da tela.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # elimina o projétil se colidir com um alien
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
            
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Tratamento das colisões com aliens."""
    # Remove todos os aliens e projéteis que colidiram.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if len(aliens) == 0:
        # Destroi todos os projéteis restantes e cria uma nova frota de aliens.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_fleet_edges(ai_settings, aliens): #13
    """Verifica se algum alienígena está proximo a borda da tela."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens): # 14
    """Abaixa toda a frota e modifica sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets): #21
    """Responde ao fato do alienígena ter atingido a nave."""
    if stats.ships_left > 0:
        # Decrementa ships_left (menos uma vida).
        stats.ships_left -= 1
    else:
        stats.game_active = False
    
    # Esvazia a lista de alienígenas e projéteis.
    aliens.empty()
    bullets.empty()
    
    # Cria uma nova frota e centraliza a espaçonave.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    ai_settings.alien_speed_factor = 0.5
    
    # Faz uma pausa.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets): #16
    """Verifica se algum alien encostou no final da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Verifica se algum alien colidiu com a nave.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets): #15 
    """ Verifica se a frota está em uma das bordas e então abaixa toda ela."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Verifica se houve colisão com um alien e a aeronave.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Verifica se algum alien colidiu com a parte inferior da tela.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
            
def get_number_aliens_x(ai_settings, alien_width): #08
    """Calcula o número de aliens que cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    
    # int arredonda para baixo o número de aliens
    number_aliens_x = int(available_space_x / (2 * alien_width)) 
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height): #09
    """Calcula o número de linhas de aliens que podem ser criadas."""
    
    # Espaco vertical disponível fqazendo a subtração da altura de um
    # alien na parte superior, a altura da espaçonave e a altura de dois
    # aliens na parte inferior
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number): #07
    """Cria um alienígena e coloca ele em uma linha."""
    alien = Alien(ai_settings, screen)
    
    # salvamos a largura de um alien em alien_width para não precisar trabalhar com rect
    alien_width = alien.rect.width
    
    # calculamos a posição horizontal que o alien vai ficar
    alien.x = alien_width + (2 * alien_width) * alien_number
    alien.rect.x = alien.x
    
    # calcula a posicão vertival que o alien vai ficar
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    
    # adiciona alien criado no grupo de alienígenas
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens): #06
    """Cria uma frota completa de alienígenas."""
    # Cria um alienígena e calcula o número de alieígenas por linha.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    ai_settings.alien_speed_factor += 0.5
    # Cria uma frota de alienígenas.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
