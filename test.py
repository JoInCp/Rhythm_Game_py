import pygame
import copy

# ========== 초기 설정 ==========
pygame.init()
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test game")

# ========== 색상 ==========
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# ========== 폰트 설정 ==========
path = "KBO Dia Gothic_medium.ttf"

button_font_size = 50
button_font = pygame.font.Font(path, button_font_size)
hp_label_font = pygame.font.Font(None, 40)
hp_label_text = hp_label_font.render("MY.HP", True, black)
hp_label_rect = hp_label_text.get_rect(right=screen_width-240, top=160)
comb_font = pygame.font.Font(path, 40)
comb_number_font_size = 80
comb_number_font = pygame.font.Font(path, comb_number_font_size)

# ========== 게임 상태 변수 ==========
comb = 0
game_state = "playing"
running = True

# ========== 위치 및 크기 변수 ==========
rect_x = 60
rect_y = 10
rect_width = 450
rect_height = 680
border_thickness = 8
note_height = 40
note_width = 80
semicolon_key = 59
hp_bar_x = screen_width - 320 
hp_bar_y = hp_label_rect.bottom 
hp_bar_width = 240
hp_bar_height = 60
hp_segment_width = hp_bar_width // 10 
player_hp = 10
button_x_centers = [73.75 + 45, 184.75 + 45, 296 + 45, 407 + 45]
button_y_center = rect_height - 132 + 65
check_line = rect_y + rect_height - 150
hit_line = rect_y + rect_height - 240

# ========== 버튼 데이터 ==========
button_data = [
    {"x": button_x_centers[0] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_s},
    {"x": button_x_centers[1] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_d},
    {"x": button_x_centers[2] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": semicolon_key},
    {"x": button_x_centers[3] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_QUOTE}
]

# ========== 노트 데이터 ==========
original_note_data = [
    {"number": 0, "color": black, "lane": 0, "note_start_delays": 0,"note_speed": 1/15},
    {"number": 1, "color": black, "lane": 1, "note_start_delays": 1000,"note_speed": 1/15},
    {"number": 2, "color": black, "lane": 2, "note_start_delays": 1000,"note_speed": 1/15},
    {"number": 3, "color": black, "lane": 3, "note_start_delays": 1800,"note_speed": 1/15},
    {"number": 4, "color": black, "lane": 1, "note_start_delays": 2500,"note_speed": 1/15},
    {"number": 5, "color": black, "lane": 2, "note_start_delays": 2500,"note_speed": 1/15},
    {"number": 6, "color": black, "lane": 3, "note_start_delays": 3200,"note_speed": 1/15}, 
    {"number": 7, "color": black, "lane": 1, "note_start_delays": 3200,"note_speed": 1/15},
    {"number": 8, "color": black, "lane": 0, "note_start_delays": 4000,"note_speed": 1/15},
    {"number": 9, "color": black, "lane": 1, "note_start_delays": 4500,"note_speed": 1/15},
    {"number": 10, "color": black, "lane": 2, "note_start_delays": 4500,"note_speed": 1/15},
    {"number": 11, "color": black, "lane": 3, "note_start_delays": 5000,"note_speed": 1/15},
]

initial_position_outside_screen = -5  # 더 큰 값을 사용해도 됩니다.
for note in original_note_data:
    note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
    note["number"] = initial_position_outside_screen

retry_button = {
    'color': white,
    'rect': pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50),
    'text': "다시 시도하기",
    'font': pygame.font.Font(path, 30),
    'text_color': black 
}

note_data = copy.deepcopy(original_note_data)
for note in note_data:
    note["hit"] = False


# ========== 함수 정의 ==========

def draw_hp_bar(): # 체력 바 그리기
    pygame.draw.rect(screen, red, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))

    for i in range(player_hp, 10):
        pygame.draw.rect(screen, white, (hp_bar_x + i * hp_segment_width, hp_bar_y, hp_segment_width, hp_bar_height))
    
    pygame.draw.rect(screen, black, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 8) 
    for i in range(1, 10):
        pygame.draw.line(screen, black, (hp_bar_x + i * hp_segment_width, hp_bar_y), 
                         (hp_bar_x + i * hp_segment_width, hp_bar_y + hp_bar_height-5), 4)

