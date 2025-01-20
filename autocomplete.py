class PythonSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'print',
            'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
            'str', 'int', 'float', 'type', 'len', 'or'

        ]
        return [kw for kw in keywords if kw.startswith(word_fragment)]

class CSSSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        properties = [
            'color', 'background', 'margin', 'padding', 'border', 'width', 'height', 'font-size', 'font-weight', 'text-align'
        ]
        return [prop for prop in properties if prop.startswith(word_fragment)]

class CppSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
            'float', 'print', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas',
            '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
        ]
        return [kw for kw in keywords if kw.startswith(word_fragment)]

class CSharpSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const', 'continue',
            'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally',
            'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock', 'long',
            'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected', 'public',
            'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string', 'struct',
            'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual',
            'void', 'volatile', 'while'
        ]
        return [kw for kw in keywords if kw.startswith(word_fragment)]

class CSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
            'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas',
            '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
        ]
        return [kw for kw in keywords if kw.startswith(word_fragment)]

class JavaScriptSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export',
            'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'let', 'new', 'return', 'super', 'switch',
            'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield'
        ]
        return [kw for kw in keywords if kw.startswith(word_fragment)]

class HTMLSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        tags = [
            'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button',
            'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div',
            'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head',
            'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map',
            'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre',
            'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style',
            'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
            'u', 'ul', 'var', 'video', 'wbr'
        ]
        return [tag for tag in tags if tag.startswith(word_fragment)]