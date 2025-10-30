import os
import cv2 as cv
import pillow_heif as ph
import rawpy

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
        is_heic = ext in {'.heic', '.heif','.avif'}

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

                heif_file = ph.from_bytes(
                    mode="BGRA;16",
                    size=(bgr_16.shape[1], bgr_16.shape[0]),
                    data=bytes(bgr_16)
                )
                
                # 输出图像，jpg、png、tiff、webp由opencv输出，heif、heic、avif由pillow_heif输出
                if format_name == 'jpg':
                    cv.imwrite(
                        output_path, bgr_8, [int(cv.IMWRITE_JPEG_QUALITY), quality]
                    )
                elif format_name == 'webp':
                    cv.imwrite(
                        output_path, bgr_8,
                        [int(cv.IMWRITE_WEBP_QUALITY), quality]
                    )
                elif format_name == 'png':
                    png_compression = int(9 - (quality / 100.0) * 9)
                    png_compression = max(0, min(9, png_compression))  # 确保在0-9范围内

                    cv.imwrite(
                        output_path, bgr_16 if bit_depth == 16 else bgr_8 , 
                        [int(cv.IMWRITE_PNG_COMPRESSION), png_compression]
                    )
                elif format_name == 'tiff':
                    cv.imwrite(
                        output_path, bgr_16 if bit_depth == 16 else bgr_8,
                        [int(cv.IMWRITE_TIFF_COMPRESSION), 1]
                    )
                else:
                    heif_file.save(output_path)
        else:
            rgb = cv.imread(input_path)


        
