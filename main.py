import pygame
import sys
import socket
import threading
import copy
import time
from enum import Enum, auto

pygame.init()

class GameState(Enum):
    MAIN_MENU = auto()
    SOLO_PLAY = auto()
    MULTI_PLAY = auto()
    LOADING = auto()
    CREATE = auto()
    GAME_WIN = auto()
    GAME_OVER = auto()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

multi_background_color = white
multi_background_size = (800, 600) 

list_background_color = white
list_background_size = (770, 400)

create_multi_menu_color = white  
create_multi_menu_size = (800, 600)     

loading_screen_color = white
loading_screen_size = (1000, 800)

solo_play_menu_color = white
solo_play_menu_size = (1000, 800)

solo_play_muisc_menu_color = white
solo_play_muisc_menu_size = (400, 800)

music_choice_color = white
music_choice_size = (240, 100)

image_path = "images//main.jpg"  
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.center = (screen_width // 2.5, screen_height // 2)

path = "KBO Dia Gothic_medium.ttf"

main_menu_button_width = 250
main_menu_button_height = 100
button_bg_color = white
button_border_color = black
main_menu_button_font_size = 46
button_font = pygame.font.Font(path, main_menu_button_font_size)

music_path = "sounds//background_music.mp3"  
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.1)  
pygame.mixer.music.play(-1)

is_sound_played = False
click_sound_path = "sounds//switch.mp3"  
click_sound = pygame.mixer.Sound(click_sound_path)
click_sound.set_volume(0.2)

is_solo_button_pressed = False
is_multi_button_pressed = False
is_create_button_pressed = False
is_ok_button_pressed = False
is_no_button_pressed = False
current_game_state = GameState.MAIN_MENU

close_button_size = 25

input_box = pygame.Rect(370, 220, 140, 70)
color_inactive = pygame.Color(black)
color_active = pygame.Color(black)
color = color_inactive
active = False
text = ''
font_input = pygame.font.Font(path, 45)
txt_surface = font_input.render(text, True, color)

close_button_rect = pygame.Rect((screen_width + multi_background_size[0]) // 2 - close_button_size - 10,
                                (screen_height - multi_background_size[1]) // 2 + 10,
                                close_button_size, close_button_size)

list_background_rect = pygame.Rect((screen_width - list_background_size[0]) // 2,
                                        (screen_height - list_background_size[1]) // 2 + 20,
                                        list_background_size[0], list_background_size[1])

multi_background_rect = pygame.Rect((screen_width - multi_background_size[0]) // 2,
                                        (screen_height - multi_background_size[1]) // 2,
                                        multi_background_size[0], multi_background_size[1])

create_multi_menu_rect = pygame.Rect((screen_width - create_multi_menu_size[0]) // 2,
                                    (screen_height - create_multi_menu_size[1]) // 2,
                                    create_multi_menu_size[0], create_multi_menu_size[1])

loading_screen_rect = pygame.Rect((screen_width - loading_screen_size[0]) // 2,
                                        (screen_height - loading_screen_size[1]) // 2,
                                        loading_screen_size[0], loading_screen_size[1])

solo_play_menu_rect = pygame.Rect((screen_width - solo_play_menu_size[0]) // 2,
                                        (screen_height - solo_play_menu_size[1]) // 2,
                                        solo_play_menu_size[0], solo_play_menu_size[1])

solo_play_muisc_menu_rect = pygame.Rect((screen_width - solo_play_menu_size[0]) // 2+600,
                                        (screen_height - solo_play_menu_size[1]) // 2,
                                        solo_play_muisc_menu_size[0], solo_play_muisc_menu_size[1])

solo_button_rect = pygame.Rect(screen_width - main_menu_button_width - 90, 340, main_menu_button_width, main_menu_button_height)
multi_button_rect = pygame.Rect(screen_width - main_menu_button_width - 90, 490, main_menu_button_width, main_menu_button_height)

join_button_rect = pygame.Rect(list_background_rect.left + 50, list_background_rect.bottom + 9, 180, 60)
create_button_rect = pygame.Rect(list_background_rect.right - 230, list_background_rect.bottom + 9, 180, 60)

