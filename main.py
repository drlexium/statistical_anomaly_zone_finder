import machine
import utime
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import urandom
import array
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Конфигурация RGB-светодиода
NUM_LEDS = 1
PIN_LED = 23

# Программа PIO для управления WS2812
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1] 
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1] 
    jmp("bitloop")          .side(1)    [T2 - 1] 
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]

# Инициализация StateMachine для светодиода
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_LED))
sm.active(1)
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def set_color(red, green, blue):
    color = (green << 16) | (red << 8) | blue
    for i in range(NUM_LEDS):
        ar[i] = color
    sm.put(ar, 8)

# Конфигурация LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Проверка подключения LCD
lcd_connected = False
try:
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    lcd_connected = True
except Exception as e:
    print("LCD error:", e)
    set_color(255, 0, 255)
    utime.sleep(2)
    while True: 
        pass

# Пользовательские символы
full_line = [0b00100, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111]
seven_line = [0b00100, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b00000]
six_line = [0b00100, 0b01110, 0b01110, 0b01110, 0b01110, 0b01110, 0b00000, 0b00000]
five_line = [0b00100, 0b01110, 0b01110, 0b01110, 0b01110, 0b00000, 0b00000, 0b00000]
coursor = [0b00100, 0b01110, 0b11011, 0b10001, 0b10001, 0b11011, 0b01110, 0b00100]
coursor_calk = [0b00100, 0b01110, 0b10001, 0b01101, 0b11111, 0b11111, 0b01110, 0b00100]

# Загрузка символов в LCD
def init_custom_chars():
    lcd.custom_char(0, full_line)
    lcd.custom_char(1, seven_line)
    lcd.custom_char(2, six_line)
    lcd.custom_char(3, five_line)
    lcd.custom_char(4, coursor)
    lcd.custom_char(5, coursor_calk)

if lcd_connected:
    init_custom_chars()

# Инициализация кнопки
button = Pin(15, Pin.IN, Pin.PULL_UP)
last_button_press = 0
DOUBLE_CLICK_DELAY = 500  # Время для двойного нажатия в мс
stat_fullscreen = False  # Флаг полноэкранного режима статистики

# Функции для работы с LCD
def draw_scale():
    lcd.move_to(0, 1)
    for i in range(16):
        if i in {6,7,8,9}:
            lcd.putchar(chr(0))
        elif i in {5,10}:
            lcd.putchar(chr(1))
        elif i in {4,11}:
            lcd.putchar(chr(2))
        else:
            lcd.putchar(chr(3))

def show_wait_screen():
    lcd.clear()
    lcd.move_to(6, 0)
    lcd.putstr("Wait")
    draw_scale()

def show_position(position, is_deviation=False, show_letter=False, letter=""):
    global stat_fullscreen
    
    if stat_fullscreen:
        # Режим полноэкранной статистики
        lcd.clear()
        if array_filled:
            stat_str = f"Range:{most_common_bin*100+1}-{(most_common_bin+1)*100}"
            lcd.move_to(0, 0)
            lcd.putstr(stat_str[:16])
            
            count_str = f"Count:{value_counts[most_common_bin]}"
            lcd.move_to(0, 1)
            lcd.putstr(count_str[:16])
        else:
            lcd.move_to(0, 0)
            lcd.putstr("No data yet")
        return
    
    # Обычный режим
    lcd.clear()
    lcd.move_to(position, 0)
    lcd.putchar(chr(5) if is_deviation else chr(4))
    draw_scale()
    if show_letter:
        lcd.move_to(position, 1)
        lcd.putstr(letter)

# Инициализация массива и статистики
array_size = 1600
data_array = [0] * array_size
current_value = 0
average_value = 0
array_filled = False
last_position = -1

# Переменные для статистики
stat_window = 1600
stat_bins = 16
bin_size = 100
value_counts = [0] * stat_bins
most_common_bin = -1

# Переменные для отклонений
deviation_counter = 0
current_deviation_letter = ""
show_deviation_letter = False
last_deviation_position = -1
current_showing_letter = ""

