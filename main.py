import argparse
import curses
import os
import re

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
            # Add four spaces when moving to the next line
            self.col = min(self.col + 4, len(buffer[self.row]))  # Ensure the column doesn't exceed the line length

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
        # Get the current line content
        current_line = buffer[self.row]

        # Check if the current line ends with ':' or '{'
        if current_line.strip().endswith(':') or current_line.strip().endswith('{'):
            # Add four spaces before the new line
            new_line_content = ' ' * self.col + '\n' + ' ' * 4 + current_line[self.col:]
            buffer.lines[self.row] = current_line[:self.col] + '\n'
            buffer.lines.insert(self.row + 1, new_line_content)
            self.row += 1
            self.col = 4  # Set the column to the first character position after the added spaces
        else:
            buffer.insert(self, '\n')  # Insert a new line character
            self.row += 1
            self.col = 0

    def backspace(self, buffer):
        """Deletes the character at the cursor position."""
        if self.col > 0:
            # Delete the character at the current position by slicing
            current = buffer[self.row]
            buffer.lines[self.row] = current[:self.col - 1] + current[self.col:]
            self.col -= 1
        elif self.row > 0:
            # Move the cursor to the end of the previous line and join the lines
            prev_line_length = len(buffer[self.row - 1])
            buffer.join_with_previous_line(self)
            self.row -= 1
            self.col = prev_line_length

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col

        # Extend self.lines if row index is out of range
        while row >= len(self.lines):
            self.lines.append('')

        current = self.lines[row]
        self.lines[row] = current[:col] + string + current[col:]

    def split(self, cursor):
        row, col = cursor.row, cursor.col
        current = self.lines[row]
        self.lines[row] = current[:col]
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if col > 0:
            current = self.lines[row]
            self.lines[row] = current[:col - 1] + current[col:]
        elif row > 0:
            self.lines[row - 1] += self.lines.pop(row)

    def join_with_previous_line(self, cursor):
        if cursor.row > 0:
            self.lines[cursor.row - 1] += self.lines.pop(cursor.row)

    def save_to_file(self, filename):
        """Save the buffer content to a file."""
        with open(filename, 'w') as f:
            f.write('\n'.join(self.lines))
            return True  # Return True if saving is successful

class HighlighterBase:
    def apply_highlighting(self, stdscr, text, start_row, highlighting_rules):
        stdscr.addstr(start_row, 0, text)  # Print the entire line as normal text
        # Apply highlighting rules
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

class JavaScriptHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'\b(var|let|const|function|if|else|while|for|return|import|export|class|try|catch|finally)\b', curses.color_pair(1)),
            (r'//.*$', curses.color_pair(2)),
            (r'/\*.*?\*/', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
            (r"'.*?'", curses.color_pair(3)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class HTMLHighlighter(HighlighterBase):
    def highlight(self, stdscr, text, start_row):
        highlighting_rules = [
            (r'<\w+\b', curses.color_pair(1)),
            (r'</\w+>', curses.color_pair(1)),
            (r'\b\w+\b(?=\s*=\s*")', curses.color_pair(2)),
            (r'".*?"', curses.color_pair(3)),
            (r"'.*?'", curses.color_pair(3)),
            (r'<!--.*?-->', curses.color_pair(2)),
        ]
        self.apply_highlighting(stdscr, text, start_row, highlighting_rules)

class SyntaxHighlighter:
    def __init__(self):
        self.python_highlighter = PythonHighlighter()
        self.css_highlighter = CSSHighlighter()
        self.cpp_highlighter = CppHighlighter()
        self.csharp_highlighter = CSharpHighlighter()
        self.c_highlighter = CHighlighter()
        self.js_highlighter = JavaScriptHighlighter()
        self.html_highlighter = HTMLHighlighter()

    def highlight(self, stdscr, text, file_extension, start_row):
        if file_extension == '.py':
            self.python_highlighter.highlight(stdscr, text, start_row)
        elif file_extension == '.css':
            self.css_highlighter.highlight(stdscr, text, start_row)
        elif file_extension in ['.cpp', '.cc', '.cxx']:
            self.cpp_highlighter.highlight(stdscr, text, start_row)
        elif file_extension == '.cs':
            self.csharp_highlighter.highlight(stdscr, text, start_row)
        elif file_extension == '.c':
            self.c_highlighter.highlight(stdscr, text, start_row)
        elif file_extension == '.js':
            self.js_highlighter.highlight(stdscr, text, start_row)
        elif file_extension == '.html':
            self.html_highlighter.highlight(stdscr, text, start_row)
        else:
            stdscr.addstr(start_row, 0, text)

def show_popup_input(stdscr, message):
    """Displays a popup window for user input within the terminal."""
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
    """Displays a popup with Yes/No buttons for user confirmation."""
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
    """Displays a popup window for the user to input a file path."""
    return show_popup_input(stdscr, "Where to save the file")


def main(stdscr, filename):
    # Initialization
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        lines = []  # Empty list for new file or non-existent file

    buffer = Buffer(lines)
    cursor = Cursor()
    window = Window(curses.LINES - 1, curses.COLS)
    syntax_highlighter = SyntaxHighlighter()

    file_extension = os.path.splitext(filename)[1]

    while True:
        stdscr.clear()

        for i, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            syntax_highlighter.highlight(stdscr, line, file_extension, i)

        stdscr.move(*window.translate(cursor))
        stdscr.refresh()

        key = stdscr.get_wch()

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
            window.adjust_horizontal_scroll(cursor)
        elif key == curses.KEY_RIGHT:
            cursor.move_right(buffer)
            window.adjust_horizontal_scroll(cursor)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            buffer.insert(cursor, "\n")
        elif key == '\x13':  # Ctrl+S to save
            save_confirmed = show_yes_no_popup(stdscr, "Do you want to save?")
            if save_confirmed:
                if os.path.exists(args.filename):
                    buffer.save_to_file(args.filename)
                else:
                    path = show_popup_save_path(stdscr)
                    if path is not None:
                        buffer.save_to_file(path)
        elif key == '\n':
            buffer.split(cursor)
            cursor.insert_newline(buffer)
            if cursor.row > window.bottom:
                window.scroll_down(buffer)
        elif key in ('\b', '\x7f', curses.KEY_BACKSPACE):  # Handle backspace
            cursor.backspace(buffer)
            if cursor.row < window.row:
                window.scroll_up()
        elif key == curses.KEY_DC:  # Delete key
            buffer.delete(cursor)
        elif key == '\x1b':  # ESC key to exit
            break
        # Handle other keys, including printable characters
        else:
            if isinstance(key, str) and len(key) == 1:
                # Check if the key is a printable character
                if key.isprintable():
                    buffer.insert(cursor, key)
                    cursor.move_right(buffer)
                    window.adjust_horizontal_scroll(cursor)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text editor with syntax highlighting.')
    parser.add_argument('filename', help='File to edit')
    args = parser.parse_args()

    curses.wrapper(main, args.filename)
