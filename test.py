import pygame

# 초기화
pygame.init()

# 화면 설정
screen_width = 1100
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle Drawing")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

# 폰트 설정 (버튼 위에 표시되는 글자 크기 조절)
button_font_size = 50
button_font = pygame.font.Font(None, button_font_size)

# 게임 루프
running = True

# 버튼 관련 정보
rect_height = 680  # 직사각형의 높이를 미리 정의

semicolon_key = 59

# 각 버튼의 영역 중앙 좌표 계산
button_x_centers = [73.75 + 45, 184.75 + 45, 296 + 45, 407 + 45]
button_y_center = rect_height - 132 + 65

button_data = [
    {"x": button_x_centers[0] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_s},
    {"x": button_x_centers[1] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_d},
    {"x": button_x_centers[2] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": semicolon_key},
    {"x": button_x_centers[3] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_QUOTE}
]

note_speed = 5
note_width = 80
note_height = 20
note_data = [
    {"number": 0, "color": black, "lane": 0, "distance": 0},
    {"number": 1, "color": black, "lane": 1, "distance": 100},
    {"number": 2, "color": black, "lane": 2, "distance": 100},
    {"number": 3, "color": black, "lane": 3, "distance": 100},
    {"number": 4, "color": black, "lane": 1, "distance": 100},
    {"number": 5, "color": black, "lane": 2, "distance": 100},
    {"number": 6, "color": black, "lane": 3, "distance": 100},
    {"number": 7, "color": black, "lane": 1, "distance": 100},
    
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # 현재 눌려진 키들 확인

    screen.fill(white)

    # 직사각형 그리기
    rect_x = 60
    rect_y = 10
    rect_width = 450
    border_thickness = 8
    pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), border_thickness)

    segment_width = rect_width // 4
    for i in range(1, 4):
        x = rect_x + i * segment_width
        pygame.draw.line(screen, black, (x, rect_y), (x, rect_y + rect_height-5), 8)
        
    # 사각형 범위 내부에 선 그리기 (선 길이 조절)
    y = rect_y + rect_height - 150
    pygame.draw.line(screen, black, (rect_x, max(y, rect_y)), (rect_x + rect_width-5, max(y, rect_y)), 8)

    y = rect_y + rect_height - 240
    pygame.draw.line(screen, black, (rect_x, max(y, rect_y)), (rect_x + rect_width-5, max(y, rect_y)), 8)

    # 버튼 그리기 및 키 입력 확인
    for button in button_data:
        if keys[button["key"]]:
            button["pressed"] = True
            button["color"] = white
        else:
            button["pressed"] = False
            button["color"] = black
        
        pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 1)
        pygame.draw.rect(screen, button["color"], (button["x"], button["y"], button["width"], button["height"]), 0)
        if button["pressed"]:
            pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 3)
            
        # 버튼 위에 키 표시 (글자 크기 조절)
        text = button_font.render(pygame.key.name(button["key"]), True, white)
        text_rect = text.get_rect(center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2))
        screen.blit(text, text_rect)
    
    for note in note_data:
        note_lane = note["lane"]
        note_x = button_data[note_lane]["x"] + (button_data[note_lane]["width"] - note_width) // 2
        note_y = rect_y - note["distance"]

        note_color = note["color"] 
        
        pygame.draw.rect(screen, note_color, (note_x, note_y, note_width, note_height))
        
        # 노트의 위치 업데이트
        note["distance"] += note_speed
    
    pygame.draw.rect(screen, note_color, (note_x, note_y, note_width, note_height))
    pygame.display.flip()

pygame.quit()
