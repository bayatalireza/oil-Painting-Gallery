from django.core.exceptions import ValidationError
from PIL import Image
def validate_artwork_image(image):
max_size = 5 * 1024 * 1024
if image.size > max_size:
raise ValidationError('حجم تصویر نباید بیشتر از ۵ مگابایت باشد.')
valid_ext = ('.jpg', '.jpeg', '.png', '.webp')
if not image.name.lower().endswith(valid_ext):
raise ValidationError('فقط فرمت‌های jpg, png, webp مجاز هستند.')
try:
img = Image.open(image)
img.verify()
except:
raise ValidationError('فایل تصویر خراب است.')