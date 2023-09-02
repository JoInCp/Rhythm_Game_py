import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ESC 키로 화면 전환")

# 화면 1
def screen1():
    screen.fill((255, 0, 0))  # 빨간 배경색
    pygame.display.flip()

# 화면 2
def screen2():
    screen.fill((0, 0, 255))  # 파란 배경색
    pygame.display.flip()

current_screen = screen1  # 초기 화면 설정

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC 키를 누르면 화면 전환
                if current_screen == screen1:
                    current_screen = screen2
                else:
                    current_screen = screen1

    current_screen()  # 현재 화면 표시

# Pygame 종료
pygame.quit()
sys.exit()
