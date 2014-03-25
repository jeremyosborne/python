from fabric.api import run

def ls_num_dirs(dir="."):
    stdout = run("ls -lha "+dir, quiet=True)
    count = sum(1 for line in stdout.splitlines() if line[0] == "d")
    print "%s has %s dirs." % (dir, count)
