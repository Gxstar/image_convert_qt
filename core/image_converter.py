import os
import cv2 as cv
from PIL import Image
from PIL.ExifTags import TAGS
import pillow_heif as ph
import rawpy
import pyexiv2
from .get_exif import get_exif_data

ph.register_heif_opener()

class ImageConverter:
    def __init__(self):
        pass

    def convert(self, input_path, output_path, format_name, quality=85, bit_depth=8):
        """转换图像格式"""
        # 判断输入类型是raw还是普通图片
        raw_extensions = {
            '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2',
            '.dng', '.orf', '.rw2', '.rwl', '.pef', '.ptx',
            '.3fr', '.fff', '.mef', '.mos', '.erf', '.dcr', '.kdc',
            '.raw', '.raf', '.x3f', '.iiq'
        }
        ext = os.path.splitext(input_path)[1].lower()
        is_raw = ext in raw_extensions
        # 如果是raw的话使用rawpy读取数据
        if is_raw:
            # 特殊处理raw的exif信息提取
            exif_data = get_exif_data(input_path)
            with rawpy.imread(input_path) as raw:
                rgb = raw.postprocess(
                    use_camera_wb=True,
                    half_size=False,
                    no_auto_bright=True,
                    output_bps=16
                )
                # 根据得到的图像分别处理16位和8位图像
                bgr_16 = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
                
                # 输出图像
                if bit_depth==8:
                    bgr_8 = raw.postprocess(
                        use_camera_wb=True,
                        half_size=False,
                        no_auto_bright=True,
                        output_bps=8
                    )
                    img_8=Image.fromarray(bgr_8)
                    if format_name not in {'HEIC','HEIF','AVIF'}:
                        img_8.save(output_path, quality=-1 if quality==100 else quality
                        )
                        with pyexiv2.Image(input_path,encoding='GBK') as img1:
                            with pyexiv2.Image(output_path,encoding='GBK') as img2:
                                img1.copy_to_another_image(img2, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
                    elif format_name in {'HEIC','HEIF','AVIF'}:
                        img_8.save(output_path, quality=-1 if quality==100 else quality,
                            exif=exif_data
                        )
                elif bit_depth>8 and format_name in {'HEIC', 'HEIF'}:
                    # 处理输出heif格式
                    heif_file = ph.from_bytes(
                        mode="RGB;16",
                        size=(rgb.shape[1], rgb.shape[0]),
                        data=bytes(rgb)
                    )
                    if bit_depth==12:
                        ph.options.SAVE_HDR_TO_12_BIT = True
                        heif_file.save(output_path, quality=-1 if quality==100 else quality,
                            exif=exif_data
                        )
                    else:  
                        heif_file.save(output_path, quality=-1 if quality==100 else quality,
                            exif=exif_data
                        )
                elif bit_depth>8 and format_name in {'PNG','TIFF'}:
                    # 处理输出png、tiff格式
                    cv.imwrite(output_path, bgr_16,
                        [int(cv.IMWRITE_PNG_COMPRESSION), 9] if format_name=='PNG' else
                        [int(cv.IMWRITE_TIFF_COMPRESSION), 32946]
                    )
                    with pyexiv2.Image(input_path,encoding='GBK') as img1:
                        with pyexiv2.Image(output_path,encoding='GBK') as img2:
                            img1.copy_to_another_image(img2, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
        else:
            img = Image.open(input_path)
            # 对于非RAW格式，使用Pillow进行转换
            # Pillow会根据output_path的后缀名自动判断格式，无需指定format参数
            if format_name in {'JPEG', 'WEBP', 'AVIF', 'HEIC', 'HEIF'}:
                # 这些格式支持quality参数
                img.save(output_path, quality=-1 if quality==100 else quality, exif=img.getexif())
            else:
                # 其他格式（PNG、TIFF等）不需要quality参数
                img.save(output_path, exif=img.getexif())

        return (True,"转换成功")


        
