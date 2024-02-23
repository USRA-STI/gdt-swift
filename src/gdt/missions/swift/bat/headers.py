# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Copyright 2024 by Universities Space Research Association (USRA). All rights
# reserved.
#
# Developed by: Corinne Fletcher
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

from gdt.core.headers import Header, FileHeaders
from ..time import Time


__all__ = ['SaoHeaders','PhaHeaders', 'RspHeaders', 'LightcurveHeaders']

# mission definitions
_telescope = 'SWIFT'
_instrument = 'BAT'
_origin = 'GSFC'
_timesys = 'TT'
_timeunit = 's'
_radecsys = 'FK5'
_equinox = 2000.0
_mjdrefi = 51910
_mjdreff = '7.428703703703703e-4'

# common keyword cards
_date_card = ('DATE', '', 'file creation date (YYYY-MM-DDThh:mm:ss UT)')
_date_end_card = ('DATE-END', '',)
_date_obs_card = ('DATE-OBS', '',)
_dec_obj_card = ('DEC_OBJ', 0.0, '[dec] Dec Object')
_extname_card = ('EXTNAME', '', 'name of this binary table extension')
_equinox_card = ('EQUINOX', _equinox, 'Equinox for pointing RA/Dec')
_mjdrefi_card = ('MJDREFI', _mjdrefi, 'MJD reference day Jan 2001 00:00:00')
_mjdreff_card = ('MJDREFF', _mjdreff, 'MJD reference (fraction of day) 01 Jan 2001 00:')
_object_card = ('OBJECT', '', 'Object name')
_origin_card = ('ORIGIN', _origin, 'file creation location')
_radecsys_card = ('RADECSYS', _radecsys, 'Coordinates System')
_ra_obj_card = ('RA_OBJ', 0.0, '[deg] R.A. Object')
_telescope_card = ('TELESCOP', _telescope, 'Telescope (mission) name')
_timesys_card = ('TIMESYS', _timesys, 'time system')
_timeunit_card = ('TIMEUNIT', _timeunit, 'Time unit for timing header keywords')
_tstart_card = ('TSTART', 0.0, 'As in the TIME column')
_tstop_card = ('TSTOP', 0.0, 'As in the TIME column')
_time_obs_card = ('TIME-OBS', ' Start time for data')
_time_end_card = ('TIME-END', '', 'End time for data')
_trigtime_card = ('TRIGTIME', 0.0, 'MET TRIGger Time for Automatic Target')
_deltat_card = ('DELTAT', 0.0, 'Interval between records [s]')
_ra_nom_card = ('RA_NOM', 0.0, 'Nominal right ascension (degrees)')
_dec_nom_card = ('DEC_NOM', 0.0, 'Nominal declination (degrees)')
_creator_card = ('CREATOR', '', 'file creator')
_checksum_card = ('CHECKSUM', '', 'HDU checksum updated 2020-06-07T06:49:01')
_datasum_card = ('DATASUM', '', 'data unit checksum updated 2020-06-07T06:32:34')
_procver_card = ('PROCVER', '', 'Processing script version')
_softver_card = ('SOFTVER', '',)
_caldbver_card = ('CALDBVER', '', 'CALDB index versions used')
_clockapp_card = ('CLOCKAPP', '', 'If clock correction are applied (F/T)')
_obs_id_card = ('OBS_ID', '', 'Observation ID')
_seqpnum_card = ('SEQPNUM', 0, 'Number of times the dataset processed')
_targ_id_card = ('TARG_ID', 0, 'Target ID')
_seg_num_card = ('SEG_NUM', 0, 'Segment number')
_ra_pnt_card = ('RA_PNT', 0.0, '[deg] RA pointing')
_dec_pnt_card = ('DEC_PNT', 0.0, '[deg] Dec pointing')
_pa_pnt_card = ('PA_PNT', 0.0,  '[deg] Position angle (roll)')
_utcfinit_card = ('UTCFINIT', 0.0, '[s] UTCF at TSTART')
_attflag_card  = ('ATTFLAG',  100, 'Attitude origin: 100=sat/spacecraft')
_catsrc_card = ('CATSRC',   '', )
_instrument_card = ('INSTRUME', _instrument, ' Instrument name')
#----------------
class BatHeader(Header):

    def __setitem__(self, key, val):
        if not isinstance(key, tuple):
            if key.upper() == 'TSTART':
                self['DATE-OBS'] = Time(val, format='swift').iso
            elif key.upper() == 'TSTOP':
                self['DATE-END'] = Time(val, format='swift').iso
            else:
                pass


        super().__setitem__(key, val)


