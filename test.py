import pygame

pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle Drawing")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

button_font_size = 50
button_font = pygame.font.Font(None, button_font_size)

running = True
rect_x = 60
rect_y = 10
rect_width = 450
rect_height = 680
border_thickness = 8

semicolon_key = 59

button_x_centers = [73.75 + 45, 184.75 + 45, 296 + 45, 407 + 45]
button_y_center = rect_height - 132 + 65

button_data = [
    {"x": button_x_centers[0] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_s},
    {"x": button_x_centers[1] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_d},
    {"x": button_x_centers[2] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": semicolon_key},
    {"x": button_x_centers[3] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_QUOTE}
]

note_data = [
    {"number": 0, "color": black, "lane": 0, "note_start_delays": 1000,"note_speed": 1/50},
    {"number": 1, "color": black, "lane": 1, "note_start_delays": 3000,"note_speed": 1/50},
    {"number": 2, "color": black, "lane": 2, "note_start_delays": 5000,"note_speed": 1/50},
    {"number": 3, "color": black, "lane": 3, "note_start_delays": 7000,"note_speed": 1/50},
    {"number": 4, "color": black, "lane": 1, "note_start_delays": 9000,"note_speed": 1/50},
    {"number": 5, "color": black, "lane": 2, "note_start_delays": 12000,"note_speed": 1/50},
    {"number": 6, "color": black, "lane": 3, "note_start_delays": 15000,"note_speed": 1/50},
    {"number": 7, "color": black, "lane": 1, "note_start_delays": 18000,"note_speed": 1/50}, 
]

note_height = 40
note_width = 80

comb = 0  # 점수 변수 초기화

for note in note_data:
    note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
    note["number"] = -1  # 화면 밖에서 시작하도록 음수로 초기화

comb_font = pygame.font.Font(None, 36)  # 점수를 나타낼 폰트 설정

def draw_notes():
    for note in note_data:
        if note["number"] >= 0:  # 화면에 보이는 노트만 그립니다.
            lane = note["lane"]
            x = button_data[lane]["x"] + button_data[lane]["width"] // 2 - note_width // 2
            y = note["number"] * note_height
            pygame.draw.rect(screen, note["color"], (x, y, note_width, note_height), 0)

clock = pygame.time.Clock()

def move_notes(note):
    note["number"] += note["note_speed"]
    if note["number"] * note_height > screen_height:
        note_data.remove(note)  # 리스트에서 해당 노트 삭제

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() 

    screen.fill(white)

    pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), border_thickness)

    segment_width = rect_width // 4
    for i in range(1, 4):
        x = rect_x + i * segment_width
        pygame.draw.line(screen, black, (x, rect_y), (x, rect_y + rect_height-5), 8)
        
    y = rect_y + rect_height - 150
    pygame.draw.line(screen, black, (rect_x, max(y, rect_y)), (rect_x + rect_width-5, max(y, rect_y)), 8)

    y = rect_y + rect_height - 240
    pygame.draw.line(screen, black, (rect_x, max(y, rect_y)), (rect_x + rect_width-5, max(y, rect_y)), 8)

    for button in button_data:
        if keys[button["key"]]:
            button["pressed"] = True
            button["color"] = white
            for note in note_data:
                if note["number"] >= 0:  # 화면에 보이는 노트만 검사
                    lane = note["lane"]
                    x = button_data[lane]["x"]
                    y = note["number"] * note_height
                    if y < rect_y + rect_height - 240 + note_height and y + note_height > rect_y + rect_height - 240:  # 노트의 아무 부분이 y = rect_y + rect_height - 240 라인과 닿으면
                        if lane == button_data.index(button):  # 버튼과 노트의 레인이 일치하면
                            comb += 1  # 점수 증가
                            note_data.remove(note)  # 노트 삭제
        else:
            button["pressed"] = False
            button["color"] = black
        
        pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 1)
        pygame.draw.rect(screen, button["color"], (button["x"], button["y"], button["width"], button["height"]), 0)
        if button["pressed"]:
            pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 3)
            
        text = button_font.render(pygame.key.name(button["key"]), True, white)
        text_rect = text.get_rect(center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2))
        screen.blit(text, text_rect)
    
    current_time = pygame.time.get_ticks()

    for note in note_data:
        if current_time >= note["start_time"]:
            move_notes(note)  # 딜레이가 지난 노트만 내려오도록 처리
            if note["number"] * note_height > rect_y + rect_height - 190:
                note_data.remove(note)  # 일정 라인 아래로 내려가면 해당 노트 삭제

    draw_notes()  # 음표 그리기 함수 호출
    
    # 점수를 화면 오른쪽 위에 표시
    comb_text = comb_font.render("COMB", True, black)
    comb_rect = comb_text.get_rect(right=screen_width-160, top=300)
    
    # 검정색 테두리와 흰색 배경을 가진 원을 그립니다.
    pygame.draw.circle(screen, black, comb_rect.center, comb_rect.width // 2 + 10, 4)

    # 콤보 텍스트를 원 바깥에 배치
    comb_text_rect = comb_text.get_rect(center=(comb_rect.centerx, comb_rect.centery - 70))
    screen.blit(comb_text, comb_text_rect)

    # 숫자를 원의 중앙에 배치
    comb_number_text = comb_font.render(str(comb), True, black)
    comb_number_rect = comb_number_text.get_rect(center=comb_rect.center)
    screen.blit(comb_number_text, comb_number_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()