#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
# import os
# import sys
# from io import BytesIO


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            print('<--- ' + i + ' : ' + str(j) + ' --->')


class BntBase():
    class FileHeader(BaseClass):
        def __init__(self):
            self.tag = ''
            self.version = ''
            self.inum = 0
            self.mdl_name = ''
            self.mdl_num = 0
            self.role_name = ''
            self.role_num = 0
            self.prop_name = ''
            self.prop_num = 0
            self.other_name = ''
            self.other_num = 0
            self.reserved = ''

    class InitBld():
        def __init__(self):
            self.itype = 0
            self.iModelAutoID = 0
            self.gp_map_pos = 0
            self.reserve = 0
            self.init_name_num = 0
            self.init_name = ''
            self.sztrigeer = ''

    def __init__(self, _filename):
        self.file_name = _filename

        self.file_header = None
        self.mdl_list = []
        self.init_data()

    def init_data(self):
        f = self.read(self.file_name)
        self.file_header = self.FileHeader()
        self.file_header.tag = struct.unpack('16c', f.read(16))[0]
        self.file_header.version = struct.unpack('16c', f.read(16))[0]
        self.file_header.inum = int(struct.unpack('h', f.read(2))[0])

        self.file_header.mdl_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.mdl_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.role_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.role_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.prop_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.prop_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.other_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.other_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.reserved = struct.unpack('86c', f.read(86))[0]
        self.file_header.printc()

        num = self.file_header.inum
        while num:
            bld = self.InitBld()
            bld.itype = int(struct.unpack('h', f.read(2))[0])
            print('bld.type: %d' % bld.itype)
            bld.iModelAutoID = struct.unpack('h', f.read(2))[0]
            bld.gp_map_pos = struct.unpack('2i', f.read(8))[0]
            bld.reserve = struct.unpack('2h', f.read(4))[0]
            bld.init_name_num = struct.unpack('i', f.read(4))[0]
            if bld.init_name_num > 0:
                bld.init_name = struct.unpack('i', f.read(4))[0]
            if bld.itype == 4:
                bld.sztrigeer = struct.unpack('128c', f.read(128))[0]

            print("%d : %s" % (bld.iModelAutoID, hex(bld.iModelAutoID)))
            num -= 1
        print('共有%d个组件' % self.file_header.inum)

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f


if __name__ == '__main__':
    file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhc_house1.BNT'
    # file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhaocun1.BNT'
    bnt = BntBase(file_name)
