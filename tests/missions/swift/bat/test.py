import numpy as np
from gdt.core import data_path
from gdt.core.coords import Quaternion
from gdt.missions.swift.bat.lightcurve import BatLightcurve
from gdt.missions.swift.bat.finders import *
from gdt.missions.swift.bat.pha import *
pha = BatPha()
pha.open('test_data/sw00974827000bevas.pha')
print(pha.data)

# finder = BatDataProductsFtp('01116441', '2022-07')
#
# #finder.get_all('.')
# #print(finder.cd())
# finder.ls_all()
# print(len(finder.ls_all()))
