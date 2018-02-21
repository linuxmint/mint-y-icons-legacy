#!/usr/bin/python3

import os
import subprocess
import sys

def check_symbolic_links_list():
    with open(SYMBOLIC_APPS_FILE, "r") as symbolic_apps_file:
        line_no = 0
        for symbolic_link_ref in symbolic_apps_file:
            line_no = line_no+1
            if " <- " not in symbolic_link_ref:
                print("Wrong symbolic link reference in line " + str(line_no) + ": " + symbolic_link_ref)
            else:
                target, symlink = symbolic_link_ref.split(" <- ")
                # check if target.svg exists
                target_svg = target.split(".")[0] + ".svg"
                if not os.path.exists(os.path.join(SRC_DIR, target_svg)):
                    print(target_svg + " does not exist (line " + str(line_no) + ")")
                    #pass

                create_symbolic_link(target, symlink)

def create_symbolic_link(target, symlink):
    for apps_pixel in os.listdir(APPS_DIR):
        target_path = os.path.join(APPS_DIR, apps_pixel, target).rstrip()
        symlink_path = os.path.join(APPS_DIR, apps_pixel, symlink).rstrip()
        subprocess.Popen(['ln', '-s', '-r', '-f', target_path, symlink_path])

def delete_symbolic_links_in_apps():
    subprocess.call(['find', APPS_DIR, '-type', 'l', '-delete'])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Pass argument: 'apps' or 'categories'")
    else:
        if sys.argv[1] in ["apps", "categories"]:
            SYMBOLIC_APPS_FILE = os.path.join(os.getcwd(), "symbolic-" + sys.argv[1] + "-list")
            SRC_DIR = os.path.join(os.getcwd(), sys.argv[1])
            APPS_DIR = os.path.join(os.getcwd(), "..", "usr", "share", "icons", "Mint-Y", sys.argv[1])

            print("Creating symbolic links in " + sys.argv[1] + " directories...")
            delete_symbolic_links_in_apps()
            check_symbolic_links_list()
            print("Done!")
        else:
            print("Wrong argument! Valid arguments are: apps, categories")