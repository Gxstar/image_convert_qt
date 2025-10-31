def get_exif_data(input_path):
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
    
    # 提取IPTC数据
    iptc_data = None
    # 查找IPTC数据块标记 (0x1C02)
    iptc_start = raw_data.find(b'\x1c\x02')
    if iptc_start != -1:
        # IPTC数据通常以0x1C开头，需要找到完整的数据块
        # 查找下一个标记或数据结束
        iptc_end = raw_data.find(b'\xff', iptc_start + 2)
        if iptc_end != -1:
            iptc_data = raw_data[iptc_start:iptc_end]
        else:
            # 如果没有找到结束标记，提取一定长度的数据
            iptc_data = raw_data[iptc_start:iptc_start+2000]
    
    # 如果第一种方法没找到，尝试查找Photoshop IPTC标记
    if iptc_data is None:
        photoshop_iptc_start = raw_data.find(b'Photoshop 3.0')
        if photoshop_iptc_start != -1:
            # 在Photoshop标记附近查找IPTC数据
            # IPTC数据通常在Photoshop标记后的特定位置
            search_start = max(0, photoshop_iptc_start - 100)
            search_end = min(len(raw_data), photoshop_iptc_start + 500)
            
            # 在搜索范围内查找IPTC标记
            for i in range(search_start, search_end - 4):
                if raw_data[i:i+2] == b'\x1c\x02':
                    iptc_end = raw_data.find(b'\xff', i + 2)
                    if iptc_end != -1:
                        iptc_data = raw_data[i:iptc_end]
                    else:
                        iptc_data = raw_data[i:i+2000]
                    break
        
    return exif_data, xmp_data, iptc_data