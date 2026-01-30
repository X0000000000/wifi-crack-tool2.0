# 技术文档 / Technical Documentation

WiFi密码破解工具 2.0 技术实现细节

Technical implementation details for WiFi Password Cracking Tool 2.0

## 架构概述 / Architecture Overview

### 核心组件 / Core Components

```
wifi_crack.py
├── WiFiCracker (主类 / Main Class)
│   ├── __init__()           # 初始化
│   ├── _hash_password()     # 密码哈希
│   ├── _verify_password()   # 密码验证
│   ├── dictionary_attack()  # 字典攻击
│   └── brute_force_attack() # 暴力破解
├── create_sample_dictionary() # 创建示例字典
└── main()                     # 主函数
```

## 工作原理 / How It Works

### 1. 密码哈希算法 / Password Hashing

本工具使用简化的哈希方案用于演示：

This tool uses a simplified hashing scheme for demonstration:

```python
def _hash_password(self, password):
    combined = f"{self.ssid}:{password}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()
```

**实际 WPA/WPA2 协议 / Real WPA/WPA2 Protocol:**

真实的 WPA/WPA2 使用 PBKDF2 (Password-Based Key Derivation Function 2):

Real WPA/WPA2 uses PBKDF2:

```python
# 实际实现示例（需要 hashlib）
import hashlib

def generate_pmk(ssid, password):
    """生成 PMK (Pairwise Master Key)"""
    return hashlib.pbkdf2_hmac(
        'sha1',                    # 哈希算法
        password.encode('utf-8'),  # 密码
        ssid.encode('utf-8'),      # SSID 作为盐值
        4096,                      # 迭代次数
        32                         # 密钥长度（字节）
    )
```

### 2. 字典攻击算法 / Dictionary Attack Algorithm

```
1. 读取字典文件 / Read dictionary file
2. 对每个密码候选:
   For each password candidate:
   a. 计算哈希 / Calculate hash
   b. 与目标比对 / Compare with target
   c. 如果匹配则返回 / Return if match
3. 显示进度 / Show progress
4. 返回结果 / Return result
```

**时间复杂度 / Time Complexity:** O(n)，其中 n 是字典大小

**空间复杂度 / Space Complexity:** O(1)，逐行读取

### 3. 暴力破解算法 / Brute Force Algorithm

```
1. 定义字符集 / Define charset
2. 对于每个长度 (min_length 到 max_length):
   For each length (min_length to max_length):
   a. 生成所有可能的组合 / Generate all combinations
   b. 对每个组合:
      For each combination:
      - 计算哈希 / Calculate hash
      - 与目标比对 / Compare with target
      - 如果匹配则返回 / Return if match
3. 显示进度 / Show progress
4. 返回结果 / Return result
```

**时间复杂度 / Time Complexity:** O(c^l)，其中 c 是字符集大小，l 是密码长度

**空间复杂度 / Space Complexity:** O(l)，当前组合的存储

## 字符集定义 / Character Set Definitions

```python
charsets = {
    'digits': string.digits,                    # 0-9 (10 字符)
    'lower': string.ascii_lowercase,            # a-z (26 字符)
    'upper': string.ascii_uppercase,            # A-Z (26 字符)
    'alpha': string.ascii_letters,              # a-zA-Z (52 字符)
    'alphanum': string.ascii_letters + string.digits,  # a-zA-Z0-9 (62 字符)
    'all': string.ascii_letters + string.digits + string.punctuation  # 所有可打印字符 (94 字符)
}
```

## 搜索空间分析 / Search Space Analysis

### 纯数字 / Digits Only

| 长度 / Length | 组合数 / Combinations | 公式 / Formula |
|--------------|---------------------|--------------|
| 4            | 10,000              | 10^4         |
| 6            | 1,000,000           | 10^6         |
| 8            | 100,000,000         | 10^8         |
| 10           | 10,000,000,000      | 10^10        |

### 小写字母 / Lowercase Letters

| 长度 / Length | 组合数 / Combinations | 公式 / Formula |
|--------------|---------------------|--------------|
| 3            | 17,576              | 26^3         |
| 4            | 456,976             | 26^4         |
| 5            | 11,881,376          | 26^5         |
| 6            | 308,915,776         | 26^6         |

### 字母数字 / Alphanumeric

| 长度 / Length | 组合数 / Combinations | 公式 / Formula |
|--------------|---------------------|--------------|
| 3            | 238,328             | 62^3         |
| 4            | 14,776,336          | 62^4         |
| 5            | 916,132,832         | 62^5         |
| 6            | 56,800,235,584      | 62^6         |

### 所有字符 / All Characters

| 长度 / Length | 组合数 / Combinations | 公式 / Formula |
|--------------|---------------------|--------------|
| 3            | 830,584             | 94^3         |
| 4            | 78,074,896          | 94^4         |
| 5            | 7,339,040,224       | 94^5         |

## 性能优化建议 / Performance Optimization

### 当前实现 / Current Implementation

- ✅ 使用生成器减少内存占用 / Use generators to reduce memory
- ✅ 批量显示进度减少 I/O / Batch progress display
- ✅ 支持中断和恢复 / Support interruption

