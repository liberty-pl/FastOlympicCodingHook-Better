# FastOlympicCodingHook

**Bring CPH-like experience to Sublime Text.**

English | [简体中文](README.zh.md)

---

## Prerequisites

| Dependency | Description |
|------------|-------------|
| **Sublime Text 3 or 4** | Your editor |
| **Python 3** | Required to run the HTTP server |
| **CppFastOlympicCoding** | Sublime plugin for running tests |
| **Competitive Companion** | Browser extension that scrapes problem data |

### Install CppFastOlympicCoding

In Sublime Text:
1. `Ctrl+Shift+P` → `Package Control: Install Package`
2. Search for `CppFastOlympicCoding` and install

### Install Competitive Companion

| Browser | Link |
|---------|------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/competitive-companion/) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/competitive-companion/) |
| Edge | Search for "Competitive Companion" in extensions store |

After installing, click the extension icon → Settings → Set **Port** to `12345`.

---

## Install This Plugin

### Linux
```bash
cd ~/.config/sublime-text/Packages/
git clone https://github.com/liberty-pl/FastOlympicCodingHook-Better.git
```

### macOS
```bash
cd ~/Library/Application\ Support/Sublime\ Text/Packages/
git clone https://github.com/liberty-pl/FastOlympicCodingHook-Better.git
```

### Windows
```powershell
cd "$env:APPDATA\Sublime Text\Packages"
git clone https://github.com/liberty-pl/FastOlympicCodingHook-Better.git
```

**Restart Sublime Text.**

---

## Configuration

Open Preferences → Settings, then paste the config for your OS.

> **Required:** add `"tests_file_suffix": "__tests"` in your settings.

<details>
<summary><b>Linux / macOS config</b></summary>

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
<summary><b>Windows config</b></summary>

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

### Settings explained

| Setting | What it does | Default |
|---------|-------------|---------|
| `tests_relative_dir` | Subdirectory where test files are saved | `"TESTCASE"` |
| `tests_file_suffix` | Suffix appended to test files | `"__tests"` |
| `template_file` | Path to your template file | Empty = blank files |

### Optional: Use a template

Create a template file, e.g. `/home/yourname/template.cpp`:

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

Then set the path in your config:

```json
"template_file": "/home/yourname/template.cpp"
```

Available variables (replaced with real data when a file is created):

| Variable | Replaced with |
|----------|---------------|
| `$(url)` | Problem URL, e.g. `https://codeforces.com/problemset/problem/4/A` |
| `$(name)` | Problem name, e.g. `4A Watermelon` |
| `$(id)` | Problem ID, e.g. `4A` |
| `$(time_limit)` | Time limit in ms |
| `$(memory_limit)` | Memory limit in MB |
| `$(date)` | Current date, e.g. `2026-05-19` |
| `$(time)` | Current time, e.g. `14:30:00` |
| `$(year)` | Current year |

---

## Usage

> **Difference from original:**
> - Original: Right-click → Listen to Competitive Companion → click browser extension → single request, server shuts down
> - This fork: Auto-listens on Sublime start, just click the browser extension directly, supports multiple problems in a row, auto-follows active file directory

### Basic workflow

1. **Navigate to your working directory in Sublime Text**
   - Open any file inside the folder where you want to save problems (e.g. `~/CF/`)
   - The plugin automatically follows the active file's directory

2. **Open a problem page in your browser**

3. **Click the Competitive Companion extension**
   - The plugin will:
     - Create `ProblemID.cpp` in your directory (e.g. `4A.cpp`)
     - Fill it with your template, or leave it blank
     - Save sample tests to `TESTCASE/ProblemID.cpp__tests`
     - Open the file in Sublime

4. **Press `F5` to run tests**
   - The test panel shows your sample results

### During a contest

Open the contest page, then click the extension for each problem. Files are created one by one: `A.cpp`, `B.cpp`, `C.cpp` … all in the same directory, each with their own tests in `TESTCASE/`.

### Re-fetching the same problem

If both the `.cpp` file and test file already exist, the plugin opens the existing file without overwriting anything.

### Stop the server

The plugin starts listening automatically when Sublime Text launches. To stop it:

`Ctrl+Shift+P` → `FastOlympicCodingHook: Stop`

---

## Key bindings

The default run shortcut in CppFastOlympicCoding is `Ctrl+Alt+B`. To use `F5` instead, open the file `Packages/CppFastOlympicCoding/Default (Linux).sublime-keymap` (or `Default (OSX).sublime-keymap` / `Default (Windows).sublime-keymap`) and replace `ctrl+alt+b` with `f5` in the two "Run" sections.

---

## Directory structure example

```
~/CF/
├── 4A.cpp              # Auto-generated code file
├── 4B.cpp
├── TESTCASE/
│   ├── 4A.cpp__tests   # Auto-saved test data
│   └── 4B.cpp__tests
```

---

## FAQ

**Q: Nothing happens when I click the extension.**
A: Make sure Competitive Companion's port is set to `12345` and the plugin is correctly installed in Sublime's Packages folder.

**Q: Compilation error: "cannot find ..."**
A: Verify your compiler is installed and the path in `compile_cmd` is correct.

**Q: New files are blank.**
A: `template_file` is either empty or points to an invalid path. Set it to a valid template file, or leave it empty if you want blank files.
