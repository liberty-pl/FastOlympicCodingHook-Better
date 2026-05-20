import sublime
import sublime_plugin
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import _thread
import threading
import re
from os import path, makedirs

_server_instance = None
_current_base_dir = path.expanduser("~")


def sanitize_filename(name):
    name = re.sub(r'[^\w\s-]', '', name.strip())
    return re.sub(r'[-\s]+', '_', name)


def extract_problem_id(data):
    url = data.get("url", "")
    contest_id = ""
    for pattern in [r'/contest/(\d+)', r'/gym/(\d+)', r'/problemset/problem/(\d+)/']:
        m = re.search(pattern, url)
        if m:
            contest_id = m.group(1)
            break

    task_class = data.get("languages", {}).get("java", {}).get("taskClass", "")
    if task_class:
        m = re.match(r'Task(\w+)', task_class)
        if m:
            return m.group(1)

    name = data.get("name", "")
    m = re.match(r'^(\d+[A-Za-z]?)', name)
    if m:
        return m.group(1)

    m = re.search(r'/problem/([A-Z]\d*)', url)
    if m:
        prob = m.group(1)
        if contest_id and re.match(r'^[A-Z]\d*$', prob) and len(prob) <= 2:
            return contest_id + prob
        return prob

    if contest_id:
        return contest_id

    return sanitize_filename(name)


def substitute_vars(content, data, prob_id):
    from datetime import datetime
    now = datetime.now()
    subs = {
        "url": data.get("url", ""),
        "name": data.get("name", ""),
        "id": prob_id,
        "contest": data.get("group", ""),
        "time_limit": str(data.get("timeLimit", "")),
        "memory_limit": str(data.get("memoryLimit", "")),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "year": str(now.year),
    }
    def replacer(m):
        key = m.group(1)
        return subs.get(key, m.group(0))
    return re.sub(r'\$\((\w+)\)', replacer, content)


def create_file_from_template(file_path, template_path, data, prob_id):
    d = path.dirname(file_path)
    if d and not path.exists(d):
        makedirs(d)
    if template_path and path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = substitute_vars(content, data, prob_id)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        with open(file_path, 'a'):
            pass


def open_file(p):
    for window in sublime.windows():
        window.open_file(p)


def update_base_dir(view):
    global _current_base_dir
    if not view:
        return
    file_path = view.file_name()
    if file_path:
        _current_base_dir = path.dirname(file_path)
    else:
        window = view.window()
        if window:
            folders = window.folders()
            if folders:
                _current_base_dir = folders[0]


def start_server():
    global _server_instance

    if _server_instance is not None:
        return

    foc_settings = sublime.load_settings("FastOlympicCoding.sublime-settings")
    hook_settings = sublime.load_settings("FastOlympicCodingHook.sublime-settings")
    context = {
        "template_file": foc_settings.get("template_file") or "",
        "tests_relative_dir": foc_settings.get("tests_relative_dir"),
        "tests_file_suffix": foc_settings.get("tests_file_suffix") or "__tests",
    }
    port = int(hook_settings.get("port", 12345))

    _server_instance = "starting"
    _thread.start_new_thread(run_server, (context, port))


def stop_server():
    global _server_instance
    if _server_instance:
        try:
            _server_instance.shutdown()
        except:
            pass
        _server_instance = None


def run_server(context, port):
    global _server_instance
    host = 'localhost'
    template_file = context["template_file"]
    tests_relative_dir = context["tests_relative_dir"]
    tests_file_suffix = context["tests_file_suffix"]

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf8'))

                self.send_response(200)
                self.end_headers()

                sublime.set_timeout(lambda d=data: _process_request(d))
            except Exception as e:
                print("Error handling POST - " + str(e))

        def log_message(self, format, *args):
            pass

    def _process_request(data):
        global _current_base_dir
        tests = data.get("tests", [])
        base_dir = _current_base_dir
        prob_id = extract_problem_id(data)
        full_path = path.join(base_dir, prob_id + ".cpp")
        file_name = path.basename(full_path)
        test_dir = path.join(base_dir, tests_relative_dir) if tests_relative_dir else base_dir
        nfilename = path.join(test_dir, file_name + tests_file_suffix)

        if path.exists(full_path) and path.exists(nfilename):
            print("Already exists: " + full_path)
        else:
            if not path.exists(full_path):
                create_file_from_template(full_path, template_file, data, prob_id)

            ntests = []
            for test in tests:
                ntests.append({
                    "test": test.get("input", ""),
                    "correct_answers": [test.get("output", "").strip()]
                })

            if not path.exists(test_dir):
                makedirs(test_dir)
            with open(nfilename, "w", encoding="utf-8") as f:
                f.write(json.dumps(ntests))

        open_file(full_path)

    for offset in range(10):
        try:
            httpd = HTTPServer((host, port + offset), Handler)
            _server_instance = httpd
            addr = httpd.server_address
            print(f"FastOlympicCodingHook: Listening on {addr[0]}:{addr[1]}")
            httpd.serve_forever()
            break
        except OSError:
            if offset < 9:
                continue
            print(f"FastOlympicCodingHook: Could not bind any port from {port} to {port + 9}")
            _server_instance = None
            return

    _server_instance = None
    print("FastOlympicCodingHook: Server stopped")


class FastOlympicCodingHookListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        update_base_dir(view)


class FastOlympicCodingHookCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        stop_server()
        start_server()
        sublime.status_message("FastOlympicCodingHook: Restarted")


class FastOlympicCodingHookStopCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        stop_server()
        sublime.status_message("FastOlympicCodingHook: Stopped")


def plugin_loaded():
    for window in sublime.windows():
        if window.active_view():
            update_base_dir(window.active_view())
            break
    start_server()
    sublime.status_message("FastOlympicCodingHook: Auto-listening")


def plugin_unloaded():
    stop_server()
