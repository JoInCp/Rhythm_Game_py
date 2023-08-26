import pygame
import sys
import socket
import threading

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)

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
is_solo_background_shown = False
is_multi_button_pressed = False
is_multi_background_shown = False
is_create_button_pressed = False
is_ok_button_pressed = False
is_no_button_pressed = False
is_join_button_visible = True
is_create_button_visible = False

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

server_data = "" 
room_name = ''

music_data = [
    {"number": 0, "title": "테스트1", "music_detail": "테스트 1과 관련된 내용", "music_list": "test1"},
    {"number": 1, "title": "테스트2", "music_detail": "테스트 2과 관련된 내용", "music_list": "test2"},
    {"number": 2, "title": "테스트3", "music_detail": "테스트 3과 관련된 내용", "music_list": "test3"},
    {"number": 3, "title": "테스트4", "music_detail": "테스트 4과 관련된 내용", "music_list": "test4"},
    {"number": 4, "title": "테스트5", "music_detail": "테스트 5과 관련된 내용", "music_list": "test5"},
    {"number": 5, "title": "테스트6", "music_detail": "테스트 6과 관련된 내용", "music_list": "test6"},
    {"number": 6, "title": "테스트7", "music_detail": "테스트 7과 관련된 내용", "music_list": "test7"},
    {"number": 7, "title": "테스트8", "music_detail": "테스트 8과 관련된 내용", "music_list": "test8"},
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

current_index = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_thread_running = False 
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and  is_solo_button_pressed:  
                current_index += 1
                if current_index > 7: 
                    current_index = 0

            elif event.button == 5 and  is_solo_button_pressed: 
                current_index -= 1
                if current_index < 0: 
                    current_index = 7

            if solo_button_rect.collidepoint(event.pos):
                is_solo_button_pressed = True
                is_solo_background_shown = True
                is_multi_button_pressed = False
                is_multi_background_shown = False
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True

            if multi_button_rect.collidepoint(event.pos):
                is_multi_button_pressed = True
                is_multi_background_shown = True
                is_solo_button_pressed = False
                is_solo_background_shown = False
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True

            if close_button_rect.collidepoint(event.pos) and is_multi_background_shown:
                is_multi_background_shown = False 
            
            if create_button_rect.collidepoint(event.pos):
                is_create_button_pressed = True

            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
            
            if no_button_rect.collidepoint(event.pos):
                is_create_button_pressed = False
            
            if ok_button_rect.collidepoint(event.pos):
                is_ok_button_pressed = True
                is_create_button_pressed = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_solo_button_pressed = False
            is_multi_button_pressed = False
            is_sound_played = False 
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_ok_button_pressed = True

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


    if is_multi_background_shown and not is_create_button_pressed:
        is_multi_background_shown = True
        is_create_button_pressed = False

    screen.fill(white)

    screen.blit(image, image_rect)
    draw_button("솔로 플레이", solo_button_rect.x, solo_button_rect.y, main_menu_button_width, main_menu_button_height, is_solo_button_pressed)
    draw_button("멀티 플레이", multi_button_rect.x, multi_button_rect.y, main_menu_button_width, main_menu_button_height, is_multi_button_pressed)

    if is_solo_background_shown:
        solo_play_menu()

    if is_multi_background_shown:
        draw_multi_background()
        create_buttons()
        close_button()

    if is_create_button_pressed:
        label_font = pygame.font.Font(path, 50)
        label_text = label_font.render("방 이름", True, black)
        label_rect = label_text.get_rect(right=input_box.left - 10, centery=input_box.centery)
        create_multi_menu()
        screen.blit(label_text, label_rect)
        multi_input_box()
        reate_multi_menu_buttons()

    if is_ok_button_pressed:
        loading_screen()

    pygame.display.update()