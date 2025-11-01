from PIL import Image
import pyexiv2
import io

def get_exif_data(input_path):
    # 从文件中读取EXIF数据
    try:
        # 1. 使用 pyexiv2 打开源文件
        with pyexiv2.Image(input_path, encoding='GBK') as img_src:
            
            # 2. 在内存中创建一个新的、极简的JPEG图片作为元数据的“容器”
            # 这个容器只用于传递元数据给Pillow，本身几乎不占空间
            # pyexiv2 需要一个有效的图片结构来写入元数据
            blank_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xda\x00\x08\x01\x01\x00\x00\x00\x00\x1f\xff\xd9'

            with pyexiv2.ImageData(data=blank_image_data) as img_target:
                # 3. 清理目标容器的元数据（虽然是空白的，但这是个好习惯）
                img_target.clear_exif()
                img_target.clear_iptc()
                img_target.clear_xmp()

                # 4. 将源文件的元数据复制到内存中的目标容器
                img_src.copy_to_another_image(img_target, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
                
                # 5. 从目标容器获取带有新元数据的图片字节流
                modified_image_bytes = img_target.get_bytes()

        # 6. 使用io.BytesIO将字节流包装成一个内存中的文件对象
        image_stream = io.BytesIO(modified_image_bytes)

        # 7. Pillow 从内存中的文件对象读取图片并获取EXIF
        with Image.open(image_stream) as exif_trans:
            exif_data = exif_trans.getexif()

        return exif_data

    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        return None