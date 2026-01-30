# 使用示例 / Usage Examples

本文档提供了 WiFi密码破解工具 2.0 的详细使用示例。

This document provides detailed usage examples for WiFi Password Cracking Tool 2.0.

## 目录 / Table of Contents

1. [基本使用 / Basic Usage](#基本使用--basic-usage)
2. [字典攻击示例 / Dictionary Attack Examples](#字典攻击示例--dictionary-attack-examples)
3. [暴力破解示例 / Brute Force Examples](#暴力破解示例--brute-force-examples)
4. [性能测试 / Performance Tests](#性能测试--performance-tests)
5. [常见问题 / Common Issues](#常见问题--common-issues)

## 基本使用 / Basic Usage

### 查看帮助信息 / View Help

```bash
python wifi_crack.py --help
```

### 创建示例字典 / Create Sample Dictionary

```bash
python wifi_crack.py --create-dict
```

这会创建一个 `sample_dictionary.txt` 文件，包含常见密码。

This creates a `sample_dictionary.txt` file with common passwords.

## 字典攻击示例 / Dictionary Attack Examples

### 示例 1: 使用示例字典（测试模式）

Example 1: Using Sample Dictionary (Test Mode)

```bash
# 首先创建示例字典
python wifi_crack.py --create-dict

# 运行字典攻击
python wifi_crack.py -s MyWiFi -m dictionary -d sample_dictionary.txt --test-password 12345678
```

**预期输出 / Expected Output:**
```
[*] 测试模式 / Test mode: 目标密码 / Target password: 12345678
[*] 开始字典攻击 / Starting dictionary attack
[*] SSID: MyWiFi
[*] 字典文件 / Dictionary: sample_dictionary.txt

[+] 成功！密码找到 / Success! Password found: 12345678
[+] 尝试次数 / Attempts: 1
[+] 耗时 / Time: 0.00 秒
```

### 示例 2: 使用自定义字典

Example 2: Using Custom Dictionary

首先创建自定义字典文件：

First create a custom dictionary file:

```bash
cat > my_passwords.txt << EOF
password123
admin2024
welcome123
test12345
qwerty2024
mypassword
secure123
EOF
```

然后运行攻击：

Then run the attack:

```bash
python wifi_crack.py -s HomeWiFi -m dictionary -d my_passwords.txt --test-password welcome123
```

### 示例 3: 测试密码不在字典中

Example 3: Password Not in Dictionary

```bash
python wifi_crack.py -s MyWiFi -m dictionary -d sample_dictionary.txt --test-password notindict123
```

**预期输出 / Expected Output:**
```
[-] 字典攻击失败 / Dictionary attack failed
[-] 尝试次数 / Attempts: 16
[-] 耗时 / Time: 0.01 秒
```

## 暴力破解示例 / Brute Force Examples

### 示例 4: 纯数字密码（4位）

Example 4: Numeric Password (4 digits)

```bash
python wifi_crack.py -s TestWiFi -m brute -l 4 -L 4 -c digits --test-password 1234
```

**预期结果 / Expected Result:**
- 搜索空间 / Search space: 10^4 = 10,000 种组合
- 平均尝试次数 / Average attempts: ~1,235 (密码 1234 的位置)

### 示例 5: 纯数字密码（6位）

Example 5: Numeric Password (6 digits)

```bash
python wifi_crack.py -s TestWiFi -m brute -l 6 -L 6 -c digits --test-password 123456
```

**预期结果 / Expected Result:**
- 搜索空间 / Search space: 10^6 = 1,000,000 种组合
- 这可能需要几秒钟 / This may take a few seconds

### 示例 6: 小写字母密码（3位）

Example 6: Lowercase Letters (3 chars)

```bash
python wifi_crack.py -s TestWiFi -m brute -l 3 -L 3 -c lower --test-password abc
```

**预期结果 / Expected Result:**
- 搜索空间 / Search space: 26^3 = 17,576 种组合
- 非常快 / Very fast

### 示例 7: 小写字母密码（4位）

Example 7: Lowercase Letters (4 chars)

```bash
python wifi_crack.py -s TestWiFi -m brute -l 4 -L 4 -c lower --test-password test
```

**预期结果 / Expected Result:**
- 搜索空间 / Search space: 26^4 = 456,976 种组合
- 可能需要几秒钟 / May take a few seconds

### 示例 8: 范围搜索（数字 4-6 位）

Example 8: Range Search (Digits 4-6 chars)

```bash
python wifi_crack.py -s TestWiFi -m brute -l 4 -L 6 -c digits --test-password 12345
```

这会依次尝试 4 位、5 位和 6 位数字密码。

This will try 4-digit, 5-digit, and 6-digit passwords sequentially.

### 示例 9: 字母数字组合（4位）⚠️ 慢

Example 9: Alphanumeric (4 chars) ⚠️ Slow

```bash
python wifi_crack.py -s TestWiFi -m brute -l 4 -L 4 -c alphanum --test-password a1b2
```

**警告 / Warning:**
- 搜索空间 / Search space: 62^4 = 14,776,336 种组合
- 这可能需要较长时间 / This may take considerable time

## 性能测试 / Performance Tests

### 测试 1: 字典攻击性能

Test 1: Dictionary Attack Performance

创建一个大字典并测试：

Create a large dictionary and test:

```bash
# 创建包含 10000 个密码的字典
for i in {1..10000}; do echo "password$i"; done > large_dict.txt

# 测试（密码在最后）
python wifi_crack.py -s TestWiFi -m dictionary -d large_dict.txt --test-password password9999
```

### 测试 2: 暴力破解性能对比

Test 2: Brute Force Performance Comparison

```bash
# 3位数字 (1000 组合)
time python wifi_crack.py -s Test -m brute -l 3 -L 3 -c digits --test-password 999

# 4位数字 (10000 组合)
time python wifi_crack.py -s Test -m brute -l 4 -L 4 -c digits --test-password 9999

# 5位数字 (100000 组合)
time python wifi_crack.py -s Test -m brute -l 5 -L 5 -c digits --test-password 99999
```

## 常见问题 / Common Issues

### 问题 1: 字典文件不存在

Issue 1: Dictionary File Not Found

**错误 / Error:**
```
[!] 错误：字典文件不存在 / Error: Dictionary file not found
```

**解决方案 / Solution:**
```bash
# 检查文件是否存在
ls -l sample_dictionary.txt

# 或创建新字典
python wifi_crack.py --create-dict
```

### 问题 2: 暴力破解太慢

Issue 2: Brute Force Too Slow

**建议 / Recommendations:**
1. 减少密码长度范围 / Reduce password length range
2. 使用更小的字符集 / Use smaller charset
3. 优先使用字典攻击 / Prefer dictionary attack
4. 考虑密码的实际特征 / Consider actual password patterns

### 问题 3: 中断程序

Issue 3: Interrupting the Program

按 `Ctrl+C` 可以安全中断程序。

Press `Ctrl+C` to safely interrupt the program.

```bash
# 程序会显示当前进度并退出
[!] 用户中断 / User interrupted
[-] 尝试次数 / Attempts: 12345
```

## 性能参考 / Performance Reference

**注意：使用PBKDF2后，速度明显降低，这更接近真实的WPA/WPA2破解速度。**

**Note: With PBKDF2, speeds are significantly slower, which is more realistic for actual WPA/WPA2 cracking.**

| 字符集 / Charset | 长度 / Length | 组合数 / Combinations | 预估时间 / Est. Time |
|-----------------|--------------|---------------------|-------------------|
| digits          | 4            | 10,000              | ~10-30 秒 / seconds |
| digits          | 6            | 1,000,000           | ~15-30 分钟 / minutes |
| digits          | 8            | 100,000,000         | ~数天 / days |
| lower           | 3            | 17,576              | ~20-60 秒 / seconds |
| lower           | 4            | 456,976             | ~10-20 分钟 / minutes |
| lower           | 5            | 11,881,376          | ~数小时 / hours |
| alphanum        | 3            | 238,328             | ~5-10 分钟 / minutes |
| alphanum        | 4            | 14,776,336          | ~数小时 / hours |

**性能说明 / Performance Notes:**
- PBKDF2 的 4096 次迭代使每次哈希计算需要更多时间
- 4096 iterations of PBKDF2 make each hash calculation much slower
- 这是WPA/WPA2安全性的重要组成部分
- This is a critical part of WPA/WPA2 security
- 实际速度取决于CPU性能
- Actual speed depends on system configuration

## 最佳实践 / Best Practices

1. **优先使用字典攻击** / Prefer Dictionary Attack
   - 对于常见密码更高效 / More efficient for common passwords
   - 创建针对目标的专用字典 / Create targeted dictionaries

2. **合理设置暴力破解参数** / Set Reasonable Brute Force Parameters
   - 从短密码开始 / Start with short passwords
   - 根据已知信息选择字符集 / Choose charset based on known info

3. **测试模式验证** / Test Mode Validation
   - 使用 `--test-password` 验证配置 / Use `--test-password` to verify settings
   - 在真实场景前先测试 / Test before real scenarios

4. **遵守法律和道德准则** / Follow Legal and Ethical Guidelines
   - 仅在授权网络上使用 / Only use on authorized networks
   - 保护好你的工具和结果 / Protect your tools and results

---

**记住：仅用于教育和授权测试！**  
**Remember: For educational and authorized testing only!**
