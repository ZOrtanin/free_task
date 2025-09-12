import random
import os
from datetime import datetime
# from io import BytesIO
from PIL import Image
import numpy as np
from django.conf import settings
from django.core.files.base import ContentFile
import base64


def generate_avatar_image() -> ContentFile:
    arr = [[random.randint(0, 1) for _ in range(5)] for _ in range(10)]
    for i in range(len(arr)):
        arr[i] += arr[i][::-1]

    array = np.array(arr)
    arr_image = (array * 255).astype(np.uint8)
    image = Image.fromarray(arr_image)

    rgba_image = image.convert("RGBA")
    mask = rgba_image.convert("L").point(lambda x: 255 if x == 0 else 0, mode='1')
    new_img = Image.new("RGBA", rgba_image.size, (
        random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 255))
    new_img.paste(rgba_image, mask=mask)
    new_img = new_img.resize((200, 200), resample=Image.BOX)
    new_img.show()

    # # Путь и имя файла
    # if not filename:
    #     filename = f"temp_avatar_{datetime.now().timestamp()}.png"
    # path = os.path.join(settings.MEDIA_ROOT, 'avatars', filename)
    # os.makedirs(os.path.dirname(path), exist_ok=True)

    filename = f"temp_avatar_{datetime.now().timestamp()}.png"
    path = os.path.join(settings.MEDIA_ROOT, 'avatars', filename)

    # new_img.save('gfg_dummy_pic-'+str(random.randint(100, 255))+'.png')
    new_img.save(path)

    return os.path.join('avatars', filename)


def test_avatar():
    print('123jklasd')


def save_avatar_from_base64(base64_data, filename=None):
    if not base64_data.startswith('data:image'):
        raise ValueError("Invalid image data")
    
    # Извлекаем данные
    format, imgstr = base64_data.split(';base64,')
    ext = format.split('/')[-1]
    
    # Генерируем имя файла
    if not filename:
        import uuid
        filename = f'avatar_{uuid.uuid4().hex[:8]}.{ext}'
    
    # Полный путь для сохранения
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    os.makedirs(avatars_dir, exist_ok=True)  # Создаем папку если нет
    
    file_path = os.path.join(avatars_dir, filename)
    
    # Декодируем и сохраняем файл
    image_data = base64.b64decode(imgstr)
    
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    # Возвращаем относительный путь для БД
    return os.path.join('avatars', filename)