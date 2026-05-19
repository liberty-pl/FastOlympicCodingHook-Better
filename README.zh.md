# FastOlympicCodingHook

基于 [DrSwad/FastOlympicCodingHook](https://github.com/DrSwad/FastOlympicCodingHook) 的增强版，支持自动模板、比赛多题、变量替换。

## 功能

- **Sublime Text 启动时自动监听** — 无需手动激活
- **自动跟随当前文件目录** — 文件创建在当前文件所在位置
- **比赛支持** — 服务器常驻，可连续接收多道题目
- **模板变量替换** — `$(url)`, `$(name)`, `$(id)`, `$(date)`, `$(time)`, `$(year)`, `$(time_limit)`, `$(memory_limit)`
- **重复检测** — 重复获取同一题目时直接打开已有文件，不覆盖
- **样例保存**到 `TESTCASE/` 子目录

## 依赖

- [Sublime Text](https://www.sublimetext.com/) 3 或 4
- [CppFastOlympicCoding](https://packagecontrol.io/packages/CppFastOlympicCoding)（通过 Package Control 安装）
- [Competitive Companion](https://github.com/jmerle/competitive-companion) 浏览器扩展（端口 12345）

## 安装

```bash
cd ~/.config/sublime-text/Packages/
git clone https://github.com/你的用户名/FastOlympicCodingHook.git
```

重启 Sublime Text。

## 配置

创建 `Packages/User/FastOlympicCoding.sublime-settings`：

```json
{
	"tests_relative_dir": "TESTCASE",
	"tests_file_suffix": "__tests",
	"template_file": "/home/你的用户名/template.cpp",
	"run_settings": [
		{
			"name": "C++",
			"extensions": ["cpp"],
			"compile_cmd": "g++ '{source_file}' -std=gnu++17 -o \"/tmp/{file_name}\"",
			"run_cmd": "/tmp/\"{file_name}\" {args} -debug",
			"lint_compile_cmd": "g++ -std=gnu++17 '{source_file}' -I '{source_file_dir}'"
		}
	]
}
```

## 模板

示例 `template.cpp`：

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

### 可用变量

| 变量 | 替换为 |
|------|--------|
| `$(url)` | 题目 URL |
| `$(name)` | 题目名称 |
| `$(id)` | 提取的题目 ID |
| `$(time_limit)` | 时间限制 (ms) |
| `$(memory_limit)` | 内存限制 (MB) |
| `$(date)` | 当前日期 (YYYY-MM-DD) |
| `$(time)` | 当前时间 (HH:MM:SS) |
| `$(year)` | 当前年份 |

## 使用方法

1. 在 Sublime Text 中打开或创建一个 `.cpp` 文件，切换到你想存放题目的目录
2. 在浏览器中打开题目页面
3. 点击 **Competitive Companion** 浏览器扩展图标
4. `.cpp` 文件自动从模板创建，样例保存到 `TESTCASE/` 目录

服务器在 Sublime Text 启动时自动运行，并跟随当前活动文件的目录。

停止服务器：`Ctrl+Shift+P` → `FastOlympicCodingHook: Stop`

## 与原版的区别

- 完全重写了 HTTP 处理器 — 常驻服务器，而非单次请求即关闭
- 自动从可配置模板创建 `.cpp` 文件
- 模板变量替换
- 从 Competitive Companion 数据中提取题目 ID
- 比赛支持（无需重启即可接收多道题目）
- 重复检测（文件+样例已存在 → 直接打开不覆盖）
- 插件加载时自动启动
- 自动跟随当前活动文件目录
- 样例文件存储在可配置的子目录（默认 `TESTCASE/`）
