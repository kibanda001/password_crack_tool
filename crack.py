import sys
import time
import hashlib
import argparse

parser = argparse.ArgumentParser(description="Password cracker")
parser.add_argument("-f", "--file", dest="file", help="Path to dictionary file", required=False)
parser.add_argument("-g", "--gen", dest="gen", help="Generate MD5 hash of Password", required=False)
parser.add_argument("-md5", "--Md5", dest="md5", help="Hashed Password (MD5)", required=False)
args = parser.parse_args()
print(args.file)

password = input("Enter you password \n")
password_md5 = hashlib.md5(password.encode("utf8")).hexdigest()
print(password_md5)
debut = time.time()


def crack_dict(md5, file):
    try:
        found = False
        for word in file:
            word = word.strip("\n").encode("utf8")
            hash_word_md5 = hashlib.md5(word).hexdigest()
            fin = time.time() - debut
            if hash_word_md5 == md5:
                print("Password found : " + str(word) + ":" + hash_word_md5)
                print("Your password found after : %s " % str(fin))
                found = True
        if not found:
            print("Password not found")
        file.close()
    except Exception as err:
        print("Error " + str(err))
        sys.exit(1)
    except FileNotFoundError as f:
        print("ERROR FILE NOT FOUND : " + str(f))
        sys.exit(2)
