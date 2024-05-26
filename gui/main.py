# Import statements
from os import close
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from syntax import *
from autocomplete import *

class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, completer, parent=None):
        super().__init__(parent)
        self.completer = completer
        self.indentation = " " * 4

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        current_line = cursor.block().text()
        current_position = cursor.positionInBlock()

        if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            cursor.insertText("\n")
            if current_line.strip().endswith(":") or current_line.strip().endswith("{"):
                cursor.insertText(self.indentation)
            return

        if event.key() == QtCore.Qt.Key.Key_Backspace:
            if current_line[:current_position].endswith(self.indentation):
                for _ in range(len(self.indentation)):
                    cursor.deletePreviousChar()
                return

        if self.completer.popup().isVisible():
            if event.key() in (QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Escape, QtCore.Qt.Key.Key_Tab, QtCore.Qt.Key.Key_Backtab):
                event.ignore()
                return

        super().keyPressEvent(event)
        self.handle_autocomplete(event)

    def handle_autocomplete(self, event):
        isShortcut = (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier) and event.key() == QtCore.Qt.Key.Key_Space
        if not self.completer or not isShortcut:
            return

        completionPrefix = self.textUnderCursor()
        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 460)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fontComboBox = QtWidgets.QFontComboBox(parent=self.centralwidget)
        self.fontComboBox.setGeometry(QtCore.QRect(180, 0, 191, 19))
        self.fontComboBox.setObjectName("fontComboBox")
        self.plainTextEdit = CustomPlainTextEdit(None, parent=self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 20, 671, 401))
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionSave.triggered.connect(self.save_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.fontComboBox.currentFontChanged.connect(self.change_font)

        # Add Autocompletion
        self.completer = QtWidgets.QCompleter()
        self.completer.setWidget(self.plainTextEdit)
        self.model = QtGui.QStandardItemModel(self.completer)
        self.completer.setModel(self.model)
        self.completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

        self.plainTextEdit.completer = self.completer
        self.plainTextEdit.textChanged.connect(self.update_completions)

        self.filename = None
        self.current_highlighter = None

    def save_file(self):
        self.filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "All Files (*)")
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.plainTextEdit.toPlainText())
            self.update_completions()
            self.apply_highlighter()

    def open_file(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*)")
        if self.filename:
            with open(self.filename, 'r') as f:
                file_content = f.read()
                self.plainTextEdit.setPlainText(file_content)
            self.update_completions()
            self.apply_highlighter()

    def apply_highlighter(self):
        if self.current_highlighter:
            self.current_highlighter.setDocument(None)
            self.current_highlighter = None

        if self.filename.endswith('.py'):
            self.current_highlighter = PythonHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.html'):
            self.current_highlighter = HTMLHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.cpp') or self.filename.endswith('.h'):
            self.current_highlighter = CppHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.css'):
            self.current_highlighter = CSSHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.cs'):
            self.current_highlighter = CSharpHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.c'):
            self.current_highlighter = CHighlighter(self.plainTextEdit.document())
        elif self.filename.endswith('.js'):
            self.current_highlighter = JavaScriptHighlighter(self.plainTextEdit.document())

    def update_completions(self):
        cursor = self.plainTextEdit.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
        word_fragment = cursor.selectedText()

        if not word_fragment:
            return

        if self.filename and self.filename.endswith('.py'):
            suggestions = PythonSuggestions.get_suggestions
        elif self.filename and self.filename.endswith('.html'):
            suggestions = HTMLSuggestions.get_suggestions
        elif self.filename and (self.filename.endswith('.cpp') or self.filename.endswith('.h')):
            suggestions = CppSuggestions.get_suggestions
        elif self.filename and self.filename.endswith('.css'):
            suggestions = CSSSuggestions.get_suggestions
        elif self.filename and self.filename.endswith('.cs'):
            suggestions = CSharpSuggestions.get_suggestions
        elif self.filename and self.filename.endswith('.c'):
            suggestions = CSuggestions.get_suggestions
        elif self.filename and self.filename.endswith('.js'):
            suggestions = JavaScriptSuggestions.get_suggestions
        else:
            suggestions = lambda word_fragment: []

        suggestions_list = suggestions(word_fragment)
        self.model.clear()
        for suggestion in suggestions_list:
            item = QtGui.QStandardItem(suggestion)
            self.model.appendRow(item)

        self.completer.setCompletionPrefix(word_fragment)
        cursor_rect = self.plainTextEdit.cursorRect()
        cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0) +
                             self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cursor_rect)

    def insert_completion(self, completion):
        cursor = self.plainTextEdit.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
        cursor.insertText(completion)
        self.plainTextEdit.setTextCursor(cursor)

    def change_font(self):
        font = self.fontComboBox.currentFont()
        self.plainTextEdit.setFont(font)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
