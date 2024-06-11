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
            r'\bdef\b', r'\bclass\b', r'\bimport\b', r'\bFalse\b', r'\bNone\b', r'\bTrue\b', r'\band\b', r'\bas\b', r'\bassert\b',
            r'\basync\b', r'\bawait\b', r'\bbreak\b', r'\bcontinue\b', r'\bdel\b', r'\belif\b', r'\belse\b', r'\bexcept\b',
            r'\bfinally\b', r'\bfor\b', r'\bfrom\b', r'\bglobal\b', r'\bif\b', r'\bin\b', r'\bis\b', r'\blambda\b', r'\bnonlocal\b',
            r'\bnot\b', r'\bpass\b', r'\braise\b', r'\breturn\b', r'\btry\b', r'\bwhile\b', r'\bwith\b', r'\byield\b', r'\bprint\b'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

        # Define the format for comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression('#.*'), comment_format))

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

        tags_format = QtGui.QTextCharFormat()
        tags_format.setForeground(QtGui.QColor('blue'))
        tags = [
            'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo', 'blockquote', 'body', 'button',
            'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div',
            'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head',
            'header', 'hgroup', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map',
            'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre',
            'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style',
            'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
            'u', 'ul', 'var', 'video', 'wbr'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), tags_format) for pattern in tags]

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

        properties_format = QtGui.QTextCharFormat()
        properties_format.setForeground(QtGui.QColor('blue'))
        properties = [
            'color', 'background', 'margin', 'padding', 'border', 'width', 'height', 'font-size', 'font-weight', 'text-align'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), properties_format) for pattern in properties]

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
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
            'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas',
            '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), keyword_format) for pattern in keyword_patterns]

        # Define the format for C++ comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression('//.*'), comment_format))
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
            'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const', 'continue',
            'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally',
            'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock', 'long',
            'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected', 'public',
            'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string', 'struct',
            'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual',
            'void', 'volatile', 'while'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), keyword_format) for pattern in keyword_patterns]

        # Define the format for C# comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression('//.*'), comment_format))
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
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
            'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas',
            '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), keyword_format) for pattern in keyword_patterns]

        # Define the format for C comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression('//.*'), comment_format))
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
            'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export',
            'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'let', 'new', 'return', 'super', 'switch',
            'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield'
        ]
        self.highlighting_rules += [(QtCore.QRegularExpression(f'\\b{pattern}\\b'), keyword_format) for pattern in keyword_patterns]

        # Define the format for JavaScript comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor('green'))
        self.highlighting_rules.append((QtCore.QRegularExpression('//.*'), comment_format))
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