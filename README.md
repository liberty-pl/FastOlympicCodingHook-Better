# FastOlympicCodingHook

Fork of [DrSwad/FastOlympicCodingHook](https://github.com/DrSwad/FastOlympicCodingHook) with auto-template, contest support, and variable substitution.

[中文版说明](README.zh.md)

## Features

- **Auto-start** on Sublime Text launch — no manual activation needed
- **Auto-follow** active file directory — files are created next to your current file
- **Contest support** — server stays alive to receive multiple problems
- **Template with variables** — `$(url)`, `$(name)`, `$(id)`, `$(date)`, `$(time)`, `$(year)`, `$(time_limit)`, `$(memory_limit)`
- **Duplicate detection** — re-fetching the same problem opens the existing file without overwriting
- **Test cases** saved to `TESTCASE/` subdirectory

## Requirements

- [Sublime Text](https://www.sublimetext.com/) 3 or 4
- [CppFastOlympicCoding](https://packagecontrol.io/packages/CppFastOlympicCoding) (via Package Control)
- [Competitive Companion](https://github.com/jmerle/competitive-companion) browser extension (port 12345)

## Installation

### Linux
```bash
cd ~/.config/sublime-text/Packages/
git clone https://github.com/YOUR_USERNAME/FastOlympicCodingHook.git
```

### macOS
```bash
cd ~/Library/Application\ Support/Sublime\ Text/Packages/
git clone https://github.com/YOUR_USERNAME/FastOlympicCodingHook.git
```

### Windows (PowerShell)
```powershell
cd "$env:APPDATA\Sublime Text\Packages"
git clone https://github.com/YOUR_USERNAME/FastOlympicCodingHook.git
```

Restart Sublime Text after cloning.

## Configuration

Create `Packages/User/FastOlympicCoding.sublime-settings` with OS-appropriate settings:

### Linux / macOS
```json
{
	"tests_relative_dir": "TESTCASE",
	"tests_file_suffix": "__tests",
	"template_file": "/home/yourname/template.cpp",
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

### Windows
```json
{
	"tests_relative_dir": "TESTCASE",
	"tests_file_suffix": "__tests",
	"template_file": "C:\\Users\\yourname\\template.cpp",
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

> **Note:** `template_file` must point to an absolute path to your template file.

## Template

Example `template.cpp`:

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

### Available variables

| Variable | Replaced with |
|----------|---------------|
| `$(url)` | Problem URL |
| `$(name)` | Problem name |
| `$(id)` | Extracted problem ID |
| `$(time_limit)` | Time limit (ms) |
| `$(memory_limit)` | Memory limit (MB) |
| `$(date)` | Current date (YYYY-MM-DD) |
| `$(time)` | Current time (HH:MM:SS) |
| `$(year)` | Current year |

## Usage

1. Open or create a `.cpp` file in the directory where you want to work
2. Open the problem page in your browser
3. Click the **Competitive Companion** extension icon
4. The `.cpp` file is created from template and test cases are saved to `TESTCASE/`

The server starts automatically with Sublime Text and follows your active file's directory.

To stop the server: `Ctrl+Shift+P` → `FastOlympicCodingHook: Stop`

## Changes from original

- Complete rewrite of the HTTP handler — always-on server, not single-request
- Auto-create `.cpp` files from configurable template
- Template variable substitution
- Problem ID extraction from Competitive Companion data
- Contest support (multiple problems without restarting)
- Duplicate detection (file + tests exist → open without overwrite)
- Auto-start on plugin load
- Auto-follow active view directory
- Test files stored in configurable subdirectory (default `TESTCASE/`)
