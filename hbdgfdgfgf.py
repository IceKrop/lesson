import pygame
import sys
import random
import string
import pyperclip

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Генератор сложных паролей")
clock = pygame.time.Clock()

# Цвета
BG_COLOR = (240, 244, 248)  # Светлый фон
TEXT_COLOR = (33, 37, 41)  # Темный текст
ACCENT_COLOR = (14, 116, 144)  # Сине-зеленый (ползунок и кнопка)
SLIDER_BG = (209, 213, 219)  # Серый трек ползунка
PANEL_BG = (255, 255, 255)  # Белая панель для пароля
BTN_HOVER = (8, 86, 107)  # Цвет кнопки при наведении

# Шрифты
FONT_MAIN = pygame.font.SysFont("Arial", 18, bold=True)
FONT_PASSWORD = pygame.font.SysFont("Courier New", 20, bold=True)
FONT_UI = pygame.font.SysFont("Arial", 16)

# Настройки ползунка (Slider)
SLIDER_X = 150
SLIDER_Y = 130
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 8
HANDLE_RADIUS = 12

MIN_LENGTH = 6
MAX_LENGTH = 30
current_length = 12  # Изначальная длина пароля


# Рассчитываем позицию ручки ползунка на основе длины
def get_handle_x(length):
    ratio = (length - MIN_LENGTH) / (MAX_LENGTH - MIN_LENGTH)
    return SLIDER_X + int(ratio * SLIDER_WIDTH)

# щавгвпавпа авовпапапаирвпа

# Рассчитываем длину пароля на основе позиции мыши
def get_length_from_x(x):
    x = max(SLIDER_X, min(x, SLIDER_X + SLIDER_WIDTH))
    ratio = (x - SLIDER_X) / SLIDER_WIDTH
    return int(MIN_LENGTH + ratio * (MAX_LENGTH - MIN_LENGTH))


handle_x = get_handle_x(current_length)
is_dragging = False

# Настройки кнопки
BTN_X, BTN_Y = 200, 180
BTN_WIDTH, BTN_HEIGHT = 200, 45

# Переменные для пароля
generated_password = ""
status_text = "Передвиньте ползунок и нажмите Сгенерировать"


def generate_complex_password(length):
    # Набор символов: буквы (верхний/нижний регистр), цифры и спецсимволы
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[{]};:,.<>?"

    # Гарантируем, что в пароле будет хотя бы по одному символу каждого типа
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()-_=+[{]};:,.<>?")
    ]

    # Добираем оставшуюся длину
    password += [random.choice(chars) for _ in range(length - 4)]

    # Перемешиваем, чтобы скрыть закономерность
    random.shuffle(password)
    return "".join(password)


# Главный цикл
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левый клик
                # Проверка клика по ручке ползунка
                distance = ((mouse_pos[0] - handle_x) ** 2 + (mouse_pos[1] - SLIDER_Y) ** 2) ** 0.5
                if distance <= HANDLE_RADIUS + 5:
                    is_dragging = True

                # Клик по кнопке генерации
                btn_rect = pygame.Rect(BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
                if btn_rect.collidepoint(mouse_pos):
                    generated_password = generate_complex_password(current_length)
                    pyperclip.copy(generated_password)  # Копируем в буфер обмена
                    status_text = "Пароль скопирован в буфер обмена!"

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False

    # Логика перетаскивания ползунка
    if is_dragging:
        handle_x = max(SLIDER_X, min(mouse_pos[0], SLIDER_X + SLIDER_WIDTH))
        current_length = get_length_from_x(handle_x)
        # Корректируем х, чтобы ручка не прыгала из-за округления шагов длины
        handle_x = get_handle_x(current_length)

    # --- Отрисовка интерфейса ---
    screen.fill(BG_COLOR)

    # 1. Текст длины пароля
    len_lbl = FONT_MAIN.render(f"Длина пароля: {current_length}", True, TEXT_COLOR)
    screen.blit(len_lbl, (WIDTH // 2 - len_lbl.get_width() // 2, 80))

    # 2. Отрисовка ползунка (трек)
    pygame.draw.rect(screen, SLIDER_BG, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT), border_radius=4)
    # Активная часть ползунка (до ручки)
    pygame.draw.rect(screen, ACCENT_COLOR, (SLIDER_X, SLIDER_Y, handle_x - SLIDER_X, SLIDER_HEIGHT), border_radius=4)
    # Ручка ползунка
    pygame.draw.circle(screen, ACCENT_COLOR, (handle_x, SLIDER_Y), HANDLE_RADIUS)
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, SLIDER_Y), HANDLE_RADIUS - 4)

    # 3. Отрисовка кнопки
    btn_rect = pygame.Rect(BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
    btn_color = BTN_HOVER if btn_rect.collidepoint(mouse_pos) else ACCENT_COLOR
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=8)

    btn_lbl = FONT_MAIN.render("Сгенерировать", True, (255, 255, 255))
    screen.blit(btn_lbl,
                (BTN_X + (BTN_WIDTH - btn_lbl.get_width()) // 2, BTN_Y + (BTN_HEIGHT - btn_lbl.get_height()) // 2))

    # 4. Поле вывода пароля (если он сгенерирован)
    if generated_password:
        panel_rect = pygame.Rect(50, 260, 500, 50)
        pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=6)
        pygame.draw.rect(screen, SLIDER_BG, panel_rect, width=2, border_radius=6)

        pass_text = FONT_PASSWORD.render(generated_password, True, ACCENT_COLOR)
        # Центрируем текст внутри панели
        screen.blit(pass_text, (WIDTH // 2 - pass_text.get_width() // 2, 273))

    # 5. Статусный текст вниз
    status_lbl = FONT_UI.render(status_text, True, (100, 116, 139))
    screen.blit(status_lbl, (WIDTH // 2 - status_lbl.get_width() // 2, 330))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()