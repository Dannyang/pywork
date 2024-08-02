from PIL import Image, ImageDraw, ImageFont
import copy


def add_text_and_extend_image(image_path, output_path, text_array):
    # 打开图像文件
    original_image = Image.open(image_path)
    width, height = original_image.size

    # 计算底部10%的高度
    bottom_10_height = int(height * 0.1)

    # 创建一个新的图像，其高度为原图像高度加上底部10%的高度乘以文本数组长度
    new_height = height + bottom_10_height * (len(text_array) - 1)
    new_image = Image.new('RGB', (width, new_height), (255, 255, 255))

    # 将原图粘贴到新图像的顶部
    # new_image.paste(original_image, (0, 0))
    font_path = r"C:\Users\Administrator\PycharmProjects\pythonProject1\my_pic\msyhbd.ttc"
    font_size = 60
    # 设置字体和字号
    font = ImageFont.truetype(font_path, size=font_size)  # 使用支持中文的字体

    original_bottom_10_image = original_image.crop((0, height - bottom_10_height, width, height))
    for i, text in enumerate(text_array):
        if i == 0:
            # 数组的第一个字符串写入到原图
            draw_text_bottom_10(original_image, font, text)
            # 并将写入字符串的原图粘贴在new_image的顶部
            new_image.paste(original_image, (0, 0))
        else:
            temp_image = copy.deepcopy(original_bottom_10_image)
            draw_text_middle(temp_image, font, text)
            # 将临时图像粘贴到新图像的相应位置
            new_image.paste(temp_image, (0, height + (i - 1) * bottom_10_height))
            # 保存新图像
    new_image.save(output_path)
    print(f"New image with text saved to {output_path}")


def draw_text_middle(image, font, text):
    draw = ImageDraw.Draw(image)
    # 获取文字的长宽
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    width, height = image.size
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill="white")


def draw_text_bottom_10(image, font, text):
    draw = ImageDraw.Draw(image)
    # 获取文字的长宽
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    width, height = image.size
    capture_height = int(height * 0.1)
    top = height - capture_height
    text_x = (width - text_width) / 2
    text_y = top + (capture_height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill="white")


# 调用函数
input_image_path = r'C:\Users\Administrator\PycharmProjects\pythonProject1\my_pic\5a594190f70a1efd6673916467ecf78f.jpg'
output_image_path = r'C:\Users\Administrator\PycharmProjects\pythonProject1\my_pic\output_image_with_text.jpg'
text_array = ["赢了会所嫩模", "输了下海干活", "我是西安龙哥", "你是个什么哥"]
add_text_and_extend_image(input_image_path, output_image_path, text_array)
