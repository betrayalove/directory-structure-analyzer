import os
import sys
import shutil
import subprocess

APP_NAME = "directory_analyzer"
ICON = "icon.ico"
MAIN_SCRIPT = "directory_analyzer.py"
DIST_DIR = "dist"

def clean():
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for file in os.listdir():
        if file.endswith(".spec"):
            os.remove(file)

def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--icon={ICON}",
        MAIN_SCRIPT
    ]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    print("Cleaning previous builds...")
    clean()
    print("Building executable...")
    build()
    print(f"Build finished. The EXE is in the '{DIST_DIR}' folder.")

if __name__ == "__main__":
    main() 