import sys
import hashlib

password = input("Enter you password \n")
password_md5 = hashlib.md5(password.encode("utf8")).hexdigest()
print(password_md5)

def get_password_hash():
    try:
        list_word = open("../contents/liste_francais.txt", "r")
        found = False
        for word in list_word:
            word = word.strip("\n").encode("utf8")
            hash_word_md5 = hashlib.md5(word).hexdigest()
            if hash_word_md5 == password_md5:
                print("Password found : " + str(word) + ":" + hash_word_md5)
                found = True
        if not found:
            print("Password not found")
            found = False
        list_word.close()
    except Exception as err:
        print("Error " + str(err))
        sys.exit(1)
    except FileNotFoundError as f:
        print("ERROR FILE NOT FOUND : " + str(f))
        sys.exit(2)


print(get_password_hash())

