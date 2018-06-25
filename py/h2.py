import sys, getopt
import os


class h2():
    
    def data_convert(from_data):
        b = bytearray(from_data)
        decode = True
        
        if len(b) > 0:
            if b[0] == 128: # 进行解密
                del b[0]
                decode = False
            else: # 进行编码转换
                b = bytearray(b.decode('utf8').encode('gbk'))
        else:
            print("NULL File")
            exit(2)
        # 进行数据偏移操作
        for i in range(len(b)):
            b[i] ^= 0x78
            
        if decode: # 加密后添加识别
            b.insert(0, 128)
            return b
        else: # 将解密编码进行转换
            return b.decode('gbk').encode('utf8')
            
    
    @classmethod
    def file_convert(self, from_file, to_file):
        ff = open(from_file, 'rb')
        read = ff.read()
        data = self.data_convert(read)
        ff.close()

        tf = open(to_file, 'wb')
        tf.write(data)
        tf.close()
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    inputfile = ''
    outputfile = ''
    
    for opt, arg in opts:
        if opt == '-h':
            print("help: test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if outputfile == '':
        filename = os.path.basename(inputfile).split('.')[0]
        outputfile = './%s_new.txt' % filename
    try:
        f = open(inputfile)
        f.close()
        h2.file_convert(inputfile, outputfile)
    except IOError:
        print("File is not accessible")

    print('创建文件成功')
    print(os.path.abspath(outputfile))

if __name__ == '__main__':
    main(sys.argv[1:])
