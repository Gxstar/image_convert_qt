import os
import cv2 as cv
from PIL import Image
import pillow_heif as ph
import rawpy
import pyexiv2
from .get_exif import get_exif_data

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
        exif_data, xmp_data, iptc_data = get_exif_data(input_path)
        # 如果是raw的话使用rawpy读取数据
        if is_raw:
            with rawpy.imread(input_path) as raw:
                rgb = raw.postprocess(
                    use_camera_wb=True,
                    half_size=False,
                    no_auto_bright=True,
                    output_bps=16
                )
                # 根据得到的图像分别处理16位和8位图像
                bgr_16 = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)

                alpha_scale = 255.0 / 65535.0
                bgr_8 = cv.convertScaleAbs(bgr_16, alpha=alpha_scale)
                
                # 输出图像，jpg、png、tiff、webp由opencv输出，heif、heic、avif由pillow_heif输出
                if format_name == 'JPEG':
                    cv.imwrite(
                        output_path, bgr_8, [int(cv.IMWRITE_JPEG_QUALITY), quality]
                    )
                elif format_name == 'WEBP':
                    cv.imwrite(
                        output_path, bgr_8,
                        [int(cv.IMWRITE_WEBP_QUALITY), quality]
                    )
                elif format_name == 'PNG':
                    png_compression = int(9 - (quality / 100.0) * 9)
                    png_compression = max(0, min(9, png_compression))  # 确保在0-9范围内

                    cv.imwrite(
                        output_path, bgr_16 if bit_depth == 16 else bgr_8 , 
                        [int(cv.IMWRITE_PNG_COMPRESSION), png_compression]
                    )
                elif format_name == 'TIFF':
                    cv.imwrite(
                        output_path, bgr_16 if bit_depth == 16 else bgr_8,
                        [int(cv.IMWRITE_TIFF_COMPRESSION), 32946]
                    )
                elif format_name == 'AVIF':
                    # 处理输出avif格式，avif现在只提供8位输出
                    img = Image.fromarray(bgr_8)
                    img.save(output_path, format='AVIF', quality=-1 if quality==100 else quality,
                        exif=exif_data,
                        xmp=xmp_data,
                        iptc=iptc_data
                    )
                elif format_name in {'HEIC', 'HEIF'}:
                    # 处理输出heif格式
                    heif_file = ph.from_bytes(
                        mode="RGB;16",
                        size=(rgb.shape[1], rgb.shape[0]),
                        data=bytes(rgb)
                    )
                    if bit_depth==12:
                        ph.options.SAVE_HDR_TO_12_BIT = True
                        heif_file.save(output_path, quality=-1 if quality==100 else quality,
                            exif=exif_data,
                            xmp=xmp_data,
                            iptc=iptc_data
                        )
                    elif bit_depth==10:  
                        heif_file.save(output_path, quality=-1 if quality==100 else quality,
                            exif=exif_data,
                            xmp=xmp_data,
                            iptc=iptc_data
                        )
                    else:
                        ph.register_heif_opener()
                        img = Image.fromarray(bgr_8)
                        img.save(output_path, format='HEIF', quality=-1 if quality==100 else quality,
                            exif=exif_data,
                            xmp=xmp_data,
                            iptc=iptc_data
                        )
        else:
            rgb = cv.imread(input_path)
        if format_name not in ['AVIF', 'HEIC', 'HEIF']:
            with pyexiv2.Image(input_path,encoding='GBK') as img1:
                with pyexiv2.Image(output_path,encoding='GBK') as img2:
                    img1.copy_to_another_image(img2, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
        # else:
        #     with pyexiv2.Image(output_path,encoding='GBK') as img:
        #         img.modify_exif(exif_data)
        #         img.modify_xmp(xmp_data)
        #         img.modify_iptc(iptc_data)
        return (True,"转换成功")


        
