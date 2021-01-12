#! /usr/bin/env python

#### CLISU v 0.1.1
#### Code by: Agentnumber47
#### Nickname: [0.1] Ground Zero [Scaled back from earlier attempts and rebuilding to higher glory]
#### Source: https://github.com/Agentnumber47/CLISU
#### Support me! https://ko-fi.com/agentnumber47
#### Differences between 0.1.1 and 0.1: Added file integrity check

# from colorama import init
import argparse
from hashlib import md5
import os
import shutil

BLOCK_SIZE = 65536

def terminal(args):
    # Grab and map the host directory
    while True:
        header()
        entry = input("What is the master directory? [Ex. /path/to/dir]\n")
        if entry.lower() == "x":
            exit()

        host_path, host = verify(entry)
        if not host: input(f"\n'{host_path}' doesn't exist or is inaccessible\n")
        else: break

    # Grab and map the parasite directory
    while True:
        header()
        entry = input("What is the directory you want to sync to?\n")
        if entry.lower() == "x":
            exit()

        parasite_path, parasite = verify(entry)
        if not parasite: input(f"\n'{parasite_path}' doesn't exist or is inaccessible\n")
        else: break

    # Begin syncing process
    header()
    sync(host_path, host, parasite_path, parasite)

def run(args):
    host_path, host = verify(args.run[0])
    if not host:
        print(f"ERROR: '{host_path}' doesn't exist or is inaccessible")
        return

    parasite_path, parasite = verify(args.run[1])
    if not parasite:
        print(f"ERROR: '{parasite_path}' doesn't exist or is inaccessible")
        return

    sync(host_path, host, parasite_path, parasite)


def verify(x_path):
    try:
        if os.path.isdir(x_path) == False:
            return False, False
        else:
            if not x_path.endswith("/"): x_path += "/"
            return x_path, generate_map(x_path)
    except:
        return False, False

def sync(host_path, host, parasite_path, parasite):
    for ld in host:
        item = ld # Do this or python will flip the fuck out

        ### Item found on both drives
        if item in parasite:
            hi, pi = render(host, parasite, item, host_path, parasite_path)
            if hi['relative path'] != pi['relative path']:
                # Check that the items are identical
                hi['fingerprint'] = fingerprinter(hi['full path'])
                pi['fingerprint'] = fingerprinter(pi['full path'])
                if hi['fingerprint'] == pi['fingerprint']:
                    try:
                        os.makedirs(hi['directory mirror'])
                    except:
                        pass
                    shutil.move(pi['full path'], hi['path mirror'])
                    rmdir(pi['directory'])
                    rmdir(pi['directory mirror'])
        else:
            shutil.copy(host[item]['path'].replace("./", host_path), host[item]['path'].replace("./", parasite_path))

    print("Sync Successful!")

def render(x, y, item, x_path, y_path):
    # x = '/path/to/x/file.txt', y = '/path/to/y/fyle.txt'

    # './file.txt', './fyle.txt'
    x_relpath, y_relpath = x[item]['path'], y[item]['path']

    # '/path/to/x/file.txt', '/path/to/y/fyle.txt'
    x_full_path, y_full_path = x[item]['path'].replace('./', x_path), y[item]['path'].replace('./', y_path) #

    # '/path/to/y/file.txt', '/path/to/x/fyle.txt'
    x_full_path_mirror, y_full_path_mirror = x[item]['path'].replace('./', y_path), y[item]['path'].replace('./', x_path)

    # '/path/to/x/', '/path/to/y/'
    x_directory, y_directory = x_full_path.replace(item, ""), y_full_path.replace(item, "")

    x_directory_mirror, y_directory_mirror = x_full_path_mirror.replace(item, ""), y_full_path_mirror.replace(item, "")

    x_render = {
    'relative path' : x_relpath,
    'full path' : x_full_path,
    'path mirror' : x_full_path_mirror,
    'directory' : x_directory,
    'directory mirror' : x_directory_mirror
    }
    y_render = {
    'relative path' : y_relpath,
    'full path' : y_full_path,
    'path mirror' : y_full_path_mirror,
    'directory' : y_directory,
    'directory mirror' : y_directory_mirror
    }
    return x_render, y_render


def header():
    shell_columns = os.get_terminal_size().columns
    # print("\033[36m")
    os.system("clear")
    print(f"#     CLISU     #".center(shell_columns, "#"))
    # print("\033[39m")
    print("")
    return

def generate_map(x_path):
    media = {}
    for root, dirs, files in os.walk(x_path):
        for name in files:
            if not "/." in root and not name.startswith("."):
                file_base = os.path.join(root, name) ## Root = path | Name = file
                media[file_base.split("/")[-1]] = {"path": file_base.replace(f"{x_path}", "./")}

    return media

def rmdir(x_path):
    try:
        if len(os.listdir(x_path)) == 0: os.rmdir(x_path) # If the directory is empty, delete it
    except:
        pass
    return

def fingerprinter(x_path):
    hash_method = md5()
    with open(x_path, 'rb') as input_file:
        buf = input_file.read(BLOCK_SIZE)
        while len(buf) > 0:
            hash_method.update(buf)
            buf = input_file.read(BLOCK_SIZE)

    return hash_method.hexdigest()

def main():
    parser = argparse.ArgumentParser(description = "CLISU (CLI Synchronization Utility)")

    parser.add_argument("-t", "--terminal", nargs = "*", metavar = "", type = str, help = "run with prompts in terminal")
    parser.add_argument("-r", "--run", nargs = 2, metavar = ('/path/from', '/path/to'), type = str, help = "run without prompts")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.terminal != None:
        terminal(args)
    elif args.run != None:
        run(args)

if __name__ == '__main__':
    main()
