import shutil
import os
from fnmatch import fnmatch



def archive_backup(path):
    return shutil.make_archive(path, "zip", base_dir=path)



def backup(from_path, to_path):
    # Backup files in a directory.
    os.makedirs(to_path)
    backed_up = []
    for f in os.listdir(from_path):
        if fnmatch(f, "*.py"):
            to = os.path.join(to_path, f)
            shutil.copy2(f, to)
            backed_up.append({"from": f, "to": to})
    return backed_up


if __name__ == "__main__":
    base_dir = os.path.realpath(os.path.dirname(__file__))
    backup_path = os.path.join(base_dir, "backup")
     
    print "Beginning backup procedure of our code..."
    backed_up = backup(".", backup_path)
    print "Backup completed. List of files copied:"
    for desc in backed_up:
        print "from:", desc["from"]
        print "\tto:", desc["to"]
    
    print "Zipping backup to:", archive_backup(backup_path)
    
    print "Removing intermediate directory"
    shutil.rmtree(backup_path)
    
    
