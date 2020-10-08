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


class MdlBase():
    class FileHeader(BaseClass):
        def __init__(self):
            self.tag = ''
            self.version = ''
            self.inum = 0
            self.szname = ''
            self.reserved = ''

    class SModelBld():
        def __init__(self):
            self.itype = 0  # 2
            self.szName = 0  # 32 char
            self.wManualID = 0  # 2
            self.wAutoID = 0  # 2
            self.PartMng = 0  # 4 char *
            self.PartNum = 0  # 2
            self.DownNum = 0  # 2
            self.MiddleNum = 0  # 2
            self.UpNum = 0  # 2
            self.booIsAnimate = 0  # 1
            self.grFrame = 0  # 20
            self.m_gpAttribLeftUp = 0  # 8
            self.m_cxDisMetrix = 0  # 2
            self.m_cyDisMetrix = 0  # 2
            self.m_gpCharacter = 0  # 80  8*10
            

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

        self.file_header.szname = struct.unpack('256c', f.read(256))[0]
        self.file_header.reserved = struct.unpack('94', f.read(94))[0]
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