class SaoPrimaryHeader(BatHeader):
    name = 'PRIMARY'
    keywords = [_date_obs_card, _time_obs_card, _date_end_card,
                _time_end_card, _tstart_card, _tstop_card, _deltat_card, _ra_nom_card, _dec_nom_card,
                _telescope_card, _timesys_card, _timeunit_card, _mjdrefi_card,
                _mjdreff_card, _equinox_card, _radecsys_card, _creator_card,
                _origin_card, _date_card, _checksum_card, _datasum_card, _procver_card,
                _softver_card, _caldbver_card, _clockapp_card, _obs_id_card,_seqpnum_card,
                _targ_id_card, _seg_num_card, _object_card, _ra_obj_card, _dec_obj_card,
                _ra_pnt_card, _dec_pnt_card,_pa_pnt_card, _trigtime_card, _utcfinit_card]


class SaoPreFilterHeader(BatHeader):
    name = 'PREFILTER'
    keywords = [_extname_card,
                _date_obs_card, _time_obs_card, _date_end_card, _time_end_card,
                _tstart_card, _tstop_card, _deltat_card, _ra_nom_card, _dec_nom_card,
                _telescope_card, _timesys_card, _timeunit_card, _mjdrefi_card,
                _mjdreff_card, _equinox_card, _radecsys_card, _creator_card, _origin_card,
                _date_card, _checksum_card, _datasum_card, _procver_card,
                _softver_card, _caldbver_card,
                ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
                ('TIERABSO', 1.0, '[s] timing  precision  in seconds'),
                _obs_id_card, _seqpnum_card, _targ_id_card, _seg_num_card,
                _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card,
                _dec_pnt_card, _pa_pnt_card, _trigtime_card, _utcfinit_card]

class PhaPrimaryHeader(BatHeader):
    name='PRIMARY'
    keywords= [_telescope_card, _instrument_card, _obs_id_card,
               _targ_id_card, _seg_num_card, _timesys_card,
               _mjdrefi_card, _mjdreff_card, _clockapp_card,
               _timeunit_card, _tstart_card, _tstop_card, _date_obs_card, _date_end_card,('ORIGIN', 'NASA/GSFC', 'file creation location'),
               _creator_card, ('TLM2FITS', '', 'Telemetry converter version number'),
               _date_card, ('NEVENTS', 0, 'Number of events'), ('DATAMODE', '' , 'Datamode'),
               _object_card, ('MJD-OBS', 0.00000000000E+04, 'MJD of data start time'),
               ('TIMEREF', 'LOCAL   ', 'reference time'), _equinox_card, _radecsys_card, ('USER', '', 'User name of creator'),
               ('FILIN001', '', 'Input file name'), ('TIMEZERO', 0.000000000000000E+00, 'Time Zero'),
               _checksum_card, _datasum_card, _procver_card, _softver_card, _caldbver_card,
               _seqpnum_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card,
               _pa_pnt_card, _trigtime_card, _catsrc_card, _attflag_card, _utcfinit_card]

