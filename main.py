import machine
import utime
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd  # Using the corrected library
import urandom  # For generating random numbers
import array
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Initialization of the addressable RGB LED (WS2812)
# Инициализация адресного RGB-светодиода (WS2812)
# Inicialigo de adresebla RGB LED (WS2812)
NUM_LEDS = 1  # Number of LEDs
PIN_LED = 23  # Pin for controlling the LED (e.g., GPIO23)

# PIO program for controlling WS2812
# Программа PIO для управления WS2812
# PIO programo por kontroli WS2812
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

# Initialization of StateMachine for controlling the LED
# Инициализация StateMachine для управления светодиодом
# Inicialigo de StateMachine por kontroli la LED
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_LED))
sm.active(1)

# Array to store the LED color
# Массив для хранения цвета светодиода
# Arrayo por stoki la koloron de la LED
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

# Function to set the LED color in GRB format
# Функция для установки цвета светодиода в формате GRB
# Funkcio por agordi la koloron de la LED en GRB-formato
def set_color(red, green, blue):
    # GRB format
    color = (green << 16) | (red << 8) | blue
    for i in range(NUM_LEDS):
        ar[i] = color
    sm.put(ar, 8)

# Initialization of the LCD screen (I2C)
# Инициализация LCD экрана (I2C)
# Inicialigo de LCD ekrano (I2C)
I2C_ADDR = 0x27  # I2C address for LCD (usually 0x27 or 0x3F)
I2C_NUM_ROWS = 2  # Number of rows
I2C_NUM_COLS = 16  # Number of columns

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # GPIO0 (SDA), GPIO1 (SCL)

# Checking LCD connection
# Проверка подключения LCD
# Kontrolo de LCD konekto
lcd_connected = False
try:
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    lcd_connected = True
except Exception as e:
    print("LCD not connected or an error occurred:", e)
    set_color(255, 0, 255)  # Purple color (red + blue)
    utime.sleep(2)  # Delay to display the purple color
    # Terminate the program if the LCD is not connected
    # Завершаем выполнение программы, если LCD не подключён
    # Finu la programon se LCD ne estas konektita
    while True:
        pass  # Infinite loop to prevent the program from continuing

# Creating custom characters
# Создание пользовательских символов
# Kreado de propraj signoj
# Each character is defined as an array of 8 bytes (each byte is a row of 5 pixels)
# Каждый символ задаётся как массив из 8 байт (каждый байт — строка из 5 пикселей)
# Ĉiu signo estas difinita kiel tabelo de 8 bajtoj (ĉiu bajto estas vico de 5 rastrumeroj)
# 1. Line 8 pixels high
# Линия высотой 8 пикселей
# Linio 8 rastrumerojn alta
full_line = [
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111
]

# 2. Line 7 pixels high
# Линия высотой 7 пикселей
# Linio 7 rastrumerojn alta
seven_line = [
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b00000
]

# 3. Line 6 pixels high
# Линия высотой 6 пикселей
# Linio 6 rastrumerojn alta
six_line = [
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000
]

# 4. Line 5 pixels high
# Линия высотой 5 пикселей
# Linio 5 rastrumerojn alta
five_line = [
    0b01110,
    0b01110,
    0b01110,
    0b01110,
    0b01110,
    0b00000,
    0b00000,
    0b00000
]

# 5. Cursor
# Курсор
# Kursoro
coursor = [
    0b00100,
    0b01110,
    0b11011,
    0b10001,
    0b10001,
    0b11011,
    0b01110,
    0b00100
]

# Loading custom characters into LCD memory
# Загрузка пользовательских символов в память LCD
# Ŝargado de propraj signoj en LCD memoron
lcd.custom_char(0, full_line)  # Character 0: 8-pixel high line
lcd.custom_char(1, seven_line)  # Character 1: 7-pixel high line
lcd.custom_char(2, six_line)  # Character 2: 6-pixel high line
lcd.custom_char(3, five_line)  # Character 3: 5-pixel high line
lcd.custom_char(4, coursor)  # Cursor

# Initialization of the button
# Инициализация кнопки
# Inicialigo de butono
button = Pin(15, Pin.IN, Pin.PULL_UP)  # Button on GPIO15 with pull-up

# Turning on blue color during initialization (addressable LED)
# Включение синего цвета при инициализации (адресный светодиод)
# Ŝaltado de blua koloro dum inicialigo (adresebla LED)
print("Initializing... Blue color")
set_color(0, 0, 50)  # Blue color with low brightness
if lcd_connected:
    lcd.clear()
    lcd.move_to(0, 0)  # Move cursor to the first row
    lcd.putstr("Initializing...")  # Display message on LCD
utime.sleep(2)  # Delay to simulate initialization