ok_button_rect = pygame.Rect(create_multi_menu_rect.left + 200, create_multi_menu_rect.bottom-160, 180, 60)
no_button_rect = pygame.Rect(create_multi_menu_rect.right - 380, create_multi_menu_rect.bottom-160, 180, 60)

start_button_rect = pygame.Rect(solo_play_menu_rect.left + 15, solo_play_menu_rect.centery - main_menu_button_height//2, main_menu_button_width, main_menu_button_height)

server_data = "" 
room_name = ''
player_hp = 10
original_note_data = []

music_data = [
    {"number": 0, "title": "테스트1", "music_detail": "테스트 1과 관련된 내용", "music_list": "test1_note_data", "sound_file": "sounds//test.mp3"},
    {"number": 1, "title": "테스트2", "music_detail": "테스트 2과 관련된 내용", "music_list": "test2_note_data", "sound_file": "sounds//test.mp3"},
    {"number": 2, "title": "테스트3", "music_detail": "테스트 3과 관련된 내용", "music_list": "test3", "sound_file": "NONE"},
    {"number": 3, "title": "테스트4", "music_detail": "테스트 4과 관련된 내용", "music_list": "test4", "sound_file": "NONE"},
    {"number": 4, "title": "테스트5", "music_detail": "테스트 5과 관련된 내용", "music_list": "test5", "sound_file": "NONE"},
    {"number": 5, "title": "테스트6", "music_detail": "테스트 6과 관련된 내용", "music_list": "test6", "sound_file": "NONE"},
    {"number": 6, "title": "테스트7", "music_detail": "테스트 7과 관련된 내용", "music_list": "test7", "sound_file": "NONE"},
    {"number": 7, "title": "테스트8", "music_detail": "테스트 8과 관련된 내용", "music_list": "test8", "sound_file": "NONE"},
]

test1_note_data = [
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

test2_note_data = [
        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 1, "color": "black", "lane": 3, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 2, "color": "black", "lane": 2, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 3, "color": "black", "lane": 3, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 4, "color": "black", "lane": 3, "note_start_delays": 3200, "note_speed": 1/10},
        {"number": 5, "color": "black", "lane": 1, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 6, "color": "black", "lane": 2, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 7, "color": "black", "lane": 3, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 8, "color": "black", "lane": 1, "note_start_delays": 5200, "note_speed": 1/10},
        {"number": 9, "color": "black", "lane": 2, "note_start_delays": 6200, "note_speed": 1/10},
        {"number": 10, "color": "black", "lane": 3, "note_start_delays": 6200, "note_speed": 1/10}
]

def draw_button(text, x, y, width, height, is_pressed):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_bg_color, button_rect)
    pygame.draw.rect(screen, button_border_color, button_rect, 8)
    button_text = button_font.render(text, True, black)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

def draw_button2(text, x, y, width, height, is_pressed):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_bg_color, button_rect)
    pygame.draw.rect(screen, button_border_color, button_rect, 4)
    button_text = button_font.render(text, True, black)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

def create_buttons():
    draw_button2("참가하기", join_button_rect.x, join_button_rect.y, join_button_rect.width, join_button_rect.height, False)
    draw_button2("방 만들기", create_button_rect.x, create_button_rect.y, create_button_rect.width, create_button_rect.height, is_create_button_pressed)

def reate_multi_menu_buttons():
    draw_button("확인", ok_button_rect.x, ok_button_rect.y, ok_button_rect.width, ok_button_rect.height, is_ok_button_pressed)
    draw_button("닫기", no_button_rect.x, no_button_rect.y, no_button_rect.width, no_button_rect.height, is_no_button_pressed)


def create_multi_menu():
    pygame.draw.rect(screen, create_multi_menu_color, create_multi_menu_rect)
    pygame.draw.rect(screen, black, create_multi_menu_rect, 4)

    pygame.draw.rect(screen, create_multi_menu_color, create_multi_menu_rect)
    pygame.draw.rect(screen, black, create_multi_menu_rect, 4)

def draw_multi_background():
    global server_data
    pygame.draw.rect(screen, multi_background_color, multi_background_rect)
    pygame.draw.rect(screen, black, multi_background_rect, 4)

    pygame.draw.rect(screen, list_background_color, list_background_rect)
    pygame.draw.rect(screen, black, list_background_rect, 4)

    font_small = pygame.font.Font(path, 50)
    text = font_small.render("방 목록", True, black)
    text_rect = text.get_rect(center=(multi_background_rect.centerx, multi_background_rect.top + 60))
    screen.blit(text, text_rect)

