from sys import flags
from app.addqueue import auto_add_queue
from app.linkgrb import print_from_url, write_from_url, edit_file_urls
import sys

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        while True:
            if args[1] == "-pu":
                url = input("input IDM Site Grabber url from bitso.ir to print urls: ")
                print_from_url(url)
            elif args[1] == "-wfu":
                url = input("input IDM Site Grabber url from bitso.ir to write idm.txt file: ")
                write_from_url(url, "idm.txt")
            elif args[1] == "-efu":
                edit_file_urls("idm.txt")
                break
            elif args[1] == "-afu":
                url = input("input IDM Site Grabber url from bitso.ir to automatically add links to idm queue: ")
                auto_add_queue(url)
                break
            else:
                sys.exit(0)
    else:
        print("\nUsage:\n\n./bitso.py -pu\n"
                "\t--Print edited links from url.\n"
                "./bitso.py -wfu\n"
                "\t--Write edited links from url to a file.\n"
                "./bitso.py -efu\n"
                "\t--Edit all links in idm.txt file.\n"
                "./bitso.py -afu\n"
                "\t--Get urls from IDMSiteGrabber and automaticly add it to idm.")
