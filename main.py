import pygame
import sys
import json
import threading
import copy
import time
from enum import Enum, auto


#========== 초기 설정 ==========
pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


#========== 게임 상태 ==========
class GameState(Enum):
    MAIN_MENU = auto()
    SOLO_PLAY = auto()
    MULTI_PLAY = auto()
    LOADING = auto()
    CREATE = auto()
    SIGNUP = auto()
    LOGIN = auto()
    LOGIN_SIGNUP = auto()
    ESC = auto()
    MAIN_MENU_ESC = auto()

current_game_state = GameState.MAIN_MENU

#========== 메인 화면 이미지 ==========
image_path = "images//main.jpg"
image = pygame.image.load(image_path)
image_rect = image.get_rect(center=(screen_width // 2.5, screen_height // 2))


#========== 배경 음악 ==========
main_menu_music_path = "sounds//background_music.mp3"
pygame.mixer.music.load(main_menu_music_path)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


#========== 클릭 사운드 ==========
click_sound_path = "sounds//switch.mp3"
click_sound = pygame.mixer.Sound(click_sound_path)
click_sound.set_volume(0.2)


#========== 폰트 및 색상 설정 ==========
font_path = "font//KBO Dia Gothic_medium.ttf"
font_path2 = "font//MBC 1961 M.ttf"
data_file = "users.json"

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


#========== 화면 사이즈 및 색 ==========
solo_play_menu_color = white
solo_play_menu_size = (1000, 800)

solo_play_muisc_menu_color = white
solo_play_muisc_menu_size = (400, 800)

music_choice_color = white
music_choice_size = (240, 100)

login_signup_menu_color = white
login_signup_menu_size = (800, 600)

esc_menu_color = white
esc_menu_size = (1000, 800)

main_menu_button_width = 250
main_menu_button_height = 100
button_bg_color = white
button_border_color = black
main_menu_button_font_size = 46

button_font = pygame.font.Font(font_path, main_menu_button_font_size)

login_signup_menu_center_x = screen_width // 2
login_signup_menu_center_y = screen_height // 2

current_index = 0
close_button_size = 25

player_hp = 10
combo = 0


#========== 로그인 & 회원가입 ==========
total_width = 2 * 120 + 20
start_x = login_signup_menu_center_x - total_width // 2
signup_close_button_center_x = screen_width // 2 + 120 // 2 + 20 // 2
signup_close_button_center_y = screen_height // 2 + 130 - 30 // 2
signup_confirm_button_center_x = signup_close_button_center_x - 120 - 20 

login_close_button_center_x = screen_width // 2 + 120 // 2 + 20 // 2
login_close_button_center_y = screen_height // 2 + 90 - 30 // 2
login_confirm_button_center_x = login_close_button_center_x - 120 - 20 


#========== 체크 ==========
is_sound_played = False
is_solo_button_pressed = False
game_over_button_pressed = False
menu_button_pressed = False
password_mismatch_warning = False
user_exists_warning = False
login_successful = False
login_failure_warning = False
signup_invalid_input_warning = False
login_invalid_input_warning = False
prev_game_state = None 
logged_in_user = None
hit_result = None

current_game_state = GameState.MAIN_MENU

hit_result_start_time = 0

#========== 노래 정보 ==========
# {"number": 노래 번호, "title": "노래 제목", "music_start_time": 노래 시작 시간, "music_sound": 소리 크기, "music_list": "노트 데이터", "sound_file": "노래 파일", "music_detail": "노래 설명"},
    
music_data = [
    {"number": 0, "title": "테스트1", "music_start_time": 1.1, "music_sound": 0.3, "music_list": "test1_note_data", "sound_file": "sounds//test.mp3", "music_detail": "테스트 1과 관련된 내용"},

    {"number": 1, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 2, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 3, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 4, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 5, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 6, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},

    {"number": 7, "title": "준비 중", "music_start_time": 0, "music_sound": 0, "music_list": "NONE", "sound_file": "NONE", "music_detail": "준비 중"},
]

original_note_data = []

music_result = {} 


#========== 위치 ==========
close_button_rect = pygame.Rect((screen_width + login_signup_menu_size[0]) // 2 - close_button_size - 10,
                                (screen_height -login_signup_menu_size[1]) // 2 + 10,
                                close_button_size, close_button_size)

esc_menu_rect = pygame.Rect((screen_width - esc_menu_size[0]) // 2,
                                        (screen_height - esc_menu_size[1]) // 2,
                                        esc_menu_size[0], esc_menu_size[1])

solo_play_menu_rect = pygame.Rect((screen_width - solo_play_menu_size[0]) // 2,
                                        (screen_height - solo_play_menu_size[1]) // 2,
                                        solo_play_menu_size[0], solo_play_menu_size[1])

solo_play_muisc_menu_rect = pygame.Rect((screen_width - solo_play_menu_size[0]) // 2+600,
                                        (screen_height - solo_play_menu_size[1]) // 2,
                                        solo_play_muisc_menu_size[0], solo_play_muisc_menu_size[1])

login_signup_menu_rect = pygame.Rect((screen_width - login_signup_menu_size[0]) // 2,
                                    (screen_height - login_signup_menu_size[1]) // 2,
                                    login_signup_menu_size[0], login_signup_menu_size[1])


solo_button_rect = pygame.Rect(screen_width - main_menu_button_width - 90, 400, main_menu_button_width, main_menu_button_height)

start_button_rect = pygame.Rect(solo_play_menu_rect.left + 15, solo_play_menu_rect.centery - main_menu_button_height//2, main_menu_button_width, main_menu_button_height)

login_button_width, login_button_height = 160, 80
signup_button_width, signup_button_height = 160, 80

login_button = pygame.Rect(0, 0, login_button_width, login_button_height) 
signup_button = pygame.Rect(0, 0, signup_button_width, signup_button_height) 

button_spacing = 50
half_total_width = (login_button.width + signup_button.width + button_spacing) // 2

login_button.topleft = ((screen_width // 2) - half_total_width, login_signup_menu_center_y - 30)
signup_button.topleft = ((screen_width // 2) + button_spacing, login_signup_menu_center_y - 30)

signup_confirm_button = pygame.Rect(start_x, signup_close_button_center_y, 120, 40)
signup_close_button = pygame.Rect(start_x + 120 + 20, signup_close_button_center_y, 120, 40)

login_confirm_button = pygame.Rect(start_x, login_close_button_center_y, 120, 40)
login_close_button = pygame.Rect(start_x + 120 + 20, login_close_button_center_y, 120, 40)

menu_button_rect = pygame.Rect((screen_width - 150) // 2, (screen_height - esc_menu_size[1]) + 330, 180, 60)
exit_button_rect = pygame.Rect((screen_width - 150) // 2, (screen_height - esc_menu_size[1]) + 400, 180, 60)


def draw_button(text, x, y, width, height, is_pressed):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_bg_color, button_rect)
    pygame.draw.rect(screen, button_border_color, button_rect, 8)
    button_text = button_font.render(text, True, black)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)


#========== 메인 화면 ==========
def main_menu():
    screen.fill(white)
    screen.blit(image, image_rect)
    draw_button("START", solo_button_rect.x, solo_button_rect.y, main_menu_button_width, main_menu_button_height, is_solo_button_pressed)
   

#========== 로그인 & 회원가입 버튼 ==========
def login_signup_draw_button(screen, button_rect, text, font_path, font_size=35):
    pygame.draw.rect(screen, white, button_rect)
    pygame.draw.rect(screen, black, button_rect, 6)
    
    font = pygame.font.Font(font_path, font_size)
    rendered_text = font.render(text, True, black)
    
    text_x = button_rect.x + (button_rect.width - rendered_text.get_width()) // 2
    text_y = button_rect.y + (button_rect.height - rendered_text.get_height()) // 2
    screen.blit(rendered_text, (text_x, text_y))


#========== 로그인 & 화원가입 화면 ==========
def login_signup_menu():
    screen.fill(login_signup_menu_color)

    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)

    login_signup_draw_button(screen, signup_button, "회원가입", font_path)
    login_signup_draw_button(screen, login_button, "로그인", font_path)


#========== 로그인 & 회원가입 파일 입출력 ==========
def user_exists(username): # 중복 아이디 체크
    with open(data_file, 'r') as f:
        users = json.load(f)
        return username in users

def save_user(username, password): # 새로운 유저 데이터 저장
    try:
        with open(data_file, 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if username not in users:
        users[username] = {"password": password, "scores": {}}
    else:
        users[username]["password"] = password

    with open(data_file, 'w') as f:
        json.dump(users, f)

def verify_login(username, password): # 아이디와 비밀번호가 파일에 저장되어있는 값과 일치하는지 체크
    try:
        with open(data_file, 'r') as f:
            users = json.load(f)
            return users.get(username, {}).get("password") == password
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def save_score(username, song_title, score, max_combo): # 플레이어의 게임 기록 저장
    with open(data_file, 'r') as f:
        users = json.load(f)

    if username not in users:
        return

    if "scores" not in users[username]:
        users[username]["scores"] = {}

    current_score_data = users[username]["scores"].get(song_title, {"score": 0, "max_combo": 0})

    new_score = max(current_score_data["score"], score)
    new_combo = max(current_score_data["max_combo"], max_combo)

    users[username]["scores"][song_title] = {"score": new_score, "max_combo": new_combo}

    with open(data_file, 'w') as f:
        json.dump(users, f)


def load_score(username, song_title): # 플레이어의 저장되어있는 값을 가져오기
    with open(data_file, 'r') as f:
        users = json.load(f)

    return users.get(username, {}).get("scores", {}).get(song_title, {"score": 0, "max_combo": 0})


#========== 로그인 & 회원가입 경고 메세지 체크 ==========
def activate_warning(warning_name): 
    global warning_activation_times, signup_invalid_input_warning, login_invalid_input_warning, user_exists_warning, password_mismatch_warning, login_failure_warning
    warning_activation_times[warning_name] = pygame.time.get_ticks()
    
    if warning_name == "login_failure":
        login_failure_warning = True

    elif warning_name == "signup_invalid_input":
        signup_invalid_input_warning = True
    
    elif warning_name == "login_invalid_input":
        login_invalid_input_warning = True
    
    elif warning_name == "user_exists":
        user_exists_warning = True
    
    elif warning_name == "password_mismatch":
        password_mismatch_warning = True

def deactivate_warnings_after_delay():
    current_time = pygame.time.get_ticks()
    for warning, activation_time in warning_activation_times.items():
        if activation_time and (current_time - activation_time) >= 2000:
            if warning == "signup_invalid_input":
                global signup_invalid_input_warning
                signup_invalid_input_warning = False

            elif warning == "login_invalid_input":
                global login_invalid_input_warning
                login_invalid_input_warning = False

            elif warning == "user_exists":
                global user_exists_warning
                user_exists_warning = False

            elif warning == "password_mismatch":
                global password_mismatch_warning
                password_mismatch_warning = False

            elif warning == "login_failure":
                global login_failure_warning
                login_failure_warning = False

            warning_activation_times[warning] = None

warning_activation_times = {
    "signup_invalid_input": None,
    "login_invalid_input": None,
    "user_exists": None,
    "password_mismatch": None,
    "login_failure": None
}

#========== 로그인 & 회원가입 입력 ==========
class InputBox:
    delete_pressed = False

    def __init__(self, x, y, w, h, text='', password_mode=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = black
        self.text = text
        self.font = pygame.font.Font(font_path, 30)
        self.txt_surface = self.font.render(text, True, black)
        self.active = False
        self.password_mode = password_mode
        self.cursor_visible = True  
        self.last_cursor_switch_time = pygame.time.get_ticks()  
        self.cursor_interval = 500  
        self.backspace_interval = 50
        self.last_backspace_time = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                InputBox.delete_pressed = True
            elif event.key not in [pygame.K_RETURN, pygame.K_SPACE] and is_valid_string(event.unicode):
                self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, black)

        if self.active and InputBox.delete_pressed:  
            current_time = pygame.time.get_ticks()
            if current_time - self.last_backspace_time > self.backspace_interval:
                self.text = self.text[:-1] 
                self.txt_surface = self.font.render(self.text, True, black)
            self.last_backspace_time = current_time

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                InputBox.delete_pressed = False 

    def draw(self, screen):
        display_text = self.text if not self.password_mode else '*' * len(self.text)
        self.txt_surface = self.font.render(display_text, True, black)

        pygame.draw.rect(screen, white, self.rect.inflate(-2, -2))
        pygame.draw.rect(screen, black, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active:
            if self.cursor_visible:
                cx = self.rect.x + self.txt_surface.get_width() + 5
                cy = self.rect.y + 5
                h = self.font.get_height()
                pygame.draw.line(screen, black, (cx, cy), (cx, cy+h-2), 2)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_cursor_switch_time > self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_switch_time = current_time

    def clear_text(self):
        self.text = ''


#========== 로그인 & 회원가입 입력 텍스트 검사 ==========
def is_valid_string(s):
    return s.isalnum() # 입력된 텍스트가 영어와 숫자로만 이루어져 있는지 검사


#========== 로그인 & 회원가입 입력 칸 ==========
input_box_width = 220  
signup_user_input = InputBox((screen_width - input_box_width) // 2, login_signup_menu_center_y - 130, 220, 40)
signup_pwd_input = InputBox((screen_width - input_box_width) // 2, login_signup_menu_center_y - 50, 220, 40, password_mode=True)
signup_confirm_input = InputBox((screen_width - input_box_width) // 2, login_signup_menu_center_y + 30, 220, 40, password_mode=True)

login_user_input = InputBox((screen_width - input_box_width) // 2, login_signup_menu_center_y - 90, 220, 40)
login_pwd_input = InputBox((screen_width - input_box_width) // 2, login_signup_menu_center_y - 10, 220, 40, password_mode=True)


#========== 로그인 화면 ==========
def login():
    global login_invalid_input_warning, login_failure_warning
    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)
    label_font = pygame.font.Font(font_path, 25)
    labels = ['아이디', '비밀번호']
    for index, label in enumerate(labels):
        rendered_label = label_font.render(label, True, black)
        screen.blit(rendered_label, (login_user_input.rect.x, login_signup_menu_center_y - 120 + index * 80))

    login_user_input.draw(screen)
    login_pwd_input.draw(screen)

    if login_invalid_input_warning:
        warning_font = pygame.font.Font(font_path, 20)
        warning_msg = warning_font.render("영어와 숫자만 사용하세요.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 40))

    if login_failure_warning:
        warning_font = pygame.font.Font(font_path, 20)
        warning_msg = warning_font.render("아이디 또는 비밀번호가 잘못되었습니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 40))

    ok_font = pygame.font.Font(font_path, 25)
    pygame.draw.rect(screen, white, login_confirm_button)
    pygame.draw.rect(screen, black, login_confirm_button, 2)
    confirm_text = ok_font.render("확인", True, black)
    screen.blit(confirm_text, (login_confirm_button.x + (login_confirm_button.width - confirm_text.get_width()) // 2, login_confirm_button.y + (login_confirm_button.height - confirm_text.get_height()) // 2))

    close_font = pygame.font.Font(font_path, 25)
    pygame.draw.rect(screen, white, login_close_button)
    pygame.draw.rect(screen, black, login_close_button, 2)
    close_text = close_font.render("닫기", True, black)
    screen.blit(close_text, (login_close_button.x + (login_close_button.width - close_text.get_width()) // 2, login_close_button.y + (login_close_button.height - close_text.get_height()) // 2))


#========== 회원가입 화면 ==========
def signup():
    global user_exists_warning, password_mismatch_warning, signup_invalid_input_warning

    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)
    label_font = pygame.font.Font(font_path, 25)

    labels = ['아이디', '비밀번호', '비밀번호 확인']
    for index, label in enumerate(labels):
        rendered_label = label_font.render(label, True, black)
        screen.blit(rendered_label, (signup_user_input.rect.x, login_signup_menu_center_y - 160 + index * 80))

    signup_user_input.draw(screen)
    signup_pwd_input.draw(screen)
    signup_confirm_input.draw(screen)

    if signup_invalid_input_warning:
        warning_font = pygame.font.Font(font_path, 20)
        warning_msg = warning_font.render("영어와 숫자만 사용하세요.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 80))

    if user_exists_warning:
        warning_font = pygame.font.Font(font_path, 20)
        warning_msg = warning_font.render("이미 있는 아이디 입니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 80))

    if password_mismatch_warning:
        warning_font = pygame.font.Font(font_path, 20)
        warning_msg = warning_font.render("비밀번호가 일치하지 않습니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 80))

    ok_font = pygame.font.Font(font_path, 25)
    pygame.draw.rect(screen, white, signup_confirm_button)
    pygame.draw.rect(screen, black, signup_confirm_button, 2)
    confirm_text = ok_font.render("확인", True, black)
    screen.blit(confirm_text, (signup_confirm_button.x + (signup_confirm_button.width - confirm_text.get_width()) // 2, signup_confirm_button.y + (signup_confirm_button.height - confirm_text.get_height()) // 2))

    close_font = pygame.font.Font(font_path, 25)
    pygame.draw.rect(screen, white, signup_close_button)
    pygame.draw.rect(screen, black, signup_close_button, 2)
    close_text = close_font.render("닫기", True, black)
    screen.blit(close_text, (signup_close_button.x + (signup_close_button.width - close_text.get_width()) // 2, signup_close_button.y + (signup_close_button.height - close_text.get_height()) // 2))


#========== esc 화면 ==========
def esc_menu():
    pygame.draw.rect(screen, esc_menu_color, esc_menu_rect)
    pygame.draw.rect(screen, white, menu_button_rect)  
    pygame.draw.rect(screen, black, menu_button_rect, 4)  
    font = pygame.font.Font(font_path, 36)
    text = font.render("메뉴 가기", True, black)
    text_rect = text.get_rect(center=menu_button_rect.center)
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, white, exit_button_rect) 
    pygame.draw.rect(screen, black, exit_button_rect, 4)  
    text = font.render("게임 종료", True, black)
    text_rect = text.get_rect(center=exit_button_rect.center)
    screen.blit(text, text_rect)


#========== 메인화면에서 esc 화면 ==========
def main_menu_esc_menu():
    pygame.draw.rect(screen, esc_menu_color, esc_menu_rect)
    font = pygame.font.Font(font_path, 36)
    pygame.draw.rect(screen, white, exit_button_rect) 
    pygame.draw.rect(screen, black, exit_button_rect, 4)  
    text = font.render("게임 종료", True, black)
    text_rect = text.get_rect(center=exit_button_rect.center)
    screen.blit(text, text_rect)


#========== 접속 아이디 표시 ==========
def display_logged_in_user(screen):
    if logged_in_user:
        font = pygame.font.Font(font_path, 30)
        text_surface = font.render("접속 아이디: [ " + logged_in_user + " ]", True, white)
        screen.blit(text_surface, (10, 15))


#========== 솔로플레이 텍스트 위치 ==========
def blit_text_centered(surface, text_surface, rect):
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


#========== 솔로 플레이 화면 ==========
def solo_play_menu():
    pygame.draw.rect(screen, solo_play_menu_color, solo_play_menu_rect)
    font = pygame.font.Font(font_path2, 50)  
    text_surface = font.render("START", True, black)  
    text_rect = text_surface.get_rect()
    text_rect.midleft = (solo_play_menu_rect.left + 15, solo_play_menu_rect.centery)  
    
    circle_offset = -50 
    circle_center = (text_rect.centerx + circle_offset, text_rect.centery)

    radius1 = 210
    pygame.draw.circle(screen, white, circle_center, radius1) 
    pygame.draw.circle(screen, black, circle_center, radius1, 6) 

    radius2 = 190
    pygame.draw.circle(screen, white, circle_center, radius2) 
    pygame.draw.circle(screen, black, circle_center, radius2, 6) 

    info_font = pygame.font.Font(font_path, 35)
    rect_width = 230
    rect_height = 90
    rect_thickness = 5
    
    rect_top = pygame.Rect(text_rect.centerx - rect_width/2 + 30, text_rect.centery - radius1 - rect_height-20, rect_width, rect_height)
    
    rect_middle1 = pygame.Rect(text_rect.centerx - rect_width/2 + 280, text_rect.centery - 200, rect_width, rect_height)
    
    rect_right = pygame.Rect(text_rect.centerx + radius1, text_rect.centery - rect_height/2, rect_width, rect_height)
    
    rect_middle2 = pygame.Rect(text_rect.centerx - rect_width/2 + 280, text_rect.centery + 110, rect_width, rect_height)
    
    rect_bottom = pygame.Rect(text_rect.centerx - rect_width/2 + 30, text_rect.centery + radius1+20, rect_width, rect_height)
    
    pygame.draw.rect(screen, solo_play_muisc_menu_color, solo_play_muisc_menu_rect)
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

    music_detail_font = pygame.font.Font(font_path, 25)
    music_detail_surface = music_detail_font.render(music_data[(current_index + 2) % len(music_data)]["music_detail"], True, black)
    
    music_detail_rect = music_detail_surface.get_rect(topleft=(solo_play_muisc_menu_rect.left + 15, solo_play_muisc_menu_rect.top + 10))
    screen.blit(music_detail_surface, music_detail_rect.topleft)

    result_font = pygame.font.Font(font_path, 25)
    song_title = music_data[(current_index + 2) % len(music_data)]["title"]

    user_score_data = load_score(logged_in_user, song_title) # 플레이어의 정보에 저장되어있는 값을 가져와 출력
    max_combo = user_score_data.get("max_combo", 0)  
    score = user_score_data.get("score", 0)       

    combo_text = "Max Combo: {}".format(max_combo)
    combo_surface = result_font.render(combo_text, True, black)
    combo_rect = combo_surface.get_rect(topleft=(solo_play_muisc_menu_rect.left + 15, music_detail_rect.bottom + 10))
    screen.blit(combo_surface, combo_rect.topleft)

    score_text = "Max Score: {}".format(score)
    score_surface = result_font.render(score_text, True, black)
    score_rect = score_surface.get_rect(topleft=(solo_play_muisc_menu_rect.left + 15, combo_rect.bottom + 10))
    screen.blit(score_surface, score_rect.topleft)

    pygame.draw.rect(screen, black, solo_play_muisc_menu_rect, 4) 

    screen.blit(text_surface, text_rect)

def close_button():
    pygame.draw.line(screen, black, close_button_rect.topleft, close_button_rect.bottomright, 6)
    pygame.draw.line(screen, black, close_button_rect.bottomleft, close_button_rect.topright, 6)


#========== 솔로 플레이 게임 ==========
def solo_run_game():
    global current_game_state, combo, player_hp 

    button_font_size = 50
    button_font = pygame.font.Font(font_path, button_font_size)

    hp_label_font = pygame.font.Font(None, 40)
    hp_label_text = hp_label_font.render("MY.HP", True, black)
    hp_label_rect = hp_label_text.get_rect(right=screen_width-270, top=180)

    combo_font = pygame.font.Font(font_path, 40)
    combo_number_font_size = 80
    combo_number_font = pygame.font.Font(font_path, combo_number_font_size)

    score = 0
    max_combo = 0
    game_state = "playing"
    running = True
    game_paused = False

    rect_x = 60
    rect_y = 10
    rect_width = 450
    rect_height = 780
    border_thickness = 8
    note_height = 30
    note_width = 80
    semicolon_key = 59

    pause_start_time = 0
    total_pause_duration = 0

    hp_bar_x = screen_width - 350
    hp_bar_y = hp_label_rect.bottom 
    hp_bar_width = 260
    hp_bar_height = 70
    hp_segment_width = hp_bar_width // 10 

    button_x_centers = [73.75 + 45, 184.75 + 45, 296 + 45, 407 + 45]
    button_y_center = rect_height - 132 + 65

    check_line = rect_y + rect_height - 150

    hit_top_line = rect_y + rect_height - 257
    hit_middle_line = rect_y + rect_height - 235
    hit_bottom_line = rect_y + rect_height - 213

    score_box_width = 260
    score_box_height = 70
    score_box_x = screen_width - 350
    score_box_y = 80

    button_data = [ # 버튼 데이터
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

    total_buttons_width = retry_button_rect.width + menu_button_rect.width + button_spacing
    retry_button_rect.topleft = ((screen_width - total_buttons_width) // 2, screen_height // 2 + 50)
    menu_button_rect.topleft = (retry_button_rect.right + button_spacing, screen_height // 2 + 50)

    note_data = copy.deepcopy(original_note_data)
    for note in note_data:
        note["hit"] = False

    def hit_box():
        rectangle_height = 35
        rectangle_width = 90
        for button in button_data:
            rectangle_x = button["x"] + button["width"] // 2 - rectangle_width // 2
            rectangle_y = button["y"] - rectangle_height - 75
            pygame.draw.rect(screen, white, (rectangle_x, rectangle_y, rectangle_width, rectangle_height)) 
            pygame.draw.rect(screen, black, (rectangle_x, rectangle_y, rectangle_width, rectangle_height), 4) 


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
        global combo, y_position, bottom_of_screen, player_hp
        bottom_of_screen = rect_y + rect_height
        current_time = pygame.time.get_ticks() - total_pause_duration
        notes_to_remove = []

        for note in note_data:
            if current_time >= note["start_time"]:
                note["number"] += note["note_speed"]
                y_position = note["number"] * note_height

                if y_position + note_height > check_line:
                    if not note["hit"]: 
                        note["hit"] = True 
                        player_hp -= 1 
                        combo = 0
                        if note not in notes_to_remove:
                            notes_to_remove.append(note)

                elif y_position >= bottom_of_screen:
                    if note not in notes_to_remove:
                        notes_to_remove.append(note)

        for note in notes_to_remove:
            note_data.remove(note)

    def draw_retry_button():
        font_retry = pygame.font.Font(font_path, 50)
        pygame.draw.rect(screen, white, retry_button_rect)
        text = font_retry.render("다시 하기", True, black)
        text_rect = text.get_rect(center=retry_button_rect.center)
        screen.blit(text, text_rect)

    def draw_menu_button():
        font_menu = pygame.font.Font(font_path, 50)
        pygame.draw.rect(screen, white, menu_button_rect)
        text = font_menu.render('메뉴 가기', True, black)
        text_rect = text.get_rect(center=menu_button_rect.center)
        screen.blit(text, text_rect)

    def stop_song():
        pygame.mixer.music.stop()

    def play_song_thread():
        time.sleep(song_start_time)
        pygame.mixer.music.set_volume(sound_volume)
        pygame.mixer.music.load(song_file_path)
        pygame.mixer.music.play()

    def draw_win_screen():
        screen.fill(white)
        
        score_font = pygame.font.Font(font_path, 70)
        score_text = score_font.render(f"Score: {score}", True, black)
        score_rect = score_text.get_rect(center=(screen_width // 2, 300))

        combo_font = pygame.font.Font(font_path, 70)
        combo_text = combo_font.render(f"Max Combo: {max_combo}", True, black)
        combo_rect = combo_text.get_rect(center=(screen_width // 2, score_rect.bottom + 50))

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
        screen.blit(combo_text, combo_rect)

    
    def draw_game_over_screen():
        screen.fill(white)
        game_over_font = pygame.font.Font(font_path, 100)
        game_over_text = game_over_font.render("Game Over", True, black)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height - 600))

        score_font = pygame.font.Font(font_path, 70)
        score_text = score_font.render(f"Score: {score}", True, black)
        score_rect = score_text.get_rect(center=(screen_width // 2, 300))

        combo_font = pygame.font.Font(font_path, 70)
        combo_text = combo_font.render(f"Max Combo: {max_combo}", True, black)
        combo_rect = combo_text.get_rect(center=(screen_width // 2, score_rect.bottom + 45))

        draw_retry_button() 
        draw_menu_button()

        line_start = (combo_rect.left, combo_rect.bottom + 20)
        line_end = (combo_rect.right, combo_rect.bottom + 20)
        pygame.draw.line(screen, black, line_start, line_end, 8)

        vertical_line_start = ((line_start[0] + line_end[0]) // 2, combo_rect.bottom + 20)
        vertical_line_end = ((line_start[0] + line_end[0]) // 2, retry_button_rect.top + 60)
        pygame.draw.line(screen, black, vertical_line_start, vertical_line_end, 8)

        screen.blit(game_over_text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(combo_text, combo_rect)


    def play_game_combo_and_score():
        pygame.draw.rect(screen, white, (score_box_x, score_box_y, score_box_width, score_box_height))
        pygame.draw.rect(screen, black, (score_box_x, score_box_y, score_box_width, score_box_height), 8)

        score_label_font = pygame.font.Font(font_path, 30)
        score_label_text = score_label_font.render("Score", True, black)
        score_label_rect = score_label_text.get_rect(midbottom=(score_box_x+45, score_box_y))
        screen.blit(score_label_text, score_label_rect)
        score_font = pygame.font.Font(font_path, 50)
        score_text = score_font.render(f"{score}", True, black)
        score_rect = score_text.get_rect(midright=(score_box_x + score_box_width - 20, score_box_y + (score_box_height // 2)))
        screen.blit(score_text, score_rect)

        combo_text = combo_font.render("COMBO", True, black)   
        combo_rect = combo_text.get_rect(right=screen_width-140, top=450)
        pygame.draw.circle(screen, black, combo_rect.center, combo_rect.width-60, 8)
        combo_text_rect = combo_text.get_rect(center=(combo_rect.centerx, combo_rect.centery - 130))
        screen.blit(combo_text, combo_text_rect)
        combo_number_text = combo_number_font.render(str(combo), True, black)
        combo_number_rect = combo_number_text.get_rect(center=combo_rect.center)
        screen.blit(combo_number_text, combo_number_rect)
    
    def draw_hit_result_label(result):
        global hit_result, hit_result_start_time
        hit_result = result
        hit_result_start_time = pygame.time.get_ticks()

    def draw_vertical_gradient(start_color, end_color, rect, end_y):
        for y in range(rect.top, end_y):
            ratio = ((y - rect.top) / (end_y - rect.top))

            r = start_color[0] * (1 - ratio) + end_color[0] * ratio
            g = start_color[1] * (1 - ratio) + end_color[1] * ratio
            b = start_color[2] * (1 - ratio) + end_color[2] * ratio
            pygame.draw.line(screen, (int(r), int(g), int(b)), (rect.x, y), (rect.x + rect.width, y))


    while running:
        global hit_result, hit_result_start_time
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
                        button["pressed"] = True  
                        
                        lane = button_data.index(button)
                        hit_note = False
                        for note in note_data:
                            y_position = note["number"] * note_height
                            line_y = hit_middle_line
                            if note["lane"] == lane and y_position <= line_y and y_position + note_height >= line_y:
                                hit_note = True
                                break

            elif event.type == pygame.KEYUP:
                for button in button_data:
                    if event.key == button["key"]:
                        button["pressed"] = False  

            if game_state in ["game_over", "win"]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if retry_button_rect.collidepoint(mouse_pos):
                        stop_song()
                        combo = 0
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
                        stop_song()
                        player_hp = 10
                        combo = 0
                        running = False
                        current_game_state = GameState.SOLO_PLAY
        
        if game_state == "playing":
            pygame.draw.line(screen, black, (rect_x, max(check_line, rect_y)), (rect_x + rect_width-5, max(check_line, rect_y)), 8)
            pygame.draw.line(screen, white, (rect_x, max(hit_top_line, rect_y)), (rect_x + rect_width-5, max(hit_top_line, rect_y)), 2)
            pygame.draw.line(screen, white, (rect_x, max(hit_middle_line, rect_y)), (rect_x + rect_width-5, max(hit_middle_line, rect_y)), 2)
            pygame.draw.line(screen, white, (rect_x, max(hit_bottom_line, rect_y)), (rect_x + rect_width-5, max(hit_bottom_line, rect_y)), 2)

            if not note_data and player_hp > 0: 
                game_state = "win"
            
            elif player_hp <=0:
                game_state = "game_over"
                
            if game_state == "win" or game_state == "game_over":
                song_title = music_data[(current_index + 2) % len(music_data)]["title"]
                if song_title not in music_result:
                    music_result[song_title] = {}
                music_result[song_title]["score"] = max(score, music_result[song_title].get("score", 0))
                music_result[song_title]["combo"] = max(max_combo, music_result[song_title].get("combo", 0))
                save_score(logged_in_user, song_title, score, max_combo)

            if pygame.mixer.music.get_busy() == 0:
                song_thread = threading.Thread(target=play_song_thread)
                song_thread.start()

            screen.blit(hp_label_text, hp_label_rect.topleft)
            move_notes()
            for button in button_data:
                if button["pressed"]:
                    gradient_rect = pygame.Rect(button["x"]-7, check_line-630, button["width"]+15, 120)
                    draw_vertical_gradient(white, black, gradient_rect, check_line)

                if button["color"] == black:
                    for note in note_data[:]:
                        if note["number"] >= 0:
                            lane = note["lane"]
                            y_position_top = note["number"] * note_height
                            y_position_bottom = y_position_top + note_height

                            if (y_position_top <= hit_top_line and y_position_bottom >= hit_middle_line) or (y_position_top <= hit_middle_line and y_position_bottom >= hit_bottom_line):
                                if lane == button_data.index(button):
                                    if button["pressed"]:
                                        draw_hit_result_label("Good")
                                        combo += 1
                                        score += 10
                                        if combo % 5 == 0 and combo != 0:
                                            score += 5

                                        if combo % 10 == 0 and combo != 0:
                                            score += 10

                                        if combo % 20 == 0 and combo != 0:
                                            score += 20
                                        if max_combo < combo:
                                            max_combo = combo
                                        note_data.remove(note)
                                    
                            elif y_position_top <= hit_middle_line and y_position_bottom >= hit_middle_line:
                                if lane == button_data.index(button):
                                    if button["pressed"]:
                                        draw_hit_result_label("Great")
                                        combo += 1
                                        score += 20
                                        if combo % 5 == 0 and combo != 0:
                                            score += 5

                                        if combo % 10 == 0 and combo != 0:
                                            score += 10

                                        if combo % 20 == 0 and combo != 0:
                                            score += 20

                                        if max_combo < combo:
                                            max_combo = combo
                                        note_data.remove(note)

                            elif y_position_top == hit_top_line or y_position_bottom == hit_top_line or (y_position_top < hit_top_line and y_position_bottom > hit_top_line):
                                    if lane == button_data.index(button):
                                        if button["pressed"]:
                                            draw_hit_result_label("Miss")
                                            combo = 0
                                            player_hp -= 1
                                            if max_combo < combo:
                                                max_combo = combo
                                            note_data.remove(note)

                            elif (y_position_bottom >= hit_bottom_line and y_position_top <= hit_bottom_line) or (y_position_top >= hit_top_line and y_position_bottom <= hit_top_line):
                                    if lane == button_data.index(button):
                                        if button["pressed"]:
                                            draw_hit_result_label("Miss")
                                            combo = 0
                                            player_hp -= 1
                                            if max_combo < combo:
                                                max_combo = combo
                                            note_data.remove(note)

                            elif y_position_bottom > rect_y + rect_height:
                                if lane == button_data.index(button):
                                    combo = 0
                                    if max_combo < combo:
                                        max_combo = combo
    
            pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), border_thickness)
            segment_width = rect_width // 4
            for i in range(1, 4):
                x = rect_x + i * segment_width
                pygame.draw.line(screen, black, (x, rect_y), (x, rect_y + rect_height-5), 8)

            hit_box()
            draw_notes()
            

            for button in button_data:
                pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 1)
                pygame.draw.rect(screen, button["color"], (button["x"], button["y"], button["width"], button["height"]), 0)
                if button["pressed"]:
                    pygame.draw.rect(screen, black, (button["x"], button["y"], button["width"], button["height"]), 3)

                text = button_font.render(pygame.key.name(button["key"]), True, white)
                text_rect = text.get_rect(center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2))
                screen.blit(text, text_rect)

            play_game_combo_and_score()

            if hit_result:
                current_time = pygame.time.get_ticks()
                if current_time - hit_result_start_time <= 1000:
                    hit_result_font = pygame.font.Font(font_path, 50)
                    hit_result_text = hit_result_font.render(hit_result, True, black)
                    hit_result_rect = hit_result_text.get_rect(bottomright=(screen_width-150, screen_height-100))
                    screen.blit(hit_result_text, hit_result_rect)
                else:
                    hit_result = None

            pygame.display.flip()
            clock.tick(144)

        elif game_state == "game_over":
            draw_game_over_screen()
            pygame.display.flip()

        elif game_state == "win":
            draw_win_screen()
            pygame.display.flip()


#========== 메인 루트 ==========
while True:
    #========== 경고 비활성화 ==========
    deactivate_warnings_after_delay()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #========== 현재 게임 상태에 따라 이벤트 처리 ==========
        if current_game_state == GameState.SIGNUP:
            signup_user_input.handle_event(event)
            signup_pwd_input.handle_event(event)
            signup_confirm_input.handle_event(event)

        elif current_game_state == GameState.LOGIN:
            login_user_input.handle_event(event)
            login_pwd_input.handle_event(event)

        #========== 마우스 버튼 이벤트 처리 ==========
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_game_state == GameState.SOLO_PLAY:
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
                    current_game_state = GameState.LOGIN_SIGNUP
                    if not is_sound_played:
                        click_sound.play()
                        is_sound_played = True

            #========== ESC 키를 눌렀을 때 메뉴 처리 ==========
            elif current_game_state == GameState.ESC:
                if menu_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.MAIN_MENU
                    pygame.mixer.music.load(main_menu_music_path)
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(-1)

                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif current_game_state == GameState.MAIN_MENU_ESC:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif current_game_state == GameState.LOGIN_SIGNUP:
                if signup_button.collidepoint(event.pos):
                    current_game_state = GameState.SIGNUP

                elif login_button.collidepoint(event.pos):
                    current_game_state = GameState.LOGIN

                if close_button_rect.collidepoint(event.pos):
                    current_game_state = GameState.MAIN_MENU
                    continue

            elif current_game_state == GameState.SIGNUP and signup_close_button.collidepoint(event.pos):
                signup_user_input.clear_text()
                signup_pwd_input.clear_text()
                signup_confirm_input.clear_text()
                current_game_state = GameState.LOGIN_SIGNUP

            elif current_game_state == GameState.LOGIN and login_close_button.collidepoint(event.pos):
                login_user_input.clear_text()
                login_pwd_input.clear_text()
                current_game_state = GameState.LOGIN_SIGNUP

            elif current_game_state == GameState.SIGNUP and signup_confirm_button.collidepoint(event.pos):
                if not is_valid_string(signup_user_input.text) or not is_valid_string(signup_pwd_input.text):
                    activate_warning("signup_invalid_input")

                elif user_exists(signup_user_input.text):
                    activate_warning("user_exists")

                else:
                    if signup_pwd_input.text != signup_confirm_input.text:
                        activate_warning("password_mismatch")
                    else:
                        save_user(signup_user_input.text, signup_pwd_input.text)
                        signup_user_input.clear_text()
                        signup_pwd_input.clear_text()
                        signup_confirm_input.clear_text()
                        print("회원가입 성공!")
                        current_game_state = GameState.LOGIN_SIGNUP

            elif current_game_state == GameState.LOGIN and login_confirm_button.collidepoint(event.pos):
                if not is_valid_string(login_user_input.text) or not is_valid_string(login_pwd_input.text):
                    activate_warning("login_invalid_input")

                elif not verify_login(login_user_input.text, login_pwd_input.text):
                    activate_warning("login_failure")

                else:
                    logged_in_user = login_user_input.text
                    login_successful = True
                    login_user_input.clear_text()
                    login_pwd_input.clear_text()
                    print("로그인 성공!")
                    current_game_state = GameState.SOLO_PLAY

        #========== 키 이벤트 처리 ==========
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                if current_game_state != GameState.ESC:
                    prev_game_state = current_game_state
            
                    if current_game_state == GameState.MAIN_MENU:
                        current_game_state = GameState.MAIN_MENU_ESC
            
                    elif current_game_state == GameState.MAIN_MENU_ESC:
                        current_game_state = GameState.MAIN_MENU
                   
                    elif current_game_state != GameState.MAIN_MENU:
                        current_game_state = GameState.ESC
            
                else:
                    if prev_game_state is not None:
                        current_game_state = prev_game_state
                        prev_game_state = None

            if current_game_state == GameState.SIGNUP and event.key == pygame.K_RETURN:
                if not is_valid_string(signup_user_input.text) or not is_valid_string(signup_pwd_input.text):
                    activate_warning("signup_invalid_input")

                elif user_exists(signup_user_input.text):
                    activate_warning("user_exists")

                else:
                    if signup_pwd_input.text != signup_confirm_input.text:
                        activate_warning("password_mismatch")
                    else:
                        save_user(signup_user_input.text, signup_pwd_input.text)
                        signup_user_input.clear_text()
                        signup_pwd_input.clear_text()
                        signup_confirm_input.clear_text()
                        print("회원가입 성공!")
                        current_game_state = GameState.LOGIN_SIGNUP

            elif current_game_state == GameState.LOGIN and event.key == pygame.K_RETURN:
                if not is_valid_string(login_user_input.text) or not is_valid_string(login_pwd_input.text):
                    activate_warning("login_invalid_input")

                elif not verify_login(login_user_input.text, login_pwd_input.text):
                    activate_warning("login_failure")

                else:
                    logged_in_user = login_user_input.text
                    login_successful = True
                    login_user_input.clear_text()
                    login_pwd_input.clear_text()
                    print("로그인 성공!")
                    current_game_state = GameState.SOLO_PLAY

        if event.type == pygame.MOUSEBUTTONDOWN and current_game_state == GameState.SOLO_PLAY:
            if start_button_rect.collidepoint(event.pos):
                current_music = music_data[(current_index + 2) % len(music_data)]
                music_list_value = current_music["music_list"]
                song_file_path = current_music["sound_file"]
                sound_volume = current_music["music_sound"]
                song_start_time = current_music["music_start_time"]

                file_name = "note_data/" + music_list_value + ".json"
                try:
                    with open(file_name, "r") as file:
                        loaded_data = json.load(file)
                    original_note_data = loaded_data.copy()
                    if len(original_note_data) != 0:
                        solo_run_game()
                except FileNotFoundError:
                    pass

        if event.type == pygame.KEYDOWN:
            if current_game_state == GameState.CREATE:
                if event.key == pygame.K_RETURN:
                    current_game_state = GameState.LOADING

            if current_game_state == GameState.SOLO_PLAY:
                if event.key == pygame.K_UP:
                    current_index += 1
                    if current_index > 7:
                        current_index = 0

                elif event.key == pygame.K_DOWN:
                    current_index -= 1
                    if current_index < 0:
                        current_index = 7

                elif event.key == pygame.K_RETURN:
                    current_music = music_data[(current_index + 2) % len(music_data)]
                    music_list_value = current_music["music_list"]
                    song_file_path = current_music["sound_file"]
                    sound_volume = current_music["music_sound"]
                    song_start_time = current_music["music_start_time"]

                    file_name = "note_data/" + music_list_value + ".json"
                    try:
                        with open(file_name, "r") as file:
                            loaded_data = json.load(file)
                        original_note_data = loaded_data.copy()

                        if len(original_note_data) != 0:
                            solo_run_game()
                    except FileNotFoundError:
                        pass

    if current_game_state == GameState.MAIN_MENU:
        main_menu()

    elif current_game_state == GameState.SOLO_PLAY:
        pygame.mixer.music.stop()
        solo_play_menu()
        display_logged_in_user(screen)

    elif current_game_state == GameState.LOGIN_SIGNUP:
        login_signup_menu()
        close_button()

    elif current_game_state == GameState.SIGNUP:
        signup()

    elif current_game_state == GameState.LOGIN:
        login()

    elif current_game_state == GameState.ESC:
        esc_menu()

    elif current_game_state == GameState.MAIN_MENU_ESC:
        main_menu_esc_menu()

    pygame.display.update()