def close_button():
    pygame.draw.line(screen, black, close_button_rect.topleft, close_button_rect.bottomright, 6)
    pygame.draw.line(screen, black, close_button_rect.bottomleft, close_button_rect.topright, 6)

def multi_input_box():
    width = max(250, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+8, input_box.y+10))
    pygame.draw.rect(screen, color, input_box, 4)

def loading_screen():
    pygame.draw.rect(screen, loading_screen_color, loading_screen_rect)

    font = pygame.font.Font(path, 40)
    text_surface = font.render("상대방을 기다리는 중", True, black)
    text_rect = text_surface.get_rect(center=loading_screen_rect.center)
    screen.blit(text_surface, text_rect)
    
def blit_text_centered(surface, text_surface, rect):
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def solo_play_menu():
    pygame.draw.rect(screen, solo_play_menu_color, solo_play_menu_rect)
    font = pygame.font.Font(path, 50)  
    text_surface = font.render("START", True, black)  
    text_rect = text_surface.get_rect()
    text_rect.midleft = (solo_play_menu_rect.left + 15, solo_play_menu_rect.centery)  
    
    circle_offset = -50 
    circle_center = (text_rect.centerx + circle_offset, text_rect.centery)

    radius1 = 210
    pygame.draw.circle(screen, white, circle_center, radius1) 
    pygame.draw.circle(screen, black, circle_center, radius1, 4) 

    radius2 = 190
    pygame.draw.circle(screen, white, circle_center, radius2) 
    pygame.draw.circle(screen, black, circle_center, radius2, 4) 

    info_font = pygame.font.Font(path, 35)
    rect_width = 230
    rect_height = 90
    rect_thickness = 5
    
    rect_top = pygame.Rect(text_rect.centerx - rect_width/2 + 30, text_rect.centery - radius1 - rect_height-20, rect_width, rect_height)
    
    rect_middle1 = pygame.Rect(text_rect.centerx - rect_width/2 + 280, text_rect.centery - 200, rect_width, rect_height)
    
    rect_right = pygame.Rect(text_rect.centerx + radius1, text_rect.centery - rect_height/2, rect_width, rect_height)
    
    rect_middle2 = pygame.Rect(text_rect.centerx - rect_width/2 + 280, text_rect.centery + 110, rect_width, rect_height)
    
    rect_bottom = pygame.Rect(text_rect.centerx - rect_width/2 + 30, text_rect.centery + radius1+20, rect_width, rect_height)
    
    pygame.draw.rect(screen, solo_play_muisc_menu_color, solo_play_muisc_menu_rect)
    pygame.draw.rect(screen, black, solo_play_muisc_menu_rect, 4)

    padding = 15
    right_box_rect = pygame.Rect(rect_right.left - padding, rect_right.top - padding, 
                                rect_right.width + 2*padding, rect_right.height + 2*padding)
    
    pygame.draw.rect(screen, white, right_box_rect)
    pygame.draw.rect(screen, black, right_box_rect, 8) 

    pygame.draw.rect(screen, white, rect_top)
    pygame.draw.rect(screen, black, rect_top, rect_thickness)

    pygame.draw.rect(screen, white, rect_middle1)
    pygame.draw.rect(screen, black, rect_middle1, rect_thickness)

    pygame.draw.rect(screen, white, rect_right)
    pygame.draw.rect(screen, black, rect_right, rect_thickness)

    pygame.draw.rect(screen, white, rect_middle2)
    pygame.draw.rect(screen, black, rect_middle2, rect_thickness)

    pygame.draw.rect(screen, white, rect_bottom)
    pygame.draw.rect(screen, black, rect_bottom, rect_thickness)

    top_info_surface = info_font.render(music_data[(current_index ) % len(music_data)]["title"], True, black)
    middle1_info_surface = info_font.render(music_data[(current_index + 1) % len(music_data)]["title"], True, black)
    right_info_surface = info_font.render(music_data[(current_index + 2) % len(music_data)]["title"], True, black)
    middle2_info_surface = info_font.render(music_data[(current_index + 3) % len(music_data)]["title"], True, black)
    bottom_info_surface = info_font.render(music_data[(current_index + 4) % len(music_data)]["title"], True, black)

    blit_text_centered(screen, top_info_surface, rect_top)
    blit_text_centered(screen, middle1_info_surface, rect_middle1)
    blit_text_centered(screen, right_info_surface, rect_right)
    blit_text_centered(screen, middle2_info_surface, rect_middle2)
    blit_text_centered(screen, bottom_info_surface, rect_bottom)

    music_detail_font = pygame.font.Font(path, 25)
    music_detail_surface = music_detail_font.render(music_data[(current_index + 2) % len(music_data)]["music_detail"], True, black)
    blit_text_centered(screen, music_detail_surface, solo_play_muisc_menu_rect)
    screen.blit(text_surface, text_rect)

