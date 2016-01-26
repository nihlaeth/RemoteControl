"""Log to console with pretty colors."""


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
        print okblue + str(msg) + endc
    elif lvl == "header":
        print header + str(msg) + endc
    elif lvl == "ok":
        print okgreen + str(msg) + endc
    elif lvl == "fail":
        print fail + str(msg) + endc
    elif lvl == "warn":
        print warning + str(msg) + endc
    else:
        print fail + "unknown log type"
        print str(msg) + endc
