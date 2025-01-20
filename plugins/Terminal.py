import cmd
import subprocess
import os

class BeagleEditorShell(cmd.Cmd):
    intro = "Welcome to BeagleEditor shell. To get help, type 'help'."
    prompt = f"[{os.getcwd()}] [beagleeditor] "
    file = None

    def do_goto(self, arg):
        if arg == 'git':
            print("Going to Git environment")
            GitEnvShell().cmdloop()
        elif arg == 'py' or arg == 'python':
            print("Going to Python environment")
            PythonEnvShell().cmdloop()
        else:
            print(f"Unknown environment: {arg}")

    def do_gotodir(self, arg):
        try:
            os.chdir(arg)
            self.prompt = f"[{os.getcwd()}] [beagleeditor] "
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def help_goto(self):
        print("""goto {git, python}: Go to an environment\n
              What is an environment in BeagleEditor shell?
              An environment specific some commands related to environment label (name).
              You have currently 2 options: git, python""")
        
    def help_gotodir(self):
        print("Same functionality with cd command in system terminal. It changes directory to specified directory")

    def help_exit(self):
        print("Getting out of BeagleEditor shell")

    def do_exit(self, arg):
        print("Thanks for using BeagleEditor shell.")
        return True

class GitEnvShell(cmd.Cmd):
    intro = "Welcome to BeagleEditor Git environment. Type 'githelp' to get help."
    prompt = f"[{os.getcwd()}] [beagleeditor] [git] "

    def do_githelp(self, arg):
        print("Available commands in Git environment:")
        print("  status - Show the git status")
        print("  checkout <branch> - Checkout a specific branch")
        print("  commit -m <message> - Commit with a message")
        print("  push - Push the repository to GitHub")
        print("  exit - Return to the default environment")

    def do_status(self, arg):
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_checkout(self, arg):
        try:
            result = subprocess.run(['git', 'checkout', arg], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_commit(self, arg):
        try:
            args = ['git'] + arg.split()
            result = subprocess.run(args, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_push(self, arg):
        try:
            result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print("An error occurred")

    def do_exit(self, arg):
        """Return to the default environment."""
        print("Returning to the default environment.")
        return True

    def do_gotodir(self, arg):
        try:
            os.chdir(arg)
            self.prompt = f"[{os.getcwd()}] [beagleeditor] [git] "
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print(f"An error occurred: {e}")

class PythonEnvShell(cmd.Cmd):
    intro = "Welcome to BeagleEditor Python environment. Type 'pyhelp' to get tutorial."
    prompt = f"[{os.getcwd()}] [beagleeditor] [py] "

    def do_pyhelp(self, arg):
        print("Available commands in Python environment:")
        print("  run <filename> - Run a Python script")
        print("  pyshell - Run Python shell")
        print("  exit - Return to the default environment")

    def do_run(self, arg):
        """Run a Python script. Usage: run <filename>"""
        try:
            result = subprocess.run(['python', arg], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_pyshell(self, arg):
        try:
            subprocess.run(['python'], text=True)
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_gotodir(self, arg):
        try:
            os.chdir(arg)
            self.prompt = f"[{os.getcwd()}] [beagleeditor] [py] "
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def do_exit(self, arg):
        """Return to the default environment."""
        print("Returning to the default environment.")
        return True

def run_from_beagleeditor():
    BeagleEditorShell().cmdloop()
