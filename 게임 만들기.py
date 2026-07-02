import pygame
import sys
import random

# 1. 초기화 및 창 설정
pygame.init()
screen_width = 450
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("나만 없어 고양이 🐈")
clock = pygame.time.Clock()

# 2. 색상 정의
BACKGROUND_COLOR = (255, 246, 230)  # 따뜻한 베이지색
TEXT_COLOR = (74, 61, 56)  # 딥 브라운
WHITE = (255, 255, 255)
BUTTON_COLOR = (255, 182, 193)  # 핑크색

# 폰트 설정 (한글 깨짐 방지)
try:
    font = pygame.font.SysFont("malgungothic", 20)
    title_font = pygame.font.SysFont("malgungothic", 26, bold=True)
    cat_font = pygame.font.SysFont("segoeuiemoji", 80)  # 고양이 이모지용
    effect_font = pygame.font.SysFont("segoeuiemoji", 24)
except:
    font = pygame.font.SysFont("arial", 20)
    title_font = pygame.font.SysFont("arial", 26)
    cat_font = pygame.font.SysFont("arial", 80)
    effect_font = pygame.font.SysFont("arial", 24)

# 3. 게임 상태 변수
happiness = 50  # 행복도 (0~100)
love_count = 0  # 쓰다듬은 횟수
cat_emoji = "🐱"  # 기본 고양이 상태
status_text = "고양이가 당신을 쳐다봅니다."

# 하트 이펙트 리스트 [(x, y, timer), ...]
hearts = []

# 버튼 영역 (간식 주기)
snack_button = pygame.Rect(150, 450, 150, 45)
# 고양이 클릭 영역 (가운데 배치)
cat_rect = pygame.Rect(165, 200, 120, 120)

# 4. 메인 루프
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # 시간의 흐름에 따라 행복도가 아주 천천히 감소 (1초에 약 1씩)
    # (60프레임 기준, 확률적으로 감소하게 만듦)
    if random.random() < 0.01 and happiness > 0:
        happiness -= 1
        if happiness < 30:
            cat_emoji = "😿"
            status_text = "고양이가 심심해서 시무룩해졌어요.."

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # 1) 고양이를 쓰다듬었을 때 (클릭)
            if cat_rect.collidepoint(mouse_pos):
                love_count += 1
                happiness = min(100, happiness + 5)
                cat_emoji = "😸"
                status_text = "골골골... 기분이 좋아 보입니다! 🐾"

                # 클릭한 위치 근처에 하트 이펙트 추가
                hearts.append([mouse_pos[0], mouse_pos[1], 30])

            # 2) 간식 주기 버튼을 눌렀을 때
            elif snack_button.collidepoint(mouse_pos):
                happiness = min(100, happiness + 15)
                cat_emoji = "😻"
                status_text = "냠냠! 최애 츄르를 먹고 행복해합니다!"

                # 버튼 위쪽에 하트 여러 개 생성
                for _ in range(3):
                    hearts.append([random.randint(150, 300), 380, 40])

    # 5. 이펙트 애니메이션 업데이트
    for heart in hearts[:]:
        heart[1] -= 2  # 위로 둥둥 떠오름
        heart[2] -= 1  # 타이머 감소
        if heart[2] <= 0:
            hearts.remove(heart)

    # 6. 화면 그리기 (렌더링)
    # 타이틀 및 상태창
    title_surf = title_font.render("방구석 야옹이 키우기 🐾", True, TEXT_COLOR)
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 40))

    status_surf = font.render(status_text, True, TEXT_COLOR)
    screen.blit(status_surf, (screen_width // 2 - status_surf.get_width() // 2, 100))

    # 행복도 바(Bar) 그리기
    bar_width = 200
    bar_height = 20
    bar_x = screen_width // 2 - bar_width // 2
    bar_y = 150
    # 배경 바 (회색)
    pygame.draw.rect(screen, (220, 220, 220), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
    # 채워지는 바 (핑크색, 행복도 비례)
    fill_width = int(bar_width * (happiness / 100))
    pygame.draw.rect(screen, (255, 105, 180), (bar_x, bar_y, fill_width, bar_height), border_radius=5)

    hp_text = font.render(f"행복도: {happiness}%", True, TEXT_COLOR)
    screen.blit(hp_text, (bar_x + bar_width + 10, bar_y - 2))

    # 고양이 그리기
    cat_surf = cat_font.render(cat_emoji, True, WHITE)
    screen.blit(cat_surf, (screen_width // 2 - cat_surf.get_width() // 2, 220))

    # 쓰다듬은 횟수 표시
    count_surf = font.render(f"집사의 손길: {love_count}번", True, TEXT_COLOR)
    screen.blit(count_surf, (screen_width // 2 - count_surf.get_width() // 2, 340))

    # 하트 이펙트 그리기
    for heart in hearts:
        heart_surf = effect_font.render("❤️", True, WHITE)
        screen.blit(heart_surf, (heart[0] - heart_surf.get_width() // 2, heart[1]))

    # 간식 주기 버튼 그리기
    pygame.draw.rect(screen, BUTTON_COLOR, snack_button, border_radius=15)
    btn_surf = font.render("츄르 주기 🐟", True, TEXT_COLOR)
    screen.blit(btn_surf,
                (snack_button.centerx - btn_surf.get_width() // 2, snack_button.centery - btn_surf.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()