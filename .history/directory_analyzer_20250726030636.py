import os
import sys
import urllib.parse
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextBrowser, QCheckBox, QSpinBox,
    QFileDialog, QHBoxLayout, QGroupBox, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QFont, QTextCursor


class DirectoryStructureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = 'rus'
        self.setWindowTitle("Анализатор структуры директорий")
        self.setGeometry(100, 100, 800, 600)
        self.statusBar().showMessage("Готово")
        self.system_dirs = {
            '__pycache__', 'node_modules', '.git', '.idea', '.vscode', 'venv', 'env', 'dist', 'build', 'target',
            '__MACOSX', '.svn', '.hg', 'bin', 'obj', 'migrations', '__ignored__', 'cache', 'logs', 'temp'
        }
        self.special_chars = {'~', '#', '%', '&', '*', '{', '}', '\\', ':', '<', '>', '?', '/', '+', '|', '"'}
        self.ui_texts = {
            'rus': {
                'window_title': "Анализатор структуры директорий",
                'directory': "Директория",
                'path_placeholder': "Укажите путь или выберите директорию...",
                'browse': "Обзор...",
                'settings': "Настройки фильтрации",
                'max_depth': "Макс. глубина:",
                'prefix': "Префикс отступа:",
                'ignore_hidden': "Игнорировать скрытые папки и файлы (системные)",
                'ignore_dot_dirs': "Игнорировать папки, начинающиеся с .",
                'ignore_dot_files': "Игнорировать файлы, начинающиеся с .",
                'ignore_special_dirs': "Игнорировать папки, начинающиеся на спецсимвол",
                'ignore_special_files': "Игнорировать файлы, начинающиеся на спецсимвол",
                'ignore_system_dirs': "Игнорировать служебные папки",
                'custom_excludes': "Дополнительные фильтры:",
                'custom_excludes_placeholder': "Например: *.tmp, temp/, backup*",
                'generate': "Сгенерировать структуру",
                'ready': "Готово",
                'language': "ENG",
                'error_path_not_exists': "Ошибка: Укажите путь к директории",
                'error_title': "Ошибка",
                'error_not_file': "Указанный путь не является файлом",
                'error_open_file': "Не удалось открыть файл: {}",
                'copied': "✓ Скопировано: {}",
                'binary_file': "× Ошибка: файл {} бинарный"
            },
            'eng': {
                'window_title': "Directory Structure Analyzer",
                'directory': "Directory",
                'path_placeholder': "Enter path or select directory...",
                'browse': "Browse...",
                'settings': "Filter Settings",
                'max_depth': "Max depth:",
                'prefix': "Indent prefix:",
                'ignore_hidden': "Ignore hidden folders and files (system)",
                'ignore_dot_dirs': "Ignore folders starting with .",
                'ignore_dot_files': "Ignore files starting with .",
                'ignore_special_dirs': "Ignore folders starting with special char",
                'ignore_special_files': "Ignore files starting with special char",
                'ignore_system_dirs': "Ignore system folders",
                'custom_excludes': "Additional filters:",
                'custom_excludes_placeholder': "Example: *.tmp, temp/, backup*",
                'generate': "Generate Structure",
                'ready': "Ready",
                'language': "RUS",
                'error_path_not_exists': "Error: Please specify directory path",
                'error_title': "Error",
                'error_not_file': "The specified path is not a file",
                'error_open_file': "Failed to open file: {}",
                'copied': "✓ Copied: {}",
                'binary_file': "× Error: file {} is binary"
            }
        }
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        path_group = QGroupBox(self.ui_texts[self.current_language]['directory'])
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(self.ui_texts[self.current_language]['path_placeholder'])
        browse_btn = QPushButton(self.ui_texts[self.current_language]['browse'])
        browse_btn.clicked.connect(self.browse_directory)
        self.language_btn = QPushButton(self.ui_texts[self.current_language]['language'])
        self.language_btn.clicked.connect(self.toggle_language)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        path_layout.addWidget(self.language_btn)
        path_group.setLayout(path_layout)
        settings_group = QGroupBox(self.ui_texts[self.current_language]['settings'])
        settings_layout = QFormLayout()
        self.depth_spin = QSpinBox()
        self.depth_spin.setRange(1, 20)
        self.depth_spin.setValue(5)
        settings_layout.addRow(self.ui_texts[self.current_language]['max_depth'], self.depth_spin)
        self.prefix_input = QLineEdit("    ")
        settings_layout.addRow(self.ui_texts[self.current_language]['prefix'], self.prefix_input)
        self.ignore_hidden_check = QCheckBox(self.ui_texts[self.current_language]['ignore_hidden'])
        self.ignore_hidden_check.setChecked(True)
        settings_layout.addRow(self.ignore_hidden_check)
        self.ignore_dot_dirs_check = QCheckBox(self.ui_texts[self.current_language]['ignore_dot_dirs'])
        self.ignore_dot_dirs_check.setChecked(True)
        settings_layout.addRow(self.ignore_dot_dirs_check)
        self.ignore_dot_files_check = QCheckBox(self.ui_texts[self.current_language]['ignore_dot_files'])
        self.ignore_dot_files_check.setChecked(False)
        settings_layout.addRow(self.ignore_dot_files_check)
        self.ignore_special_dirs_check = QCheckBox(self.ui_texts[self.current_language]['ignore_special_dirs'])
        self.ignore_special_dirs_check.setChecked(True)
        self.ignore_special_dirs_check.setToolTip(f"Special chars: {''.join(sorted(self.special_chars))}")
        settings_layout.addRow(self.ignore_special_dirs_check)
        self.ignore_special_files_check = QCheckBox(self.ui_texts[self.current_language]['ignore_special_files'])
        self.ignore_special_files_check.setChecked(True)
        self.ignore_special_files_check.setToolTip(f"Special chars: {''.join(sorted(self.special_chars))}")
        settings_layout.addRow(self.ignore_special_files_check)
        self.ignore_system_dirs_check = QCheckBox(self.ui_texts[self.current_language]['ignore_system_dirs'])
        self.ignore_system_dirs_check.setChecked(True)
        self.ignore_system_dirs_check.setToolTip(f"Will be hidden: {', '.join(sorted(self.system_dirs))}")
        settings_layout.addRow(self.ignore_system_dirs_check)
        self.custom_excludes_input = QLineEdit()
        self.custom_excludes_input.setPlaceholderText(
            self.ui_texts[self.current_language]['custom_excludes_placeholder'])
        settings_layout.addRow(self.ui_texts[self.current_language]['custom_excludes'], self.custom_excludes_input)
        settings_group.setLayout(settings_layout)
        self.generate_btn = QPushButton(self.ui_texts[self.current_language]['generate'])
        self.generate_btn.clicked.connect(self.generate_structure)
        self.output_area = QTextBrowser()
        self.output_area.setReadOnly(True)
        self.output_area.setOpenLinks(False)
        self.output_area.anchorClicked.connect(self.on_link_clicked)
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.output_area.setFont(font)
        layout.addWidget(path_group)
        layout.addWidget(settings_group)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.output_area)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def toggle_language(self):
        self.current_language = 'eng' if self.current_language == 'rus' else 'rus'
        self.update_ui_texts()

    def update_ui_texts(self):
        texts = self.ui_texts[self.current_language]
        self.setWindowTitle(texts['window_title'])
        self.statusBar().showMessage(texts['ready'])
        self.findChild(QGroupBox, None).setTitle(texts['directory'])
        self.path_input.setPlaceholderText(texts['path_placeholder'])
        self.findChild(QPushButton, None).setText(texts['browse'])
        self.language_btn.setText(texts['language'])
        for group in self.findChildren(QGroupBox):
            if group.title() in [self.ui_texts['rus']['settings'], self.ui_texts['eng']['settings']]:
                group.setTitle(texts['settings'])
                break
        for i in range(self.findChild(QFormLayout).rowCount()):
            item = self.findChild(QFormLayout).itemAt(i, QFormLayout.LabelRole)
            if item and item.widget():
                label = item.widget()
                if label.text() == self.ui_texts['rus']['max_depth'] or label.text() == self.ui_texts['eng']['max_depth']:
                    label.setText(texts['max_depth'])
                elif label.text() == self.ui_texts['rus']['prefix'] or label.text() == self.ui_texts['eng']['prefix']:
                    label.setText(texts['prefix'])
                elif label.text() == self.ui_texts['rus']['custom_excludes'] or label.text() == self.ui_texts['eng']['custom_excludes']:
                    label.setText(texts['custom_excludes'])
        self.ignore_hidden_check.setText(texts['ignore_hidden'])
        self.ignore_dot_dirs_check.setText(texts['ignore_dot_dirs'])
        self.ignore_dot_files_check.setText(texts['ignore_dot_files'])
        self.ignore_special_dirs_check.setText(texts['ignore_special_dirs'])
        self.ignore_special_files_check.setText(texts['ignore_special_files'])
        self.ignore_system_dirs_check.setText(texts['ignore_system_dirs'])
        self.custom_excludes_input.setPlaceholderText(texts['custom_excludes_placeholder'])
        self.generate_btn.setText(texts['generate'])

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, self.ui_texts[self.current_language]['browse'])
        if directory:
            self.path_input.setText(directory)

    def generate_structure(self):
        path = self.path_input.text().strip()
        if not path:
            self.output_area.setPlainText(self.ui_texts[self.current_language]['error_path_not_exists'])
            return
        try:
            structure = self.get_directory_structure(
                path=path,
                max_depth=self.depth_spin.value(),
                prefix=self.prefix_input.text(),
                ignore_hidden=self.ignore_hidden_check.isChecked(),
                ignore_dot_dirs=self.ignore_dot_dirs_check.isChecked(),
                ignore_dot_files=self.ignore_dot_files_check.isChecked(),
                ignore_special_dirs=self.ignore_special_dirs_check.isChecked(),
                ignore_special_files=self.ignore_special_files_check.isChecked(),
                ignore_system_dirs=self.ignore_system_dirs_check.isChecked(),
                custom_excludes=[x.strip() for x in self.custom_excludes_input.text().split(",") if x.strip()]
            )
            self.output_area.setHtml(f"<pre>{structure}</pre>")
        except Exception as e:
            self.output_area.setPlainText(f"Error: {str(e)}")

    def get_directory_structure(self, path, max_depth=5, prefix='    ',
                                ignore_hidden=True, ignore_dot_dirs=True,
                                ignore_dot_files=False, ignore_special_dirs=True,
                                ignore_special_files=True, ignore_system_dirs=True,
                                custom_excludes=None, current_depth=0):
        if current_depth > max_depth:
            return ""
        path = Path(path)
        if not path.exists():
            return f"Path does not exist: {path}"
        current_prefix = prefix * current_depth
        result = f"{current_prefix}{path.name}/\n"
        try:
            for entry in sorted(os.listdir(path)):
                full_path = path / entry
                if self.should_exclude(
                        entry=entry,
                        full_path=full_path,
                        ignore_hidden=ignore_hidden,
                        ignore_dot_dirs=ignore_dot_dirs,
                        ignore_dot_files=ignore_dot_files,
                        ignore_special_dirs=ignore_special_dirs,
                        ignore_special_files=ignore_special_files,
                        ignore_system_dirs=ignore_system_dirs,
                        custom_excludes=custom_excludes
                ):
                    continue
                if full_path.is_dir():
                    result += self.get_directory_structure(
                        path=full_path,
                        max_depth=max_depth,
                        prefix=prefix,
                        ignore_hidden=ignore_hidden,
                        ignore_dot_dirs=ignore_dot_dirs,
                        ignore_dot_files=ignore_dot_files,
                        ignore_special_dirs=ignore_special_dirs,
                        ignore_special_files=ignore_special_files,
                        ignore_system_dirs=ignore_system_dirs,
                        custom_excludes=custom_excludes,
                        current_depth=current_depth + 1
                    )
                else:
                    file_url = QUrl.fromLocalFile(str(full_path)).toString()
                    result += f'{current_prefix}{prefix}<a href="{file_url}" style="color: blue; text-decoration: underline;">{entry}</a>\n'
        except PermissionError:
            result += f"{current_prefix}{prefix}[Permission denied]\n"
        return result

    def on_link_clicked(self, url):
        try:
            file_path = Path(url.toLocalFile())
            if not file_path.exists():
                file_path = Path(urllib.parse.unquote(url.toString()))
                if not file_path.exists():
                    raise FileNotFoundError
            if file_path.is_file():
                self.copy_file_contents(file_path)
            else:
                QMessageBox.warning(self, self.ui_texts[self.current_language]['error_title'],
                                    self.ui_texts[self.current_language]['error_not_file'])
        except Exception as e:
            QMessageBox.warning(self, self.ui_texts[self.current_language]['error_title'],
                                self.ui_texts[self.current_language]['error_open_file'].format(str(e)))

    def copy_file_contents(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contents = f.read()
            clipboard = QApplication.clipboard()
            clipboard.setText(contents)
            self.statusBar().showMessage(self.ui_texts[self.current_language]['copied'].format(file_path.name), 2000)
        except UnicodeDecodeError:
            self.statusBar().showMessage(self.ui_texts[self.current_language]['binary_file'].format(file_path.name),
                                         2000)
        except Exception as e:
            self.statusBar().showMessage(f"× Error: {str(e)}", 2000)

    def show_error_message(self, message):
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_area.setTextCursor(cursor)
        self.output_area.insertHtml(f'<br><span style="color: red;">{message}</span><br>')

    def should_exclude(self, entry, full_path, ignore_hidden,
                       ignore_dot_dirs, ignore_dot_files,
                       ignore_special_dirs, ignore_special_files,
                       ignore_system_dirs, custom_excludes):
        if ignore_system_dirs and full_path.is_dir() and entry in self.system_dirs:
            return True
        if ignore_hidden and self.is_hidden(full_path):
            return True
        if ignore_dot_dirs and full_path.is_dir() and entry.startswith('.'):
            return True
        if ignore_dot_files and not full_path.is_dir() and entry.startswith('.'):
            return True
        if ignore_special_dirs and full_path.is_dir() and entry[0] in self.special_chars:
            return True
        if ignore_special_files and not full_path.is_dir() and entry[0] in self.special_chars:
            return True
        if custom_excludes:
            for pattern in custom_excludes:
                pattern = pattern.strip()
                if not pattern:
                    continue
                if pattern.endswith('/'):
                    if not full_path.is_dir():
                        continue
                    pattern = pattern[:-1]
                if pattern == entry:
                    return True
                if pattern.startswith('*') and entry.endswith(pattern[1:]):
                    return True
                if pattern.endswith('*') and entry.startswith(pattern[:-1]):
                    return True
                if pattern.startswith('*') and pattern.endswith('*') and pattern[1:-1] in entry:
                    return True
        return False

    def is_hidden(self, path):
        try:
            if os.name == 'nt':
                import ctypes
                return bool(ctypes.windll.kernel32.GetFileAttributesW(str(path)) & 2)
            else:
                return path.name.startswith('.')
        except:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirectoryStructureApp()
    window.show()
    sys.exit(app.exec_())