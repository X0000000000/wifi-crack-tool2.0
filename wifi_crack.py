#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi密码破解工具 2.0
WiFi Password Cracking Tool 2.0

警告：本工具仅供学习和授权测试使用！
WARNING: This tool is for educational and authorized testing purposes only!

未经授权访问他人网络是违法的！
Unauthorized access to networks is illegal!
"""

import argparse
import hashlib
import itertools
import string
import sys
import time
from pathlib import Path


class WiFiCracker:
    """WiFi密码破解工具主类 / Main WiFi Cracker Class"""
    
    def __init__(self, ssid):
        """
        初始化WiFi破解工具
        
        Args:
            ssid: WiFi网络名称 (SSID)
        """
        self.ssid = ssid
        self.attempts = 0
        self.start_time = None
        
    def hash_password(self, password):
        """
        使用PBKDF2算法哈希密码（类似WPA/WPA2）
        
        Args:
            password: 待测试的密码
            
        Returns:
            密码的哈希值
        """
        # 使用PBKDF2算法，类似实际WPA/WPA2
        # 迭代次数4096是WPA2标准
        return hashlib.pbkdf2_hmac(
            'sha1',
            password.encode('utf-8'),
            self.ssid.encode('utf-8'),
            4096,
            32
        ).hex()
    
    def _verify_password(self, password, target_hash=None):
        """
        验证密码是否正确
        
        Args:
            password: 待验证的密码
            target_hash: 目标哈希值（用于测试）
            
        Returns:
            True 如果密码正确，否则 False
        """
        self.attempts += 1
        
        # 如果提供了目标哈希，验证它
        if target_hash:
            return self.hash_password(password) == target_hash
        
        # 实际应用中，这里应该验证握手包
        # 这里返回False表示需要继续尝试
        return False
    
    def dictionary_attack(self, dictionary_file, target_hash=None):
        """
        字典攻击模式
        
        Args:
            dictionary_file: 字典文件路径
            target_hash: 目标哈希值（用于测试）
            
        Returns:
            找到的密码，或 None
        """
        print(f"\n[*] 开始字典攻击 / Starting dictionary attack")
        print(f"[*] SSID: {self.ssid}")
        print(f"[*] 字典文件 / Dictionary: {dictionary_file}")
        
        dict_path = Path(dictionary_file)
        if not dict_path.exists():
            print(f"[!] 错误：字典文件不存在 / Error: Dictionary file not found: {dictionary_file}")
            return None
        
        self.start_time = time.time()
        
        try:
            with open(dictionary_file, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    password = line.strip()
                    if not password:
                        continue
                    
                    if self._verify_password(password, target_hash):
                        elapsed = time.time() - self.start_time
                        print(f"\n[+] 成功！密码找到 / Success! Password found: {password}")
                        print(f"[+] 尝试次数 / Attempts: {self.attempts}")
                        print(f"[+] 耗时 / Time: {elapsed:.2f} 秒")
                        return password
                    
                    if self.attempts % 1000 == 0:
                        print(f"[*] 已尝试 / Tried: {self.attempts} 密码...")
                        
        except KeyboardInterrupt:
            print(f"\n[!] 用户中断 / User interrupted")
            return None
        
        elapsed = time.time() - self.start_time
        print(f"\n[-] 字典攻击失败 / Dictionary attack failed")
        print(f"[-] 尝试次数 / Attempts: {self.attempts}")
        print(f"[-] 耗时 / Time: {elapsed:.2f} 秒")
        return None
    
    def brute_force_attack(self, min_length=8, max_length=10, charset='digits', target_hash=None):
        """
        暴力破解模式
        
        Args:
            min_length: 最小密码长度
            max_length: 最大密码长度
            charset: 字符集类型 ('digits', 'lower', 'upper', 'alpha', 'alphanum', 'all')
            target_hash: 目标哈希值（用于测试）
            
        Returns:
            找到的密码，或 None
        """
        # 验证长度参数
        if min_length < 1 or max_length < 1:
            print(f"[!] 错误：密码长度必须为正数 / Error: Password length must be positive")
            return None
        
        if min_length > max_length:
            print(f"[!] 错误：最小长度不能大于最大长度 / Error: min_length cannot be greater than max_length")
            return None
        
        print(f"\n[*] 开始暴力破解 / Starting brute force attack")
        print(f"[*] SSID: {self.ssid}")
        print(f"[*] 密码长度范围 / Length range: {min_length}-{max_length}")
        print(f"[*] 字符集 / Charset: {charset}")
        
        # 定义字符集
        charsets = {
            'digits': string.digits,
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'alpha': string.ascii_letters,
            'alphanum': string.ascii_letters + string.digits,
            'all': string.ascii_letters + string.digits + string.punctuation
        }
        
        if charset not in charsets:
            print(f"[!] 错误：无效的字符集 / Error: Invalid charset")
            return None
        
        chars = charsets[charset]
        print(f"[*] 使用字符 / Using characters: {chars[:20]}{'...' if len(chars) > 20 else ''}")
        
        self.start_time = time.time()
        
        try:
            for length in range(min_length, max_length + 1):
                print(f"\n[*] 尝试长度 / Trying length: {length}")
                
                for combo in itertools.product(chars, repeat=length):
                    password = ''.join(combo)
                    
                    if self._verify_password(password, target_hash):
                        elapsed = time.time() - self.start_time
                        print(f"\n[+] 成功！密码找到 / Success! Password found: {password}")
                        print(f"[+] 尝试次数 / Attempts: {self.attempts}")
                        print(f"[+] 耗时 / Time: {elapsed:.2f} 秒")
                        return password
                    
                    if self.attempts % 10000 == 0:
                        print(f"[*] 已尝试 / Tried: {self.attempts} 密码...")
                        
        except KeyboardInterrupt:
            print(f"\n[!] 用户中断 / User interrupted")
            return None
        
        elapsed = time.time() - self.start_time
        print(f"\n[-] 暴力破解失败 / Brute force attack failed")
        print(f"[-] 尝试次数 / Attempts: {self.attempts}")
        print(f"[-] 耗时 / Time: {elapsed:.2f} 秒")
        return None


def create_sample_dictionary():
    """创建示例字典文件 / Create sample dictionary file"""
    sample_passwords = [
        '12345678', 'password', '123456789', '12345678910',
        'qwerty123', 'abc123456', 'password123', 'admin123',
        '11111111', '88888888', '66668888', 'test1234',
        'welcome123', 'password1', 'admin888', 'root1234'
    ]
    
    dict_file = Path('sample_dictionary.txt')
    with open(dict_file, 'w', encoding='utf-8') as f:
        for pwd in sample_passwords:
            f.write(f"{pwd}\n")
    
    print(f"[+] 创建示例字典 / Sample dictionary created: {dict_file}")
    return str(dict_file)


def main():
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description='WiFi密码破解工具 2.0 / WiFi Password Cracking Tool 2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例 / Examples:
  # 字典攻击 / Dictionary attack
  python wifi_crack.py -s MyWiFi -m dictionary -d passwords.txt
  
  # 暴力破解（纯数字，8位） / Brute force (digits only, 8 chars)
  python wifi_crack.py -s MyWiFi -m brute -l 8 -L 8 -c digits
  
  # 创建示例字典 / Create sample dictionary
  python wifi_crack.py --create-dict

警告 / WARNING:
本工具仅供学习和授权测试使用！
This tool is for educational and authorized testing purposes only!
未经授权访问他人网络是违法的！
Unauthorized access to networks is illegal!
        '''
    )
    
    parser.add_argument('-s', '--ssid', help='目标WiFi网络名称 / Target WiFi SSID')
    parser.add_argument('-m', '--mode', choices=['dictionary', 'brute'], 
                        help='攻击模式 / Attack mode')
    parser.add_argument('-d', '--dictionary', help='字典文件路径 / Dictionary file path')
    parser.add_argument('-l', '--min-length', type=int, default=8, 
                        help='最小密码长度 / Minimum password length (default: 8)')
    parser.add_argument('-L', '--max-length', type=int, default=8, 
                        help='最大密码长度 / Maximum password length (default: 8)')
    parser.add_argument('-c', '--charset', 
                        choices=['digits', 'lower', 'upper', 'alpha', 'alphanum', 'all'],
                        default='digits',
                        help='字符集 / Character set (default: digits)')
    parser.add_argument('--test-password', help='测试密码（用于演示） / Test password (for demo)')
    parser.add_argument('--create-dict', action='store_true', 
                        help='创建示例字典文件 / Create sample dictionary file')
    
    args = parser.parse_args()
    
    # 创建示例字典
    if args.create_dict:
        create_sample_dictionary()
        return
    
    # 检查必需参数
    if not args.ssid or not args.mode:
        parser.print_help()
        return
    
    # 显示警告
    print("\n" + "="*70)
    print("警告 / WARNING".center(70))
    print("="*70)
    print("本工具仅供学习和授权测试使用！")
    print("This tool is for educational and authorized testing purposes only!")
    print("未经授权访问他人网络是违法的！")
    print("Unauthorized access to networks is illegal!")
    print("="*70)
    
    # 创建破解器实例
    cracker = WiFiCracker(args.ssid)
    
    # 如果提供了测试密码，计算其哈希
    target_hash = None
    if args.test_password:
        target_hash = cracker.hash_password(args.test_password)
        print(f"\n[*] 测试模式 / Test mode: 目标密码 / Target password: {args.test_password}")
    
    # 执行相应的攻击模式
    result = None
    if args.mode == 'dictionary':
        if not args.dictionary:
            print("[!] 错误：字典攻击需要指定字典文件 / Error: Dictionary file required")
            return
        result = cracker.dictionary_attack(args.dictionary, target_hash)
    
    elif args.mode == 'brute':
        result = cracker.brute_force_attack(
            args.min_length, 
            args.max_length, 
            args.charset,
            target_hash
        )
    
    # 显示结果
    if result:
        print(f"\n{'='*70}")
        print(f"[+] 破解成功 / Cracking successful!")
        print(f"[+] SSID: {args.ssid}")
        print(f"[+] 密码 / Password: {result}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}")
        print(f"[-] 破解失败 / Cracking failed")
        print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
