#!/usr/bin/env python3

import requests
import threading
import sys
import threading
import time



extensions = ["",".php", ".html", ".txt"]
ignore_status_codes = [404]
ignore_response_lengths = []
max_threads = 300


def help():
    print(f"\nUsage: python3 {sys.argv[0]} --target http://target.com")
    print(f"\n\nOptional Extras:\n\n")
    print("     -w     Wordlist   -w wordlist.txt")
    print("     -e     Extensions     default: php, txt, html   -e txt,php,html")
    print("     -s     Ignore status codes    default:404   -s 403")
    print("     -t     maximum threads   default: 300     -t 100")
    print("     -l     Ignore response lengths    default: none     -l 0,2000")
    exit()




#fuck for loops with if statements
for arg in sys.argv:

    if arg == "-h" or arg == "--help":
        help()
    if arg == "--target":
        target = sys.argv[sys.argv.index(arg)+1]
        if target[-1] == "/":
            target = target[:-1]
    if arg == "-w":
        wordlist = sys.argv[sys.argv.index(arg)+1]
    if arg == "-t":
        max_threads = int(sys.argv[sys.argv.index(arg)+1])

    if arg == "-e":
        add_ext = sys.argv[sys.argv.index(arg)+1]
        if "," in add_ext:
            add_ext = add_ext.split(",")
            for exten in add_ext:
                if exten not in extensions:
                    extensions.append("." + exten)
        else:
            if add_ext not in extensions:
                extensions.append("." + add_ext)
    if arg == "-l":
        add_len = sys.argv[sys.argv.index(arg)+1]
        if "," in add_len:
            add_len = add_len.split(",")
            for lens in add_len:
                if lens not in ignore_response_lengths:
                    ignore_response_lengths.append(int(lens))
        else:
            if add_len not in ignore_response_lengths:
                ignore_response_lengths.append(int(add_len))
    if arg == "-s":
        add_status = sys.argv[sys.argv.index(arg)+1]
        if "," in add_status:
            add_status = add_status.split(",")
            for stat in add_status:
                if stat not in ignore_status_codes:
                    ignore_status_codes.append(int(stat))
        else:
            if add_status not in ignore_status_codes:
                ignore_status_codes.append(int(add_status))





try:

    if target == "-h" or target == "--help":
        exit()
    try:

        requests.get(target)
        print("Connected to target successfully")
    except:
        print(f"Could not connect to {target}")
        exit()

except:
    help()
try:
    ammount_left = len(open(wordlist,"r").readlines()) * len(extensions)
    wordlist = open(wordlist,"r")




except:
    print("No wordlist selected.")
    try:
        ammount_left = len(open("./wordlist.txt","r").readlines()) * len(extensions)
        wordlist = open("./wordlist.txt")
        print("using existing wordlist file named wordlist.txt")
    except:
        print("fetching a wordlist file named wordlist.txt")
        new_file = open("wordlist.txt", "w")
        new_file.write(requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/big.txt").text)
        new_file.close()
        ammount_left = len(open("wordlist.txt","r").readlines()) * len(extensions)
        wordlist = open("wordlist.txt")



def check(resource):
    try:


        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36'}
        req = requests.get(f"{target}/{resource}", headers=headers)

        if req.status_code not in ignore_status_codes:
            if len(req.text) not in ignore_response_lengths:
                print(f"{target}/{resource}   [status code: {str(req.status_code)}]   [Length:{str(len(req.text))}]                          ")



    except:
        pass

print("\n\n------------------------------------------\nFINDING\n\n\n\n")
completed = 0


for resource in wordlist:
    if resource[0] != "#":
        for ext in extensions:
            ext = resource + ext
            ext = ''.join(ext.split()) #get rid of all whitespace
            if threading.active_count() > max_threads:
                time.sleep(1)
            else:
                completed += 1
                thread = threading.Thread(target=check, args=(ext,))
                thread.start()
                print(f"Current ammount of threads: {str(threading.active_count())}   Completed:{str(completed)}/{str(ammount_left)}   [/{ext}]                     ", end='\r')