def run_game():
    pygame.init()
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("test game")
    song_file_path = "sounds//test.mp3"


    global current_game_state

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    button_font_size = 50
    button_font = pygame.font.Font(path, button_font_size)
    hp_label_font = pygame.font.Font(None, 40)
    hp_label_text = hp_label_font.render("MY.HP", True, black)
    hp_label_rect = hp_label_text.get_rect(right=screen_width-240, top=180)
    comb_font = pygame.font.Font(path, 40)
    comb_number_font_size = 80
    comb_number_font = pygame.font.Font(path, comb_number_font_size)

    score = 0
    comb = 0
    max_comb = 0
    game_state = "playing"
    running = True
    global player_hp 

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

    button_data = [
        {"x": button_x_centers[0] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_s},
        {"x": button_x_centers[1] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_d},
        {"x": button_x_centers[2] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": semicolon_key},
        {"x": button_x_centers[3] - 45, "y": button_y_center - 65, "width": 90, "height": 130, "color": black, "pressed": False, "key": pygame.K_QUOTE}
    ]

    initial_position_outside_screen = -5 
    for note in original_note_data:
        note["start_time"] = pygame.time.get_ticks() + note["note_start_delays"]
        note["number"] = initial_position_outside_screen

    retry_button_rect = pygame.Rect(screen_width-22, screen_height // 2 + 50, 200, 50)
    menu_button_rect = pygame.Rect(screen_width - 250, screen_height // 2 + 150, 200, 50)


    button_spacing = 60
    half_spacing = button_spacing / 2

    total_buttons_width = retry_button_rect.width + menu_button_rect.width + button_spacing
    retry_button_rect.topleft = ((screen_width - total_buttons_width) // 2, screen_height // 2 + 50)
    menu_button_rect.topleft = (retry_button_rect.right + button_spacing, screen_height // 2 + 50)

    note_data = copy.deepcopy(original_note_data)
    for note in note_data:
        note["hit"] = False

    def draw_hp_bar():
        pygame.draw.rect(screen, red, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))

        for i in range(player_hp, 10):
            pygame.draw.rect(screen, white, (hp_bar_x + i * hp_segment_width, hp_bar_y, hp_segment_width, hp_bar_height))
        
        pygame.draw.rect(screen, black, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 8) 
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
        global comb, y_position, bottom_of_screen, player_hp 
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
        font_retry = pygame.font.Font(path, 50)
        pygame.draw.rect(screen, white, retry_button_rect)
        text = font_retry.render("다시 하기", True, black)
        text_rect = text.get_rect(center=retry_button_rect.center)
        screen.blit(text, text_rect)

    def draw_menu_button():
        font_menu = pygame.font.Font(path, 50)
        pygame.draw.rect(screen, white, menu_button_rect)
        text = font_menu.render('메뉴 가기', True, black)
        text_rect = text.get_rect(center=menu_button_rect.center)
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
        comb_text = comb_font.render(f"Max Combo: {max_comb}", True, black)
        comb_rect = comb_text.get_rect(center=(screen_width // 2, score_rect.bottom + 50))

        draw_retry_button()
        draw_menu_button()

        line_start = (score_rect.left-90, score_rect.bottom + 90)
        line_end = (score_rect.right+90, score_rect.bottom + 90)
        pygame.draw.line(screen, black, line_start, line_end, 8)

        vertical_line_start_x = (retry_button_rect.right + menu_button_rect.left) // 2
        vertical_line_start = (vertical_line_start_x, score_rect.bottom + 90)   
        vertical_line_end = (vertical_line_start_x, retry_button_rect.top + 50)
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
        vertical_line_end = ((line_start[0] + line_end[0]) // 2, retry_button_rect.top + 60)
        pygame.draw.line(screen, black, vertical_line_start, vertical_line_end, 8)


        screen.blit(game_over_text, text_rect)
        stop_song()
        
    while running:
        screen.fill(white) 
        draw_hp_bar()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

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
                    if retry_button_rect.collidepoint(mouse_pos):
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
                    if menu_button_rect.collidepoint(event.pos):
                        running = False
                        current_game_state = GameState.SOLO_PLAY

            elif event.type == pygame.KEYUP:
                for button in button_data:
                    if event.key == button["key"]:
                        button["color"] = black
        
        if game_state == "playing":
            if not note_data and player_hp > 0: 
                game_state = "win"
            
            elif player_hp <=0:
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
                                    if comb > max_comb:
                                        max_comb = comb
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

        elif game_state == "game_over":
            draw_game_over_screen()
            pygame.display.flip()

        elif game_state == "win":
            draw_win_screen()
            pygame.display.flip()
        

current_index = 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_thread_running = False 
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  
                current_index += 1
                if current_index > 7: 
                    current_index = 0

            elif event.button == 5: 
                current_index -= 1
                if current_index < 0: 
                    current_index = 7

            if current_game_state == GameState.MAIN_MENU:
                if solo_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.SOLO_PLAY
                    if not is_sound_played:
                        click_sound.play()
                        is_sound_played = True

                elif multi_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.MULTI_PLAY
                    if not is_sound_played:
                        click_sound.play()
                        is_sound_played = True
                
            elif current_game_state == GameState.MULTI_PLAY:
                if create_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.CREATE

                if close_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.MAIN_MENU
                    continue  

                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            
            elif current_game_state == GameState.CREATE:
                if no_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.MULTI_PLAY

                if ok_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.LOADING


        if event.type == pygame.MOUSEBUTTONDOWN and current_game_state == GameState.SOLO_PLAY:
            if start_button_rect.collidepoint(event.pos):
                music_list_value = music_data[(current_index + 2) % len(music_data)]["music_list"]
                song_file_path = music_data[(current_index + 2) % len(music_data)]["sound_file"]

                if music_list_value == "test1_note_data":
                    original_note_data = test1_note_data.copy()
                elif music_list_value == "test2_note_data":
                    original_note_data = test2_note_data.copy()

                if len(original_note_data) == 0:
                    pass
                elif len(original_note_data) != 0:
                    run_game()
            
        if event.type == pygame.KEYDOWN:
                if current_game_state == GameState.CREATE:
                    if event.key == pygame.K_RETURN:
                        current_game_state = GameState.LOADING

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        txt_surface = font_input.render(text, True, black)  
                    else:
                        text += event.unicode
                        txt_surface = font_input.render(text, True, black)
            
                if event.key == pygame.K_UP:
                    current_index += 1
                    if current_index > 7: 
                        current_index = 0

                elif event.key == pygame.K_DOWN:
                    current_index -= 1
                    if current_index < 0: 
                        current_index = 7

    screen.fill(white)

    screen.blit(image, image_rect)
    draw_button("솔로 플레이", solo_button_rect.x, solo_button_rect.y, main_menu_button_width, main_menu_button_height, is_solo_button_pressed)
    draw_button("멀티 플레이", multi_button_rect.x, multi_button_rect.y, main_menu_button_width, main_menu_button_height, is_multi_button_pressed)

    if current_game_state == GameState.MAIN_MENU:
        pass

    elif current_game_state == GameState.SOLO_PLAY:
        solo_play_menu()

    elif current_game_state == GameState.MULTI_PLAY:
        draw_multi_background()
        create_buttons()
        close_button()

    elif current_game_state == GameState.CREATE:
        label_font = pygame.font.Font(path, 50)
        label_text = label_font.render("방 이름", True, black)
        label_rect = label_text.get_rect(right=input_box.left - 10, centery=input_box.centery)
        create_multi_menu()
        screen.blit(label_text, label_rect)
        multi_input_box()
        reate_multi_menu_buttons()

    elif current_game_state == GameState.LOADING:
        loading_screen()

    pygame.display.update()