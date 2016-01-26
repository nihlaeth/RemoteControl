"""Log to console with pretty colors."""
import sys

class LogLevel(object):
    
    """Keep track of log level."""

    def __init__(self):
        """Set basic log level (0 = none)."""
        self.loglevel = 0

    def set_level(self, level):
        """Set log level (from string to int)."""
        if level == "none":
            self.loglevel = 0
        elif level == "err":
            self.loglevel = 1
        elif level == "warn":
            self.loglevel = 2
        elif level == "info":
            self.loglevel = 3
        elif level == "verbose":
            self.loglevel = 4

LOGLEVEL = LogLevel()


def log(lvl, msg):
    """Log data (with pretty colors)."""
    header = '\033[95m'
    okblue = '\033[94m'
    okgreen = '\033[32m'  # '\033[92m'
    warning = '\033[36m'  # '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    # bold = "\033[1m"
    if lvl == "info":
        if LOGLEVEL.loglevel >= 4:
            sys.stdout.write(okblue + str(msg) + endc + '\n')
    elif lvl == "header":
        if LOGLEVEL.loglevel >= 4:
            sys.stdout.write(header + str(msg) + endc + '\n')
    elif lvl == "ok":
        if LOGLEVEL.loglevel >= 3:
            sys.stdout.write(okgreen + str(msg) + endc + '\n')
    elif lvl == "fail":
        if LOGLEVEL.loglevel >= 1:
            sys.stderr.write(fail + str(msg) + endc + '\n')
    elif lvl == "warn":
        if LOGLEVEL.loglevel >= 2:
            sys.stderr.write(warning + str(msg) + endc + '\n')
    else:
        if LOGLEVEL.loglevel >= 1:
            sys.stderr.write(fail + "unknown log type" + '\n')
            sys.stderr.write(str(msg) + endc + '\n')
