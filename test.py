import pygame

pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

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
    {"number": 0, "color": black, "lane": 0, "note_start_delays": 0,"note_speed": 1/10},
    {"number": 1, "color": black, "lane": 1, "note_start_delays": 700,"note_speed": 1/10},
    {"number": 2, "color": black, "lane": 2, "note_start_delays": 700,"note_speed": 1/10},
    {"number": 3, "color": black, "lane": 3, "note_start_delays": 1500,"note_speed": 1/10},
    {"number": 4, "color": black, "lane": 1, "note_start_delays": 1800,"note_speed": 1/10},
    {"number": 5, "color": black, "lane": 2, "note_start_delays": 1800,"note_speed": 1/10},
    {"number": 6, "color": black, "lane": 3, "note_start_delays": 2300,"note_speed": 1/10}, 
    {"number": 7, "color": black, "lane": 1, "note_start_delays": 2300,"note_speed": 1/10},
    {"number": 8, "color": black, "lane": 0, "note_start_delays": 2700,"note_speed": 1/10},
    {"number": 9, "color": black, "lane": 1, "note_start_delays": 3300,"note_speed": 1/10},
    {"number": 10, "color": black, "lane": 2, "note_start_delays": 4000,"note_speed": 1/10},
    {"number": 11, "color": black, "lane": 3, "note_start_delays": 4000,"note_speed": 1/10},
]

note_height = 40
note_width = 80

comb = 0

initial_position_outside_screen = -5  # 더 큰 값을 사용해도 됩니다.
for note in note_data:
    note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
    note["number"] = initial_position_outside_screen
comb_font = pygame.font.Font(None, 40)
comb_number_font_size = 100
comb_number_font = pygame.font.Font(None, comb_number_font_size)

# MY.HP 라벨 관련 설정
hp_label_font = pygame.font.Font(None, 40)
hp_label_text = hp_label_font.render("MY.HP", True, black)
hp_label_rect = hp_label_text.get_rect(right=screen_width-230, top=150)

# HP 바 관련 설정
hp_bar_x = screen_width - 320 
hp_bar_y = hp_label_rect.bottom + 10
hp_bar_width = 240
hp_bar_height = 60
hp_segment_width = hp_bar_width // 10 

player_hp = 10

def draw_hp_bar():
    # 먼저 전체 바를 빨간색으로 그립니다.
    pygame.draw.rect(screen, red, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))

    # 빠진 체력에 따라 하얀색으로 그립니다.
    for i in range(player_hp, 10):
        pygame.draw.rect(screen, white, (hp_bar_x + i * hp_segment_width, hp_bar_y, hp_segment_width, hp_bar_height))
    
    # 테두리와 구분선을 그립니다.
    pygame.draw.rect(screen, black, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 8)  # 테두리
    for i in range(1, 10):
        pygame.draw.line(screen, black, (hp_bar_x + i * hp_segment_width, hp_bar_y), 
                         (hp_bar_x + i * hp_segment_width, hp_bar_y + hp_bar_height-5), 4)


def draw_notes():
    for note in note_data:
        if note["number"] >= 0:
            lane = note["lane"]
            x = button_data[lane]["x"] + button_data[lane]["width"] // 2 - note_width // 2
            y = note["number"] * note_height
            pygame.draw.rect(screen, note["color"], (x, y, note_width, note_height), 0)

clock = pygame.time.Clock()

def move_notes():
    global comb, y_position, bottom_of_screen, player_hp  # player_hp를 추가합니다.
    bottom_of_screen = rect_y + rect_height  
    hit_line = rect_y + rect_height - 240
    current_time = pygame.time.get_ticks()
    notes_to_remove = []

    for note in note_data:
        if current_time >= note["start_time"]:
            note["number"] += note["note_speed"]
            y_position = note["number"] * note_height

            # 노트가 라인에 닿을 때
            if hit_line <= y_position and y_position <= hit_line + note_height:
                player_hp -= 1 
                if note not in notes_to_remove:
                    notes_to_remove.append(note)
                comb = 0

            # 노트가 화면 아래로 사라지는 지점을 넘었을 때
            elif y_position >= bottom_of_screen:
                if note not in notes_to_remove:
                    notes_to_remove.append(note)

    # 노트 삭제
    for note in notes_to_remove:
        note_data.remove(note)




while running:
    screen.fill(white)  # 화면을 흰색으로 채우기

    move_notes()  # while 루프의 시작 부분에서 move_notes() 함수를 호출합니다.

    draw_hp_bar()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for button in button_data:
                if event.key == button["key"]:
                    button["color"] = white
                    
                    # 라인과 겹치지 않는 상태에서 버튼이 눌리면 콤보 초기화
                    lane = button_data.index(button)
                    hit_note = False
                    for note in note_data:
                        y_position = note["number"] * note_height
                        line_y = rect_y + rect_height - 240
                        if note["lane"] == lane and y_position <= line_y and y_position + note_height >= line_y:
                            hit_note = True
                            break
                    if not hit_note:
                        comb = 0

        elif event.type == pygame.KEYUP:
            for button in button_data:
                if event.key == button["key"]:
                    button["color"] = black
    
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
        if button["color"] == white:  # 키가 눌렸을 때만 노트와 충돌 검사
            for note in note_data[:]:
                if note["number"] >= 0:
                    lane = note["lane"]
                    y_position = note["number"] * note_height
                    line_y = rect_y + rect_height - 240
                    if y_position <= line_y and y_position + note_height >= line_y:
                        if lane == button_data.index(button):
                            comb += 1
                            note_data.remove(note)
                            break
                    elif y_position > rect_y + rect_height:
                        if lane == button_data.index(button):
                            comb = 0
    draw_notes()

    for button in button_data:
        pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 1)
        pygame.draw.rect(screen, button["color"], (button["x"], button["y"], button["width"], button["height"]), 0)
        if button["pressed"]:
            pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 3)

        text = button_font.render(pygame.key.name(button["key"]), True, white)
        text_rect = text.get_rect(center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2))
        screen.blit(text, text_rect)

    comb_text = comb_font.render("COMB", True, black)
    comb_rect = comb_text.get_rect(right=screen_width-160, top=400)
    pygame.draw.circle(screen, black, comb_rect.center, comb_rect.width, 8)
    comb_text_rect = comb_text.get_rect(center=(comb_rect.centerx, comb_rect.centery - 100))
    screen.blit(comb_text, comb_text_rect)
    comb_number_text = comb_number_font.render(str(comb), True, black)
    comb_number_rect = comb_number_text.get_rect(center=comb_rect.center)
    screen.blit(comb_number_text, comb_number_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
