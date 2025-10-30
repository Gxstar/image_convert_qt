import rawpy
import pillow_heif as ph


class ImageConverter:
    """图片转换器类，支持RAW文件转换为HEIF格式"""
    
    def __init__(self):
        self.supported_formats = ['heic', 'heif', 'avif']
    
    def convert_image(self, input_path, output_path, format_name='heic', quality=100, bit_depth=8):
        """
        转换图片格式
        
        Args:
            input_path: 输入RAW文件路径
            output_path: 输出文件路径
            format_name: 输出格式名称 ('heic', 'heif', 'avif')
            quality: 输出质量 (100为无损，对应-1；0-99为有损)
            bit_depth: 输出位深 (8、10或12)
            
        Returns:
            bool: 转换成功返回True，失败返回False
        """
        try:
            # 验证输入参数
            if not self._validate_input(input_path, output_path, format_name, bit_depth):
                return False
            
            # 提取元数据
            exif_data, xmp_data = self._extract_metadata(input_path)
            
            # 处理RAW图像
            image_data = self._process_raw_image(input_path, bit_depth)
            
            # 创建并保存HEIF文件
            return self._save_heif_file(image_data, output_path, format_name, quality, bit_depth, exif_data, xmp_data)
            
        except Exception as e:
            return False
    
    def _validate_input(self, input_path, output_path, format_name, bit_depth):
        """验证输入参数"""
        if format_name.lower() not in self.supported_formats:
            return False
        
        if bit_depth not in [8, 10, 12]:
            return False
            
        return True
    
    def _extract_metadata(self, input_path):
        """从RAW文件提取元数据"""
        with open(input_path, 'rb') as f:
            raw_data = f.read()
        
        # 提取EXIF数据
        exif_start = raw_data.find(b'\xff\xe1')
        if exif_start != -1:
            exif_length = int.from_bytes(raw_data[exif_start+2:exif_start+4], 'big')
            exif_data = raw_data[exif_start:exif_start+exif_length+2]
        else:
            exif_data = None
        
        # 提取XMP数据
        xmp_start = raw_data.find(b'http://ns.adobe.com/xap/1.0/')
        if xmp_start != -1:
            xmp_end = raw_data.find(b'\x00', xmp_start)
            if xmp_end != -1:
                xmp_data = raw_data[xmp_start:xmp_end]
            else:
                xmp_data = raw_data[xmp_start:xmp_start+5000]
        else:
            xmp_data = None
            
        return exif_data, xmp_data
    
    def _process_raw_image(self, input_path, bit_depth):
        """处理RAW图像"""
        img = rawpy.imread(input_path)
        
        # 对于8位、10位、12位输出，都使用16位RAW处理，让pillow_heif处理位深转换
        output_bps = 16
        
        t = img.postprocess(
            use_camera_wb=True,
            half_size=False,
            no_auto_bright=True,
            output_bps=output_bps
        )
        
        return t
    
    def _save_heif_file(self, image_data, output_path, format_name, quality, bit_depth, exif_data, xmp_data):
        """保存HEIF文件"""
        # 根据位深设置模式
        if bit_depth == 8:
            mode = "RGB"  # 8位输出
        else:
            mode = "RGB;16"  # 10位和12位输出
        
        # 处理quality参数：100对应无损（-1），0-99对应有损
        heif_quality = -1 if quality == 100 else quality
        
        # 对于12位输出，需要设置SAVE_HDR_TO_12_BIT选项
        if bit_depth == 12:
            ph.options.SAVE_HDR_TO_12_BIT = True
        
        heif_file = ph.from_bytes(
            mode=mode,
            size=(image_data.shape[1], image_data.shape[0]),
            data=bytes(image_data)
        )
        
        # 保存文件
        heif_file.save(output_path, 
                      quality=heif_quality,
                      exif=exif_data, 
                      xmp=xmp_data)
        
        return True


# 使用示例
if __name__ == "__main__":
    converter = ImageConverter()
    
    # 示例调用 - 8位输出
    success = converter.convert_image(
        input_path="test.RW2",
        output_path="output_8bit.heic",
        format_name="heic",
        quality=100,
        bit_depth=8
    )
    
    if success:
        print("8位图片转换成功")
    else:
        print("8位图片转换失败")
    
    # 示例调用 - 10位输出
    success = converter.convert_image(
        input_path="test.RW2",
        output_path="output_10bit.heic",
        format_name="heic",
        quality=100,
        bit_depth=10
    )
    
    if success:
        print("10位图片转换成功")
    else:
        print("10位图片转换失败")
    
    # 示例调用 - 12位输出
    success = converter.convert_image(
        input_path="test.RW2",
        output_path="output_12bit.heic",
        format_name="heic",
        quality=100,
        bit_depth=12
    )
    
    if success:
        print("12位图片转换成功")
    else:
        print("12位图片转换失败")
