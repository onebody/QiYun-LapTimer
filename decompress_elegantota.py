#!/usr/bin/env python3
import gzip
import io
import re
import sys

def extract_array_from_cpp(cpp_file_path):
    """从elop.cpp文件中提取ELEGANT_HTML数组数据"""
    with open(cpp_file_path, 'r') as f:
        content = f.read()
    
    # 查找数组定义
    pattern = r'const uint8_t ELEGANT_HTML\[10214\] PROGMEM = \{([^}]+)\};'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        # 尝试更宽松的匹配
        pattern = r'ELEGANT_HTML\[10214\] PROGMEM = \{([^}]+)\}'
        match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError("无法在文件中找到ELEGANT_HTML数组")
    
    array_content = match.group(1)
    
    # 提取所有数字
    numbers = []
    for line in array_content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # 移除行尾的逗号（如果有）
        if line.endswith(','):
            line = line[:-1]
        
        # 分割数字
        parts = line.split(',')
        for part in parts:
            part = part.strip()
            if part:
                try:
                    numbers.append(int(part))
                except ValueError:
                    # 忽略非数字部分
                    pass
    
    print(f"提取了 {len(numbers)} 个数字")
    return numbers

def decompress_gzip_data(byte_data):
    """解压缩gzip数据"""
    try:
        # 将字节数据转换为字节数组
        byte_array = bytes(byte_data)
        
        # 使用gzip解压缩
        decompressed = gzip.decompress(byte_array)
        
        return decompressed.decode('utf-8')
    except Exception as e:
        print(f"解压缩失败: {e}")
        # 尝试直接解码（可能不是gzip格式）
        try:
            return bytes(byte_data).decode('utf-8', errors='ignore')
        except:
            return None

def main():
    cpp_file_path = ".pio/libdeps/PhobosLT/ElegantOTA/src/elop.cpp"
    output_file = "elegantota_decompressed.html"
    
    print(f"从 {cpp_file_path} 提取数组数据...")
    
    try:
        # 提取数组数据
        numbers = extract_array_from_cpp(cpp_file_path)
        
        print(f"成功提取 {len(numbers)} 个数字")
        print(f"前10个数字: {numbers[:10]}")
        print(f"最后10个数字: {numbers[-10:]}")
        
        # 解压缩数据
        print("解压缩数据...")
        html_content = decompress_gzip_data(numbers)
        
        if html_content:
            print(f"解压缩成功，内容长度: {len(html_content)} 字符")
            
            # 保存到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"解压缩的HTML已保存到: {output_file}")
            
            # 分析WebSocket代码
            analyze_websocket_code(html_content)
        else:
            print("解压缩失败")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

def analyze_websocket_code(html_content):
    """分析HTML内容中的WebSocket代码"""
    print("\n分析WebSocket代码...")
    
    # 查找WebSocket相关代码
    websocket_patterns = [
        r'new WebSocket\([^)]+\)',
        r'\.send\([^)]+\)',
        r'\.readyState',
        r'CONNECTING|OPEN|CLOSING|CLOSED',
        r'\.onopen\s*=',
        r'\.onmessage\s*=',
        r'\.onerror\s*=',
        r'\.onclose\s*='
    ]
    
    found_patterns = []
    
    for pattern in websocket_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            found_patterns.append((pattern, matches))
    
    if found_patterns:
        print("找到WebSocket相关代码:")
        for pattern, matches in found_patterns:
            print(f"\n模式: {pattern}")
            print(f"匹配数: {len(matches)}")
            if len(matches) <= 5:  # 只显示前几个匹配
                for match in matches[:5]:
                    print(f"  - {match}")
            else:
                print(f"  - 显示前5个匹配:")
                for match in matches[:5]:
                    print(f"    {match}")
                print(f"  - ... 还有 {len(matches)-5} 个匹配")
    else:
        print("未找到WebSocket相关代码")
    
    # 查找可能的错误位置
    error_pattern = r'InvalidStateError|Still in CONNECTING state'
    error_matches = re.findall(error_pattern, html_content, re.IGNORECASE)
    if error_matches:
        print(f"\n找到错误模式: {error_pattern}")
        print(f"匹配: {error_matches}")
    
    # 查找send()调用
    send_pattern = r'\.send\([^)]+\)'
    send_matches = re.finditer(send_pattern, html_content)
    
    print("\n分析send()调用周围的代码:")
    for i, match in enumerate(list(send_matches)[:10]):  # 只检查前10个
        start = max(0, match.start() - 200)
        end = min(len(html_content), match.end() + 200)
        context = html_content[start:end]
        
        # 检查是否有readyState检查
        if 'readyState' not in context and 'OPEN' not in context:
            print(f"\n可能的问题send()调用 #{i+1}:")
            print(f"位置: {match.start()}-{match.end()}")
            print(f"上下文:\n{context}")
            print("-" * 80)

if __name__ == "__main__":
    main()
