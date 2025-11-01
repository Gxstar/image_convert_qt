from PIL import Image
import pyexiv2

def get_exif_data(input_path):
    # 从文件中读取EXIF数据
    # 通过一个中间图片来存储并输出来源图片的exif信息
    with pyexiv2.Image(input_path,encoding='GBK') as img1:
        with pyexiv2.Image('exif_trans.jpg',encoding='GBK') as img2:
            img2.clear_exif()
            img2.clear_iptc()
            img2.clear_xmp()
            img1.copy_to_another_image(img2, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
        exif_trans=Image.open('exif_trans.jpg')
        exif_data=exif_trans.getexif()
    return exif_data