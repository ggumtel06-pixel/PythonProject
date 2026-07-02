import pygame
import sys

# 1. 초기화 및 창 설정
pygame.init()
screen_width = 400
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("마음 챙김 화분 키우기 🌿")
clock = pygame.time.Clock()

# 2. 색상 및 폰트 정의
BACKGROUND_COLOR = (224, 242, 254)  # 연한 하늘색
POT_COLOR = (205, 133, 63)  # 황토색 화분
TEXT_COLOR = (51, 65, 85)  # 짙은 회색
WHITE = (255, 255, 255)

# 시스템 폰트 설정 (한글 깨짐 방지)
try:
    font = pygame.font.SysFont("malgungothic", 20)
    title_font = pygame.font.SysFont("malgungothic", 28, bold=True)
    emoji_font = pygame.font.SysFont("segoeuiemoji", 60)  # 이모지용 폰트
except:
    font = pygame.font.SysFont("arial", 20)
    title_font = pygame.font.SysFont("arial", 28)
    emoji_font = pygame.font.SysFont("arial", 60)

# 3. 게임 상태 변수
clicks = 0
status_text = "아직은 작은 흙더미입니다."
plant_emoji = "🌱"

# 물방울 이펙트 리스트 [(x, y), ...]
water_drops = []

# 버튼 영역 (x, y, width, height)
button_rect = pygame.Rect(130, 400, 140, 45)

# 4. 메인 게임 루프
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # 버튼을 클릭했을 때
            if button_rect.collidepoint(mouse_pos):
                clicks += 1
                # 새로운 물방울 생성 (화분 위쪽 랜덤 위치)
                water_drops.append([200, 150])

                # 성장 단계별 업데이트
                if clicks >= 12:
                    plant_emoji = "🌸"
                    status_text = "와아! 예쁜 꽃이 피어났습니다!"
                elif clicks >= 7:
                    plant_emoji = "🌳"
                    status_text = "제법 든든한 나무가 되었네요!"
                elif clicks >= 3:
                    plant_emoji = "🌿"
                    status_text = "조금씩 줄기가 자라나고 있어요."

    # 5. 물방울 애니메이션 업데이트
    for drop in water_drops[:]:
        drop[1] += 5  # 아래로 떨어짐
        if drop[1] > 320:  # 화분에 닿으면 소멸
            water_drops.remove(drop)

    # 6. 화면 그리기 (렌더링)
    # 타이틀 및 텍스트
    title_surf = title_font.render("나만의 작은 정원", True, TEXT_COLOR)
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 40))

    status_surf = font.render(status_text, True, TEXT_COLOR)
    screen.blit(status_surf, (screen_width // 2 - status_surf.get_width() // 2, 90))

    # 클릭 횟수 표시
    count_surf = font.render(f" 준 수분량: {clicks} 💧", True, TEXT_COLOR)
    screen.blit(count_surf, (screen_width // 2 - count_surf.get_width() // 2, 130))

    # 식물 (이모지 텍스트로 대체)
    plant_surf = emoji_font.render(plant_emoji, True, WHITE)
    screen.blit(plant_surf, (screen_width // 2 - plant_surf.get_width() // 2, 240))

    # 화분 그리기 (다각형)
    pot_points = [(150, 320), (250, 320), (230, 370), (170, 370)]
    pygame.draw.polygon(screen, POT_COLOR, pot_points)

    # 떨어지는 물방울 그리기
    for drop in water_drops:
        drop_surf = font.render("💧", True, WHITE)
        screen.blit(drop_surf, (drop[0] - drop_surf.get_width() // 2, drop[1]))

    # 물주기 버튼 그리기
    pygame.draw.rect(screen, (56, 189, 248), button_rect, border_radius=10)
    btn_surf = font.render("물 주기 💧", True, WHITE)
    screen.blit(btn_surf,
                (button_rect.centerx - btn_surf.get_width() // 2, button_rect.centery - btn_surf.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

