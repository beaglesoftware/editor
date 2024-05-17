import argparse
import curses
import sys

class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1
    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1

    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)


class Cursor:
    def __init__(self, row=0, col=0, col_hint=None):
        self.row = row
        self._col = col
        self._col_hint = col if col_hint is None else col_hint

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col
        self._col_hint = col

    def _champ_col(self, buffer):
        self.col = min(self._col_hint, len(buffer[self.row]))


    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._champ_col(buffer)

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._champ_col(buffer)

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 1
        elif self.row < buffer.bottom:
            self.row += 1
            self.col = 0

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    @property
    def bottom(self):
        return len(self) - 1

    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        current = self.lines.pop(row)
        new = current[:col] + string + current[col:]
        self.lines.insert(row, new)

    def split(self, cursor):
        row, col = cursor.row, cursor.col
        current = self.lines.pop(row)
        self.lines.insert(row, current[:col])
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if row < len(self.lines):
            current = self.lines[row]
            if col < len(current):
                new = current[:col] + current[col + 1:]
                self.lines[row] = new
            elif row + 1 < len(self.lines):
                next_line = self.lines.pop(row + 1)
                self.lines[row] = current + next_line

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.lines))


def left(window, buffer, cursor):
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)


def right(window, buffer, cursor):
    cursor.right(buffer)
    window.down(buffer, cursor)
    window.horizontal_scroll(cursor)

def show_popup(stdscr, message):
    rows, cols = stdscr.getmaxyx()
    popup_height = 5
    popup_width = len(message) + 4
    popup_y = (rows - popup_height) // 2
    popup_x = (cols - popup_width) // 2

    popup_win = curses.newwin(popup_height, popup_width, popup_y, popup_x)
    popup_win.border()
    popup_win.addstr(1, 2, message)
    popup_win.addstr(3, 2, "Input: ")
    popup_win.refresh()

    # Wait for any key press to continue
    while popup_win.getch() == curses.ERR:
        pass

    # Clear the popup window
    popup_win.clear()
    popup_win.refresh()

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer(f.read().splitlines())


    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor))

        k = stdscr.getkey()

        if k == "\x11":
            sys.exit(0)
        elif k == "\x13":
            show_popup(stdscr, "Do you want to save it?")
            buffer.save_to_file(args.filename)
        elif k == "KEY_LEFT":
            left(window, buffer, cursor)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_RIGHT":
            right(window, buffer, cursor)
        elif k == "\n":
            buffer.split(cursor)
            right(window, buffer, cursor)
        elif k in ("KEY_DELETE", "\x04"):
            buffer.delete(cursor)
        elif k in ("KEY_BACKSPACE", "\b", "\x7f"):
            if (cursor.row, cursor.col) > (0, 0):
                left(window, buffer, cursor)
                buffer.delete(cursor)
        else:
            buffer.insert(cursor, k)
            for _ in k:
                right(window, buffer, cursor)


if __name__ == "__main__":
    curses.wrapper(main)