class PhaSpectrumHeader(BatHeader):
    name='SPECTRUM'
    keywords= [_extname_card, ('HDUCLASS', '', 'Conforms to OGIP/GSFC standards'), ('HDUCLAS1', '', 'Contains spectrum'),
               ('GAINAPP', '', 'Gain correction has been applied'),
               _timesys_card, _mjdrefi_card, _mjdreff_card, ('TIMEREF', 'LOCAL', 'reference time'),
               ('TASSIGN', 'SATELLITE', 'Time assigned by clock'),
               _timeunit_card, ('TIERRELA', 0.0E-0, '[s/s] relative errors expressed as rate'),
               ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),_trigtime_card,
               _tstart_card, _tstop_card, _date_obs_card, _date_end_card,
               _clockapp_card, ('TELAPSE', 0.0, '[s] Total elapsed time from start to stop'),
               ('ONTIME', 0.0, '[s] Accumulated on-time'), ('LIVETIME', 0.0, '[s] ONTIME multiplied by DEADC'),
               ('EXPOSURE', 0.0, '[s] Accumulated exposure'), ('DEADC', 0., 'Dead time correction factor'),
               ('TIMEPIXR', 0., 'Time bin alignment'), ('TIMEDEL', 0.0E-00, '[s] time resolution of data'),
               _telescope_card, _instrument_card, ('DATAMODE', '', 'Datamode'),
               _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card,
               _radecsys_card, ('OBS_MODE', '', 'default'),
               ('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card, ('TLM2FITS', '', 'Telemetry converter version number'),
               _date_card, _procver_card, _softver_card, _caldbver_card,
               _seqpnum_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,
               _catsrc_card, _attflag_card,_utcfinit_card, _checksum_card, _datasum_card]