def reset_array():
    global data_array, array_filled, last_position
    global deviation_counter, current_deviation_letter, show_deviation_letter, last_deviation_position
    global current_showing_letter, value_counts, most_common_bin
    
    data_array = [0] * array_size
    array_filled = False
    set_color(50, 0, 50)
    
    deviation_counter = 0
    current_deviation_letter = ""
    show_deviation_letter = False
    last_deviation_position = -1
    current_showing_letter = ""
    
    value_counts = [0] * stat_bins
    most_common_bin = -1
    
    if lcd_connected:
        show_wait_screen()
    last_position = -1

def get_deviation_letter(position):
    if position in {5,10}: return "E"
    elif position in {4,11}: return "D"
    elif position in {3,12}: return "C"
    elif position in {2,13}: return "B"
    elif position in {1,14}: return "A"
    elif position in {0,15}: return "S"
    return ""

def update_statistics(new_value):
    global value_counts, most_common_bin
    
    bin_num = min(new_value // bin_size, stat_bins - 1)
    value_counts[bin_num] += 1
    
    if array_filled:
        old_value = data_array[-1]
        old_bin = min(old_value // bin_size, stat_bins - 1)
        value_counts[old_bin] -= 1
    
    max_count = max(value_counts)
    most_common_bin = value_counts.index(max_count)

def get_statistics_string():
    bin_start = most_common_bin * bin_size + 1
    bin_end = (most_common_bin + 1) * bin_size
    return f"{bin_start}-{bin_end}:{value_counts[most_common_bin]}"

# Начальная инициализация
print("Initializing... Blue")
set_color(0, 0, 50)
if lcd_connected:
    show_wait_screen()
utime.sleep(2)

print("Initialization complete. Green")
set_color(0, 50, 0)
if lcd_connected:
    show_wait_screen()

# Основной цикл
while True:
    # Обработка кнопки
    if button.value() == 0:
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, last_button_press) < DOUBLE_CLICK_DELAY:
            # Двойное нажатие - переключаем режим
            stat_fullscreen = not stat_fullscreen
            if lcd_connected:
                if stat_fullscreen:
                    set_color(50, 50, 0)  # Желтый цвет в режиме статистики
                else:
                    set_color(0, 50, 0) if array_filled else set_color(50, 0, 50)
        else:
            # Одинарное нажатие - сброс массива
            reset_array()
        
        last_button_press = current_time
        utime.sleep_ms(200)  # Задержка для антидребезга

    # Генерация и обработка данных
    current_value = urandom.randint(1, 1600)
    
    if not array_filled:
        data_array.pop()
        data_array.insert(0, current_value)
        if data_array[-1] != 0:
            array_filled = True
            set_color(0, 50, 0)
    else:
        data_array.pop()
        data_array.insert(0, current_value)
    
    update_statistics(current_value)
    average_value = sum(data_array) / array_size

    # Обработка позиции и отклонений
    if array_filled:
        position = min(int(average_value / 100), 15)
        
        if position not in {6,7,8,9}:
            if position != last_deviation_position:
                deviation_counter = 0
                last_deviation_position = position
                if not current_showing_letter:
                    show_deviation_letter = False
            
            deviation_counter += 1
            current_deviation_letter = get_deviation_letter(position)
            
            if deviation_counter >= 16000:
                show_deviation_letter = True
                current_showing_letter = current_deviation_letter
        else:
            deviation_counter = 0
            if not current_showing_letter:
                show_deviation_letter = False
            last_deviation_position = -1
        
        # Обновление дисплея
        if position != last_position or show_deviation_letter:
            last_position = position
            if lcd_connected:
                is_dev = position not in {6,7,8,9} and deviation_counter > 0
                show_letter = show_deviation_letter or current_showing_letter
                letter = current_showing_letter if current_showing_letter else current_deviation_letter
                show_position(position, is_dev, show_letter, letter)
    else:
        if last_position != -1:
            last_position = -1
            deviation_counter = 0
            current_deviation_letter = ""
            show_deviation_letter = False
            last_deviation_position = -1
            current_showing_letter = ""
            if lcd_connected:
                show_wait_screen()

    # Короткая задержка для стабильности
    #utime.sleep_ms(10)
