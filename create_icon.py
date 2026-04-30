from PIL import Image, ImageDraw

# Создаём иконку 256x256
size = 256
img = Image.new('RGB', (size, size), color='#0f0f1a')
draw = ImageDraw.Draw(img)

# Рисуем щит
draw.ellipse((size//4, size//4, size*3//4, size*3//4), fill='#00d4ff')
draw.ellipse((size//4+20, size//4+20, size*3//4-20, size*3//4-20), fill='#0f0f1a')

# Рисуем букву "NG"
draw.text((size//2-45, size//2-30), "N", fill='#00d4ff', size=80)
draw.text((size//2+10, size//2-30), "G", fill='#00d4ff', size=80)

# Сохраняем
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
print("✅ Иконка создана: icon.ico")