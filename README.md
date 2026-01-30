# WiFi密码破解工具 2.0 / WiFi Password Cracking Tool 2.0

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](LICENSE)

一个用于教育和授权安全测试的WiFi密码破解工具。

A WiFi password cracking tool for educational and authorized security testing purposes.

## ⚠️ 重要警告 / Important Warning

**本工具仅供学习和授权测试使用！**  
**This tool is for educational and authorized testing purposes only!**

**未经授权访问他人网络是违法的！**  
**Unauthorized access to networks is illegal!**

使用本工具前，请确保：
- 您拥有目标网络的所有权或明确的书面授权
- 您了解并遵守当地的法律法规
- 您理解网络安全测试的道德规范

Before using this tool, make sure:
- You own the target network or have explicit written authorization
- You understand and comply with local laws and regulations
- You understand the ethical standards of network security testing

## 功能特性 / Features

- ✅ **字典攻击 / Dictionary Attack**: 使用密码字典进行快速测试
- ✅ **暴力破解 / Brute Force**: 支持多种字符集的暴力破解
- ✅ **多字符集支持 / Multiple Charsets**: 数字、字母、字母数字、全字符
- ✅ **进度显示 / Progress Display**: 实时显示破解进度
- ✅ **性能统计 / Performance Stats**: 显示尝试次数和耗时
- ✅ **中断恢复 / Interrupt Support**: 支持 Ctrl+C 安全中断

## 安装 / Installation

### 前置要求 / Prerequisites

- Python 3.6 或更高版本 / Python 3.6 or higher

### 克隆仓库 / Clone Repository

```bash
git clone https://github.com/X0000000000/wifi-crack-tool2.0.git
cd wifi-crack-tool2.0
```

### 使工具可执行 / Make Tool Executable

```bash
chmod +x wifi_crack.py
```

## 使用方法 / Usage

### 基本语法 / Basic Syntax

```bash
python wifi_crack.py [选项] / [options]
```

### 命令行选项 / Command Line Options

| 选项 / Option | 说明 / Description |
|--------------|-------------------|
| `-s, --ssid` | 目标WiFi网络名称 / Target WiFi SSID |
| `-m, --mode` | 攻击模式: `dictionary` 或 `brute` / Attack mode: `dictionary` or `brute` |
| `-d, --dictionary` | 字典文件路径 / Dictionary file path |
| `-l, --min-length` | 最小密码长度（默认：8）/ Minimum password length (default: 8) |
| `-L, --max-length` | 最大密码长度（默认：8）/ Maximum password length (default: 8) |
| `-c, --charset` | 字符集类型 / Character set type |
| `--test-password` | 测试密码（用于演示）/ Test password (for demo) |
| `--create-dict` | 创建示例字典文件 / Create sample dictionary file |

### 字符集类型 / Character Set Types

- `digits`: 纯数字 0-9 / Digits only (0-9)
- `lower`: 小写字母 a-z / Lowercase letters (a-z)
- `upper`: 大写字母 A-Z / Uppercase letters (A-Z)
- `alpha`: 所有字母 a-zA-Z / All letters (a-zA-Z)
- `alphanum`: 字母+数字 / Letters + digits
- `all`: 所有可打印字符 / All printable characters

## 使用示例 / Examples

### 1. 创建示例字典 / Create Sample Dictionary

```bash
python wifi_crack.py --create-dict
```

### 2. 字典攻击（测试模式）/ Dictionary Attack (Test Mode)

```bash
python wifi_crack.py -s MyWiFi -m dictionary -d sample_dictionary.txt --test-password 12345678
```

### 3. 暴力破解（纯数字，8位）/ Brute Force (Digits, 8 chars)

```bash
python wifi_crack.py -s MyWiFi -m brute -l 8 -L 8 -c digits --test-password 12345678
```

### 4. 暴力破解（小写字母，4-6位）/ Brute Force (Lowercase, 4-6 chars)

```bash
python wifi_crack.py -s MyWiFi -m brute -l 4 -L 6 -c lower --test-password test
```

### 5. 使用自定义字典 / Use Custom Dictionary

```bash
python wifi_crack.py -s MyWiFi -m dictionary -d /path/to/your/passwords.txt
```

## 输出示例 / Output Example

```
======================================================================
                          警告 / WARNING                            
======================================================================
本工具仅供学习和授权测试使用！
This tool is for educational and authorized testing purposes only!
未经授权访问他人网络是违法的！
Unauthorized access to networks is illegal!
======================================================================

[*] 测试模式 / Test mode: 目标密码 / Target password: 12345678

[*] 开始字典攻击 / Starting dictionary attack
[*] SSID: MyWiFi
[*] 字典文件 / Dictionary: sample_dictionary.txt

[+] 成功！密码找到 / Success! Password found: 12345678
[+] 尝试次数 / Attempts: 1
[+] 耗时 / Time: 0.00 秒

======================================================================
[+] 破解成功 / Cracking successful!
[+] SSID: MyWiFi
[+] 密码 / Password: 12345678
======================================================================
```

## 工作原理 / How It Works

### 字典攻击 / Dictionary Attack

1. 从字典文件读取密码候选
2. 对每个候选密码进行哈希计算
3. 与目标哈希值比对
4. 找到匹配项则返回密码

### 暴力破解 / Brute Force

1. 根据字符集生成所有可能的组合
2. 按长度递增顺序尝试
3. 对每个组合进行哈希计算
4. 找到匹配项则返回密码

## 性能考虑 / Performance Considerations

- **字典攻击**通常更快，适合常见密码
- **暴力破解**计算密集，长密码需要大量时间
- 8位纯数字密码：100,000,000 种可能
- 8位字母数字密码：218,340,105,584,896 种可能

## 技术细节 / Technical Details

- 使用 SHA-256 进行密码哈希（简化版）
- 实际 WPA/WPA2 使用 PBKDF2 算法
- 支持自定义字符集和长度范围
- 包含进度监控和性能统计

## 法律声明 / Legal Disclaimer

本工具的开发者不对任何非法使用本工具的行为负责。使用者必须：

The developers of this tool are not responsible for any illegal use. Users must:

1. 仅在自己拥有或已获授权的网络上使用 / Only use on networks you own or are authorized to test
2. 遵守所有适用的法律法规 / Comply with all applicable laws and regulations
3. 承担所有使用本工具的责任 / Take full responsibility for use of this tool

## 贡献 / Contributing

欢迎贡献！请确保：
- 代码符合 PEP 8 规范
- 添加适当的注释和文档
- 遵守道德和法律准则

Contributions welcome! Please ensure:
- Code follows PEP 8 style
- Includes appropriate comments and documentation
- Adheres to ethical and legal guidelines

## 许可证 / License

本项目仅供教育目的使用。严禁用于非法活动。

This project is for educational purposes only. Illegal use is strictly prohibited.

## 联系方式 / Contact

如有问题或建议，请提交 Issue。

For questions or suggestions, please submit an Issue.

---

**再次提醒：请负责任地使用本工具！**  
**Remember: Use this tool responsibly!**
