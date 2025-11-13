import os
import ctypes
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import platform
import time

BUILD_ENV = "prod"          #(dev,test,prod)  <-- prod skip Environment page, show Version page


EXE_PATH = r"C:\exe_files"
LOG_FILE = os.path.join(EXE_PATH, "HitmanEdge_installer_log.txt")
os.makedirs(EXE_PATH, exist_ok=True)

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

CURRENT_OS = platform.system().lower()
IS_WINDOWS = CURRENT_OS == "windows"
if not IS_WINDOWS:
    sys.exit(1)

BG_COLOR = "white"
BTN_COLOR = "#0078D7"
BTN_TEXT = "white"
LABEL_COLOR = "#0078D7"
DEFAULT_TARGET_DIR = r"C:\HitmanEdge"

# Global config
CONFIG_TARGET_DIR = None
SELECTED_ENVIRONMENT = None
SELECTED_VERSION = None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except:
        messagebox.showerror("Error", "Failed to elevate privileges.")


class InstallerApp(tk.Tk):
    instance = None
    def __init__(self):
        super().__init__()
        InstallerApp.instance = self
        self.title("Setup - HitmanEdge Application")
        self.win_w, self.win_h = 550, 400
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = int((screen_w / 2) - (self.win_w / 2)), int((screen_h / 2) - (self.win_h / 2))
        self.geometry(f"{self.win_w}x{self.win_h}+{x}+{y}")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.bind("<Button-1>", lambda e: None)
        self.current_frame = None

        self.full_pages = [
            WelcomePage, BrowsePage, EnvironmentPage,
            VersionPage, ConfirmationPage, InstallationPage, FinishPage
        ]

        if BUILD_ENV.lower() == "prod":
            self.pages = [WelcomePage, BrowsePage, VersionPage, ConfirmationPage, InstallationPage, FinishPage]
            self.selected_env = "prod"
            self.selected_version = None          # will be filled on VersionPage
        else:
            self.pages = self.full_pages[:]
            self.selected_env = "dev"
            self.selected_version = None

        self.page_index = 0
        self.install_thread = None
        self.success_steps = 0
        self.failed_steps = []
        self.total_steps = 13
        self.target_dir = DEFAULT_TARGET_DIR
        self.show_frame(self.pages[self.page_index])

    def show_frame(self, page_class):
        if self.current_frame:
            self.current_frame.destroy()
        frame = page_class(self)
        self.current_frame = frame
        frame.pack(fill="both", expand=True)
        frame.bind("<Button-1>", lambda e: None)

    def next_page(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self.show_frame(self.pages[self.page_index])
        else:
            self.quit()

    def back_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.show_frame(self.pages[self.page_index])

    def update_progress(self, message):
        if isinstance(self.current_frame, InstallationPage):
            self.current_frame.update_progress(message)
            self.current_frame.update_step_progress()

    def start_installation(self):
        global CONFIG_TARGET_DIR, SELECTED_ENVIRONMENT, SELECTED_VERSION
        CONFIG_TARGET_DIR = self.target_dir
        SELECTED_ENVIRONMENT = self.selected_env
        SELECTED_VERSION = self.selected_version
        if isinstance(self.current_frame, InstallationPage):
            self.current_frame.install_btn.config(state="disabled")
        if self.install_thread and self.install_thread.is_alive():
            return
        self.install_thread = threading.Thread(target=self.run_installation)
        self.install_thread.start()

    def run_installation(self):
        self.success_steps = 0
        self.failed_steps = []
        self.next_page()


class WelcomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Welcome to HitmanEdge Setup Wizard",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="This wizard will guide you through the installation of HitmanEdge.",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(btn_frame, text="Next >", command=master.next_page, style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit, style="Rounded.TButton").pack(side="right", padx=5)
        btn_back = ttk.Button(btn_frame, text="< Back", command=master.back_page, style="Rounded.TButton")
        btn_back.pack(side="right", padx=5)
        btn_back.state(["disabled"])


class BrowsePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Installation Folder",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="Please choose a folder to install HitmanEdge:",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        path_frame = tk.Frame(main_frame, bg=BG_COLOR)
        path_frame.pack(pady=20, fill="x", anchor="w")
        border_frame = tk.Frame(path_frame, bg="black", bd=1)
        border_frame.pack(side="left")
        self.path_var = tk.StringVar(value=DEFAULT_TARGET_DIR)
        tk.Entry(border_frame, textvariable=self.path_var,
                 font=("Arial", 10), relief="flat", width=50).pack(padx=.2, pady=.2, ipady=2)
        ttk.Button(path_frame, text="Browse", command=self.browse,
                   style="Rounded.TButton").pack(side="left", padx=7, pady=0, ipady=2)

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(btn_frame, text="Next >", command=self.proceed,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="< Back", command=master.back_page,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def browse(self):
        folder = filedialog.askdirectory(initialdir="C:\\")
        if folder:
            self.path_var.set(os.path.normpath(os.path.join(folder, "HitmanEdge")))

    def proceed(self):
        self.master.target_dir = self.path_var.get()
        self.master.next_page()


class EnvironmentPage(tk.Frame):
    """Only shown when BUILD_ENV != prod"""
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Select Environment",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="Choose the environment for your installation:",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        env_frame = tk.Frame(main_frame, bg=BG_COLOR)
        env_frame.pack(pady=30, fill="both", expand=True)

        self.env_var = tk.StringVar(value="dev")
        environments = [
            ("Development", "dev", "For development and testing purposes."),
            ("Testing", "test", "For quality assurance and testing.")
        ]
        for label, value, desc in environments:
            radio_frame = tk.Frame(env_frame, bg=BG_COLOR)
            radio_frame.pack(pady=8, fill="x", anchor="w")
            tk.Radiobutton(radio_frame, text=label, variable=self.env_var, value=value,
                           font=("Arial", 11, "bold"), bg=BG_COLOR, fg=LABEL_COLOR,
                           activebackground=BG_COLOR, selectcolor="white", cursor="hand2").pack(anchor="w")
            tk.Label(radio_frame, text=desc, font=("Arial", 9), bg=BG_COLOR,
                     fg="gray", anchor="w").pack(anchor="w", padx=25)

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(btn_frame, text="Next >", command=self.proceed,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="< Back", command=master.back_page,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def proceed(self):
        self.master.selected_env = self.env_var.get()
        self.master.next_page()


class VersionPage(tk.Frame):
    """Always shown – even for prod builds"""
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Select Version",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="Choose the version to install:",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        version_frame = tk.Frame(main_frame, bg=BG_COLOR)
        version_frame.pack(pady=30, fill="x")

        self.version_var = tk.StringVar()
        versions = self.get_available_versions(master.selected_env)
        if versions:
            self.version_var.set(versions[0])

        tk.Label(version_frame, text="Available Versions:",
                 font=("Arial", 10, "bold"), bg=BG_COLOR).pack(anchor="w")
        dropdown = ttk.Combobox(version_frame, textvariable=self.version_var,
                                values=versions, state="readonly", width=30)
        dropdown.pack(pady=5, anchor="w")

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(btn_frame, text="Next >", command=self.proceed,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="< Back", command=master.back_page,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def get_available_versions(self, env: str):
        if env == "dev":
            return [f"v1.0.{i}" for i in range(5)]
        if env == "test":
            return [f"v1.0.{i}" for i in range(3)]
        if env == "prod":
            return [f"v1.0.{i}" for i in range(4)]   # <-- production versions
        return []

    def proceed(self):
        self.master.selected_version = self.version_var.get()
        self.master.next_page()


class ConfirmationPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Confirm Installation",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="Please review the installation settings:",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        info_frame = tk.Frame(main_frame, bg=BG_COLOR, relief="sunken", bd=1)
        info_frame.pack(pady=20, fill="both", expand=True)

        env_names = {"dev": "Development", "test": "Testing", "prod": "Production"}
        env_name = env_names.get(master.selected_env, "Development")
        db_name = get_db_name_by_environment(master.selected_env, master.selected_version)
        version_line = f"Version: {master.selected_version}" if master.selected_version else ""

        info_text = (
            f"Installation Directory: {master.target_dir}\n\n"
            f"Environment: {env_name}\n\n"
            f"Database: {db_name}\n\n"
            f"{version_line}"
        )
        tk.Label(info_frame, text=info_text, font=("Arial", 10),
                 bg="white", justify="left", anchor="w").pack(
                     padx=15, pady=15, fill="both", expand=True)

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(btn_frame, text="Confirm", command=self.confirm_installation,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit,
                   style="Rounded.TButton").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="< Back", command=master.back_page,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def confirm_installation(self):
        global CONFIG_TARGET_DIR, SELECTED_ENVIRONMENT, SELECTED_VERSION
        CONFIG_TARGET_DIR = self.master.target_dir
        SELECTED_ENVIRONMENT = self.master.selected_env
        SELECTED_VERSION = self.master.selected_version

        if check_setup_lock():
            messagebox.showwarning(
                "Setup Already Completed",
                f"HitmanEdge setup already exists in:\n\n{CONFIG_TARGET_DIR}\n\n"
                "Please choose a different directory or remove the existing installation."
            )
            self.master.page_index = 1
            self.master.show_frame(BrowsePage)
            return

        env_names = {"dev": "Development", "test": "Testing", "prod": "Production"}
        env_name = env_names.get(SELECTED_ENVIRONMENT, "Development")
        db_name = get_db_name_by_environment(SELECTED_ENVIRONMENT, SELECTED_VERSION)

        popup = tk.Toplevel(self)
        popup.title("Installation Started")
        popup.configure(bg="white")
        version_line = f"Version: {SELECTED_VERSION}\n" if SELECTED_VERSION else ""
        tk.Label(
            popup,
            text=(
                f"HitmanEdge will be installed at:\n\n{CONFIG_TARGET_DIR}\n\n"
                f"Environment: {env_name}\n"
                f"Database: {db_name}\n"
                f"{version_line}\n"
                "Downloading and configuring required components"
            ),
            font=("Arial", 9), bg="white", justify="left", anchor="w",
            padx=25, pady=25
        ).pack()
        popup.update_idletasks()
        x = self.winfo_rootx() + 250
        y = self.winfo_rooty() + 150
        popup.geometry(f"+{x}+{y}")
        popup.after(1500, lambda: [popup.destroy(), self.master.next_page()])


class InstallationPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Installing HitmanEdge",
                 font=("Arial", 14, "bold"), fg=LABEL_COLOR, bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")
        tk.Label(main_frame, text="Please wait while the installation completes.",
                 font=("Arial", 10), bg=BG_COLOR, anchor="w").pack(pady=1, fill="x")

        progress_frame = tk.Frame(main_frame, bg=BG_COLOR)
        progress_frame.pack(pady=10, fill="x")
        tk.Label(progress_frame, text="Installation Progress:",
                 font=("Arial", 10, "bold"), bg=BG_COLOR, anchor="w").pack(fill="x")
        self.step_progress_var = tk.StringVar(value="Step 0/13")
        tk.Label(progress_frame, textvariable=self.step_progress_var,
                 font=("Arial", 9), fg="blue", bg=BG_COLOR, anchor="w").pack(pady=2, fill="x")
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5, fill="x")

        self.progress_text = tk.Text(main_frame, height=8, width=60,
                                     font=("Consolas", 9), state='disabled')
        self.progress_text.pack(pady=10, fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.progress_text)
        scrollbar.pack(side="right", fill="y")
        self.progress_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.progress_text.yview)

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        self.install_btn = ttk.Button(btn_frame, text="Install",
                                      command=master.start_installation,
                                      style="Rounded.TButton")
        self.install_btn.pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=master.quit,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def update_progress(self, message):
        self.progress_text.config(state='normal')
        self.progress_text.insert(tk.END, f"{message}\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state='disabled')
        self.update()

    def update_step_progress(self):
        cur = self.master.success_steps
        tot = self.master.total_steps
        self.step_progress_var.set(f"Step {cur}/{tot}")
        self.progress_bar['value'] = (cur / tot) * 100
        self.update()


class FinishPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Installation Complete!",
                 font=("Arial", 14, "bold"), fg="green", bg=BG_COLOR,
                 anchor="w").pack(pady=1, fill="x", padx=10)
        tk.Label(self, text="HitmanEdge has been successfully installed.",
                 font=("Arial", 10), bg=BG_COLOR,
                 anchor="w").pack(pady=1, fill="x", padx=10)

        summary_frame = tk.Frame(self, bg="white", relief="sunken", bd=1)
        summary_frame.pack(pady=20, padx=30, fill="both", expand=True)

        env_names = {"dev": "Development", "test": "Testing", "prod": "Production"}
        env_name = env_names.get(master.selected_env, "Development")
        db_name = get_db_name_by_environment(master.selected_env, master.selected_version)
        version_line = f"Version: {master.selected_version}\n" if master.selected_version else ""

        summary_text = (
            f"Setup Status: {master.success_steps}/{master.total_steps} steps completed\n"
            f"Installation Directory: {CONFIG_TARGET_DIR}\n"
            f"Environment: {env_name}\n"
            f"Database: {db_name}\n"
            f"{version_line}\n"
        )
        if master.failed_steps:
            summary_text += f"Failed Steps: {', '.join(master.failed_steps)}"
        else:
            summary_text += "All steps completed successfully."

        tk.Label(summary_frame, text=summary_text,
                 font=("Arial", 9), bg="white",
                 justify="left", anchor="w").pack(pady=10, padx=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(side="bottom", fill="x", padx=1, pady=10)
        ttk.Button(btn_frame, text="Finish", command=self.finish_and_close,
                   style="Rounded.TButton").pack(side="right", padx=5)

    def finish_and_close(self):
        open_target_directory()
        self.master.quit()

def get_db_name_by_environment(env, version=None):
    """
    Returns versioned DB name: hitman_edge_dev_v1.0.0
    """
    base_map = {
        "dev": "hitman_edge_dev",
        "test": "hitman_edge_test",
        "prod": "hitman_edge_prod"
    }
    base = base_map.get(env.lower(), "hitman_edge_dev")
    if version:
    
        clean_version = version.lstrip('v')  # v1.0.0 → 1.0.0
        return f"{base}_{clean_version}"
    return base


def check_setup_lock():
    global CONFIG_TARGET_DIR
    if CONFIG_TARGET_DIR:
        return os.path.exists(os.path.join(CONFIG_TARGET_DIR, "setup.lock"))
    return False


def open_target_directory():
    try:
        if os.path.exists(CONFIG_TARGET_DIR):
            os.startfile(CONFIG_TARGET_DIR)
    except Exception:
        pass


def main():
    global LOG_FILE, CONFIG_TARGET_DIR
    lock_file = os.path.join(os.path.dirname(sys.argv[0]), "setup.lock")
    if os.path.exists(lock_file):
        sys.exit(1)

    try:
        with open(lock_file, 'w') as f:
            f.write(f"Lock created at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if GUI_AVAILABLE:
            app = InstallerApp()
            app.mainloop()
        else:
            print("GUI not available. Please install tkinter to use the GUI installer.")
            sys.exit(1)
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)

    if CONFIG_TARGET_DIR:
        LOG_FILE = os.path.join(CONFIG_TARGET_DIR, "installation.log")
    else:
        LOG_FILE = os.path.join(os.path.expanduser("~"), "hitman_edge_install.log")


if __name__ == "__main__":
    main()