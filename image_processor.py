"""
Скрипт для обработки изображений с использованием OpenCV.
Вариант 3: Выделение центральной области (ROI) и инверсия цветов.
"""

import cv2
import numpy as np
import os

def create_fallback_image(filename="test_image.jpg"):
    """Создает красивую тестовую картинку, если пользователь не добавил свою."""
    print("Создаем тестовое изображение...")
    # Создаем холст 600x800 с 3 цветовыми каналами (BGR)
    img = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Рисуем градиент и геометрические фигуры для наглядности
    for y in range(600):
        img[y, :] = [y % 255, 150, 255 - (y % 255)] # BGR
        
    cv2.circle(img, (400, 300), 150, (0, 255, 255), -1) # Желтый круг по центру
    cv2.imwrite(filename, img)
    return filename

def load_image(file_path: str):
    """Безопасно загружает изображение."""
    if not os.path.exists(file_path):
        print(f"[INFO] Файл {file_path} не найден.")
        create_fallback_image(file_path)
        
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError(f"Не удалось декодировать изображение: {file_path}")
        
    h, w, channels = img.shape
    print(f"[*] Изображение успешно загружено!")
    print(f"    Разрешение: {w}x{h} пикселей, Каналов: {channels}")
    return img

def process_roi_inversion(img, roi_width=300, roi_height=300):
    """
    Вариант 3: Выделяет центральную область и инвертирует цвета.
    """
    print(f"[*] Применяем эффект инверсии к области {roi_width}x{roi_height}...")
    
    # 1. Делаем копию, чтобы не портить оригинал
    result = img.copy()
    h, w = result.shape[:2]
    
    # 2. Находим координаты центра
    cy, cx = h // 2, w // 2
    
    # 3. Вычисляем координаты углов нашей области (ROI)
    # Используем max и min, чтобы рамка не вылезла за края картинки
    y1 = max(0, cy - roi_height // 2)
    y2 = min(h, cy + roi_height // 2)
    x1 = max(0, cx - roi_width // 2)
    x2 = min(w, cx + roi_width // 2)
    
    # 4. ВЫДЕЛЯЕМ ОБЛАСТЬ ИНТЕРЕСА (ROI) с помощью срезов NumPy
    roi = result[y1:y2, x1:x2]
    
    # 5. ИНВЕРСИЯ ЦВЕТА
    # Способ 1: Математический (255 - roi)
    # Способ 2: Встроенная функция OpenCV (bitwise_not) - она работает быстрее
    inverted_roi = cv2.bitwise_not(roi)
    
    # 6. Вставляем измененный кусок обратно в большую картинку
    result[y1:y2, x1:x2] = inverted_roi
    
    # 7. (Дополнительно) Рисуем зеленую рамку вокруг измененной зоны для красоты
    cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    return result

def main():
    """Главная функция скрипта."""
    original_path = 'test_image.jpg'
    result_path = 'result_variant3.jpg'
    
    try:
        # Загрузка
        img = load_image(original_path)
        
        # Обработка (Вариант 3)
        processed_img = process_roi_inversion(img)
        
        # Сохранение
        cv2.imwrite(result_path, processed_img)
        print(f"[*] Готово! Результат сохранен в файл: {result_path}")
        
    except Exception as e:
        print(f"[ОШИБКА]: {e}")

if __name__ == '__main__':
    main()
