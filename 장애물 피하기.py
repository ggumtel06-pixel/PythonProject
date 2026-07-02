import pygame
import sys
import random

# 1. 초기화
pygame.init()

# 화면 크기 및 FPS 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Runner - Interactive Game Over UI")
clock = pygame.time.Clock()
FPS = 60

# 색상 정의 (레트로 픽셀 스타일)
BG_BLUE = (50, 110, 180)  # 하늘 색상
CLOUD_WHITE = (240, 245, 250)  # 구름 연한 색
CLOUD_SHADOW = (200, 215, 230)  # 구름 음영 색
DIRT_BROWN = (140, 90, 60)  # 흙 색상
DIRT_DARK = (95, 60, 40)  # 어두운 흙 (철도 침목용)
GRASS_GREEN = (60, 160, 60)  # 잔디 색상
RAIL_GRAY = (180, 185, 190)  # 철로 철제 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)
RED = (210, 50, 50)
BLUE = (0, 160, 240)
YELLOW = (255, 215, 0)
PURPLE = (140, 100, 200)  # 키 가이드 버튼용 보라색

# 꽃 색상 조합들 (노랑, 빨강, 보라, 흰색)
FLOWER_COLORS = [(255, 220, 0), (240, 60, 60), (160, 80, 220), (255, 255, 255)]

# 폰트 설정
font_huge = pygame.font.SysFont("malgungothic", 55, bold=True)
font_large = pygame.font.SysFont("malgungothic", 35, bold=True)
font_small = pygame.font.SysFont("malgungothic", 22, bold=True)
font_micro = pygame.font.SysFont("malgungothic", 18, bold=True)

# 게임 상태 변수
STATE_START = 0
STATE_GAME = 1
STATE_PAUSE = 2
STATE_GAMEOVER = 3
game_state = STATE_START

# 키 가이드 팝업 온/오프 변수
show_key_guide = False

# 유저 정보 및 최고 기록 데이터
user_name = ""
score = 0
high_score = 1876

# --- 배경 요소 고정 데이터 ---
clouds_data = [
    (40, 30, 120, 40), (130, 20, 160, 50), (260, 45, 90, 35),
    (450, 25, 140, 45), (560, 15, 180, 55), (710, 40, 80, 30)
]
flowers_data = []
random.seed(42)
for _ in range(25):
    fx = random.randint(0, SCREEN_WIDTH)
    fy = random.randint(342, 348)
    fcol = random.choice(FLOWER_COLORS)
    flowers_data.append((fx, fy, fcol))


# --- 캐릭터 클래스 ---
class Player:
    def __init__(self):
        self.normal_size = 40
        self.squash_height = 12
        self.width = self.normal_size
        self.height = self.normal_size

        self.x = 120
        self.base_y = SCREEN_HEIGHT - 60 - self.normal_size
        self.y = self.base_y

        self.color = BLUE
        self.is_jumping = False
        self.is_squashed = False
        self.jump_velocity = 15
        self.gravity = 0.8
        self.velocity_y = 0

        # 납작 게이지 관련 변수
        self.squash_gauge = 0.0
        self.max_gauge = 100.0
        self.gauge_charge_speed = 1.2
        self.gauge_drain_speed = 1.5

    def jump(self):
        if not self.is_jumping and not self.is_squashed:
            self.is_jumping = True
            self.velocity_y = -self.jump_velocity

    def squash(self):
        if not self.is_jumping:
            self.is_squashed = True
            self.height = self.squash_height
            self.y = SCREEN_HEIGHT - 60 - self.squash_height

    def stretch(self):
        if self.is_squashed:
            self.is_squashed = False
            self.height = self.normal_size
            self.y = self.base_y

    def update(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            if self.y >= self.base_y:
                self.y = self.base_y
                self.is_jumping = False
                self.velocity_y = 0

        if self.is_squashed:
            self.squash_gauge += self.gauge_charge_speed
            if self.squash_gauge >= self.max_gauge:
                self.squash_gauge = self.max_gauge
                return True
        else:
            self.squash_gauge -= self.gauge_drain_speed
            if self.squash_gauge < 0:
                self.squash_gauge = 0
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)

        eye_y = self.y + (4 if self.is_squashed else 10)
        eye_h = 3 if self.is_squashed else 6
        pygame.draw.rect(surface, BLACK, (self.x + 8, eye_y, 6, eye_h))
        pygame.draw.rect(surface, BLACK, (self.x + 24, eye_y, 6, eye_h))

    def draw_gauge(self, surface):
        if self.squash_gauge > 0:
            bar_width = 200
            bar_height = 15
            bar_x = SCREEN_WIDTH // 2 - bar_width // 2
            bar_y = 25

            pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            fill_width = int((self.squash_gauge / self.max_gauge) * bar_width)
            pygame.draw.rect(surface, RED, (bar_x, bar_y, fill_width, bar_height))
            pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)

            gauge_text = font_small.render("OVERHEAT!", True, RED if self.squash_gauge > 70 else WHITE)
            surface.blit(gauge_text, (bar_x - 110, bar_y - 5))


