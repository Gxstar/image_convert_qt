import os
import cv2 as cv
import pillow_heif as ph

class ImageOutput:
    def __init__(self):
        pass
    
    def output(self,bgr,output_path,format_name,quality=85,bit_depth=8):
        bgr_16=bgr
        alpha_scale = 255.0 / 65535.0
        bgr_8 = cv.convertScaleAbs(bgr_16, alpha=alpha_scale)
        heif_file = ph.from_bytes(
                    mode="BGRA;16",
                    size=(bgr.shape[1], bgr.shape[0]),
                    data=bytes(bgr)
                )
        """输出图像"""
        # 输出图像，jpg、png、tiff、webp由opencv输出，heif、heic、avif由pillow_heif输出
        if format_name == 'jpg':
            cv.imwrite(
                output_path, bgr, [int(cv.IMWRITE_JPEG_QUALITY), quality]
            )
        elif format_name == 'webp':
            cv.imwrite(
                output_path, bgr,
                [int(cv.IMWRITE_WEBP_QUALITY), quality]
            )
        elif format_name == 'png':
            png_compression = int(9 - (quality / 100.0) * 9)
            png_compression = max(0, min(9, png_compression))  # 确保在0-9范围内