class PhaEboundsHeader(BatHeader):
    name='EBOUNDS'
    keywords=[_extname_card, ('HDUCLASS', '', 'Conforms to OGIP/GSFC standards'), ('HDUCLAS1', '', 'Contains spectrum'),
             ('GAINAPP', '', 'Gain correction has been applied'),
             _timesys_card, _mjdrefi_card, _mjdreff_card,
             ('TIMEREF', 'LOCAL' , 'reference time'),
             ('TASSIGN', '', 'Time assigned by clock'),
             _timeunit_card, ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
             ('TIERABSO', 1.0, '[s] timing  precision  in seconds'),
             _tstart_card, _tstop_card, _date_obs_card, _date_end_card, _clockapp_card,_trigtime_card,
             ('DEADC', 1., 'dead time correction'), ('TIMEPIXR', 0.0 , 'Bin time beginning=0 middle=0.5 end=1'),
             ('TIMEDEL', 100.0E-6, '[s] time resolution of data'),
             _telescope_card, _instrument_card, ('DATAMODE', '' , 'Datamode'),
            _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
            ('OBS_MODE', '', 'default'),('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card,
            ('TLM2FITS', '' , 'Telemetry converter version number'),
            _date_card, _procver_card, _softver_card, _caldbver_card, _seqpnum_card, _ra_obj_card, _dec_obj_card,
            _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,_catsrc_card, _attflag_card, _utcfinit_card, _checksum_card, _datasum_card]

class PhaStdgtiHeader(BatHeader):
    name='STDGTI'
    keywords= [_extname_card, ('HDUCLASS', '', 'Conforms to OGIP/GSFC standards'), ('HDUCLAS1', '', 'Contains good time intervals'),
              ('HDUCLAS2', '', 'Contains standard good time intervals'),
              ('HDUVERS', '', 'Version of GTI header'),
              ('TIMEZERO', 0., 'Zero-point offset for TIME column'),
              ('MJDREF', 0.000000000E+00, 'MJD Epoch of TIME = 0'), _tstart_card, _tstop_card,
              ('GAINAPP', '', 'Gain correction has been applied'), _timesys_card,_trigtime_card,
              ('TIMEREF', 'LOCAL', 'reference time'), ('TASSIGN', '', 'Time assigned by clock'),
              _timeunit_card, ('TIERRELA', 0.0E-0, '[s/s] relative errors expressed as rate'),
              ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
              _date_obs_card, _date_end_card, _clockapp_card,
              ('DEADC', 0., 'dead time correction'),
              ('TIMEPIXR', 0.0, 'Bin time beginning=0 middle=0.5 end=1'),
              ('TIMEDEL', 00.0E-0, '[s] time resolution of data'),
              _telescope_card, _instrument_card, ('DATAMODE', '', 'Datamode'),
              _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
              ('OBS_MODE', '', 'default'),
              ('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card, ('TLM2FITS', '', 'Telemetry converter version number'),
              _date_card, _object_card, ('MJD-OBS', 5.899743394888889E+04, 'MJD of data start time'),
              ('USER', '', 'User name of creator'), ('FILIN001', '',  'Input file name'),
              ('NPIXSOU', 0.0000000E+00, 'Number of pixels in selected region'),
              _procver_card, _seqpnum_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,
              _catsrc_card, _attflag_card, _utcfinit_card, _checksum_card, _datasum_card]

class RspPrimaryHeader(BatHeader):
     name = 'PRIMARY'
     keywords=[_procver_card, _softver_card, _caldbver_card, _timesys_card,
            _mjdrefi_card, _mjdreff_card, _clockapp_card, _timeunit_card,
            _obs_id_card, _seqpnum_card, _targ_id_card, _seg_num_card,
            _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card,
            _pa_pnt_card, _trigtime_card, _catsrc_card, _attflag_card, _checksum_card, _datasum_card]

class RspSpecHeader(BatHeader):
      name = 'SPECRESP MATRIX'
      keywords =[ _extname_card, ('HDUCLASS', '', 'Conforms to OGIP/GSFC standards'),
      ('HDUCLAS1', '', 'Dataset relates to spectral response'),
      ('GAINAPP' , '','Gain correction has been applied'),
      _timesys_card, _mjdrefi_card, _mjdreff_card,
      ('TIMEREF', '',  'reference time'),
      ('TASSIGN', '', 'Time assigned by clock'),
      _timeunit_card,
      ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
      ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
       _tstart_card, _tstop_card, _date_obs_card, _date_end_card,
      ('CLOCKAPP', '', 'default'),
      ('TELAPSE', 0.0, '[s] Total elapsed time from start to stop'),
      ('ONTIME', 0.0, '[s] Accumulated on-time'),
      ('LIVETIME', 0.0, '[s] ONTIME multiplied by DEADC'),
      ('EXPOSURE', 0.0, '[s] Accumulated exposure'),
      ('DEADC', 0.,  'Dead time correction factor'),
      ('TIMEPIXR', 0., 'Time bin alignment'),
      ('TIMEDEL', 100.0E-6, '[s] time resolution of data'),
      _telescope_card, _instrument_card,
      ('DATAMODE', '', 'Datamode'),
      _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
      ('OBS_MODE', '', 'default'),
      ('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card,
      ('TLM2FITS', '', 'Telemetry converter version number'), _date_card, ('TIMEZERO', 0.000E+00,'Time Zero' ),
      _object_card, ('MJD-OBS', 5.899743394888889E+04, 'MJD of data start time'),  ('USER', '', 'User name of creator'), ('FILIN001', '',  'Input file name'),
      ('NPIXSOU', 0.0000000E+00, 'Number of pixels in selected region'),  ('BACKAPP', '', 'Was background correction applied?'),
      ('HDUCLAS2', 'RSP_MATRIX','Dataset is a spectral response matrix'),('HDUCLAS3', '','Convolvved with det. effects and mask'), ('PHAVERSN', '', 'Vversion of spectrum format'),
      ('HDUVERS', '', 'Version of GTI header'), ('FLUXMETH', '', 'Flux extraction method'),('DETCHANS', 0, 'Total number of detector channels availalble'),('NUMGRP', 0, 'Number of channel subsets'), _procver_card, _softver_card,_caldbver_card, _seqpnum_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,
       _catsrc_card, _attflag_card, _utcfinit_card, _checksum_card, _datasum_card]

class RspEboundsHeader(BatHeader):
    name = 'EBOUNDS'
    keywords = [_extname_card, ('HDUCLASS', '', 'Conforms to OGIP/GSFC standards'),
    ('HDUCLAS1', '','Contains spectrum'),
    ('GAINAPP' , '','Gain correction has been applied'),
    _timesys_card, _mjdrefi_card, _mjdreff_card,
    ('TIMEREF', '',  'reference time'),
    ('TASSIGN', '', 'Time assigned by clock'),
     _timeunit_card,
     ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
     ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
     _tstart_card, _tstop_card, _date_obs_card, _date_end_card,
     ('CLOCKAPP', '', 'default'),
     ('TELAPSE', 0.0, '[s] Total elapsed time from start to stop'),
     ('ONTIME', 0.0, '[s] Accumulated on-time'),
     ('LIVETIME', 0.0, '[s] ONTIME multiplied by DEADC'),
     ('EXPOSURE', 0.0, '[s] Accumulated exposure'),('DEADC', 0.,  'Dead time correction factor'),
     ('TIMEPIXR', 0., 'Time bin alignment'),
     ('TIMEDEL', 100.0E-6, '[s] time resolution of data'),
     _telescope_card, _instrument_card,
     ('DATAMODE', '', 'Datamode'),
     _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
     ('OBS_MODE', '', 'default'),('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card,('TLM2FITS', '', 'Telemetry converter version number'), _date_card,
     ('TIMEZERO', 0.000E+00,'Time Zero' ),
     _object_card, ('MJD-OBS', 5.899743394888889E+04, 'MJD of data start time'),  ('USER', '', 'User name of creator'), ('FILIN001', '',  'Input file name'),
     ('NPIXSOU', 0.0000000E+00, 'Number of pixels in selected region'),  ('BACKAPP', '', 'Was background correction applied?'),
     ('HDUCLAS2', 'RSP_MATRIX','Dataset is a spectral response matrix'),('HDUCLAS3', '','Convolvved with det. effects and mask'), ('PHAVERSN', '', 'Version of spectrum format'),
     ('HDUVERS', '', 'Version of GTI header'), ('FLUXMETH', '', 'Flux extraction method'), ('DETCHANS', 0, 'Total number of detector channels availalble'),_procver_card, _softver_card,_caldbver_card, _seqpnum_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,
      _catsrc_card, _attflag_card, _utcfinit_card, _checksum_card, _datasum_card]

class LcPrimaryHeader(BatHeader):
     name = 'PRIMARY'
     keywords=[_telescope_card, _instrument_card, _obs_id_card,_targ_id_card, _seg_num_card,_timesys_card,
            _mjdrefi_card, _mjdreff_card, _clockapp_card, _timeunit_card, _tstart_card,
            _tstop_card, _date_obs_card, _date_end_card, _origin_card, _creator_card,
            ('TLM2FITS', '' , 'Telemetry converter version number'), _date_card, _procver_card,
            _softver_card, _caldbver_card, _seqpnum_card,
            _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card,
            _pa_pnt_card, _trigtime_card, _catsrc_card, _attflag_card, ('UTCFINIT', '0.0', '[s] UTCF at TSTART'),
            _checksum_card, _datasum_card]

class LcRateHeader(BatHeader):
     name = 'RATE'
     keywords=[_extname_card, ('HDUCLASS', 'OGIP', 'Conforms to OGIP/GSFC standards'),
     ('HDUCLAS1', 'LIGHTCURVE','Contains light curve'),
     ('GAINAPP' , '','Gain correction has been applied'),
     _timesys_card, _mjdrefi_card, _mjdreff_card,('TIMEREF', '',  'reference time'),
     ('TASSIGN', '', 'Time assigned by clock'),
      _timeunit_card,
      ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
      ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
      _tstart_card, _tstop_card, _date_obs_card, _date_end_card,
      ('CLOCKAPP', '', 'default'),
      ('TELAPSE', 0.0, '[s] Total elapsed time from start to stop'),
      ('ONTIME', 0.0, '[s] Accumulated on-time'),
      ('LIVETIME', 0.0, '[s] ONTIME multiplied by DEADC'),
      ('EXPOSURE', 0.0, '[s] Accumulated exposure'),('DEADC', 0.,  'Dead time correction factor'),
      ('TIMEPIXR', 0., 'Time bin alignment'),
      ('TIMEDEL', 100.0E-6, '[s] time resolution of data'),
      _telescope_card, _instrument_card,('DATAMODE', '', 'Datamode'),
      _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
      ('OBS_MODE', '', 'default'),('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card,('TLM2FITS', '', 'Telemetry converter version number'), _date_card,
      _trigtime_card, _procver_card, _softver_card, _caldbver_card, _seqpnum_card,
      _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card,
      _pa_pnt_card,_attflag_card, ('UTCFINIT', '0.0', '[s] UTCF at TSTART'), _checksum_card, _datasum_card
      ]

class LcEboundsHeader(BatHeader):
  name = 'EBOUNDS'
  keywords = [_extname_card, ('HDUCLASS', 'OGIP', 'Conforms to OGIP/GSFC standards'),
  ('HDUCLAS1', 'RESPONSE','Contains spectrum'),
  ('GAINAPP' , '','Gain correction has been applied'),
  _timesys_card, _mjdrefi_card, _mjdreff_card,
  ('TIMEREF', '',  'reference time'),
  ('TASSIGN', '', 'Time assigned by clock'),
  _timeunit_card,
   ('TIERRELA', 1.0E-8, '[s/s] relative errors expressed as rate'),
   ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
   _tstart_card, _tstop_card, _date_obs_card, _date_end_card,
   ('CLOCKAPP', '', 'default'),('DEADC', 0.,  'Dead time correction factor'),
   ('TIMEPIXR', 0., 'Time bin alignment'),
   ('TIMEDEL', 100.0E-6, '[s] time resolution of data'),
   _telescope_card, _instrument_card,
   ('DATAMODE', '', 'Datamode'),
   _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
   ('OBS_MODE', '', 'default'),('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card,
   ('TLM2FITS', '', 'Telemetry converter version number'), _date_card,
    _trigtime_card, _procver_card, _softver_card, _caldbver_card, _seqpnum_card,
    _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card,
    _pa_pnt_card,_attflag_card, ('UTCFINIT', '0.0', '[s] UTCF at TSTART'), _checksum_card, _datasum_card
   ]

class LcStdgtiHeader(BatHeader):
   name='STDGTI'
   keywords= [_extname_card, ('HDUCLASS', 'OGIP', 'Conforms to OGIP/GSFC standards'), ('HDUCLAS1', 'GTI', 'Contains good time intervals'),
             ('HDUCLAS2', 'STANDARD', 'Contains standard good time intervals'),
             ('HDUVERS', '', 'Version of GTI header'),
             ('TIMEZERO', 0., 'Zero-point offset for TIME column'),
             ('MJDREF', 0.000000000E+00, 'MJD Epoch of TIME = 0'), _tstart_card, _tstop_card,
             ('GAINAPP', '', 'Gain correction has been applied'), _timesys_card,
             ('TIMEREF', 'LOCAL', 'reference time'), ('TASSIGN', '', 'Time assigned by clock'),
             _timeunit_card, ('TIERRELA', 0.0E-0, '[s/s] relative errors expressed as rate'),
             ('TIERABSO', 0.0, '[s] timing  precision  in seconds'),
             _date_obs_card, _date_end_card, _clockapp_card,('EXPOSURE', 0.0, '[s] Accumulated exposure'),
             ('DEADC', 0., 'dead time correction'),
             ('TIMEPIXR', 0.0, 'Bin time beginning=0 middle=0.5 end=1'),
             ('TIMEDEL', 00.0E-0, '[s] time resolution of data'),
             _telescope_card, _instrument_card, ('DATAMODE', '', 'Datamode'),
             _obs_id_card, _targ_id_card, _seg_num_card, _equinox_card, _radecsys_card,
             ('OBS_MODE', '', 'default'),
             ('ORIGIN', 'NASA/GSFC', 'file creation location'), _creator_card, ('TLM2FITS', '', 'Telemetry converter version number'),
             _trigtime_card,_date_card, _procver_card, _seqpnum_card, _object_card, _ra_obj_card, _dec_obj_card, _ra_pnt_card, _dec_pnt_card, _pa_pnt_card,
             _catsrc_card, _attflag_card, _utcfinit_card, _checksum_card, _datasum_card]


#-------------------------------------


class RspHeaders(FileHeaders):
    _header_templates = [RspPrimaryHeader(), RspSpecHeader(), RspEboundsHeader()]

class SaoHeaders(FileHeaders):
    _header_templates = [SaoPrimaryHeader(), SaoPreFilterHeader()]

class PhaHeaders(FileHeaders):
    _header_templates =[PhaPrimaryHeader(), PhaSpectrumHeader(), PhaEboundsHeader(), PhaStdgtiHeader()]

class LightcurveHeaders(FileHeaders):
    _header_templates = [LcPrimaryHeader(), LcRateHeader(), LcEboundsHeader(), LcStdgtiHeader()]