# --- 장애물 클래스 ---
class Obstacle:
    def __init__(self):
        self.type = random.choice(["LOW", "HIGH"])
        self.speed = 6
        self.color = RED
        self.x = SCREEN_WIDTH

        if self.type == "LOW":
            self.width = 30
            self.height = random.randint(35, 55)
            self.y = SCREEN_HEIGHT - 60 - self.height
        else:
            self.width = 130
            self.height = 35
            self.y = SCREEN_HEIGHT - 60 - 15 - self.height

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)


# --- 환경 그리기 함수 ---
def draw_environment():
    for cx, cy, cw, ch in clouds_data:
        pygame.draw.rect(screen, CLOUD_SHADOW, (cx, cy + 8, cw, ch), 0, 8)
        pygame.draw.rect(screen, CLOUD_WHITE, (cx, cy, cw, ch - 4), 0, 8)

    pygame.draw.rect(screen, DIRT_BROWN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, GRASS_GREEN, (0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 10))
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 60), (SCREEN_WIDTH, SCREEN_HEIGHT - 60), 2)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)

    rail_y = SCREEN_HEIGHT - 35
    for rx in range(0, SCREEN_WIDTH, 35):
        pygame.draw.rect(screen, DIRT_DARK, (rx, rail_y, 12, 22))
        pygame.draw.rect(screen, BLACK, (rx, rail_y, 12, 22), 1)
    pygame.draw.line(screen, RAIL_GRAY, (0, rail_y + 4), (SCREEN_WIDTH, rail_y + 4), 3)
    pygame.draw.line(screen, BLACK, (0, rail_y + 3), (SCREEN_WIDTH, rail_y + 3), 1)
    pygame.draw.line(screen, RAIL_GRAY, (0, rail_y + 16), (SCREEN_WIDTH, rail_y + 16), 3)
    pygame.draw.line(screen, BLACK, (0, rail_y + 15), (SCREEN_WIDTH, rail_y + 15), 1)

    for fx, fy, fcol in flowers_data:
        pygame.draw.rect(screen, (40, 110, 40), (fx, fy + 3, 2, 3))
        pygame.draw.rect(screen, fcol, (fx, fy, 3, 3))
        pygame.draw.rect(screen, YELLOW if fcol != YELLOW else WHITE, (fx + 1, fy + 1, 1, 1))


# 객체 생성
player = Player()
obstacles = []
obstacle_timer = 0

# 버튼 영역 선언 (마우스 클릭 충돌 판정 및 드로잉용 공용 범위)
btn_play_rect = pygame.Rect(180, 245, 210, 50)
btn_guide_rect = pygame.Rect(410, 245, 210, 50)
btn_again_rect = pygame.Rect(210, 260, 180, 48)  # 게임오버 재시작 버튼
btn_quit_rect = pygame.Rect(410, 260, 180, 48)  # 게임오버 메인화면(종료) 버튼