def draw_notes(): # 노트 그리기
    for note in note_data:
        if note["number"] >= 0:
            lane = note["lane"]
            x = button_data[lane]["x"] + button_data[lane]["width"] // 2 - note_width // 2
            y = note["number"] * note_height
            pygame.draw.rect(screen, note["color"], (x, y, note_width, note_height), 0)

clock = pygame.time.Clock()

def move_notes():
    global comb, y_position, bottom_of_screen, player_hp, game_state  
    bottom_of_screen = rect_y + rect_height  
    current_time = pygame.time.get_ticks()
    notes_to_remove = []
    
    for note in note_data:
        if current_time >= note["start_time"]:
            note["number"] += note["note_speed"]
            y_position = note["number"] * note_height

            if y_position + note_height > check_line:
                if not note["hit"]: 
                    note["hit"] = True 
                    player_hp -= 1 
                    comb = 0
                    if note not in notes_to_remove:
                        notes_to_remove.append(note)

            elif y_position >= bottom_of_screen:
                if note not in notes_to_remove:
                    notes_to_remove.append(note)

    for note in notes_to_remove:
        note_data.remove(note)

def check_game_over(): # 게임 오버 체크
    global game_state, player_hp
    if player_hp <= 0:
        game_state = "game_over"

def draw_retry_button():
    pygame.draw.rect(screen, retry_button['color'], retry_button['rect'])
    text = retry_button['font'].render(retry_button['text'], True, retry_button['text_color'])
    text_rect = text.get_rect(center=retry_button['rect'].center)
    screen.blit(text, text_rect)


# ========== 메인 게임 루프 ==========
while running:
    screen.fill(white) 
    draw_hp_bar()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for button in button_data:
                if event.key == button["key"]:
                    button["color"] = white
                    
                    lane = button_data.index(button)
                    hit_note = False
                    for note in note_data:
                        y_position = note["number"] * note_height
                        line_y = hit_line
                        if note["lane"] == lane and y_position <= line_y and y_position + note_height >= line_y:
                            hit_note = True
                            break
                    if not hit_note:
                        comb = 0
        if game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button['rect'].collidepoint(mouse_pos):
                    comb = 0
                    player_hp = 10
                    game_state = "playing"
                    
                    note_data = copy.deepcopy(original_note_data)
                    
                    for note in note_data:
                        note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
                        note["number"] = initial_position_outside_screen
                        note["hit"] = False


        elif event.type == pygame.KEYUP:
            for button in button_data:
                if event.key == button["key"]:
                    button["color"] = black
    
    # 게임 중일 때
    if game_state == "playing":
        screen.blit(hp_label_text, hp_label_rect.topleft)
        move_notes()
        check_game_over()
        pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), border_thickness)
    
        segment_width = rect_width // 4
        for i in range(1, 4):
            x = rect_x + i * segment_width
            pygame.draw.line(screen, black, (x, rect_y), (x, rect_y + rect_height-5), 8)

        pygame.draw.line(screen, black, (rect_x, max(check_line, rect_y)), (rect_x + rect_width-5, max(check_line, rect_y)), 8)

        pygame.draw.line(screen, black, (rect_x, max(hit_line, rect_y)), (rect_x + rect_width-5, max(hit_line, rect_y)), 8)

        for button in button_data:  
            if button["color"] == white:  
                for note in note_data[:]:
                    if note["number"] >= 0:
                        lane = note["lane"]
                        y_position = note["number"] * note_height
                        line_y = hit_line
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
        comb_rect = comb_text.get_rect(right=screen_width-140, top=450)
        pygame.draw.circle(screen, black, comb_rect.center, comb_rect.width-30, 8)
        comb_text_rect = comb_text.get_rect(center=(comb_rect.centerx, comb_rect.centery - 130))
        screen.blit(comb_text, comb_text_rect)
        comb_number_text = comb_number_font.render(str(comb), True, black)
        comb_number_rect = comb_number_text.get_rect(center=comb_rect.center)
        screen.blit(comb_number_text, comb_number_rect)

        pygame.display.flip()
        clock.tick(60)

    # 게임 오버일 때
    elif game_state == "game_over":
        screen.fill(white)
        game_over_font = pygame.font.Font(path, 100)
        game_over_text = game_over_font.render("Game Over", True, black)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        draw_retry_button() 
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        
        
pygame.quit()
