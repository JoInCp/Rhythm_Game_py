import pygame
import sys
import socket
import threading

pygame.init()

HOST = '127.0.0.1'
PORT = 2001

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)

small_background_color = white
small_background_size = (800, 600) 

list_background_color = white
list_background_size = (770, 400)

create_multi_menu_color = white  
create_multi_menu_size = (800, 600)     

loading_screen_color = white
loading_screen_size = (900, 700)

image_path = "images//main.jpg"  
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.center = (screen_width // 2.5, screen_height // 2)

path = "KBO Dia Gothic_medium.ttf"

button_width = 230
button_height = 90
button_bg_color = white
button_border_color = black
button_font_size = 40
button_font = pygame.font.Font(path, button_font_size)

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
is_small_background_shown = False
is_create_button_pressed = False
is_ok_button_pressed = False
is_no_button_pressed = False
check = True

server_thread_running = True

close_button_size = 25

input_box = pygame.Rect(370, 220, 140, 70)
color_inactive = pygame.Color(black)
color_active = pygame.Color(black)
color = color_inactive
active = False
text = ''
font_input = pygame.font.Font(path, 45)
txt_surface = font_input.render(text, True, color)

close_button_rect = pygame.Rect((screen_width + small_background_size[0]) // 2 - close_button_size - 10,
                                (screen_height - small_background_size[1]) // 2 + 10,
                                close_button_size, close_button_size)

list_background_rect = pygame.Rect((screen_width - list_background_size[0]) // 2,
                                        (screen_height - list_background_size[1]) // 2 + 20,
                                        list_background_size[0], list_background_size[1])

small_background_rect = pygame.Rect((screen_width - small_background_size[0]) // 2,
                                        (screen_height - small_background_size[1]) // 2,
                                        small_background_size[0], small_background_size[1])

create_multi_menu_rect = pygame.Rect((screen_width - create_multi_menu_size[0]) // 2,
                                    (screen_height - create_multi_menu_size[1]) // 2,
                                    create_multi_menu_size[0], create_multi_menu_size[1])

loading_screen_rect = pygame.Rect((screen_width - loading_screen_size[0]) // 2,
                                        (screen_height - loading_screen_size[1]) // 2,
                                        loading_screen_size[0], loading_screen_size[1])

solo_button_rect = pygame.Rect(screen_width - button_width - 60, 300, button_width, button_height)
multi_button_rect = pygame.Rect(screen_width - button_width - 60, 420, button_width, button_height)

join_button_rect = pygame.Rect(list_background_rect.left + 50, list_background_rect.bottom + 9, 180, 60)
create_button_rect = pygame.Rect(list_background_rect.right - 230, list_background_rect.bottom + 9, 180, 60)

ok_button_rect = pygame.Rect(create_multi_menu_rect.left + 200, create_multi_menu_rect.bottom-160, 180, 60)
no_button_rect = pygame.Rect(create_multi_menu_rect.right - 380, create_multi_menu_rect.bottom-160, 180, 60)

server_data = "" 
room_name = ''

def draw_button(text, x, y, width, height, is_pressed):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_bg_color, button_rect)

    if is_pressed:
        button_rect.inflate_ip(10, 10)
        pygame.draw.rect(screen, black, button_rect, 8)
        button_text = button_font.render(text, True, black)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
    else:
        pygame.draw.rect(screen, button_border_color, button_rect, 4)
        button_text = button_font.render(text, True, black)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

def create_buttons():
    draw_button("참가하기", join_button_rect.x, join_button_rect.y, join_button_rect.width, join_button_rect.height, False)
    draw_button("방 만들기", create_button_rect.x, create_button_rect.y, create_button_rect.width, create_button_rect.height, is_create_button_pressed)

def reate_multi_menu_buttons():
    draw_button("확인", ok_button_rect.x, ok_button_rect.y, ok_button_rect.width, ok_button_rect.height, is_ok_button_pressed)
    draw_button("닫기", no_button_rect.x, no_button_rect.y, no_button_rect.width, no_button_rect.height, is_no_button_pressed)


