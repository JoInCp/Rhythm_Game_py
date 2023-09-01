import pygame
import json
import sys
from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    SOLO_PLAY = auto()
    MULTI_PLAY = auto()
    LOADING = auto()
    CREATE = auto()
    GAME_WIN = auto()
    GAME_OVER = auto()
    SIGNUP = auto()
    LOGIN = auto()
    LOGIN_SIGNUP = auto()

current_game_state = GameState.LOGIN_SIGNUP

pygame.init()
pygame.display.set_caption("Login & Signup")

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
data_file = "users.json"
path = "font/KBO Dia Gothic_medium.ttf"

login_signup_menu_color = white

login_signup_menu_center_x = screen_width // 2
login_signup_menu_center_y = screen_height // 2

login_signup_menu_size = (800, 600)
login_signup_menu_rect = pygame.Rect((screen_width - login_signup_menu_size[0]) // 2,
                                    (screen_height - login_signup_menu_size[1]) // 2,
                                    login_signup_menu_size[0], login_signup_menu_size[1])

signup_button = pygame.Rect(login_signup_menu_center_x + 25, login_signup_menu_center_y - 30, 100, 60)
login_button = pygame.Rect(login_signup_menu_center_x - 125, login_signup_menu_center_y - 30, 100, 60)


total_width = 2 * 100 + 10

start_x = login_signup_menu_center_x - total_width // 2


signup_close_button_center_x = screen_width // 2 + 100 // 2 + 10 // 2
signup_close_button_center_y = screen_height // 2 + 130 - 30 // 2
signup_close_button = pygame.Rect(signup_close_button_center_x, signup_close_button_center_y, 100, 30)

signup_confirm_button_center_x = signup_close_button_center_x - 100 - 10 

signup_confirm_button = pygame.Rect(start_x, signup_close_button_center_y, 100, 30)
signup_close_button = pygame.Rect(start_x + 100 + 10, signup_close_button_center_y, 100, 30)

login_close_button_center_x = screen_width // 2 + 100 // 2 + 10 // 2
login_close_button_center_y = screen_height // 2 + 90 - 30 // 2
login_close_button = pygame.Rect(login_close_button_center_x, login_close_button_center_y, 100, 30)

login_confirm_button_center_x = login_close_button_center_x - 100 - 10 

login_confirm_button = pygame.Rect(start_x, login_close_button_center_y, 100, 30)
login_close_button = pygame.Rect(start_x + 100 + 10, login_close_button_center_y, 100, 30)

