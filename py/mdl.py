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

            self.m_wSound = 0
            self.m_bLight = 0
            self.m_bAniDisplay = 0

    class AModelBld():
        def __init__(self):
            self.m_szName = ''
            self.m_booIsSpr = 0
            self.m_dPicID = 0
            self.m_pos_x = 0
            self.m_pos_y = 0

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
        self.file_header.reserved = struct.unpack('94c', f.read(94))[0]
        self.file_header.printc()

        num = self.file_header.inum
        while num:
            bld = self.SModelBld()

            bld.itype = int(struct.unpack('h', f.read(2))[0])
            print('bld.type: %d' % bld.itype)

            test = 'B4 A5 B7 A2 Bf E9'
            or_name = struct.unpack('32s', f.read(32))[0]
            bld.szName = or_name.replace(b'\xcd', b'')
            print(or_name)
            print('szname:%s' % bld.szName.decode(encoding='gbk', errors='replace'))
            bld.wManualID = struct.unpack('h', f.read(2))[0]
            bld.wAutoID = struct.unpack('h', f.read(2))[0]
            bld.PartMng = struct.unpack('2h', f.read(4))[0]

            bld.PartNum = struct.unpack('h', f.read(2))[0]
            bld.DownNum = struct.unpack('h', f.read(2))[0]
            bld.MiddleNum = struct.unpack('h', f.read(2))[0]
            bld.UpNum = struct.unpack('h', f.read(2))[0]

            bld.booIsAnimate = struct.unpack('c', f.read(1))[0]
            bld.grFrame = struct.unpack('5i', f.read(20))[0]
            bld.m_gpAttribLeftUp = struct.unpack('2i', f.read(8))

            bld.m_cxDisMetrix = struct.unpack('h', f.read(2))[0]
            bld.m_cyDisMetrix = struct.unpack('h', f.read(2))[0]

            bld.m_gpCharacter = struct.unpack('20i', f.read(80))[0]

            for i in range(bld.m_cyDisMetrix):
                for j in range(bld.m_cxDisMetrix):
                    building_node = struct.unpack('2c', f.read(2))[0]

            bld.m_wSound = struct.unpack('h', f.read(2))
            bld.m_bLight = struct.unpack('c', f.read(1))
            bld.m_bAniDisplay = struct.unpack('c', f.read(1))

            for z in range(bld.PartNum):
                a_bld = self.AModelBld()
                a_bld.m_szName = struct.unpack('8c', f.read(8))
                a_bld.m_booIsSpr = struct.unpack('c', f.read(1))
                a_bld.m_dPicID = struct.unpack('4c', f.read(4))
                a_bld.m_pos_x = struct.unpack('i', f.read(4))
                a_bld.m_pos_y = struct.unpack('i', f.read(4))

            # print("%d : %s" % (bld.iModelAutoID, hex(bld.iModelAutoID)))
            num -= 1
        print('共有%d个组件' % self.file_header.inum)

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f


if __name__ == '__main__':
    file_name = '/home/jeroen/work/qinshang/game/mdl/house.Mdl'
    # file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhaocun1.BNT'
    bnt = MdlBase(file_name)
