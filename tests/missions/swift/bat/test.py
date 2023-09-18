import numpy as np
from gdt.core import data_path
from gdt.core.coords import Quaternion
from gdt.missions.swift.bat.poshist import BatSao

def test_file():
    print(data_path)
    return 'test_data/sw00974827000sao.fits'
test_file = 'test_data/sw00974827000sao.fits'
with BatSao.open(test_file) as poshist:

    frame = poshist.get_spacecraft_frame()
    state =poshist.get_spacecraft_states()
