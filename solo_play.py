import pygame
import pygame_gui
import sys

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Display Image with Buttons")

# 이미지 로드
image_path = "main.jpg"
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.center = (screen_width // 2.5, screen_height // 2)


# GUI 매니저 초기화
gui_manager = pygame_gui.UIManager((screen_width, screen_height))

def main():
   

        # 화면 업데이트
        screen.fill((255, 255, 255))
        screen.blit(image, image_rect)

        # 폰트 파일 경로 설정
        font_path = "KBO Dia Gothic_medium.ttf"
        font_size = 50
        custom_font = pygame.font.Font(font_path, font_size)


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
