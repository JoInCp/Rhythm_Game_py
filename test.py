import pygame
import copy
import time
import threading

player_hp = 10

def run_game():
    pygame.init()
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("test game")
    # song_file_path = "sounds\\test.mp3"
    song_file_path = "sounds//test.mp3"

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
    hp_label_rect = hp_label_text.get_rect(right=screen_width-240, top=180)
    comb_font = pygame.font.Font(path, 40)
    comb_number_font_size = 80
    comb_number_font = pygame.font.Font(path, comb_number_font_size)

    # ========== 게임 상태 변수 ==========
    score = 0
    comb = 0
    game_state = "playing"
    running = True
    global player_hp 

    # ========== 위치 및 크기 변수 ==========
    rect_x = 60
    rect_y = 10
    rect_width = 450
    rect_height = 780
    border_thickness = 8
    note_height = 35
    note_width = 80
    semicolon_key = 59

    hp_bar_x = screen_width - 320 
    hp_bar_y = hp_label_rect.bottom 
    hp_bar_width = 240
    hp_bar_height = 60
    hp_segment_width = hp_bar_width // 10 

    button_x_centers = [73.75 + 45, 184.75 + 45, 296 + 45, 407 + 45]
    button_y_center = rect_height - 132 + 65

    check_line = rect_y + rect_height - 150
    hit_line = rect_y + rect_height - 240

    score_box_width = 240
    score_box_height = 70
    score_box_x = screen_width - 320
    score_box_y = 80

    # ========== 버튼 데이터 ==========
    button_data = [
        {"x": button_x_centers[0] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_s},
        {"x": button_x_centers[1] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_d},
        {"x": button_x_centers[2] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": semicolon_key},
        {"x": button_x_centers[3] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_QUOTE}
    ]

    # ========== 노트 데이터 ==========
    original_note_data  = [
        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 1, "color": "black", "lane": 1, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 2, "color": "black", "lane": 0, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 3, "color": "black", "lane": 1, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 4, "color": "black", "lane": 3, "note_start_delays": 3200, "note_speed": 1/10},
        {"number": 5, "color": "black", "lane": 1, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 6, "color": "black", "lane": 2, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 7, "color": "black", "lane": 3, "note_start_delays": 5200, "note_speed": 1/10},
        {"number": 8, "color": "black", "lane": 1, "note_start_delays": 5200, "note_speed": 1/10},
        {"number": 9, "color": "black", "lane": 2, "note_start_delays": 6200, "note_speed": 1/10},
        {"number": 10, "color": "black", "lane": 3, "note_start_delays": 6200, "note_speed": 1/10}
]

    initial_position_outside_screen = -5  # 더 큰 값을 사용해도 됩니다.
    for note in original_note_data:
        note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
        note["number"] = initial_position_outside_screen

    retry_button = {
        'color': white,
        'rect': pygame.Rect(screen_width-22, screen_height // 2 + 50, 200, 50),
        'text': "다시 하기",
        'font': pygame.font.Font(path, 50),
        'text_color': black 
    }

    menu_button = {
        'color': white,
        'rect': pygame.Rect(screen_width - 250, screen_height // 2 + 150, 200, 50),
        'text': "메뉴 가기",
        'font': pygame.font.Font(path, 50),
        'text_color': black 
    }

    button_spacing = 60
    half_spacing = button_spacing / 2

    total_buttons_width = retry_button['rect'].width + menu_button['rect'].width + button_spacing
    retry_button['rect'].topleft = ((screen_width - total_buttons_width) // 2, screen_height // 2 + 50)
    menu_button['rect'].topleft = (retry_button['rect'].right + button_spacing, screen_height // 2 + 50)

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

    def draw_retry_button():
        pygame.draw.rect(screen, retry_button['color'], retry_button['rect'])
        text = retry_button['font'].render(retry_button['text'], True, retry_button['text_color'])
        text_rect = text.get_rect(center=retry_button['rect'].center)
        screen.blit(text, text_rect)

    def draw_menu_button():
        pygame.draw.rect(screen, menu_button['color'], menu_button['rect'])
        text = menu_button['font'].render(menu_button['text'], True, menu_button['text_color'])
        text_rect = text.get_rect(center=menu_button['rect'].center)
        screen.blit(text, text_rect)

    def play_song():
        pygame.mixer.music.load(song_file_path)
        pygame.mixer.music.play()

    def stop_song():
        pygame.mixer.music.stop()

    def play_song_thread():
        time.sleep(2)
        pygame.mixer.music.load(song_file_path)
        pygame.mixer.music.play()

    def draw_win_screen():
        screen.fill(white)
        
        score_font = pygame.font.Font(path, 70)
        score_text = score_font.render(f"Score: {score}", True, black)
        score_rect = score_text.get_rect(center=(screen_width // 2, 300))

        comb_font = pygame.font.Font(path, 70)
        comb_text = comb_font.render(f"Max Combo: {comb}", True, black)
        comb_rect = comb_text.get_rect(center=(screen_width // 2, score_rect.bottom + 50))

        draw_retry_button()
        draw_menu_button()

        line_start = (score_rect.left-90, score_rect.bottom + 90)
        line_end = (score_rect.right+90, score_rect.bottom + 90)
        pygame.draw.line(screen, black, line_start, line_end, 8)

        vertical_line_start_x = (retry_button['rect'].right + menu_button['rect'].left) // 2
        vertical_line_start = (vertical_line_start_x, score_rect.bottom + 90)
        vertical_line_end = (vertical_line_start_x, retry_button['rect'].top+60)
        pygame.draw.line(screen, black, vertical_line_start, vertical_line_end, 8)  

        screen.blit(score_text, score_rect)
        screen.blit(comb_text, comb_rect)

        stop_song()
    
    def draw_game_over_screen():
        screen.fill(white)
        game_over_font = pygame.font.Font(path, 100)
        game_over_text = game_over_font.render("Game Over", True, black)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 60))

        draw_retry_button() 
        draw_menu_button()

        line_start = (text_rect.left, text_rect.bottom + 20)
        line_end = (text_rect.right, text_rect.bottom + 20)
        pygame.draw.line(screen, black, line_start, line_end, 8)

        vertical_line_start = ((line_start[0] + line_end[0]) // 2, text_rect.bottom + 20)
        vertical_line_end = ((line_start[0] + line_end[0]) // 2, retry_button['rect'].top+60)
        pygame.draw.line(screen, black, vertical_line_start, vertical_line_end, 8)  

        screen.blit(game_over_text, text_rect)
        stop_song()

        
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
            if game_state in ["game_over", "win"]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if retry_button['rect'].collidepoint(mouse_pos):
                        comb = 0
                        player_hp = 10
                        score = 0
                        game_state = "playing"

                        for button in button_data:
                            button["color"] = black
                            button["pressed"] = False
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
            if not note_data and player_hp > 0:  # 모든 노트가 사라지고 체력이 0 이상인 경우
                game_state = "win"
            
            if player_hp <= 0:
                game_state = "game_over"

            if pygame.mixer.music.get_busy() == 0:
                song_thread = threading.Thread(target=play_song_thread)
                song_thread.start()

            screen.blit(hp_label_text, hp_label_rect.topleft)
            move_notes()
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
                                    score += 10
                                    comb += 1
                                    if comb % 10 == 0 and comb != 0:
                                        score += 5
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

            pygame.draw.rect(screen, white, (score_box_x, score_box_y, score_box_width, score_box_height))
            pygame.draw.rect(screen, black, (score_box_x, score_box_y, score_box_width, score_box_height), 8)
            score_label_font = pygame.font.Font(path, 30)
            score_label_text = score_label_font.render("Score", True, black)
            score_label_rect = score_label_text.get_rect(midbottom=(score_box_x+45, score_box_y))
            screen.blit(score_label_text, score_label_rect)
            score_font = pygame.font.Font(path, 50)
            score_text = score_font.render(f"{score}", True, black)
            score_rect = score_text.get_rect(midright=(score_box_x + score_box_width - 20, score_box_y + (score_box_height // 2)))
            screen.blit(score_text, score_rect)

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
            draw_game_over_screen()
            pygame.display.flip()

        elif game_state == "win":
            draw_win_screen()
            pygame.display.flip()
            
            
    pygame.quit()

if __name__ == "__main__":
    run_game()
