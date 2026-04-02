import pygame
import random
import sys
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# New-Stalgia Palette
CHARCOAL = (18, 18, 18)      # Deep Background
FOREST_GREEN = (27, 48, 34)  # Enemies
COBALT_BLUE = (0, 71, 171)   # Player
MUSTARD_GOLD = (225, 173, 1) # Projectiles / UI
WHITE_SOFT = (220, 220, 210) # Text

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Artisanal Diamond Shape
        pygame.draw.polygon(self.image, COBALT_BLUE, [(20, 0), (40, 20), (20, 40), (0, 20)])
        pygame.draw.polygon(self.image, MUSTARD_GOLD, [(20, 0), (40, 20), (20, 40), (0, 20)], 1)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        self.speed = 6
        self.target_x = WIDTH // 2

    def update(self):
        # "Heavy" smooth movement (Interp)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.target_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.target_x += self.speed
        
        # Clamp
        self.target_x = max(40, min(WIDTH - 40, self.target_x))
        # Smooth slide
        self.rect.centerx += (self.target_x - self.rect.centerx) * 0.15

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15), pygame.SRCALPHA)
        # Soft glow projectile
        pygame.draw.rect(self.image, MUSTARD_GOLD, (0, 0, 4, 15))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        # Sophisticated Hexagon
        pygame.draw.rect(self.image, FOREST_GREEN, (5, 5, 25, 25))
        pygame.draw.rect(self.image, (255, 255, 255, 30), (5, 5, 25, 25), 1)
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))
        self.speed = random.uniform(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def create_grain(width, height):
    grain = pygame.Surface((width, height))
    for _ in range(10000):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        val = random.randint(0, 20)
        grain.set_at((x, y), (val, val, val))
    grain.set_alpha(40)
    return grain

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aether Wing")
    clock = pygame.time.Clock()
    
    try:
        font_serif = pygame.font.SysFont("georgia", 48, italic=True)
        font_sans = pygame.font.SysFont("arial", 16)
    except:
        font_serif = pygame.font.SysFont("serif", 48, italic=True)
        font_sans = pygame.font.SysFont("sans", 16)

    grain_overlay = create_grain(WIDTH, HEIGHT)
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    score = 0
    game_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    else:
                        game_active = True
                        score = 0
                        enemies.empty()
                        bullets.empty()

        if game_active:
            all_sprites.update()
            
            # Spawn enemies
            if random.random() < 0.03:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

            # Collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for _ in hits:
                score += 100

            if pygame.sprite.spritecollide(player, enemies, False):
                game_active = False

        # --- Drawing ---
        screen.fill(CHARCOAL)

        # Atmospheric Background Glows
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow, (27, 48, 34, 20), (0, 0), 400)
        pygame.draw.circle(glow, (0, 71, 171, 20), (WIDTH, HEIGHT), 400)
        screen.blit(glow, (0, 0))

        all_sprites.draw(screen)
        
        # HUD
        score_text = font_sans.render(f"AETHER RESONANCE: {score}", True, MUSTARD_GOLD)
        screen.blit(score_text, (30, 30))

        # Film Grain
        screen.blit(grain_overlay, (0, 0), special_flags=pygame.BLEND_ADD)

        if not game_active:
            # Glassmorphism Menu
            menu_surface = pygame.Surface((400, 250), pygame.SRCALPHA)
            menu_surface.fill((20, 20, 20, 230))
            pygame.draw.rect(menu_surface, MUSTARD_GOLD, (0, 0, 400, 250), 1)
            screen.blit(menu_surface, (WIDTH//2 - 200, HEIGHT//2 - 125))
            
            title = font_serif.render("Aether Wing", True, WHITE_SOFT)
            prompt = font_sans.render("PRESS SPACE TO ASCEND", True, MUSTARD_GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 30))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
