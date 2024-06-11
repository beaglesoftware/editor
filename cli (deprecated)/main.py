import importlib
import argparse
import inspect
import curses
import sys
import ast
import os
import re

from pyparsing import java_style_comment

class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def scroll_up(self):
        if self.row > 0:
            self.row -= 1

    def scroll_down(self, buffer):
        if self.bottom < len(buffer) - 1:
            self.row += 1

    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col

    def adjust_horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        if cursor.col < self.col + left_margin:
            self.col = max(cursor.col - left_margin, 0)
        elif cursor.col >= self.col + self.n_cols - right_margin:
            self.col = cursor.col - self.n_cols + right_margin + 1

class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Cursor(row={self.row}, col={self.col})"

    def _clamp_col(self, buffer):
        self.col = min(self.col, len(buffer[self.row]))

    def move_up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def move_down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._clamp_col(buffer)

    def move_to(self, row, col):
        self.row = row
        self.col = col

    def move_left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def move_right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 1
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0

    def insert_newline(self, buffer):
        current_line = buffer[self.row]
        if current_line.strip().endswith(':') or current_line.strip().endswith('{'):
            new_line_content = ' ' * 4
            buffer.split(self)
            buffer[self.row + 1] = new_line_content + buffer[self.row + 1]
            self.row += 1
            self.col = len(new_line_content)
        else:
            buffer.split(self)
            self.row += 1
            self.col = 0

    def backspace(self, buffer):
        print(f"Before backspace: {buffer.lines}, {self}")
        if self.col > 0:
            current = buffer[self.row]
            buffer[self.row] = current[:self.col - 1] + current[self.col:]
            self.col -= 1
        elif self.row > 0:
            prev_line_length = len(buffer[self.row - 1])
            buffer.join_with_previous_line(self)
            self.row -= 1
            self.col = prev_line_length
        print(f"After backspace: {buffer.lines}, {self}")

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, idx, value):
        self.lines[idx] = value

    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        while row >= len(self.lines):
            self.lines.append('')

        current = self.lines[row]
        self.lines[row] = current[:col] + string + current[col:]

    def split(self, cursor):
        row, col = cursor.row, cursor.col
        if row >= len(self.lines):
            raise IndexError(f"Cursor row {row} is out of range.")
        
        current = self.lines[row]
        self.lines[row] = current[:col]
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if col > 0:
            current = self.lines[row]
            self.lines[row] = current[:col - 1] + current[col:]
            cursor.col -= 1
        elif row > 0:
            cursor.row -= 1
            cursor.col = len(self.lines[cursor.row])
            self.lines[cursor.row] += self.lines.pop(row)

    def join_with_previous_line(self, cursor):
        if cursor.row > 0:
            cursor.col = len(self.lines[cursor.row - 1])
            self.lines[cursor.row - 1] += self.lines.pop(cursor.row)
            cursor.row -= 1

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.lines))
            return True

    def doublequote(self, cursor):
        row, col = cursor.row, cursor.col
        while row >= len(self.lines):
            self.lines.append('')
        
        current = self.lines[row]
        self.lines[row] = current[:col] + '"' + current[col:]

    def singlequote(self, cursor):
        row, col = cursor.row, cursor.col
        while row >= len(self.lines):
            self.lines.append('')
        
        current = self.lines[row]
        self.lines[row] = current[:col] + "'" + current[col:]



class HighlighterBase:
    def apply_highlighting(self, stdscr, text, start_row, highlighting_rules):
        stdscr.addstr(start_row, 0, text)
        for pattern, color in highlighting_rules:
            for match in re.finditer(pattern, text):
                stdscr.addstr(start_row, match.start(), match.group(), color)

class PythonHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'\b(def|class|if|else|while|for|return|import|from|as|with|self)\b', curses.color_pair(1)),
            (r'#.*$', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
            (r"'.*?'", curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class CSSHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'(\b\w+\b)(?=\s*{)', curses.color_pair(1)),
            (r'(\b\w+\b)(?=\s*:\s*")', curses.color_pair(2)),
            (r':\s*".*?"', curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class CppHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'\b(int|float|double|char|if|else|while|for|return|#include|namespace|using|class|public|private)\b', curses.color_pair(1)),
            (r'//.*$', curses.color_pair(2)),
            (r'/\*.*?\*/', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class CSharpHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'\b(namespace|using|class|struct|int|float|double|char|if|else|while|for|return|public|private)\b', curses.color_pair(1)),
            (r'//.*$', curses.color_pair(2)),
            (r'/\*.*?\*/', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class CHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'\b(int|float|double|char|if|else|while|for|return|#include|struct|typedef|extern|void|sizeof)\b', curses.color_pair(1)),
            (r'//.*$', curses.color_pair(2)),
            (r'/\*.*?\*/', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

def select_highlighter(file_extension):
    highlighters = {
        '.py': PythonHighlighter(),
        '.css': CSSHighlighter(),
        '.cpp': CppHighlighter(),
        '.cs': CSharpHighlighter(),
        '.c': CHighlighter(),
    }
    return highlighters.get(file_extension)

class PythonSuggestions:
    @staticmethod
    def get_suggestions(word_fragment):
        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
            'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
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
            'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed',
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

class Autocomplete:
    def __init__(self, suggestion_classes):
        self.suggestion_classes = suggestion_classes

    def suggest(self, word_fragment):
        suggestions = []
        for suggestion_class in self.suggestion_classes:
            try:
                module_name = suggestion_class.__module__
                module = importlib.import_module(module_name)
                suggestions += suggestion_class().get_suggestions(word_fragment)
            except AttributeError as e:
                print(f"Error in suggestion class {suggestion_class.__name__}: {e}", file=sys.stderr)
        return suggestions

    def suggest_from_module(self, partial_name, module_name):
        try:
            module = importlib.import_module(module_name)
            return [name for name in dir(module) if name.startswith(partial_name)]
        except ImportError:
            return []
    
    def show_suggestions(self, stdscr, suggestions):
        # Get screen dimensions
        max_y, max_x = stdscr.getmaxyx()

        # Define popup window size and position
        popup_height = len(suggestions) + 2
        popup_width = max(max(len(s) for s in suggestions) + 4, 20)  # Adjust width based on longest suggestion
        start_y = (max_y - popup_height) // 2
        start_x = (max_x - popup_width) // 2

        # Create a temporary window for the popup
        popup = curses.newwin(popup_height, popup_width, start_y, start_x)
        popup.box()

        # Initialize user input
        selected_suggestion = 0

        while True:
            # Clear previous suggestions
            popup.clear()
            popup.box()

            # Display suggestions
            for idx, suggestion in enumerate(suggestions):
                if idx == selected_suggestion:
                    popup.addstr(idx + 1, 2, suggestion, curses.A_REVERSE)
                else:
                    popup.addstr(idx + 1, 2, suggestion)

            stdscr.refresh()
            popup.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_suggestion = (selected_suggestion - 1) % len(suggestions)
            elif key == curses.KEY_DOWN:
                selected_suggestion = (selected_suggestion + 1) % len(suggestions)
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
                return suggestions[selected_suggestion]
            elif key == 27:  # ESC key
                return None


def show_popup_input(stdscr, message):
    # Get screen dimensions
    max_y, max_x = stdscr.getmaxyx()

    # Define popup window size and position
    popup_height = 7
    popup_width = max(len(message) + 20, 50)  # Adjust width based on message length
    start_y = (max_y - popup_height) // 2
    start_x = (max_x - popup_width) // 2

    # Create a temporary window for the popup
    popup = curses.newwin(popup_height, popup_width, start_y, start_x)
    popup.box()

    # Display message
    message_y = 2  # Adjust for positioning within the popup
    message_x = 2
    popup.addstr(message_y, message_x, message)

    # Create an entry field for user input
    entry_y = message_y + 2
    entry_x = message_x + 1  # Adjust to leave space for the border
    entry_width = popup_width - (message_x * 2) - 2  # Account for borders

    # Refresh all windows
    stdscr.refresh()
    popup.refresh()

    # Initialize user input
    user_input = []

    while True:
        key = popup.getch(entry_y, entry_x + len(user_input))

        if key in (10, 13):  # Enter key
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):  # Handle backspace
            if len(user_input) > 0:
                user_input.pop()  # Remove last character
                # Clear the line and redraw input
                popup.addstr(entry_y, entry_x, ' ' * entry_width)
                popup.addstr(entry_y, entry_x, ''.join(user_input))
                popup.move(entry_y, entry_x + len(user_input))  # Move cursor to new position
        elif key == 27:  # ESC key
            user_input = None
            break
        elif 32 <= key <= 126 and len(user_input) < entry_width:  # Printable characters
            user_input.append(chr(key))
            popup.addstr(entry_y, entry_x, ''.join(user_input))
            popup.move(entry_y, entry_x + len(user_input))

        popup.refresh()

    # Destroy the temporary windows and return user input
    popup.clear()
    popup.refresh()
    curses.curs_set(1)  # Show cursor again (if hidden)
    curses.echo()  # Enable character echoing

    return ''.join(user_input) if user_input is not None else None


def show_yes_no_popup(stdscr, message):
    # Get screen dimensions
    max_y, max_x = stdscr.getmaxyx()

    # Define popup window size and position
    popup_height = 7
    popup_width = max(len(message) + 4, 30)  # Adjust width based on message length
    start_y = (max_y - popup_height) // 2
    start_x = (max_x - popup_width) // 2

    # Create a temporary window for the popup
    popup = curses.newwin(popup_height, popup_width, start_y, start_x)
    popup.box()

    # Display message
    message_y = 2  # Adjust for positioning within the popup
    message_x = (popup_width - len(message)) // 2
    popup.addstr(message_y, message_x, message)

    # Highlight options (modify colors as desired)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)

    # Define button positions
    button_y = message_y + 2
    yes_button_x = (popup_width // 2) - 5
    no_button_x = (popup_width // 2) + 2

    # Display Yes button (initially highlighted)
    popup.addstr(button_y, yes_button_x, " Yes ", curses.color_pair(1))
    # Display No button
    popup.addstr(button_y, no_button_x, " No ", curses.color_pair(0))

    # Refresh the window
    stdscr.refresh()
    popup.refresh()

    selected_button = 0  # 0 for Yes, 1 for No

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Toggle highlight between Yes and No buttons
            selected_button = 1 - selected_button  # Toggle between 0 and 1
            if selected_button == 0:
                popup.addstr(button_y, yes_button_x, " Yes ", curses.color_pair(1))
                popup.addstr(button_y, no_button_x, " No ", curses.color_pair(0))
            else:
                popup.addstr(button_y, yes_button_x, " Yes ", curses.color_pair(0))
                popup.addstr(button_y, no_button_x, " No ", curses.color_pair(1))
            stdscr.refresh()
            popup.refresh()
        elif key in [curses.KEY_ENTER, 10, 13]:
            break

    # Destroy the popup and return True for Yes or False for No
    popup.clear()
    popup.refresh()
    curses.curs_set(1)  # Show cursor again (if hidden)
    curses.echo()  # Enable character echoing

    return selected_button == 0

def show_popup_save_path(stdscr):
    return show_popup_input(stdscr, "Where to save the file")

def show_suggestions(stdscr, buffer, cursor, autocomplete):
    current_line = buffer[cursor.row]
    word_fragment_match = re.search(r'\b\w*$', current_line[:cursor.col])

    if word_fragment_match:
        word_fragment = word_fragment_match.group()
        suggestions = autocomplete.suggest(word_fragment)

        if suggestions:
            selected_suggestion = autocomplete.show_suggestions(stdscr, suggestions)

            if selected_suggestion:
                insertion_text = selected_suggestion[len(word_fragment):]
                buffer.insert_text(cursor.row, cursor.col, insertion_text)
                cursor.move_to(cursor.row, cursor.col + len(insertion_text))


def main(stdscr):
    parser = argparse.ArgumentParser(description="Text Editor")
    parser.add_argument("filename", help="File to open")
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as f:
            lines = f.read().split('\n')
    except FileNotFoundError:
        with open(args.filename, 'w') as f:
            f.write("")

    buffer = Buffer(lines)
    cursor = Cursor()
    window = Window(curses.LINES - 1, curses.COLS)
    file_extension = os.path.splitext(args.filename)[1]
    highlighter = select_highlighter(file_extension)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        window.adjust_horizontal_scroll(cursor)

        for i, line in enumerate(buffer.lines[window.row:window.row + window.n_rows]):
            start_row = i + window.row
            if highlighter:
                highlighter.highlight(stdscr, line, i)
            else:
                stdscr.addstr(i, 0, line)

        stdscr.move(*window.translate(cursor))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor.move_up(buffer)
            if cursor.row < window.row:
                window.scroll_up()
        elif key == curses.KEY_DOWN:
            cursor.move_down(buffer)
            if cursor.row > window.bottom:
                window.scroll_down(buffer)
        elif key == curses.KEY_LEFT:
            cursor.move_left(buffer)
        elif key == curses.KEY_RIGHT:
            cursor.move_right(buffer)
        elif key == curses.KEY_ENTER or key == 10:
            cursor.insert_newline(buffer)
        elif key == 27:  # ESC key
            break
        elif key == 127:  # Backspace key
            cursor.backspace(buffer)
        elif key == 9:  # Tab key
            buffer.insert(cursor, ' ' * 4)
            cursor.move_right(buffer)
        else:
            buffer.insert(cursor, chr(key))
            cursor.move_right(buffer)

    buffer.save_to_file(args.filename)

if __name__ == "__main__":
    curses.wrapper(main)