# Turning on green color after initialization (addressable LED)
# Включение зелёного цвета по окончании инициализации (адресный светодиод)
# Ŝaltado de verda koloro post inicialigo (adresebla LED)
print("Initialization complete. Green color")
set_color(0, 50, 0)  # Green color with low brightness
if lcd_connected:
    lcd.clear()
    lcd.move_to(7, 0)  # Move cursor to the center of the first row (position 7)
    lcd.putstr("Wait")  # Display "Wait" in the center
    # Draw an improved scale in the bottom row
    # Рисуем улучшенную шкалу в нижней строке
    # Desegni plibonigitan skalon en la malsupra vico
    lcd.move_to(0, 1)  # Move cursor to the second row
    for i in range(16):
        if i in {6, 7, 8, 9}:  # Long lines at positions 6, 7, 8, 9
            lcd.putchar(chr(0))  # Use character 0 (8-pixel high line)
        elif i in {5, 10}:  # Medium lines at positions 5, 10
            lcd.putchar(chr(1))  # Use character 1 (7-pixel high line)
        elif i in {4, 11}:  # Medium lines at positions 5, 10
            lcd.putchar(chr(2))  # Use character 2 (6-pixel high line)
        else:  # Short lines at other positions
            lcd.putchar(chr(3))  # Use character 3 (5-pixel high line)

# Initialization of the array and variables
# Инициализация массива и переменных
# Inicialigo de tabelo kaj variabloj
array_size = 1600
data_array = [0] * array_size  # Array with 1600 cells
current_value = 0  # Variable for random number
average_value = 0  # Variable for arithmetic mean
array_filled = False  # Flag indicating if the array is filled
last_position = -1  # Last position of the rectangle (for optimization)

# Function to reset the array
# Функция для сброса массива
# Funkcio por restarigi la tabelon
def reset_array():
    global data_array, array_filled, last_position
    data_array = [0] * array_size  # Fill the array with zeros
    array_filled = False  # Reset the filled flag
    set_color(50, 0, 50)  # Purple color (array not filled)
    if lcd_connected:
        lcd.clear()
        lcd.move_to(7, 0)  # Move cursor to the center of the first row
        lcd.putstr("Wait")  # Display "Wait" in the center
        # Draw an improved scale in the bottom row
        # Рисуем улучшенную шкалу в нижней строке
        # Desegni plibonigitan skalon en la malsupra vico
        lcd.move_to(0, 1)  # Move cursor to the second row
        for i in range(16):
            if i in {6, 7, 8, 9}:  # Long lines at positions 6, 7, 8, 9
                lcd.putchar(chr(0))  # Use character 0 (8-pixel high line)
            elif i in {5, 10}:  # Medium lines at positions 5, 10
                lcd.putchar(chr(1))  # Use character 1 (7-pixel high line)
            elif i in {4, 11}:  # Medium lines at positions 5, 10
                lcd.putchar(chr(2))  # Use character 2 (6-pixel high line)
            else:  # Short lines at other positions
                lcd.putchar(chr(3))  # Use character 3 (5-pixel high line)
    last_position = -1  # Reset the last position

