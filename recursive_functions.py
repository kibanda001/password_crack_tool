import urllib.request
import urllib.response
import urllib.error
import sys
import string
import hashlib
from utils import *


class Cracker:

    @staticmethod
    def crack_dict(md5, file, order, done_queu):
        """
        Crack MD5 HASH by USING A LIST KEYS WORDS
        :param md5:
        :param file:
        :return:
        """
        try:
            found = False
            ofile = open(file, "r")
            if Order.ASCEND == order:
                content = reversed(list(ofile.readlines()))
            else:
                content = ofile.readlines()
            for word in content:
                word = word.strip("\n").encode("utf8")
                hash_word_md5 = hashlib.md5(word).hexdigest()
                if hash_word_md5 == md5:
                    print(Couleur.VERT + "" + "[+] Password found : " + str(word) + ":" + "" + hash_word_md5 + Couleur.FIN)
                    found = True
                    done_queu.put("FOUND")
                    break
            if not found:
                print(Couleur.ROUGE + "" + "Password not found" + "" + Couleur.FIN)
                done_queu.put("NOT FOUND")
            ofile.close()
        except Exception as err:
            print(Couleur.ROUGE + "Error " + str(err) + Couleur.FIN)
            sys.exit(1)
        except FileNotFoundError as f:
            print(Couleur.ROUGE + "ERROR FILE NOT FOUND : " + str(f) + Couleur.FIN)
            sys.exit(2)

    @staticmethod
    def crac_incr(md5, length, _currpass=[]):
        """
        :param md5:
        :param length:
        :param currpass:
        :return:
        """
        letters = string.printable
        if length >= 1:
            if len(_currpass) == 0:
                _currpass = ["a" for _ in range(length)]
                Cracker.crac_incr(md5, length, _currpass)
            else:
                for c in letters:
                    _currpass[length - 1] = c
                    currHash = hashlib.md5("".join(_currpass).encode("utf8")).hexdigest()
                    print("[*] Trying : " + "".join(_currpass) + " (" + currHash + ")")
                    if currHash == md5:
                        print(Couleur.VERT + " " + "[+] PASSWORD FOUND : " + "".join(_currpass) + " " + Couleur.FIN)
                        sys.exit(0)
                    else:
                        Cracker.crac_incr(md5, length - 1, _currpass)

    @staticmethod
    def crac_online(md5):
        """
        :param md5:
        :return:
        """
        try:
            url = "https://www.google.fr/search?hl=fr&q=" + md5
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/127.0.0.0 Safari/537.36"
            headers = {"user-agent" : user_agent}
            requete = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(requete)
        except urllib.error.HTTPError as e:
            print("HTTP ERROR " + e.code)
        except urllib.error.URLError as e:
            print("URL ERROR " + str(e.reason))
        if "Aucun document" in response.read().decode("utf8"):
            print(Couleur.ROUGE + "[-] HASH NOT FIND IN GOOGLE" + Couleur.FIN)
        else:
            print(Couleur.VERT + "[+]PASSWORD FOUND IN " + url + Couleur.FIN)

    @staticmethod
    def work(work_queu, done_queu, md5, file, order):
        """
        :param work_queu:
        :param done_queue:
        :param md5:
        :param file:
        :param order:
        :return:
        """
        o = work_queu.get()
        o.crack_dict(md5, file, order, done_queu)

    @staticmethod
    def crack_smart(md5, pattern, _index=0):
        MAJ = string.ascii_uppercase
        NUMBERS = string.digits
        MIN = string.ascii_lowercase

        if _index < len(pattern):
            if pattern[_index] in MAJ + NUMBERS + MIN:
                Cracker.crack_smart(md5, pattern, _index + 1)
            if "^" == pattern[_index]:
                for c in MAJ:
                    p = pattern.replace("^", c, 1)
                    currHash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currHash == md5:
                        print(Couleur.VERT + "[+]PASSWORD FOUND" + p + Couleur.FIN)
                        sys.exit(0)
                    print("MAJ" + p + "(" + currHash + ")")
                    Cracker.crack_smart(md5, p , _index + 1)

            if "*" == pattern[_index]:
                for c in MIN:
                    p = pattern.replace("*", c, 1)
                    currHash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currHash == md5:
                        print(Couleur.VERT + "[+]PASSWORD FOUND" + p + Couleur.FIN)
                        sys.exit(0)
                    print("MIN" + p + "(" + currHash + ")")
                    Cracker.crack_smart(md5, p , _index + 1)

            if "²" == pattern[_index]:
                for c in NUMBERS:
                    p = pattern.replace("²", c, 1)
                    currHash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currHash == md5:
                        print(Couleur.VERT + "[+]PASSWORD FOUND" + p + Couleur.FIN)
                        sys.exit(0)
                    print("NUMBERS" + p + "(" + currHash + ")")
                    Cracker.crack_smart(md5, p , _index + 1)

        else:
            return