password_mismatch_warning = False
user_exists_warning = False
login_successful = False
login_failure_warning = False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = black
        self.text = text
        self.font = pygame.font.Font(path, 20)
        self.txt_surface = self.font.render(text, True, black)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, black)

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect.inflate(-2, -2))
        pygame.draw.rect(screen, black, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

signup_user_input = InputBox(login_signup_menu_center_x - 100, login_signup_menu_center_y - 90, 200, 30)
signup_pwd_input = InputBox(login_signup_menu_center_x - 100, login_signup_menu_center_y - 10, 200, 30)
signup_confirm_input = InputBox(login_signup_menu_center_x - 100, login_signup_menu_center_y + 70, 200, 30)

login_user_input = InputBox(login_signup_menu_center_x - 100, login_signup_menu_center_y - 90, 200, 30)
login_pwd_input = InputBox(login_signup_menu_center_x - 100, login_signup_menu_center_y - 10, 200, 30)


def login_signup_draw_button(screen, button_rect, text, font_path, font_size=20):
    pygame.draw.rect(screen, white, button_rect)
    pygame.draw.rect(screen, black, button_rect, 2)
    
    font = pygame.font.Font(font_path, font_size)
    rendered_text = font.render(text, True, black)
    
    text_x = button_rect.x + (button_rect.width - rendered_text.get_width()) // 2
    text_y = button_rect.y + (button_rect.height - rendered_text.get_height()) // 2
    screen.blit(rendered_text, (text_x, text_y))


def main_menu():
    screen.fill(white)


def user_exists(username):
    try:
        with open(data_file, 'r') as f:
            users = json.load(f)
            return username in users
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def verify_login(username, password):
    try:
        with open(data_file, 'r') as f:
            users = json.load(f)
            return users.get(username) == password
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def save_user(username, password):
    try:
        with open(data_file, 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    
    users[username] = password
    with open(data_file, 'w') as f:
        json.dump(users, f)

def signup():
    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)
    label_font = pygame.font.Font(path, 25)

    labels = ['아이디', '비밀번호', '비밀번호 확인']
    for index, label in enumerate(labels):
        rendered_label = label_font.render(label, True, black)
        screen.blit(rendered_label, (signup_user_input.rect.x, login_signup_menu_center_y - 120 + index * 80))

    signup_user_input.draw(screen)
    signup_pwd_input.draw(screen)
    signup_confirm_input.draw(screen)

    if user_exists_warning:
        warning_font = pygame.font.Font(path, 20)
        warning_msg = warning_font.render("이미 있는 아이디 입니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y - 60))

    if password_mismatch_warning:
        warning_font = pygame.font.Font(path, 20)
        warning_msg = warning_font.render("비밀번호가 일치하지 않습니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 105))

    ok_font = pygame.font.Font(path, 25)
    pygame.draw.rect(screen, white, signup_confirm_button)
    pygame.draw.rect(screen, black, signup_confirm_button, 2)
    confirm_text = ok_font.render("확인", True, black)
    screen.blit(confirm_text, (signup_confirm_button.x + (signup_confirm_button.width - confirm_text.get_width()) // 2, signup_confirm_button.y + (signup_confirm_button.height - confirm_text.get_height()) // 2))

    close_font = pygame.font.Font(path, 25)
    pygame.draw.rect(screen, white, signup_close_button)
    pygame.draw.rect(screen, black, signup_close_button, 2)
    close_text = close_font.render("닫기", True, black)
    screen.blit(close_text, (signup_close_button.x + (signup_close_button.width - close_text.get_width()) // 2, signup_close_button.y + (signup_close_button.height - close_text.get_height()) // 2))


def login():
    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)
    label_font = pygame.font.Font(path, 25)
    labels = ['아이디', '비밀번호']
    for index, label in enumerate(labels):
        rendered_label = label_font.render(label, True, black)
        screen.blit(rendered_label, (login_user_input.rect.x, login_signup_menu_center_y - 120 + index * 80))
        
    login_user_input.draw(screen)
    login_pwd_input.draw(screen)

    if login_failure_warning:
        warning_font = pygame.font.Font(path, 20)
        warning_msg = warning_font.render("아이디 또는 비밀번호가 잘못되었습니다.", True, (255, 0, 0))
        screen.blit(warning_msg, (login_signup_menu_center_x - (warning_msg.get_width() // 2), login_signup_menu_center_y + 30))

    ok_font = pygame.font.Font(path, 25)
    pygame.draw.rect(screen, white, login_confirm_button)
    pygame.draw.rect(screen, black, login_confirm_button, 2)
    confirm_text = ok_font.render("확인", True, black)
    screen.blit(confirm_text, (login_confirm_button.x + (login_confirm_button.width - confirm_text.get_width()) // 2, login_confirm_button.y + (login_confirm_button.height - confirm_text.get_height()) // 2))

    close_font = pygame.font.Font(path, 25)
    pygame.draw.rect(screen, white, login_close_button)
    pygame.draw.rect(screen, black, login_close_button, 2)
    close_text = close_font.render("닫기", True, black)
    screen.blit(close_text, (login_close_button.x + (login_close_button.width - close_text.get_width()) // 2, login_close_button.y + (login_close_button.height - close_text.get_height()) // 2))


def login_signup_menu():
    screen.fill(login_signup_menu_color)
    font = pygame.font.Font(path, 20)

    pygame.draw.rect(screen, login_signup_menu_color, login_signup_menu_rect)
    pygame.draw.rect(screen, black, login_signup_menu_rect, 4)

    login_signup_draw_button(screen, signup_button, "회원가입", path)
    login_signup_draw_button(screen, login_button, "로그인", path)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_game_state == GameState.SIGNUP:
            signup_user_input.handle_event(event)
            signup_pwd_input.handle_event(event)
            signup_confirm_input.handle_event(event)

        elif current_game_state == GameState.LOGIN:
            login_user_input.handle_event(event)
            login_pwd_input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_game_state == GameState.LOGIN_SIGNUP:
                if signup_button.collidepoint(event.pos):
                    current_game_state = GameState.SIGNUP

                elif login_button.collidepoint(event.pos):
                    current_game_state = GameState.LOGIN

            elif current_game_state == GameState.SIGNUP and signup_close_button.collidepoint(event.pos):
                current_game_state = GameState.LOGIN_SIGNUP

            elif current_game_state == GameState.LOGIN and login_close_button.collidepoint(event.pos):
                current_game_state = GameState.LOGIN_SIGNUP


            elif current_game_state == GameState.SIGNUP and signup_confirm_button.collidepoint(event.pos):
                if user_exists(signup_user_input.text):
                    user_exists_warning = True
                    print("이미 있는 아이디 입니다.")
                else:
                    if signup_pwd_input.text == signup_confirm_input.text:
                        save_user(signup_user_input.text, signup_pwd_input.text)
                        user_exists_warning = False
                        password_mismatch_warning = False
                        print("회원가입 성공!")
                        current_game_state = GameState.LOGIN_SIGNUP
                    else:
                        password_mismatch_warning = True
                        print("비밀번호가 일치하지 않습니다.")
            elif current_game_state == GameState.LOGIN and login_confirm_button.collidepoint(event.pos):
                if verify_login(login_user_input.text, login_pwd_input.text):
                    login_successful = True
                    login_failure_warning = False
                    screen.fill(white)
                    print("로그인 성공!")
                    current_game_state = GameState.LOGIN_SIGNUP
                else:
                    login_failure_warning = True
                    print("로그인 실패!")

    if current_game_state == GameState.LOGIN_SIGNUP:
        login_signup_menu()

    elif current_game_state == GameState.SIGNUP:
        signup()

    elif current_game_state == GameState.LOGIN:
        login()

    pygame.display.update()
