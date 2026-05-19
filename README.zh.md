# FastOlympicCodingHook

[English](README.md) | 简体中文

---

## 安装前需要准备

| 依赖 | 说明 |
|------|------|
| **Sublime Text 3 或 4** | 代码编辑器 |
| **CppFastOlympicCoding** | Sublime 插件，用来管理和运行测试 |
| **Competitive Companion** | 浏览器扩展，负责从题目页面抓取数据 |

### 安装 CppFastOlympicCoding

在 Sublime Text 中：
1. `Ctrl+Shift+P` → `Package Control: Install Package`
2. 搜索 `CppFastOlympicCoding` 并安装

### 安装 Competitive Companion

| 浏览器 | 安装地址 |
|--------|----------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/competitive-companion/) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/competitive-companion/) |
| Edge | 在扩展商店搜索 "Competitive Companion" |

安装后点击扩展图标 → 设置 → 在 Port 一栏填 `12345`。

---

## 安装本插件

### Linux
```bash
cd ~/.config/sublime-text/Packages/
git clone https://github.com/liberty-pl/FastOlympicCodingHook.git
```

### macOS
```bash
cd ~/Library/Application\ Support/Sublime\ Text/Packages/
git clone https://github.com/liberty-pl/FastOlympicCodingHook.git
```

### Windows
```powershell
cd "$env:APPDATA\Sublime Text\Packages"
git clone https://github.com/liberty-pl/FastOlympicCodingHook.git
```

**重启 Sublime Text。**

---

## 配置

在顶部Preference选项栏中打开Settings后，按需求进行以下配置

<details>
<summary><b>Linux / macOS 配置</b></summary>

```json
{
    "tests_relative_dir": "TESTCASE",
    "tests_file_suffix": "__tests",
    "template_file": "",
    "run_settings": [
        {
            "name": "C++",
            "extensions": ["cpp"],
            "compile_cmd": "g++ '{source_file}' -std=g++17 -o \"/tmp/{file_name}\"",
            "run_cmd": "/tmp/\"{file_name}\" {args} -debug",
            "lint_compile_cmd": "g++ -std=gnu++17 '{source_file}' -I '{source_file_dir}'"
        }
    ]
}
```
</details>

<details>
<summary><b>Windows 配置</b></summary>

```json
{
    "tests_relative_dir": "TESTCASE",
    "tests_file_suffix": "__tests",
    "template_file": "",
    "run_settings": [
        {
            "name": "C++",
            "extensions": ["cpp"],
            "compile_cmd": "g++ \"{source_file}\" -std=gnu++17 -o \"%TEMP%\\{file_name}.exe\"",
            "run_cmd": "\"%TEMP%\\{file_name}.exe\" {args} -debug",
            "lint_compile_cmd": "g++ -std=gnu++17 \"{source_file}\" -I \"{source_file_dir}\""
        }
    ]
}
```
</details>

### 配置项说明

| 配置项 | 作用 | 默认值 |
|--------|------|--------|
| `tests_relative_dir` | 样例文件存在哪个子目录里 | `"TESTCASE"`，即创建 `TESTCASE/` 文件夹存放样例 |
| `tests_file_suffix` | 样例文件的结尾标识 | `"__tests"`，如 `4A.cpp__tests` |
| `template_file` | 模板文件路径 | 留空则创建空白文件 |

### 设置模板（可选）

如果你想每次创建文件时有默认代码（头文件、main 函数等），创建一个模板文件，比如 `/home/你的名字/template.cpp`：

```cpp
// $(name)
// $(url)

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    
}
```

然后在配置中填入路径：

```json
"template_file": "/home/你的名字/template.cpp"
```

模板中可以使用以下变量，创建文件时会自动替换为真实内容：

| 变量 | 被替换成 |
|------|----------|
| `$(url)` | 题目链接，如 `https://codeforces.com/problemset/problem/4/A` |
| `$(name)` | 题目名称，如 `4A Watermelon` |
| `$(id)` | 题目 ID，如 `4A` |
| `$(time_limit)` | 时间限制（毫秒） |
| `$(memory_limit)` | 内存限制（MB） |
| `$(date)` | 当前日期，如 `2026-05-19` |
| `$(time)` | 当前时间，如 `14:30:00` |
| `$(year)` | 当前年份 |

---

## 使用方法

### 基本流程

1. **在 Sublime 中切换到你要存放题目的目录**
   - 比如你正在刷 Codeforces，可以打开或新建一个 `~/CF/` 下的任意文件
   - 插件会自动以这个文件所在的目录作为基准

2. **在浏览器中打开题目页面**

3. **点击 Competitive Companion 扩展图标**
   - 插件会自动：
     - 在目录下创建 `题目ID.cpp`（如 `4A.cpp`）
     - 若配置了模板，用它填充；否则创建空白文件
     - 将题目样例保存到 `TESTCASE/题目ID.cpp__tests`
     - 在 Sublime 中打开这个文件

4. **按 `F5` 运行测试**
   - 编译运行你的代码，测试面板会显示样例结果

### 比赛场景

打开比赛页面后，每点一个题目的扩展图标，就会依次创建 `A.cpp`、`B.cpp`、`C.cpp` …… 所有文件都在同一个目录下，测试数据分别存在 `TESTCASE/` 里。

### 重复获取同一道题

如果文件和样例已经存在，插件会直接打开已有文件，不会覆盖你的代码和测试数据。

### 停止服务器

插件在 Sublime 启动时自动在后台监听。如需停止：

`Ctrl+Shift+P` → `FastOlympicCodingHook: Stop`

---

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `F5` | 编译并运行当前测试 |

如果快捷键不生效，检查是否与其他插件冲突，或手动在 `Packages/User/Default (Linux).sublime-keymap` 中添加快捷键。

---

## 目录结构示例

```
~/CF/
├── 4A.cpp              # 自动创建的代码文件
├── 4B.cpp
├── TESTCASE/
│   ├── 4A.cpp__tests   # 自动保存的样例数据
│   └── 4B.cpp__tests
```

---

## 常见问题

**Q: 点击扩展后没反应？**
A: 确保 Competitive Companion 的端口设置为 `12345`，且本插件已正确安装到 Sublime 的 Packages 目录。

**Q: 编译报错 "找不到 xxx"？**
A: 确认你的编译器已正确安装，检查 `compile_cmd` 中的编译器路径是否正确。

**Q: 新建的文件是空白内容？**
A: 因为 `template_file` 未设置或路径无效。配置一个模板文件路径即可。
