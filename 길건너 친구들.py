import pygame
import random
import sys

# 1. 초기화 및 상수 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)  # 플레이어 (닭)
GREEN = (34, 139, 34)  # 잔디 (안전지대)
GRAY = (105, 105, 105)  # 도로
RED = (220, 20, 60)  # 빨간 자동차
BLUE = (30, 144, 255)  # 파란 자동차
ORANGE = (255, 140, 0)  # 주황 자동차

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vibe Coding: Crossy Road Style")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 30)  # 한글 폰트 (없으면 기본 폰트 작동)


# 2. 클래스 정의
class Player:
    def __init__(self):
        self.grid_x = WIDTH // 2 // GRID_SIZE
        self.grid_y = (HEIGHT // GRID_SIZE) - 2
        self.max_grid_y = self.grid_y  # 최고 기록 계산용
        self.score = 0

    def get_rect(self, camera_y):
        # 카메라 좌표를 반영한 실제 화면상의 Rect 반환
        return pygame.Rect(self.grid_x * GRID_SIZE, (self.grid_y * GRID_SIZE) - camera_y, GRID_SIZE, GRID_SIZE)

    def move(self, dx, dy, max_lanes):
        self.grid_x += dx
        self.grid_y += dy

        # 화면 좌우 가두기
        if self.grid_x < 0: self.grid_x = 0
        if self.grid_x >= WIDTH // GRID_SIZE: self.grid_x = (WIDTH // GRID_SIZE) - 1

        # 위로 전진했을 때 최고 점수 갱신
        if self.grid_y < self.max_grid_y:
            steps_forward = self.max_grid_y - self.grid_y
            if steps_forward > self.score:
                self.score = steps_forward


class Car:
    def __init__(self, lane_grid_y, direction, speed, color):
        self.lane_grid_y = lane_grid_y
        self.direction = direction  # 1: 오른쪽, -1: 왼쪽
        self.speed = speed
        self.color = color
        self.width = GRID_SIZE * 2  # 자동차는 2칸 크기
        self.height = GRID_SIZE - 4

        if direction == 1:
            self.x = -self.width
        else:
            self.x = WIDTH

    def update(self):
        self.x += self.direction * self.speed

    def get_rect(self, camera_y):
        y_pos = (self.lane_grid_y * GRID_SIZE) - camera_y + 2
        return pygame.Rect(self.x, y_pos, self.width, self.height)


class Lane:
    def __init__(self, grid_y, is_initial=False):
        self.grid_y = grid_y
        # 처음 5칸은 안전하게 무조건 잔디, 그 외에는 랜덤 (도로 60%, 잔디 40%)
        if is_initial and grid_y >= (HEIGHT // GRID_SIZE) - 5:
            self.type = "GRASS"
        else:
            self.type = random.choice(["GRASS", "ROAD", "ROAD"])

        self.color = GREEN if self.type == "GRASS" else GRAY

        # 도로인 경우 자동차 스폰 정보 설정
        self.cars = []
        if self.type == "ROAD":
            self.direction = random.choice([1, -1])
            self.speed = random.randint(3, 6)
            self.car_color = random.choice([RED, BLUE, ORANGE])
            self.spawn_timer = random.randint(0, 90)  # 스폰 타이머 초기화 엇갈리게

    def update_cars(self):
        if self.type != "ROAD":
            return

        # 자동차 이동
        for car in self.cars[:]:
            car.update()
            # 화면 밖으로 완전히 벗어나면 삭제
            if car.direction == 1 and car.x > WIDTH:
                self.cars.remove(car)
            elif car.direction == -1 and car.x < -car.width:
                self.cars.remove(car)

        # 일정 주기마다 자동차 생성
        self.spawn_timer += 1
        if self.spawn_timer > 90:  # 약 1.5초마다
            self.cars.append(Car(self.grid_y, self.direction, self.speed, self.car_color))
            self.spawn_timer = random.randint(0, 30)  # 랜덤 딜레이 부여

    def draw(self, screen, camera_y):
        y_pos = (self.grid_y * GRID_SIZE) - camera_y
        pygame.draw.rect(screen, self.color, (0, y_pos, WIDTH, GRID_SIZE))


def show_menu():
    title_font = pygame.font.SysFont("malgungothic", 72)
    button_font = pygame.font.SysFont("malgungothic", 36)

    play_w, play_h = 200, 60
    play_rect = pygame.Rect(WIDTH // 2 - play_w // 2, HEIGHT // 2 + 20, play_w, play_h)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        hovered = play_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "PLAYING"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    return "PLAYING"

        screen.fill(BLACK)

        title = title_font.render("Crossy Road", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - 40))

        button_color = (46, 160, 67) if hovered else GRAY
        pygame.draw.rect(screen, button_color, play_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, play_rect, 2, border_radius=8)

        play_txt = button_font.render("Play", True, WHITE)
        screen.blit(
            play_txt,
            (
                play_rect.centerx - play_txt.get_width() // 2,
                play_rect.centery - play_txt.get_height() // 2,
            ),
        )

        pygame.display.flip()
        clock.tick(FPS)


# 3. 게임 플레이 함수
def run_game():
    player = Player()
    lanes = {}

    # 처음 화면을 채울 지형 생성 (넉넉하게 위쪽까지 생성)
    start_lane = (HEIGHT // GRID_SIZE) + 5
    end_lane = -20
    for gy in range(end_lane, start_lane):
        lanes[gy] = Lane(gy, is_initial=True)

    camera_y = 0
    game_over = False

    # 연속 입력 방지 변수
    key_pressed = False

    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:  # R 누르면 재시작
                        return "PLAYING"
                else:
                    if not key_pressed:
                        if event.key == pygame.K_UP:
                            player.move(0, -1, len(lanes))
                            key_pressed = True
                        elif event.key == pygame.K_DOWN:
                            player.move(0, 1, len(lanes))
                            key_pressed = True
                        elif event.key == pygame.K_LEFT:
                            player.move(-1, 0, len(lanes))
                            key_pressed = True
                        elif event.key == pygame.K_RIGHT:
                            player.move(1, 0, len(lanes))
                            key_pressed = True

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    key_pressed = False

        if not game_over:
            # 무한 맵 생성 로직: 플레이어 앞쪽으로 새로운 지형 계속 보충
            min_required_lane = player.grid_y - 20
            for gy in range(min_required_lane, player.grid_y + 20):
                if gy not in lanes:
                    lanes[gy] = Lane(gy)

            # 자동차 업데이트
            for lane in lanes.values():
                lane.update_cars()

            # 부드러운 카메라 추적 (플레이어가 위로 올라갈수록 카메라도 따라 올라감)
            # 플레이어 기준 화면 아래쪽 여백 유지 목적
            target_camera_y = (player.grid_y * GRID_SIZE) - (HEIGHT - 160)
            camera_y += (target_camera_y - camera_y) * 0.1

            # 충돌 감지
            player_rect = player.get_rect(camera_y)
            for lane in lanes.values():
                if lane.type == "ROAD":
                    for car in lane.cars:
                        if player_rect.colliderect(car.get_rect(camera_y)):
                            game_over = True

        # 4. 그리기 (Rendering)
        screen.fill(BLACK)

        # 지형 및 자동차 그리기 (카메라 범위 안의 것만)
        for gy in sorted(lanes.keys()):
            y_pos = (gy * GRID_SIZE) - camera_y
            if -GRID_SIZE <= y_pos <= HEIGHT:
                lanes[gy].draw(screen, camera_y)
                if lanes[gy].type == "ROAD":
                    for car in lanes[gy].cars:
                        pygame.draw.rect(screen, car.color, car.get_rect(camera_y))

        # 플레이어 그리기
        player_rect = player.get_rect(camera_y)
        pygame.draw.rect(screen, YELLOW, player_rect)
        # 미니 닭 부리 표현 (눈에 잘 띄게 작은 사각형 추가)
        pygame.draw.rect(screen, ORANGE, (player_rect.centerx + 4, player_rect.centery - 8, 8, 8))

        # UI (점수) 표시
        score_txt = font.render(f"SCORE: {player.score}", True, WHITE)
        screen.blit(score_txt, (20, 20))

        # 게임오버 오버레이
        if game_over:
            # 반투명 어두운 화면 연출
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            go_txt = font.render("GAME OVER", True, RED)
            retry_txt = font.render("retry", True, WHITE)

            screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(retry_txt, (WIDTH // 2 - retry_txt.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    state = "MENU"
    while True:
        if state == "MENU":
            state = show_menu()
        elif state == "PLAYING":
            state = run_game()


if __name__ == "__main__":
    main()