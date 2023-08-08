import pygame
import pygame_gui
import sys

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1100
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Display Image with Buttons")

# 이미지 로드
main_image_path = "images\\main.jpg"
image = pygame.image.load(main_image_path)
image_rect = image.get_rect()
image_rect.center = (screen_width // 2.5, screen_height // 2)

sound_image_path = "images\\sound.jpg"
sound_image = pygame.image.load(sound_image_path)
sound_image_size = (60, 50)
sound_image = pygame.transform.scale(sound_image, sound_image_size)
sound_image_rect = sound_image.get_rect()
sound_image_rect.bottomright = (screen_width - 10, screen_height - 10)  # 원하는 위치로 조정



# 버튼 색상 정의
button_bg_color = (255, 255, 255)
button_border_color = (0, 0, 0)

# 버튼 크기 및 위치
button_width = 300
button_height = 100
solo_button_rect = pygame.Rect((screen_width // 1.3 - button_width // 2, screen_height // 2.5), (button_width, button_height))
multi_button_rect = pygame.Rect((screen_width // 1.3 - button_width // 2, screen_height // 1.75), (button_width, button_height))

# 버튼 크기 조정 관련 변수
original_button_size = solo_button_rect.size
pressed_button_size = (int(button_width * 1.1), int(button_height * 1.1))
is_solo_button_pressed = False
is_multi_button_pressed = False

# 딸깍 소리 로드
click_sound = pygame.mixer.Sound("sounds\\switch.mp3")  # 사용할 사운드 파일의 경로를 입력하세요
click_sound.set_volume(0.2) 

# 노래 재생 설정
pygame.mixer.music.load("sounds\\background_music.mp3")  # 메인 화면에 재생할 노래 파일의 경로를 입력하세요
pygame.mixer.music.set_volume(0.05)  # 초기 음량 설정
pygame.mixer.music.play(-1)  # 노래를 반복재생 (-1: 무한반복)

# GUI 매니저 초기화
gui_manager = pygame_gui.UIManager((screen_width, screen_height))

def main():
    global is_solo_button_pressed, is_multi_button_pressed

    clock = pygame.time.Clock()

    # 폰트 파일 경로 설정
    font_path = "KBO Dia Gothic_medium.ttf"
    font_size = 50
    custom_font = pygame.font.Font(font_path, font_size)

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo_button_rect.collidepoint(event.pos):
                    is_solo_button_pressed = True
                    click_sound.play()  
                if multi_button_rect.collidepoint(event.pos):
                    is_multi_button_pressed = True
                    click_sound.play()  

            if event.type == pygame.MOUSEBUTTONUP:
                if solo_button_rect.collidepoint(event.pos):
                    is_solo_button_pressed = False
                    click_sound.play()  
                if multi_button_rect.collidepoint(event.pos):
                    is_multi_button_pressed = False
                    click_sound.play()  

            # UI 이벤트 처리
            gui_manager.process_events(event)

        # 화면 업데이트
        screen.fill((255, 255, 255))
        screen.blit(image, image_rect)

        # 솔로 플레이 버튼 그리기
        solo_button_size = pressed_button_size if is_solo_button_pressed else original_button_size
        solo_button_rect.size = solo_button_size
        solo_button_rect.center = (screen_width // 1.3, screen_height // 2.1)
        pygame.draw.rect(screen, button_bg_color, solo_button_rect)
        pygame.draw.rect(screen, button_border_color, solo_button_rect, 10)
        solo_text = custom_font.render("솔로 플레이", True, (0, 0, 0))
        solo_text_rect = solo_text.get_rect(center=solo_button_rect.center)
        screen.blit(solo_text, solo_text_rect)

        # 멀티 플레이 버튼 그리기
        multi_button_size = pressed_button_size if is_multi_button_pressed else original_button_size
        multi_button_rect.size = multi_button_size
        multi_button_rect.center = (screen_width // 1.3, screen_height // 1.55)
        pygame.draw.rect(screen, button_bg_color, multi_button_rect)
        pygame.draw.rect(screen, button_border_color, multi_button_rect, 10)
        multi_text = custom_font.render("멀티 플레이", True, (0, 0, 0))
        multi_text_rect = multi_text.get_rect(center=multi_button_rect.center)
        screen.blit(multi_text, multi_text_rect)

        screen.blit(sound_image, sound_image_rect)

        # GUI 업데이트
        gui_manager.update(time_delta)
        gui_manager.draw_ui(screen)

        pygame.display.update()


def decrease_volume():
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(current_volume - 0.1, 0.0)
    pygame.mixer.music.set_volume(new_volume)

def increase_volume():
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(current_volume + 0.1, 1.0)
    pygame.mixer.music.set_volume(new_volume)

if __name__ == "__main__":
    main()
