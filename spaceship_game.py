

import pygame
import random
import webbrowser

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spaceship Shooting Game")

# Load images
spaceship_image = pygame.image.load("image/spaceship.png").convert_alpha()
asteroid_image = pygame.image.load("image/asteroid.png").convert_alpha()
bullet_image = pygame.image.load("image/bullet.png").convert_alpha()
power_up_image = pygame.image.load("image/power_up.png").convert_alpha()
background_image = pygame.image.load("image/background.png").convert_alpha()
pause_button_image = pygame.image.load("image/pause.png").convert_alpha()
play_button_image = pygame.image.load("image/play.png").convert_alpha()
sound_on_image = pygame.image.load("image/sound_on.png").convert_alpha()
sound_off_image = pygame.image.load("image/sound_off.png").convert_alpha()
start_button_image = pygame.image.load("image/start_button.png").convert_alpha()

# Scale images
player_size = 90  # Increased size of the spaceship
spaceship_image = pygame.transform.scale(spaceship_image, (player_size, player_size))
bullet_size = 20
bullet_image = pygame.transform.scale(bullet_image, (bullet_size, bullet_size))
power_up_size = 35
power_up_image = pygame.transform.scale(power_up_image, (power_up_size, power_up_size))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
button_size = 50
pause_button_image = pygame.transform.scale(pause_button_image, (button_size, button_size))
play_button_image = pygame.transform.scale(play_button_image, (button_size, button_size))
sound_on_image = pygame.transform.scale(sound_on_image, (button_size, button_size))
sound_off_image = pygame.transform.scale(sound_off_image, (button_size, button_size))
start_button_size = (125, 125)
start_button_image = pygame.transform.scale(start_button_image, start_button_size)

# Load sounds
shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
hit_sound = pygame.mixer.Sound("sound/hit.wav")
lose_life_sound = pygame.mixer.Sound("sound/lose_life.wav")
power_up_sound = pygame.mixer.Sound("sound/power_up.wav")
pygame.mixer.music.load("sound/background.mp3")

# Set up fonts
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)  # New font for smaller text