# --- 메인 루프 ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_START:
            if show_key_guide:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    show_key_guide = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_name.strip() != "":
                            player = Player()
                            obstacles = []
                            obstacle_timer = 0
                            score = 0
                            game_state = STATE_GAME
                    else:
                        if len(user_name) < 12 and event.unicode.isprintable():
                            user_name += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if btn_play_rect.collidepoint(mouse_pos):
                        if user_name.strip() != "":
                            player = Player()
                            obstacles = []
                            obstacle_timer = 0
                            score = 0
                            game_state = STATE_GAME
                    elif btn_guide_rect.collidepoint(mouse_pos):
                        show_key_guide = True

        elif game_state == STATE_GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    game_state = STATE_PAUSE

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.squash()
            else:
                player.stretch()

        elif game_state == STATE_PAUSE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    game_state = STATE_GAME

        # [수정] 게임오버 상태에서의 마우스 클릭 이벤트 상호작용 추가
        elif game_state == STATE_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = STATE_GAME
                    player = Player()
                    obstacles = []
                    obstacle_timer = 0
                    high_score = max(high_score, score)
                    score = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 1. PLAY AGAIN 버튼 클릭 시 게임 재시작
                if btn_again_rect.collidepoint(mouse_pos):
                    game_state = STATE_GAME
                    player = Player()
                    obstacles = []
                    obstacle_timer = 0
                    high_score = max(high_score, score)
                    score = 0
                # 2. QUIT 버튼 클릭 시 메인(시작) 화면으로 복귀
                elif btn_quit_rect.collidepoint(mouse_pos):
                    high_score = max(high_score, score)
                    game_state = STATE_START

    screen.fill(BG_BLUE)
    draw_environment()

    # [시작 화면]
    if game_state == STATE_START:
        title_text = font_large.render("SQUARE RUNNER", True, YELLOW)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))

        info_text = font_small.render("Enter Your Name:", True, WHITE)
        screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, 125))

        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 125, 165, 250, 40)
        pygame.draw.rect(screen, WHITE, input_box, 0, 5)
        pygame.draw.rect(screen, BLACK, input_box, 3, 5)
        name_text = font_small.render(user_name, True, BLACK)
        screen.blit(name_text, (input_box.x + 10, input_box.y + 5))

        pygame.draw.rect(screen, GRASS_GREEN, btn_play_rect, 0, 5)
        pygame.draw.rect(screen, BLACK, btn_play_rect, 3, 5)
        txt_play = font_small.render("PLAY GAME", True, WHITE)
        screen.blit(txt_play,
                    (btn_play_rect.x + (btn_play_rect.width // 2 - txt_play.get_width() // 2), btn_play_rect.y + 10))

        pygame.draw.rect(screen, PURPLE, btn_guide_rect, 0, 5)
        pygame.draw.rect(screen, BLACK, btn_guide_rect, 3, 5)
        txt_guide = font_small.render("KEY GUIDE", True, WHITE)
        screen.blit(txt_guide, (btn_guide_rect.x + (btn_guide_rect.width // 2 - txt_guide.get_width() // 2),
                                btn_guide_rect.y + 10))

        if show_key_guide:
            guide_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            guide_overlay.fill((0, 0, 0, 100))
            screen.blit(guide_overlay, (0, 0))

            popup_rect = pygame.Rect(250, 100, 300, 190)
            pygame.draw.rect(screen, WHITE, popup_rect, 0, 10)
            pygame.draw.rect(screen, PURPLE, popup_rect, 4, 10)
            pygame.draw.rect(screen, BLACK, popup_rect, 2, 10)

            g_title = font_small.render("— KEY GUIDE —", True, BLACK)
            screen.blit(g_title, (popup_rect.x + (popup_rect.width // 2 - g_title.get_width() // 2), popup_rect.y + 12))

            g_txt1 = font_micro.render("• SPACE / UP : Jump", True, DARK_GRAY)
            g_txt2 = font_micro.render("• A Key (Hold) : Squash", True, DARK_GRAY)
            g_txt3 = font_micro.render("• SHIFT Key : Pause", True, DARK_GRAY)
            g_close = font_micro.render("Press any key to close", True, RED)

            screen.blit(g_txt1, (popup_rect.x + 35, popup_rect.y + 50))
            screen.blit(g_txt2, (popup_rect.x + 35, popup_rect.y + 82))
            screen.blit(g_txt3, (popup_rect.x + 35, popup_rect.y + 114))
            screen.blit(g_close,
                        (popup_rect.x + (popup_rect.width // 2 - g_close.get_width() // 2), popup_rect.y + 155))

    elif game_state == STATE_GAME or game_state == STATE_PAUSE:
        if game_state == STATE_GAME:
            is_overheated = player.update()
            if is_overheated:
                game_state = STATE_GAMEOVER

            obstacle_timer += 1
            if obstacle_timer > random.randint(70, 130):
                obstacles.append(Obstacle())
                obstacle_timer = 0

            for obstacle in obstacles[:]:
                obstacle.update()

                p_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                o_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)

                if p_rect.colliderect(o_rect):
                    game_state = STATE_GAMEOVER

                if obstacle.x + obstacle.width < 0:
                    obstacles.remove(obstacle)
                    if obstacle.type == "LOW":
                        score += 12
                    else:
                        score += 20

        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        player.draw_gauge(screen)

        score_text = font_micro.render(f"NAME: {user_name}  |  SCORE: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        if game_state == STATE_PAUSE:
            pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 120))
            screen.blit(pause_overlay, (0, 0))
            p_text = font_large.render("PAUSED", True, WHITE)
            screen.blit(p_text, (SCREEN_WIDTH // 2 - p_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

    # [게임오버 화면]
    elif game_state == STATE_GAMEOVER:
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        go_text_bg = font_huge.render("GAME OVER!", True, RED)
        go_text_fg = font_huge.render("GAME OVER!", True, YELLOW)
        go_x = SCREEN_WIDTH // 2 - go_text_fg.get_width() // 2
        screen.blit(go_text_bg, (go_x + 3, 23))
        screen.blit(go_text_fg, (go_x, 20))

        board_rect = pygame.Rect(220, 110, 360, 120)
        pygame.draw.rect(screen, WHITE, board_rect, 0, 8)
        pygame.draw.rect(screen, (180, 160, 220), board_rect, 4, 8)
        pygame.draw.rect(screen, BLACK, board_rect, 2, 8)

        badge_text = font_small.render(f"NAME : {user_name.upper()}", True, BLACK)
        final_text = font_small.render(f"FINAL SCORE : {score}", True, BLACK)
        high_text = font_small.render(f"HIGHEST SCORE : {high_score}", True, BLACK)

        screen.blit(badge_text, (245, 125))
        screen.blit(final_text, (245, 157))
        screen.blit(high_text, (245, 189))

        bubble_rect = pygame.Rect(player.x - 10, player.y - 40, 95, 32)
        pygame.draw.rect(screen, WHITE, bubble_rect, 0, 5)
        pygame.draw.rect(screen, BLACK, bubble_rect, 2, 5)
        pygame.draw.polygon(screen, WHITE, [(player.x + 15, player.y - 10), (player.x + 20, player.y - 2),
                                            (player.x + 25, player.y - 10)])
        pygame.draw.polygon(screen, BLACK, [(player.x + 15, player.y - 10), (player.x + 20, player.y - 2),
                                            (player.x + 25, player.y - 10)], 2)

        b_text = font_micro.render("SQUASH!", True, BLACK)
        screen.blit(b_text, (bubble_rect.x + (bubble_rect.width // 2 - b_text.get_width() // 2), bubble_rect.y + 4))

        # PLAY AGAIN 버튼 그리기
        pygame.draw.rect(screen, GRASS_GREEN, btn_again_rect, 0, 6)
        pygame.draw.rect(screen, BLACK, btn_again_rect, 3, 6)
        txt_again = font_small.render("PLAY AGAIN", True, WHITE)
        screen.blit(txt_again, (btn_again_rect.x + (btn_again_rect.width // 2 - txt_again.get_width() // 2),
                                btn_again_rect.y + 10))

        # QUIT 버튼 그리기
        pygame.draw.rect(screen, DARK_GRAY, btn_quit_rect, 0, 6)
        pygame.draw.rect(screen, BLACK, btn_quit_rect, 3, 6)
        txt_quit = font_small.render("QUIT", True, WHITE)
        screen.blit(txt_quit,
                    (btn_quit_rect.x + (btn_quit_rect.width // 2 - txt_quit.get_width() // 2), btn_quit_rect.y + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()