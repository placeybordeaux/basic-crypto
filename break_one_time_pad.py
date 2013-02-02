def str_xor(a,b):
    if len(a) > len(b):
        a,b = b,a
    pairs = zip(a[:len(b)], b)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in pairs])

def hex_to_str(hex):
    s = ""
    #we must read two characters in at a time
    for i in range(0, len(hex), 2):
        s += chr(int(hex[i:i+2], 16))
    return s

def str_to_hex(s):
    #have to cut off the 0x that python appends
    #                                       \
    return ''.join(map(lambda x: hex(ord(x))[2:], s))

def xor_one_w_all(one,all):
    return map(lambda x: str_xor(all[one],x), all)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Takes a series of cyphertexts all using the same one time pad and decrypts one of your choosing. Built for decrypting ASCII encoded English')
    parser.add_argument('--input', type=str, default='cyphertexts', help='The file with cyphertexts, must be ASCII hexencoded, seperated by \\n')
    parser.add_argument('-n', type=int, default=0, help='The cyphertext to decode')
    args = parser.parse_args()

    #               newline or space characters will create errors                       
    #                               \
    cyphertexts = map(lambda x: x.strip(),open(args.input,'r').readlines())
    c_as_str = map(hex_to_str,cyphertexts)

    # char of str
    #    \      confidence in correct decoding
    #     \    /
    m = [("_",0)]*len(c_as_str[args.n])

    for i in range(len(c_as_str)):
        temp = xor_one_w_all(i,c_as_str)
        for j in range(len(c_as_str[args.n])):
            count = 0
            for k in range(len(c_as_str)):
                if j < len(temp[k]):
                    if temp[k][j].isalpha():
                        count += 1
            if m[j][1] < count:
                character = str_xor(str_xor(' ',c_as_str[i][j]),c_as_str[args.n][j])
                m[j] = (character,count)
    m = ''.join(map(lambda x: x[0], m))
    print m