# Game variables
player_pos = [screen_width // 2, screen_height - player_size - 10]
bullet_speed = 10
asteroid_speed = 2
power_up_speed = 3
score = 0
lives = 5
bullets = []
asteroids = []
power_ups = []
level = 1
high_scores = [0, 0, 0]  # To store top 3 high scores
paused = False
music_muted = False

# Level progression based on score
level_scores = [10, 15, 25, 40, 60, 85, 115, 150, 190, float('inf')]  # Scores needed to reach next level

# Function to create asteroids with random sizes
def create_asteroid():
    x_pos = random.randint(0, screen_width - 50)
    y_pos = 0
    size = random.choice([50, 70, 90])  # Larger sizes for better visibility
    asteroid_img = pygame.transform.scale(asteroid_image, (size, size))
    return [x_pos, y_pos, size, asteroid_img]

# Function to create power-ups
def create_power_up():
    x_pos = random.randint(0, screen_width - power_up_size)
    y_pos = 0
    return [x_pos, y_pos]

# Function to draw text on the screen
def draw_text(text, color, x, y, font_size=36):
    font_to_use = pygame.font.Font(None, font_size)
    label = font_to_use.render(text, 1, color)
    screen.blit(label, (x, y))

# Function to reset game
def reset_game():
    global player_pos, bullets, asteroids, power_ups, score, lives, level, asteroid_speed, paused, game_over
    player_pos = [screen_width // 2, screen_height - player_size - 10]
    bullets = []
    asteroids = []
    power_ups = []
    score = 0
    lives = 5
    level = 1
    asteroid_speed = 2
    paused = False
    game_over = False  # Reset game_over flag
    pygame.mixer.music.play(-1)

# Function to toggle background music on/off
def toggle_music():
    global music_muted
    if music_muted:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    music_muted = not music_muted

# Function to toggle pause/play
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

# Function to draw the home screen
def draw_home_screen():
    screen.blit(background_image, (0, 0))  # Draw background image
    draw_text("Spaceship Shooting Game", (231, 248, 254), screen_width // 2 - 150, screen_height // 2 - 100)
    draw_text("Developed by Malitha Gunathilaka", (255, 255, 255), screen_width - 340, screen_height - 30, 24)  # Font size 24
    draw_text("GitHub: Click to open", (255, 255, 255), screen_width - 200, screen_height - 70, 24)  # Font size 24
    screen.blit(start_button_image, (screen_width // 2 - start_button_size[0] // 2, screen_height // 2 - start_button_size[1] // 2))

# Function to start the game
def start_game():
    global game_started
    game_started = True
    pygame.mixer.music.play(-1)

# Function to draw bullets with transparency
def draw_bullet_with_transparency(bullet):
    bullet_surface = bullet_image.copy()
    bullet_height = bullet[1]
    transparency = max(0, min(255, int((1 - (bullet_height - 0.75 * screen_height) / (0.25 * screen_height)) * 255)))
    bullet_surface.set_alpha(transparency)
    screen.blit(bullet_surface, (bullet[0], bullet[1]))

# Start background music
pygame.mixer.music.play(-1)

# Main game loop
running = True
game_started = False
game_over = False
clock = pygame.time.Clock()

while running:
    if not game_started:
        draw_home_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (screen_width // 2 - start_button_size[0] // 2 <= mouse_pos[0] <= screen_width // 2 + start_button_size[0] // 2 and
                        screen_height // 2 - start_button_size[1] // 2 <= mouse_pos[1] <= screen_height // 2 + start_button_size[1] // 2):
                    start_game()
                elif screen_width - 200 <= mouse_pos[0] <= screen_width - 10 and screen_height - 70 <= mouse_pos[1] <= screen_height - 30:
                    webbrowser.open("https://github.com/Malitha-Gunathilaka")
        pygame.display.update()
        clock.tick(30)
    elif not game_over:
        screen.blit(background_image, (0, 0))  # Draw background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]])
                    shoot_sound.play()
                elif event.key == pygame.K_p:
                    toggle_pause()
                elif event.key == pygame.K_m:
                    toggle_music()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width - 10 - button_size <= mouse_pos[0] <= screen_width - 10 and 70 <= mouse_pos[1] <= 70 + button_size:
                    toggle_music()
                elif screen_width - 10 - button_size <= mouse_pos[0] <= screen_width - 10 and 10 <= mouse_pos[1] <= 10 + button_size:
                    toggle_pause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += 10

        if not paused:
            # Add new asteroids
            if random.randint(1, 30 - min(level, 20)) == 1:
                asteroids.append(create_asteroid())

            # Add new power-ups
            if random.randint(1, 500) == 1:
                power_ups.append(create_power_up())

            # Move and draw asteroids
            for asteroid in asteroids[:]:
                asteroid[1] += asteroid_speed
                if asteroid[1] > screen_height:
                    asteroids.remove(asteroid)
                screen.blit(asteroid[3], (asteroid[0], asteroid[1]))

            # Move and draw power-ups
            for power_up in power_ups[:]:
                power_up[1] += power_up_speed
                if power_up[1] > screen_height:
                    power_ups.remove(power_up)
                screen.blit(power_up_image, (power_up[0], power_up[1]))

            # Move and draw bullets
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < -bullet_size:
                    bullets.remove(bullet)
                elif 0.75 * screen_height <= bullet[1] <= screen_height:
                    draw_bullet_with_transparency(bullet)
                else:
                    screen.blit(bullet_image, (bullet[0], bullet[1]))

            # Check for bullet-asteroid collisions
            for asteroid in asteroids[:]:
                asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[2])
                for bullet in bullets[:]:
                    bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
                    if asteroid_rect.colliderect(bullet_rect):
                        asteroids.remove(asteroid)
                        bullets.remove(bullet)
                        score += 1
                        hit_sound.play()
                        break

            # Check for player-asteroid collisions
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
            for asteroid in asteroids[:]:
                asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[2])
                if player_rect.colliderect(asteroid_rect):
                    asteroids.remove(asteroid)
                    lives -= 1
                    lose_life_sound.play()
                    if lives <= 0:
                        game_over = True
                    break

            # Check for player-power-up collisions
            for power_up in power_ups[:]:
                power_up_rect = pygame.Rect(power_up[0], power_up[1], power_up_size, power_up_size)
                if player_rect.colliderect(power_up_rect):
                    power_ups.remove(power_up)
                    lives += 1
                    power_up_sound.play()

            # Level up
            for i, level_score in enumerate(level_scores):
                if score >= level_score:
                    level = i + 1
                else:
                    break

            # Increase asteroid speed based on level
            asteroid_speed = 2 + level // 2

        # Draw player spaceship
        screen.blit(spaceship_image, (player_pos[0], player_pos[1]))

        # Draw HUD
        draw_text(f"Score: {score}", (255, 255, 255), 10, 10)
        draw_text(f"Lives: {lives}", (255, 255, 255), 10, 50)
        draw_text(f"Level: {level}", (255, 255, 255), screen_width // 2 - 50, 10)
        if paused:
            draw_text("Paused", (255, 255, 255), screen_width // 2 - 50, screen_height // 2)
            screen.blit(play_button_image, (screen_width - 10 - button_size, 10))
        else:
            screen.blit(pause_button_image, (screen_width - 10 - button_size, 10))

        # Draw sound button
        if music_muted:
            screen.blit(sound_off_image, (screen_width - 10 - button_size, 70))
        else:
            screen.blit(sound_on_image, (screen_width - 10 - button_size, 70))

        pygame.display.update()
        clock.tick(30)
    else:
        draw_text("Game Over", (255, 0, 0), screen_width // 2 - 100, screen_height // 2 - 50)
        draw_text(f"Score: {score}", (255, 255, 255), screen_width // 2 - 50, screen_height // 2)
        draw_text("Press R to Restart or Q to Quit", (255, 255, 255), screen_width // 2 - 150, screen_height // 2 + 50)

        # Update high scores
        high_scores.append(score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:1]

        # Display high scores
        draw_text("High Scores:", (255, 255, 255), screen_width // 2 - 70, screen_height // 2 + 100)
        for i, high_score in enumerate(high_scores):
            draw_text(f"{i + 1}. {high_score}", (255, 255, 255), screen_width // 2 - 50, screen_height // 2 + 140 + i * 40)

        # Draw Developer Name and GitHub Link
        draw_text("Developed by Malitha Gunathilaka", (255, 255, 255), screen_width - 340, screen_height - 30, 24)  # Font size 24
        draw_text("GitHub: Click to open", (255, 255, 255), screen_width - 200, screen_height - 70, 24)  # Font size 24
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width - 200 <= mouse_pos[0] <= screen_width - 10 and screen_height - 70 <= mouse_pos[1] <= screen_height - 30:
                    webbrowser.open("https://github.com/Malitha-Gunathilaka")
        pygame.display.update()
        clock.tick(30)
pygame.quit()