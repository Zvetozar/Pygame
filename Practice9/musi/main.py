import pygame
import os
from mutagen.mp3 import MP3  # Для получения длины трека

pygame.init()

WIDTH, HEIGHT = 500, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыкальный плеер 🎵")

MUSIC_FOLDER = "Music"
songs = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

if not songs:
    raise FileNotFoundError("Нет музыкальных файлов в папке 'Music'")

current_song = 0
is_playing = True 

pygame.mixer.init()

def play_song():
    """Воспроизведение текущего трека."""
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, songs[current_song]))
    pygame.mixer.music.play()
    global track_length
    track_length = MP3(os.path.join(MUSIC_FOLDER, songs[current_song])).info.length  # Длина трека

play_song() # Запускаем первый трек


IMAGE_PATH = "Player/Shape_of_You_single_cover.jpg"
if os.path.exists(IMAGE_PATH):
    background = pygame.image.load(IMAGE_PATH)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
else:
    print(f"Файл {IMAGE_PATH} не найден!")


button_images = {
    "play": pygame.image.load("Player/play.png"),
    "pause": pygame.image.load("Player/pause.png"),
    "next": pygame.image.load("Player/next.png"),
    "prev": pygame.image.load("Player/back.png"),
}


for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], (80, 80))


button_positions = {
    "prev": (100, 320),
    "play_pause": (210, 320),  
    "next": (320, 320),
}


progress_bar_x = 50
progress_bar_y = 290
progress_bar_width = 400
progress_bar_height = 10
progress_circle_radius = 8 
is_dragging = False  


running = True
while running:
    screen.fill((30, 30, 30)) 
    
    if 'background' in locals():
        screen.blit(background, (0, 0))

    screen.blit(button_images["prev"], button_positions["prev"])
    screen.blit(button_images["next"], button_positions["next"])

    # Отображаем Play или Pause в зависимости от состояния
    if is_playing:
        screen.blit(button_images["pause"], button_positions["play_pause"])
    else:
        screen.blit(button_images["play"], button_positions["play_pause"])

    # Получаем текущее время трека в секундах
    current_time = pygame.mixer.music.get_pos() / 1000 

    if not is_dragging:
        progress = min(current_time / track_length, 1.0)  
    else:
        progress = circle_x / progress_bar_width  

    pygame.draw.rect(screen, (180, 180, 180), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
    
    circle_x = progress_bar_x + int(progress * progress_bar_width)
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, progress_bar_y + progress_bar_height // 2), progress_circle_radius)
 
    font = pygame.font.Font(None, 24)
    time_text = f"{int(current_time // 60)}:{int(current_time % 60):02d} / {int(track_length // 60)}:{int(track_length % 60):02d}"
    text_surface = font.render(time_text, True, (255, 255, 255))
    screen.blit(text_surface, (WIDTH // 2 - 40, progress_bar_y - 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Управление клавиатурой:  P - Play/Pause, N - Next, B - Previous
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: 
                if is_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                is_playing = not is_playing
            elif event.key == pygame.K_n:  
                current_song = (current_song + 1) % len(songs)
                play_song()
                is_playing = True
            elif event.key == pygame.K_b: 
                current_song = (current_song - 1) % len(songs)
                play_song()
                is_playing = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for key, pos in button_positions.items():
                btn_x, btn_y = pos
                if btn_x <= x <= btn_x + 80 and btn_y <= y <= btn_y + 80:
                    if key == "play_pause":
                        if is_playing:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        is_playing = not is_playing
                    elif key == "next":
                        current_song = (current_song + 1) % len(songs)
                        play_song()
                        is_playing = True
                    elif key == "prev":
                        current_song = (current_song - 1) % len(songs)
                        play_song()
                        is_playing = True
     
            if progress_bar_x <= x <= progress_bar_x + progress_bar_width and progress_bar_y - 10 <= y <= progress_bar_y + progress_bar_height + 10:
                is_dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                new_time = ((x - progress_bar_x) / progress_bar_width) * track_length
                pygame.mixer.music.play(start=new_time)  
            is_dragging = False

    pygame.display.flip()

pygame.quit()