import chardet
def decode_f(file_name):
    f = open(file_name,'r')
    print(chardet.detect(f))

if __name__ == '__main__':
    decode_f('Database/CB72006001.csv')