def create_multi_menu():
    pygame.draw.rect(screen, create_multi_menu_color, create_multi_menu_rect)
    pygame.draw.rect(screen, black, create_multi_menu_rect, 4)

    pygame.draw.rect(screen, create_multi_menu_color, create_multi_menu_rect)
    pygame.draw.rect(screen, black, create_multi_menu_rect, 4)

def draw_small_background():
    global server_data
    pygame.draw.rect(screen, small_background_color, small_background_rect)
    pygame.draw.rect(screen, black, small_background_rect, 4)

    pygame.draw.rect(screen, list_background_color, list_background_rect)
    pygame.draw.rect(screen, black, list_background_rect, 4)

    font_small = pygame.font.Font(path, 50)
    text = font_small.render("방 목록", True, black)
    text_rect = text.get_rect(center=(small_background_rect.centerx, small_background_rect.top + 60))
    screen.blit(text, text_rect)

    server_data_text = font_small.render(server_data, True, black)
    server_data_rect = server_data_text.get_rect(center=(small_background_rect.centerx, text_rect.bottom + 40))
    screen.blit(server_data_text, server_data_rect)

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
    
room_list = []

def server():
    global room_name, server_thread_running, room_list
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1)
        print("서버 시작")
        while server_thread_running:
            conn, addr = s.accept()
            print(f"클라이언트 {addr}")
            with conn:
                # 방 이름 저장
                if room_name not in room_list:
                    room_list.append(room_name)
                
                # 클라이언트에게 방 목록 전송
                rooms_string = "\n".join(room_list)
                conn.sendall(rooms_string.encode())

def client():
    global server_data
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("서버와 연결이 되었습니다.")
            data = s.recv(1024)
            # 서버로부터 받은 방 목록을 server_data에 저장
            server_data = data.decode()
            print(f"받는 방 목록: \n{server_data}")
    except socket.error as e:
        print(f"서버에 연결할 수 없습니다: {e}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_thread_running = False 
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if solo_button_rect.collidepoint(event.pos):
                is_solo_button_pressed = True
                check = False
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True

            if multi_button_rect.collidepoint(event.pos):
                is_multi_button_pressed = True
                is_small_background_shown = True
                if not is_sound_played:
                    click_sound.play()
                    is_sound_played = True

            if close_button_rect.collidepoint(event.pos) and is_small_background_shown:
                is_small_background_shown = False 
                check = True
            
            if create_button_rect.collidepoint(event.pos):
                is_create_button_pressed = True
                check = True
                server_thread = threading.Thread(target=server)
                server_thread.start()

            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
            
            if no_button_rect.collidepoint(event.pos):
                is_create_button_pressed = False
                check = True
            
            if ok_button_rect.collidepoint(event.pos):
                is_ok_button_pressed = True
                is_create_button_pressed = False
                room_name = text 
                text = ''

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_solo_button_pressed = False
            is_multi_button_pressed = False
            is_sound_played = False 
        
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    room_name = text 
                    text = ''
                    is_ok_button_pressed = True

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    txt_surface = font_input.render(text, True, black)  
                else:
                    text += event.unicode
                    txt_surface = font_input.render(text, True, black)


    if is_small_background_shown and not is_create_button_pressed:
        is_small_background_shown = True
        is_create_button_pressed = False
        client_thread = threading.Thread(target=client)
        client_thread.start()

    if is_ok_button_pressed:
        is_ok_button_pressed = False
        client_thread = threading.Thread(target=client)
        client_thread.start()

    # 이후에 화면 그리기
    screen.fill(white)

    screen.blit(image, image_rect)
    draw_button("솔로 플레이", solo_button_rect.x, solo_button_rect.y, button_width, button_height, is_solo_button_pressed)
    draw_button("멀티 플레이", multi_button_rect.x, multi_button_rect.y, button_width, button_height, is_multi_button_pressed)

    if is_small_background_shown:
        draw_small_background()
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
        draw_small_background()

    pygame.display.update()