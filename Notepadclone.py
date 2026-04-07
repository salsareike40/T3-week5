
#NAMA: SALSA REIKE MAHARANI
#NIM: F1D02310136
#KELAS: C

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QFontDialog, QDialog, QVBoxLayout,
    QLineEdit, QLabel, QDialogButtonBox, QStyle
)
from PySide6.QtGui import QAction, QKeySequence, QTextCursor, QTextCharFormat, QColor
from PySide6.QtCore import Qt, QSize


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find & Replace")

        layout = QVBoxLayout()

        self.find_input = QLineEdit()
        self.replace_input = QLineEdit()

        layout.addWidget(QLabel("Find:"))
        layout.addWidget(self.find_input)

        layout.addWidget(QLabel("Replace:"))
        layout.addWidget(self.replace_input)

        self.button_box = QDialogButtonBox()
        self.find_btn = self.button_box.addButton("Find Next", QDialogButtonBox.ActionRole)
        self.replace_btn = self.button_box.addButton("Replace", QDialogButtonBox.ActionRole)
        self.replace_all_btn = self.button_box.addButton("Replace All", QDialogButtonBox.ActionRole)

        layout.addWidget(self.button_box)
        self.setLayout(layout)


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.is_modified = False

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self.setWindowTitle("Untitled - Notepad")
        self.resize(800, 600)

        self.create_actions()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.apply_style()

        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.cursorPositionChanged.connect(self.update_status)

    def create_actions(self):
        self.new_act = QAction("New", self)
        self.new_act.setShortcut(QKeySequence.New)
        self.new_act.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.new_act.triggered.connect(self.new_file)

        self.open_act = QAction("Open", self)
        self.open_act.setShortcut(QKeySequence.Open)
        self.open_act.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.open_act.triggered.connect(self.open_file)

        self.save_act = QAction("Save", self)
        self.save_act.setShortcut(QKeySequence.Save)
        self.save_act.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_act.triggered.connect(self.save_file)

        self.save_as_act = QAction("Save As", self)
        self.save_as_act.setShortcut("Ctrl+Shift+S")
        self.save_as_act.triggered.connect(self.save_as)

        self.exit_act = QAction("Exit", self)
        self.exit_act.triggered.connect(self.close)

        self.undo_act = QAction("Undo", self)
        self.undo_act.setShortcut(QKeySequence.Undo)
        self.undo_act.triggered.connect(self.editor.undo)

        self.redo_act = QAction("Redo", self)
        self.redo_act.setShortcut(QKeySequence.Redo)
        self.redo_act.triggered.connect(self.editor.redo)

        self.cut_act = QAction("Cut", self)
        self.cut_act.setShortcut(QKeySequence.Cut)
        self.cut_act.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))  # ⬅️ TAMBAH INI
        self.cut_act.triggered.connect(self.editor.cut)

        self.copy_act = QAction("Copy", self)
        self.copy_act.setShortcut(QKeySequence.Copy)
        self.copy_act.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))  # ⬅️ TAMBAH
        self.copy_act.triggered.connect(self.editor.copy)

        self.paste_act = QAction("Paste", self)
        self.paste_act.setShortcut(QKeySequence.Paste)
        self.paste_act.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))  # ⬅️ TAMBAH
        self.paste_act.triggered.connect(self.editor.paste)

        self.select_all_act = QAction("Select All", self)
        self.select_all_act.setShortcut(QKeySequence.SelectAll)
        self.select_all_act.triggered.connect(self.editor.selectAll)

        self.font_act = QAction("Font", self)
        self.font_act.triggered.connect(self.choose_font)

        self.wrap_act = QAction("Word Wrap", self, checkable=True)
        self.wrap_act.setChecked(True)
        self.wrap_act.triggered.connect(self.toggle_wrap)

        self.find_act = QAction("Find", self)
        self.find_act.setShortcut(QKeySequence.Find)
        self.find_act.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))  # ⬅️ TAMBAH
        self.find_act.triggered.connect(self.open_find_dialog)

    def create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addActions([
            self.new_act, self.open_act,
            self.save_act, self.save_as_act,
            self.exit_act
        ])

        edit_menu = menu.addMenu("Edit")
        edit_menu.addActions([
            self.undo_act, self.redo_act,
            self.cut_act, self.copy_act,
            self.paste_act, self.select_all_act,
            self.find_act
        ])

        format_menu = menu.addMenu("Format")
        format_menu.addAction(self.font_act)
        format_menu.addAction(self.wrap_act)

        help_menu = menu.addMenu("Help")
        about_act = QAction("About", self)
        about_act.triggered.connect(lambda: QMessageBox.information(self, "About", "Notepad Clone PySide6"))
        help_menu.addAction(about_act)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")

        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        toolbar.setIconSize(QSize(16, 16))  
        toolbar.setMinimumHeight(32)           

        toolbar.addAction(self.new_act)
        toolbar.addAction(self.open_act)
        toolbar.addAction(self.save_act)

        toolbar.addSeparator()

        toolbar.addAction(self.cut_act)
        toolbar.addAction(self.copy_act)
        toolbar.addAction(self.paste_act)

        toolbar.addSeparator()

        toolbar.addAction(self.find_act)

    def create_statusbar(self):
        self.status = self.statusBar()
        self.update_status()

    def update_status(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        char_count = len(self.editor.toPlainText())

        self.status.showMessage(f"Baris: {line} | Karakter: {char_count}")

    def new_file(self):
        if self.confirm_exit():
            self.editor.clear()
            self.file_path = None
            self.setWindowTitle("Untitled - Notepad")
            self.is_modified = False

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.editor.setText(f.read())
            self.file_path = path
            self.setWindowTitle(os.path.basename(path) + " - Notepad")
            self.is_modified = False

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.is_modified = False
            self.setWindowTitle(os.path.basename(self.file_path) + " - Notepad")
        else:
            self.save_as()

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File")
        if path:
            self.file_path = path
            self.save_file()

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)

    def toggle_wrap(self):
        if self.wrap_act.isChecked():
            self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.editor.setLineWrapMode(QTextEdit.NoWrap)

    def open_find_dialog(self):
        self.dialog = FindReplaceDialog(self)
        self.dialog.find_btn.clicked.connect(self.find_text)
        self.dialog.replace_btn.clicked.connect(self.replace_text)
        self.dialog.replace_all_btn.clicked.connect(self.replace_all)
        self.dialog.show()

    def find_text(self):
        text = self.dialog.find_input.text()
        
        if not text:
            return

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Start)

        extra_selections = []

        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("#2980b9"))
        highlight_format.setForeground(QColor("white"))         

        while True:
            cursor = self.editor.document().find(text, cursor)
            if cursor.isNull():
                break

            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format = highlight_format
            extra_selections.append(selection)

        self.editor.setExtraSelections(extra_selections)

    def replace_text(self):
        text = self.dialog.find_input.text()
        replace = self.dialog.replace_input.text()

        if not text:
            return

        # cari dari awal
        cursor = QTextCursor(self.editor.document())
        cursor = self.editor.document().find(text, cursor)

        if not cursor.isNull():
            cursor.insertText(replace)

            # pindahkan cursor ke hasil
            self.editor.setTextCursor(cursor)

            # highlight ulang
            self.find_text()

    def replace_all(self):
        text = self.dialog.find_input.text()
        replace = self.dialog.replace_input.text()
        content = self.editor.toPlainText().replace(text, replace)
        self.editor.setText(content)

    def on_text_changed(self):
        if not self.is_modified:
            self.setWindowTitle(self.windowTitle() + " *")
        self.is_modified = True

    def confirm_exit(self):
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Konfirmasi",
                "Perubahan belum disimpan. Keluar?",
                QMessageBox.Yes | QMessageBox.No
            )
            return reply == QMessageBox.Yes
        return True

    def closeEvent(self, event):
        if self.confirm_exit():
            event.accept()
        else:
            event.ignore()

    def apply_style(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                font-family: Consolas;
                font-size: 14px;
            }

            QMenuBar {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
            }

            QMenuBar::item:selected {
                background-color: #34495e;
            }

            QToolBar {
                background-color: #ecf0f1;
                spacing: 4px;
                padding: 4px;
                border-bottom: 1px solid #ccc;
            }

            QToolButton {
                background-color: #ffffff;
                border: 1px solid #ccc;
                padding: 3px 8px;
                border-radius: 4px;
                min-width: 60px;
                color: black;
            }

           QToolButton:hover {
                background-color: #dfe6e9;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec())
