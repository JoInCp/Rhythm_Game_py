import pygame
from pygame.locals import QUIT

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gradient Example')

def draw_vertical_gradient(screen, start_color, end_color):
    """
    세로 방향 그라데이션 그리기
    :param screen: pygame screen 객체
    :param start_color: 시작 색상 (R, G, B)
    :param end_color: 종료 색상 (R, G, B)
    """
    for y in range(SCREEN_HEIGHT):
        r = start_color[0] * (1 - y / SCREEN_HEIGHT) + end_color[0] * (y / SCREEN_HEIGHT)
        g = start_color[1] * (1 - y / SCREEN_HEIGHT) + end_color[1] * (y / SCREEN_HEIGHT)
        b = start_color[2] * (1 - y / SCREEN_HEIGHT) + end_color[2] * (y / SCREEN_HEIGHT)
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (SCREEN_WIDTH, y))

running = True
gradient_active = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                gradient_active = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                gradient_active = False

    screen.fill((0, 0, 0))  # 화면을 검정색으로 지우기
    if gradient_active:
        draw_vertical_gradient(screen, (0, 0, 0), (255, 255, 255))  # 검정색에서 하얀색으로 그라데이션 그리기
    pygame.display.flip()

pygame.quit()
