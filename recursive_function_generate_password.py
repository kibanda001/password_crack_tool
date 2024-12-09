# coding:utf-8
import atexit
import time
import argparse
from recursive_functions import *
import multiprocessing # Pour réaliser le parallisme


def display_second():
    print("Duration " + str(time.time() - begin) + "seconds")


if __name__ == "__main__":

    # C'est pour déterminer ce fichier comme le fichier principal et ne pourra être exécuté ailleurs.

    parser = argparse.ArgumentParser(description="Password cracker")
    parser.add_argument("-f", "--file", dest="file", help="Path to dictionary file", required=False)
    parser.add_argument("-g", "--gen", dest="gen", help="Generate MD5 hash of Password", required=False)
    parser.add_argument("-md5", "--Md5", dest="md5", help="Hashed Password (MD5)", required=False)
    parser.add_argument("-l", "--length", dest="plength", help="PASSWORD length", required=False, type=int)
    parser.add_argument("-o", "--online", dest="online", help="SEARCH PASSWORD ONLINE (Google)", required=False, action= "store_true")
    parser.add_argument("-p", "--pattern", dest="pattern", help="USING MOTIF OF PASSWORD (^=MAJ , *=MIN, ²=NUMBERS)", required=False, action= "store_true")
    args = parser.parse_args()
    processes = []
    work_queu = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()
    cracker = Cracker()
    print(args.file)

    begin = time.time()
    atexit.register(display_second)


    if args.md5:
        print("[-] [CRACKING HASH " + args.md5 + "]")
        if args.file and not args.plength:
            print("[-] [USING DICTIONARY FILE" + args.file + "]")

            p1 = multiprocessing.Process(target=Cracker.work, args=(work_queu, done_queue, args.md5, args.file, Order.ASCEND))

            work_queu.put(cracker)
            p1.start()

            p2 = multiprocessing.Process(target=Cracker.work, args=(work_queu, done_queue, args.md5, args.file, Order.DESCENTE))

            work_queu.put(cracker)
            p2.start()
            while True:
                data = done_queue().get()
                if data == "FOUND" or data == "NOT FOUND":
                    p1.kill()
                    p2.kill()
                    break
            Cracker.crack_dict(args.md5, args.file)
        elif args.plength and not args.file:
            print("[-] [USING INCREMENTAL FOR " + str(args.plength) + " letter(s) ]")
            Cracker.crac_incr(args.md5, args.plength)
        elif args.online:
            print("[-] [USING SEARCH ONLINE " + str(args.online) + " MD5 ]")
            Cracker.crac_online(args.md5)
        elif args.pattern:
            print("[-] [USING MODELE OF PASSWORD " + str(args.pattern) + "")
            Cracker.crack_smart(args.md5, args.pattern)
        else:
            print("[-] Please choose either -f or -l argument")
    else:
        print("[-] MD5 Hash not provided")
    if args.gen:
        print("[-] MD5 HASH OF " + args.gen + " : " + hashlib.md5(args.gen.encode("utf8")).hexdigest())