# Main program loop
# Основной цикл программы
# Ĉefa programciklo
while True:
    # Button press check
    # Проверка нажатия кнопки
    # Kontrolo de butona premo
    if button.value() == 0:  # If the button is pressed (logical 0)
        reset_array()  # Reset the array
        if lcd_connected:
            lcd.clear()
            lcd.move_to(0, 0)  # Move cursor to the first row
            lcd.putstr("Array reset!")  # Display reset message
            # Draw an improved scale in the bottom row
            # Рисуем улучшенную шкалу в нижней строке
            # Desegni plibonigitan skalon en la malsupra vico
            lcd.move_to(0, 1)  # Move cursor to the second row
            for i in range(16):
                if i in {6, 7, 8, 9}:  # Long lines at positions 6, 7, 8, 9
                    lcd.putchar(chr(0))  # Use character 0 (8-pixel high line)
                elif i in {5, 10}:  # Medium lines at positions 5, 10
                    lcd.putchar(chr(1))  # Use character 1 (7-pixel high line)
                elif i in {4, 11}:  # Medium lines at positions 5, 10
                    lcd.putchar(chr(2))  # Use character 2 (6-pixel high line)
                else:  # Short lines at other positions
                    lcd.putchar(chr(3))  # Use character 3 (5-pixel high line)
        #utime.sleep(1)  # Delay for debouncing
        if lcd_connected:
            lcd.clear()
            if array_filled:
                position = min(int(average_value / 100), 15)  # Limit position from 0 to 15
                lcd.move_to(position, 0)  # Move cursor to the desired position
                #lcd.putstr("\xFF")  # Display rectangle
                lcd.putchar(chr(4))
            else:
                lcd.move_to(7, 0)  # Move cursor to the center of the first row
                lcd.putstr("Wait")  # Display "Wait" in the center

    # Generate a random number from 1 to 1600
    # Генерация случайного числа от 1 до 1600
    # Generado de hazarda nombro de 1 ĝis 1600
    current_value = urandom.randint(1, 1600)

    # Shift the array to the right and add a new value
    # Сдвиг массива вправо и добавление нового значения
    # Ŝovi la tabelon dekstren kaj aldoni novan valoron
    if not array_filled:
        # If the array is not yet filled, add a new value
        # Если массив ещё не заполнен, добавляем новое значение
        # Se la tabelo ankoraŭ ne estas plena, aldoni novan valoron
        data_array.pop()  # Remove the last element
        data_array.insert(0, current_value)  # Add a new value at the beginning

        # Check if the array is filled
        # Проверка, заполнен ли массив
        # Kontroli ĉu la tabelo estas plena
        if data_array[-1] != 0:  # If the last element is no longer 0
            array_filled = True  # The array is filled
            set_color(0, 50, 0)  # Green color (array filled)
    else:
        # If the array is filled, just shift the values
        # Если массив заполнен, просто сдвигаем значения
        # Se la tabelo estas plena, simple ŝovi la valorojn
        data_array.pop()  # Remove the last element
        data_array.insert(0, current_value)  # Add a new value at the beginning

    # Calculate the arithmetic mean
    # Вычисление среднего арифметического
    # Kalkuli la aritmetikan meznombron
    average_value = sum(data_array) / array_size

    # Determine the position of the rectangle
    # Определение позиции прямоугольника
    # Determini la pozicion de la rektangulo
    if array_filled:
        position = min(int(average_value / 100), 15)  # Limit position from 0 to 15
        if position != last_position:  # Redraw only if the position has changed
            last_position = position
            if lcd_connected:
                lcd.clear()
                lcd.move_to(position, 0)  # Move cursor to the desired position
                #lcd.putstr("\xFF")  # Display rectangle
                lcd.putchar(chr(4))
                # Draw an improved scale in the bottom row
                # Рисуем улучшенную шкалу в нижней строке
                # Desegni plibonigitan skalon en la malsupra vico
                lcd.move_to(0, 1)  # Move cursor to the second row
                for i in range(16):
                    if i in {6, 7, 8, 9}:  # Long lines at positions 6, 7, 8, 9
                        lcd.putchar(chr(0))  # Use character 0 (8-pixel high line)
                    elif i in {5, 10}:  # Medium lines at positions 5, 10
                        lcd.putchar(chr(1))  # Use character 1 (7-pixel high line)
                    elif i in {4, 11}:  # Medium lines at positions 5, 10
                        lcd.putchar(chr(2))  # Use character 2 (6-pixel high line)
                    else:  # Short lines at other positions
                        lcd.putchar(chr(3))  # Use character 3 (5-pixel high line)
    else:
        if last_position != -1:  # Redraw only if the array is not filled
            last_position = -1
            if lcd_connected:
                lcd.clear()
                lcd.move_to(7, 0)  # Move cursor to the center of the first row
                lcd.putstr("Wait")  # Display "Wait" in the center

    # Indication of the array state (purple/green)
    # Индикация состояния массива (фиолетовый/зелёный)
# Indikado de la stato de la tabelo (purpura/verda)
    if not array_filled:
        # Purple color (red + blue)
        # Фиолетовый цвет (красный + синий)
        # Purpura koloro (ruĝa + blua)
        set_color(50, 0, 50)  # Purple color
    else:
        # Green color
        # Зелёный цвет
        # Verda koloro
        set_color(0, 50, 0)  # Green color
        # Draw an improved scale in the bottom row
        # Рисуем улучшенную шкалу в нижней строке
        # Desegni plibonigitan skalon en la malsupra vico
        lcd.move_to(0, 1)  # Move cursor to the second row
        for i in range(16):
            if i in {6, 7, 8, 9}:  # Long lines at positions 6, 7, 8, 9
                lcd.putchar(chr(0))  # Use character 0 (8-pixel high line)
            elif i in {5, 10}:  # Medium lines at positions 5, 10
                lcd.putchar(chr(1))  # Use character 1 (7-pixel high line)
            elif i in {4, 11}:  # Medium lines at positions 5, 10
                lcd.putchar(chr(2))  # Use character 2 (6-pixel high line)
            else:  # Short lines at other positions
                lcd.putchar(chr(3))  # Use character 3 (5-pixel high line)

    # Delay for 1 microsecond
    # Задержка на 1 микросекунду
    # Prokrasto de 1 mikrosekundo
    #utime.sleep_us(1)