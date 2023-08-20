import pygame
import sys

pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

small_background_color = (255, 255, 255)  # 작은 흰색 배경의 색상
small_background_size = (800, 600)  # 작은 흰색 배경의 크기

list_background_color = (255, 255, 255)
list_background_size = (770, 400)

image_path = "images\\main.jpg"  # 이미지 파일 경로를 해당 이미지 파일의 실제 경로로 바꾸세요
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.center = (screen_width // 2.5, screen_height // 2)

path = "KBO Dia Gothic_medium.ttf"

button_width = 230
button_height = 90
button_bg_color = (255, 255, 255)
button_border_color = (0, 0, 0)
button_font_size = 40
button_font = pygame.font.Font(path, button_font_size)

music_path = "sounds\\background_music.mp3"  # 음악 파일 경로를 해당 음악 파일의 실제 경로로 바꾸세요
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.1)  # 음량 설정
pygame.mixer.music.play(-1)

is_sound_played = False
click_sound_path = "sounds\\switch.mp3"  # 클릭 소리 파일 경로를 해당 소리 파일의 실제 경로로 바꾸세요
click_sound = pygame.mixer.Sound(click_sound_path)
click_sound.set_volume(0.2)

close_button_size = 25
close_button_rect = pygame.Rect((screen_width + small_background_size[0]) // 2 - close_button_size - 10,
                                (screen_height - small_background_size[1]) // 2 + 10,
                                close_button_size, close_button_size)

def draw_button(text, x, y, width, height, is_pressed):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_bg_color, button_rect)

    if is_pressed:
        button_rect.inflate_ip(10, 10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 8)
        button_text = button_font.render(text, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
    else:
        pygame.draw.rect(screen, button_border_color, button_rect, 4)
        button_text = button_font.render(text, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

def create_buttons():
    join_button_rect = pygame.Rect(list_background_rect.left + 50, list_background_rect.bottom + 9, 180, 60)
    create_button_rect = pygame.Rect(list_background_rect.right - 230, list_background_rect.bottom + 9, 180, 60)

    draw_button("참가하기", join_button_rect.x, join_button_rect.y, join_button_rect.width, join_button_rect.height, False)
    draw_button("방 만들기", create_button_rect.x, create_button_rect.y, create_button_rect.width, create_button_rect.height, False)



is_solo_button_pressed = False
is_multi_button_pressed = False
is_small_background_shown = False

# 버튼의 위치 및 초기 크기 정의
solo_button_rect = pygame.Rect(screen_width - button_width - 60, 300, button_width, button_height)
multi_button_rect = pygame.Rect(screen_width - button_width - 60, 420, button_width, button_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if solo_button_rect.collidepoint(event.pos):
                is_solo_button_pressed = True
                # 소리 재생
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True
            if multi_button_rect.collidepoint(event.pos):
                is_multi_button_pressed = True
                is_small_background_shown = True
                # 소리 재생
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True
            if close_button_rect.collidepoint(event.pos) and is_small_background_shown:
                is_small_background_shown = False 

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_solo_button_pressed = False
            is_multi_button_pressed = False
            is_sound_played = False  # 소리 재생 상태 초기화

    screen.fill((255, 255, 255))

    screen.blit(image, image_rect)
    draw_button("솔로 플레이", solo_button_rect.x, solo_button_rect.y, button_width, button_height, is_solo_button_pressed)
    draw_button("멀티 플레이", multi_button_rect.x, multi_button_rect.y, button_width, button_height, is_multi_button_pressed)

    if is_small_background_shown:
        # 작은 흰색 배경 그리기
        small_background_rect = pygame.Rect((screen_width - small_background_size[0]) // 2,
                                        (screen_height - small_background_size[1]) // 2,
                                        small_background_size[0], small_background_size[1])
        pygame.draw.rect(screen, small_background_color, small_background_rect)
        pygame.draw.rect(screen, (0, 0, 0), small_background_rect, 4)

        list_background_rect = pygame.Rect((screen_width - list_background_size[0]) // 2,
                                        (screen_height - list_background_size[1]) // 2 + 20,
                                        list_background_size[0], list_background_size[1])
        pygame.draw.rect(screen, list_background_color, list_background_rect)
        pygame.draw.rect(screen, (0, 0, 0), list_background_rect, 4)

        font = pygame.font.Font(path, 50)
        text = font.render("방 목록", True, (0, 0, 0))
        text_rect = text.get_rect(center=(small_background_rect.centerx, small_background_rect.top + 60))
        screen.blit(text, text_rect)

        create_buttons()

        pygame.draw.line(screen, (0, 0, 0), close_button_rect.topleft, close_button_rect.bottomright, 6)
        pygame.draw.line(screen, (0, 0, 0), close_button_rect.bottomleft, close_button_rect.topright, 6)

    pygame.display.update()