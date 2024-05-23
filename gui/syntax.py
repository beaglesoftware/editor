from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os
import re

class PythonHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor('blue'))
        keyword_patterns = [
            r'\bdef\b', r'\bclass\b', r'\bif\b', r'\belse\b', r'\bfor\b',
            r'\bwhile\b', r'\breturn\b', r'\bimport\b', r'\bfrom\b',
            r'\bas\b', r'\bwith\b', r'\bself\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'#.*'), comment_format))

        # Define the format for strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r"'.*?'"), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class HTMLHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for HTML tags
        tag_format = QtGui.QTextCharFormat()
        tag_format.setForeground(QtGui.QColor('blue'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'<[^>]+>'), tag_format))

        # Define the format for HTML comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'<!--[^>]+-->'), comment_format))

        # Define the format for HTML attributes
        attr_format = QtGui.QTextCharFormat()
        attr_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'\b[a-zA-Z-]+(?=\=)'), attr_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CSSHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for CSS selectors
        selector_format = QtGui.QTextCharFormat()
        selector_format.setForeground(QtGui.QColor('blue'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'\b\w+\b'), selector_format))

        # Define the format for CSS properties
        property_format = QtGui.QTextCharFormat()
        property_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'\b\w+\b(?=\s*:)'), property_format))

        # Define the format for CSS values
        value_format = QtGui.QTextCharFormat()
        value_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r':\s*\b\w+\b'), value_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CppHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for C++ keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor('blue'))
        keyword_patterns = [
            r'\bint\b', r'\bfloat\b', r'\bdouble\b', r'\bchar\b',
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b',
            r'\breturn\b', r'\b#include\b', r'\bnamespace\b',
            r'\busing\b', r'\bclass\b', r'\bpublic\b', r'\bprivate\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for C++ comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'//.*'), comment_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'/\*.*\*/'), comment_format))

        # Define the format for C++ strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'".*?"'), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CSharpHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for C# keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor('blue'))
        keyword_patterns = [
            r'\bnamespace\b', r'\busing\b', r'\bclass\b', r'\bstruct\b',
            r'\bint\b', r'\bfloat\b', r'\bdouble\b', r'\bchar\b',
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b',
            r'\breturn\b', r'\bpublic\b', r'\bprivate\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for C# comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'//.*'), comment_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'/\*.*\*/'), comment_format))

        # Define the format for C# strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'".*?"'), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for C keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor('blue'))
        keyword_patterns = [
            r'\bint\b', r'\bfloat\b', r'\bdouble\b', r'\bchar\b',
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b',
            r'\breturn\b', r'\b#include\b', r'\bstruct\b', r'\btypedef\b',
            r'\bextern\b', r'\bvoid\b', r'\bsizeof\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for C comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'//.*'), comment_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'/\*.*\*/'), comment_format))

        # Define the format for C strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'".*?"'), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class JavaScriptHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Define the format for JavaScript keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor('blue'))
        keyword_patterns = [
            r'\bvar\b', r'\blet\b', r'\bconst\b', r'\bfunction\b',
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b',
            r'\breturn\b', r'\bimport\b', r'\bexport\b', r'\bclass\b',
            r'\btry\b', r'\bcatch\b', r'\bfinally\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for JavaScript comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'//.*'), comment_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'/\*.*\*/'), comment_format))

        # Define the format for JavaScript strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor('red'))
        self.highlighting_rules.append((QtCore.QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QtCore.QRegularExpression(r"'.*?'"), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
