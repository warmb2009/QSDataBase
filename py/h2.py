#!/usr/bin/env python2
import os

def filecovert(file_path, out_dir):
	b = bytearray(open(file_path, 'rb').read())
	
	isSec = 1
	
	if len(b) > 0:
		if b[0] == 128 :
			del b[0]
			isSec = 0
	for i in range(len(b)):
		b[i] ^= 0x78
	newfilename =  out_dir + '/' + file_path
	
	if isSec == 1:
		b.insert(0, 128)
			
	open(newfilename, 'wb').write(b)

if __name__ == '__main__':
	
	out_dir = 'out'
	
	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)
	
	for i in os.listdir('.'):
		if i[i.rfind('.'):] == '.txt':
			filecovert(i, out_dir)
			print i[:i.find('.')]