### 可能的优化 / Possible Optimizations

1. **并行处理 / Parallel Processing**
   ```python
   from multiprocessing import Pool
   # 多进程暴力破解
   ```

2. **GPU 加速 / GPU Acceleration**
   ```python
   import hashcat  # 使用 hashcat 等工具
   ```

3. **彩虹表 / Rainbow Tables**
   - 预计算常见 SSID 的哈希值
   - 空间换时间

4. **智能字典 / Smart Dictionary**
   - 基于常见密码模式
   - 组合字典和规则

## 安全考虑 / Security Considerations

### 防御措施 / Defense Measures

作为渗透测试工具，了解防御措施很重要：

As a penetration testing tool, understanding defenses is important:

1. **强密码策略 / Strong Password Policy**
   - 最少 12 字符 / Minimum 12 characters
   - 混合字符类型 / Mixed character types
   - 避免常见词汇 / Avoid common words

2. **WPA3 升级 / WPA3 Upgrade**
   - 更强的加密 / Stronger encryption
   - 抗离线攻击 / Resistant to offline attacks

3. **MAC 地址过滤 / MAC Filtering**
   - 额外的访问控制层 / Additional access control

4. **隐藏 SSID / Hidden SSID**
   - 增加发现难度 / Increase discovery difficulty

## 代码结构 / Code Structure

### 类图 / Class Diagram

```
┌─────────────────────────────────┐
│        WiFiCracker              │
├─────────────────────────────────┤
│ - ssid: str                     │
│ - handshake_file: str           │
│ - attempts: int                 │
│ - start_time: float             │
├─────────────────────────────────┤
│ + __init__(ssid, handshake)     │
│ + _hash_password(password)      │
│ + _verify_password(password)    │
│ + dictionary_attack(dict_file)  │
│ + brute_force_attack(params)    │
└─────────────────────────────────┘
```

### 流程图 / Flowchart

```
开始 / Start
    ↓
解析命令行参数 / Parse CLI args
    ↓
显示警告 / Show warning
    ↓
创建 WiFiCracker 实例 / Create WiFiCracker
    ↓
选择攻击模式 / Choose attack mode
    ├─→ 字典攻击 / Dictionary
    │       ↓
    │   读取字典 / Read dictionary
    │       ↓
    │   逐行测试 / Test each line
    │       ↓
    │   找到匹配? / Found match?
    │
    └─→ 暴力破解 / Brute Force
            ↓
        生成组合 / Generate combinations
            ↓
        逐个测试 / Test each
            ↓
        找到匹配? / Found match?
    ↓
显示结果 / Display result
    ↓
结束 / End
```

## 错误处理 / Error Handling

### 异常类型 / Exception Types

1. **文件不存在 / File Not Found**
   ```python
   if not dict_path.exists():
       print("[!] 错误：字典文件不存在")
       return None
   ```

2. **用户中断 / User Interrupt**
   ```python
   except KeyboardInterrupt:
       print("[!] 用户中断")
       return None
   ```

3. **编码错误 / Encoding Error**
   ```python
   with open(file, 'r', encoding='utf-8', errors='ignore') as f:
       # 自动忽略无效字符
   ```

## 测试策略 / Testing Strategy

### 单元测试 / Unit Tests

```python
# 测试密码哈希
def test_hash_password():
    cracker = WiFiCracker("TestSSID")
    hash1 = cracker._hash_password("password123")
    hash2 = cracker._hash_password("password123")
    assert hash1 == hash2  # 相同密码应产生相同哈希

# 测试密码验证
def test_verify_password():
    cracker = WiFiCracker("TestSSID")
    target = cracker._hash_password("test123")
    assert cracker._verify_password("test123", target) == True
    assert cracker._verify_password("wrong", target) == False
```

### 集成测试 / Integration Tests

```bash
# 测试字典攻击
python wifi_crack.py -s Test -m dictionary -d sample_dictionary.txt --test-password 12345678

# 测试暴力破解
python wifi_crack.py -s Test -m brute -l 4 -L 4 -c digits --test-password 1234
```

## 扩展功能建议 / Extension Suggestions

1. **握手包支持 / Handshake File Support**
   - 解析 .cap 文件
   - 提取握手数据

2. **进度保存 / Progress Saving**
   - 保存当前状态
   - 支持断点续传

3. **统计分析 / Statistical Analysis**
   - 密码强度评估
   - 常见模式识别

4. **Web 界面 / Web Interface**
   - Flask/Django 后端
   - 实时进度显示

## 参考资料 / References

1. **WPA/WPA2 协议 / Protocol**
   - IEEE 802.11i 标准
   - PBKDF2 算法 (RFC 2898)

2. **安全工具 / Security Tools**
   - Aircrack-ng
   - Hashcat
   - John the Ripper

3. **Python 文档 / Documentation**
   - hashlib 模块
   - itertools 模块
   - argparse 模块

---

**免责声明 / Disclaimer:**

本文档仅用于教育目的。请遵守法律和道德准则。

This documentation is for educational purposes only. Follow legal and ethical guidelines.
