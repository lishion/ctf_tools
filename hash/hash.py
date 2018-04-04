import string, random
import hashlib   
import itertools
import string
import sys

def random_md5(s,e,strs,length=None):
    chars = string.ascii_letters + string.digits
    target_len = length if length  else 16
   
    while True:
        md5_target = ""
        for i in range(0,target_len):
            md5_target += random.choice(chars)

        if hashlib.md5(md5_target.encode("ascii")).hexdigest()[s:e] == strs:
            return md5_target

if __name__ == "__main__":
    length = sys.argv[4] if len(sys.argv)>=5 else None
    print( random_md5(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],length) )

    
