""" Implements support for CX Controller Hardware features

Copyright (C) Nanosurf AG - All Rights Reserved (2021)
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
https://www.nanosurf.com
"""

from enum import IntEnum
import time
import numpy as np
import nanosurf

class Converter(IntEnum):
    HiResOut_POSITIONX = 1
    HiResOut_POSITIONY = 2
    HiResOut_POSITIONZ = 3
    HiResOut_POSITIONW = 4
    HiResOut_TIPVOLTAGE = 5
    HiResOut_OUT6 = 6
    HiResOut_OUT7 = 7
    HiResOut_OUT8 = 8
    HiResOut_USER1= 9
    HiResOut_USER2 = 10
    HiResOut_USER3 = 11
    HiResOut_USER4 = 12
    FastOut_EXCITATION = 13
    FastOut_USER = 14
    FastOut_FAST2 = 15
    FastOut_FAST3 = 16
    HiResIn_DEFLECTION = 17
    HiResIn_LATERAL = 18
    HiResIn_POSITIONX = 19
    HiResIn_POSITIONY = 20
    HiResIn_POSITIONZ = 21
    HiResIn_DETECTORSUM = 22
    HiResIn_TIPCURRENT = 23
    HiResIn_IN6 = 24
    HiResIn_USER1 = 25
    HiResIn_USER2 = 26
    HiResIn_USER3 = 27
    HiResIn_USER4 = 28
    FastIn_DEFLECTION = 29
    FastIn_CH2 = 30
    FastIn_USER = 31

class Module(IntEnum):
    SigAnalyzer_1 = 1
    SigAnalyzer_2 = 2
    AnalogHiResOutMux = 3
    AnalogFastOutMux = 4
    CaptureHiRes = 5
    CaptureFast = 6

class _SPMModule:
    def __init__(self, spm):
        self._spm = spm
        self._lu = None
        self.__source = None
        self.__target = None

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, val):
        self.__source = val

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, val):
        self.__target = val


class _SPMAnalogOut(_SPMModule):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm)
        self._lu_inst_name = lu_inst_name

    @property
    def inst_name(self):
        return self._lu_inst_name
    @property
    def dc(self):
        return self._lu.current_output_value.value

    @dc.setter
    def dc(self, val):
        self._lu.static_value.value = val
        self._lu.input.value = self._static_input_channel_index

    @property
    def dc_norm(self):
        return self._lu.current_output_value.value / self.max

    @dc_norm.setter
    def dc_norm(self, val):
        self.dc = val * self.max

    @property
    def dc_v(self):
        return self.dc_norm * self._voltage_range

    @dc_v.setter
    def dc_v(self, val):
        self.dc_norm = val / self._voltage_range

    @property
    def unit(self):
        return self._lu.current_output_value.unit

    @property
    def max(self):
        return self._lu.current_output_value.value_max

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, val):
        self.__source = val
        if isinstance(self.__source,SPMSineWaveGenerator):
            self.__source.target = self
            self._lu.input.value = self._ac_input_channel_index[self.__source.inst_name]
            self._lu.calib_sig_source_dir.value = self._spm.lowlevel.AnalogHiResOut.CalibSigSourceDir.FromOutputToInput
        elif isinstance(self.__source,_SPMChannelMux):
            self.__source.channelmap = self._channelmap
            self.__source.target = self
            if self.__source.channel != "":
                self.__source.channel =  self.__source.channel  # reset channel to saved value
            self._lu.calib_sig_source_dir.value = self._spm.lowlevel.AnalogHiResOut.CalibSigSourceDir.FromInputToOutput
        else:
            self._lu.input.value = self._static_input_channel_index
            self._lu.calib_sig_source_dir.value = self._spm.lowlevel.AnalogHiResOut.CalibSigSourceDir.FromOutputToInput

    @property
    def inverted(self):
        return self._lu.calib_polarity.value == self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Negative

    @inverted.setter
    def inverted(self, val):
        if val == True:
            self._lu.calib_polarity.value = self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Negative
        else:
            self._lu.calib_polarity.value = self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Positive

    @property
    def calib_gain(self):
        return self._lu.calib_gain.value

    @calib_gain.setter
    def calib_gain(self, val):
        self._lu.calib_gain.value = val

    @property
    def calib_offset(self):
        return self._lu.calib_offset.value

    @calib_offset.setter
    def calib_offset(self, val):
        self._lu.calib_offset.value = val

class SPMAnalogHiresOut(_SPMAnalogOut):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm, lu_inst_name)
        self._lu = spm.lowlevel.AnalogHiResOut(spm.lowlevel.AnalogHiResOut.Instance[lu_inst_name])
        self._voltage_range = 10.0
        self._channelmap = self._spm.lowlevel.AnalogHiResOut.InputChannels
        self._static_input_channel_index = spm.lowlevel.AnalogHiResOut.InputChannels.Static
        self._ac_input_channel_index = {
            "INST2":spm.lowlevel.AnalogHiResOut.InputChannels.GenTest_Dynamic
            }

class SPMAnalogFastOut(_SPMAnalogOut):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm, lu_inst_name)
        self._lu = spm.lowlevel.AnalogFastOut(spm.lowlevel.AnalogFastOut.Instance[lu_inst_name])
        self._voltage_range = 1.0
        self._channelmap = self._spm.lowlevel.AnalogFastOut.InputChannels
        self._static_input_channel_index = spm.lowlevel.AnalogFastOut.InputChannels.Static
        self._ac_input_channel_index = {
            "INST1":spm.lowlevel.AnalogFastOut.InputChannels.Analyzer1_Reference,
            "INST2":spm.lowlevel.AnalogFastOut.InputChannels.Analyzer2_Reference,
            }

class _SPMAnalogIn(_SPMModule):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm)
        self._lu_inst_name = lu_inst_name

    @property
    def inst_name(self):
        return self._lu_inst_name

    @property
    def dc(self):
        return self._lu.current_input_value.value

    @property
    def dc_norm(self):
        return self._lu.current_input_value.value / self.max

    @property
    def dc_v(self):
        return self.dc_norm * self._voltage_range

    @property
    def unit(self):
        return self._lu.current_input_value.unit

    @property
    def max(self):
        return self._lu.current_input_value.value_max

    @property
    def inverted(self):
        return self._lu.calib_polarity.value == self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Negative

    @inverted.setter
    def inverted(self, val):
        if val == True:
            self._lu.calib_polarity.value = self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Negative
        else:
            self._lu.calib_polarity.value = self._spm.lowlevel.AnalogHiResIn.CalibPolarity.Positive

    @property
    def calib_gain(self):
        return self._lu.calib_gain.value

    @calib_gain.setter
    def calib_gain(self, val):
        self._lu.calib_gain.value = val

    @property
    def calib_offset(self):
        return self._lu.calib_offset.value

    @calib_offset.setter
    def calib_offset(self, val):
        self._lu.calib_offset.value = val

class SPMAnalogHiresIn(_SPMAnalogIn):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm,lu_inst_name)
        self._lu = self._spm.lowlevel.AnalogHiResIn(spm.lowlevel.AnalogHiResIn.Instance[lu_inst_name])
        if 'USER' in lu_inst_name:
            self._voltage_range = 10.0
        else:
            self._voltage_range = 5.0

class SPMAnalogFastIn(_SPMAnalogIn):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm,lu_inst_name)
        self._lu = self._spm.lowlevel.AnalogFastIn(spm.lowlevel.AnalogFastIn.Instance[lu_inst_name])
        self._voltage_range = 1.0


class SPMSineWaveGenerator(_SPMModule):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm)
        self._lu_inst_name = lu_inst_name
        self._lu = self._spm.lowlevel.SignalAnalyzer(spm.lowlevel.SignalAnalyzer.Instance[lu_inst_name])
        self._lu.operating_mode.value = self._lu.OperatingMode.LockIn
        self._lu.target_amplitude_ctrl_mode.value = self._lu.AmplitudeCtrlMode.ConstDrive
        #self._lu.demodulator_bw.value = self._lu.DemodulatorBW.BW_360Hz

    @property
    def inst_name(self):
        return self._lu_inst_name

    @property
    def amp(self):
        return self.amp_norm * self.amp_max

    @amp.setter
    def amp(self, val):
        self.amp_norm = val / self.amp_max

    @property
    def amp_norm(self):
        return self._lu.reference_amplitude.value / self._lu.reference_amplitude.value_max

    @amp_norm.setter
    def amp_norm(self, val):
        self._lu.reference_amplitude.value = val * self._lu.reference_amplitude.value_max
        self._lu.switch_to_target_amplitude_ctrl_mode()

    @property
    def amp_v(self):
        return self.amp_norm * self.target._voltage_range

    @amp_v.setter
    def amp_v(self, val):
        self.amp_norm = val / self.target._voltage_range

    @property
    def amp_max(self):
        return self.target.max

    @property
    def amp_unit(self):
        return self.target.unit

    @property
    def freq(self):
        return  self._lu.reference_frequency.value

    @freq.setter
    def freq(self, val):
        self._lu.reference_frequency.value = val

class SPMLockIn(SPMSineWaveGenerator):
    def __init__(self, spm, lu_inst_name):
        super().__init__(spm, lu_inst_name)
        self.list_of_bandwidth = self._lu.DemodulatorBW
        self.demodulation_bw = self.list_of_bandwidth.BW_360Hz
        self._lu.input.value = self._lu.Input.FastInDeflection
        self._fast_input_channel_index = {
            "DEFLECTION":spm.lowlevel.SignalAnalyzer.Input.FastInDeflection,
            "CH2":spm.lowlevel.SignalAnalyzer.Input.FastIn2,
            "USER":spm.lowlevel.SignalAnalyzer.Input.FastInUser,
            }
        self._hires_input_channel_index = {
            "LATERAL":spm.lowlevel.SignalAnalyzer.Input.InLateral,
            "USER1":spm.lowlevel.SignalAnalyzer.Input.InUser1,
            "USER2":spm.lowlevel.SignalAnalyzer.Input.InUser2,
            "USER3":spm.lowlevel.SignalAnalyzer.Input.InUser3,
            "USER4":spm.lowlevel.SignalAnalyzer.Input.InUser4,
            "TIPCURRENT":spm.lowlevel.SignalAnalyzer.Input.InTipCurrent,
            "POSITIONX":spm.lowlevel.SignalAnalyzer.Input.InPositionX,
            "POSITIONY":spm.lowlevel.SignalAnalyzer.Input.InPositionY,
            "POSITIONZ":spm.lowlevel.SignalAnalyzer.Input.InPositionZ,
            }

    @property
    def reference_phase(self):
        return self._lu.reference_pase.value

    @reference_phase.setter
    def reference_phase(self, val):
        self._lu.reference_pase.value = val

    @property
    def demodulation_bw(self):
        return self._lu.demodulator_bw.value

    @demodulation_bw.setter
    def demodulation_bw(self, val):
        self._lu.demodulator_bw.value = val

    @property
    def input_amp(self):
        return self._lu.current_amplitude.value

    @property
    def input_phase(self):
        return self._lu.current_phase.value

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, val):
        self.__source = val
        if isinstance(self.__source,SPMAnalogFastIn):
            self.__source.target = self
            self._lu.input.value = self._fast_input_channel_index[self.__source.inst_name]
        elif isinstance(self.__source,SPMAnalogHiresIn):
            self.__source.target = self
            self._lu.input.value = self._hires_input_channel_index[self.__source.inst_name]
        elif isinstance(self.__source,SPMLockInMux):
            self.__source.channelmap = self._channelmap
            self.__source.target = self
            if self.__source.channel != "":
                self.__source.channel =  self.__source.channel  # reset channel to saved value
        else:
            assert False, "Assigned Lock-In source not supported: type: "+str(type(val))
            self.__source = None


class _SPMChannelMux(_SPMModule):
    def __init__(self, spm):
        self._channelmap = None
        self._channel_name = ""

    @property
    def channelmap(self):
        return self._channelmap

    @channelmap.setter
    def channelmap(self, val):
        self._channelmap = val

    @property
    def channel(self):
        return self._channel_name

    @channel.setter
    def channel(self, val):
        self._channel_name = val
        self.target._lu.input.value = self._channelmap[val]

class SPMHiResOutMux(_SPMChannelMux):
    def __init__(self, spm):
        super().__init__(spm)
        self.channelmap = spm.lowlevel.AnalogHiResOut.InputChannels

class SPMFastOutMux(_SPMChannelMux):
    def __init__(self, spm):
        super().__init__(spm)
        self.channelmap = spm.lowlevel.AnalogFastOut.InputChannels

class SPMLockInMux(_SPMChannelMux):
    def __init__(self, spm):
        super().__init__(spm)
        self.channelmap = spm.lowlevel.SignalAnalyzer.Input


class _SPMCapture(_SPMModule):
    def __init__(self, spm):
        super().__init__(spm)
        self._lu = self._spm.lowlevel.DataAcquisition()
        self._databuffer = self._spm.lowlevel.DataBuffer()
        self._channel_list = []
        self._channel_index = {}
        self.data = {}
        self.data_max = {}
        self.data_unit = {}

    @property
    def samples(self):
        return self.__samples

    @samples.setter
    def samples(self, val):
        if val > self.samples_max:
            val = self.samples_max
        if val > int(self._get_samples_max()):
            val = int(self._get_samples_max())

        self.__samples = val

    @property
    def samples_max(self):
        max_samples = self._get_samples_max()
        if max_samples > self._databuffer.available_points:
            max_samples = self._databuffer.available_points
        return int(max_samples)

    @property
    def channels(self):
        return self._channel_list

    @property
    def sample_rate(self):
        return self._get_capture_rate()

    @sample_rate.setter
    def sample_rate(self, val):
        return self._set_capture_rate(val)

    @channels.setter
    def channels(self, val):
        self._channel_list = val
        self._channel_index.clear()
        index = 0
        for ch in self._channel_list:
            self._channel_index[ch] = index
            index += 1

    def measure(self):
        self._lu.number_of_capture_sets.value = 1
        self._lu.active_capture_set.value = 0
        self._setup_inputs_and_mask()

        print("Measuring", end='')
        self._lu.capture_start()
        time.sleep(2.0) # these waiting time is important to let controller sw prepare the start and avoid wrong valid buffer message
        while not self._databuffer.is_valid:
            print(".", end='')
            time.sleep(1.0)
        print("")

        print("Read data", end='')
        self.data.clear()
        self.data_max.clear()
        self.data_unit.clear()
        for ch in self._channel_list:
            print(".", end='')
            data_channel = self._databuffer.channel(self._channel_index[ch])
            self.data[ch] = np.array(data_channel.data)/(pow(2, 31) - 1) * data_channel.dimension(2).data_range / 2.0
            self.data_max[ch] = data_channel.dimension(2).data_range / 2.0
            self.data_unit[ch] = data_channel.dimension(2).unit
        print("")

        self.timeline = np.linspace(0, 1.0 / self.sample_rate * (self.samples - 1), self.samples, endpoint=True)

    def _setup_inputs_and_mask(self):
        raise NotImplementedError

    def _get_capture_rate(self):
        raise NotImplementedError

    def _set_capture_rate(self, val):
        raise NotImplementedError

    def _get_samples_max(self):
        raise NotImplementedError


class SPMCaptureHiRes(_SPMCapture):
    def __init__(self, spm):
        super().__init__(spm)

    def _get_capture_rate(self):
        return self._lu.sampler_data_rate.value_max

    def _set_capture_rate(self, val):
       raise NotImplementedError

    def _get_samples_max(self):
       return int(self._lu.capture_hi_res_datapoints.value_max)

    def _set_daq_input_channel(self, ch):
        index = self._channel_index[ch]
        if index == 0:
            self._lu.capture_hi_res_ch_0_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 1:
            self._lu.capture_hi_res_ch_1_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 2:
            self._lu.capture_hi_res_ch_2_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 3:
            self._lu.capture_hi_res_ch_3_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 4:
            self._lu.capture_hi_res_ch_4_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 5:
            self._lu.capture_hi_res_ch_5_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 6:
            self._lu.capture_hi_res_ch_6_input.value = self._lu.CaptureHiResInSignal[ch]
        elif index == 7:
            self._lu.capture_hi_res_ch_7_input.value = self._lu.CaptureHiResInSignal[ch]
        else:
            assert False, f"index={index} is out of range"

    def _setup_inputs_and_mask(self):
        mask = 0
        for ch in self._channel_list:
            mask |= 1 << self._channel_index[ch]
            self._set_daq_input_channel(ch)
        self._lu.capture_fast_channel_mask.value = 0
        self._lu.capture_hi_res_channel_mask.value = mask
        self._lu.capture_hi_res_group_id.value = self._databuffer.group_id
        self._lu.capture_hi_res_datapoints.value = self.samples

class SPMCaptureFast(_SPMCapture):
    def __init__(self, spm):
        super().__init__(spm)

    def _get_capture_rate(self):
        return self._lu.capture_fast_sampling_rate.value

    def _set_capture_rate(self, val):
       self._lu.capture_fast_sampling_rate.value = val

    def _get_samples_max(self):
       return int(self._lu.capture_fast_datapoints.value_max)

    def _set_daq_input_channel(self, ch):
        index = self._channel_index[ch]
        if index == 0:
            self._lu.capture_fast_ch_0_input.value = self._lu.CaptureFastInSignal[ch]
        elif index == 1:
            self._lu.capture_fast_ch_1_input.value = self._lu.CaptureFastInSignal[ch]
        else:
            assert False, f"index={index} is out of range"

    def _setup_inputs_and_mask(self):
        mask = 0
        for ch in self._channel_list:
            mask |= 1 << self._channel_index[ch]
            self._set_daq_input_channel(ch)
        self._lu.capture_hi_res_channel_mask.value = 0
        self._lu.capture_fast_channel_mask.value = mask
        self._lu.capture_fast_group_id.value = self._databuffer.group_id
        self._lu.capture_fast_datapoints.value = self.samples
        self._lu.capture_fast_sampling_rate.value = 24000000.0

class SPMController:
    """Main class for working with the CX of the teststand """

    def __init__(self, spm):
        """
        Parameters
        ----------
        spm
            reference to the nanosurf.spm class used
        """
        self._spm = spm
        self._channelmap = {
            Converter.HiResOut_POSITIONX:["AnalogHiResOut", "POSITIONX"],
            Converter.HiResOut_POSITIONY:["AnalogHiResOut", "POSITIONY"],
            Converter.HiResOut_POSITIONZ:["AnalogHiResOut", "POSITIONZ"],
            Converter.HiResOut_POSITIONW:["AnalogHiResOut", "POSITIONW"],
            Converter.HiResOut_TIPVOLTAGE:["AnalogHiResOut", "TIPVOLTAGE"],
            Converter.HiResOut_OUT6:["AnalogHiResOut", "APPROACH"],
            Converter.HiResOut_OUT7:["AnalogHiResOut", "OUT7"],
            Converter.HiResOut_OUT8:["AnalogHiResOut", "OUT8"],
            Converter.HiResOut_USER1:["AnalogHiResOut", "USER1"],
            Converter.HiResOut_USER2:["AnalogHiResOut", "USER2"],
            Converter.HiResOut_USER3:["AnalogHiResOut", "USER3"],
            Converter.HiResOut_USER4:["AnalogHiResOut", "USER4"],
            Converter.FastOut_EXCITATION:["AnalogFastOut", "EXCITATION"],
            Converter.FastOut_USER:["AnalogFastOut", "USER"],
            Converter.FastOut_FAST2:["AnalogFastOut", "FAST2"],
            Converter.FastOut_FAST3:["AnalogFastOut", "FAST3"],
            Converter.HiResIn_DEFLECTION:["AnalogHiResIn", "DEFLECTION"],
            Converter.HiResIn_LATERAL:["AnalogHiResIn", "LATERAL"],
            Converter.HiResIn_POSITIONX:["AnalogHiResIn", "POSITIONX"],
            Converter.HiResIn_POSITIONY:["AnalogHiResIn", "POSITIONY"],
            Converter.HiResIn_POSITIONZ:["AnalogHiResIn", "POSITIONZ"],
            Converter.HiResIn_DETECTORSUM:["AnalogHiResIn", "DETECTORSUM"],
            Converter.HiResIn_TIPCURRENT:["AnalogHiResIn", "TIPCURRENT"],
            Converter.HiResIn_IN6:["AnalogHiResIn", "IN6"],
            Converter.HiResIn_USER1:["AnalogHiResIn", "USER1"],
            Converter.HiResIn_USER2:["AnalogHiResIn", "USER2"],
            Converter.HiResIn_USER3:["AnalogHiResIn", "USER3"],
            Converter.HiResIn_USER4:["AnalogHiResIn", "USER4"],
            Converter.FastIn_DEFLECTION:["AnalogFastIn", "DEFLECTION"],
            Converter.FastIn_CH2:["AnalogFastIn", "CH2"],
            Converter.FastIn_USER :["AnalogFastIn", "USER"],
            }
        self._analyzermap = {
            Module.SigAnalyzer_1:["SignalAnalyzer", "INST1"],
            Module.SigAnalyzer_2:["SignalAnalyzer", "INST2"],
            }

    def get_dac(self, channel):
        if self._channelmap[channel][0] == "AnalogHiResOut":
            return SPMAnalogHiresOut(self._spm, self._channelmap[channel][1])
        if self._channelmap[channel][0] == "AnalogFastOut":
            return SPMAnalogFastOut(self._spm, self._channelmap[channel][1])
        return None

    def get_adc(self, channel):
        if self._channelmap[channel][0] == "AnalogHiResIn":
            return SPMAnalogHiresIn(self._spm, self._channelmap[channel][1])
        if self._channelmap[channel][0] == "AnalogFastIn":
            return SPMAnalogFastIn(self._spm, self._channelmap[channel][1])
        return None

    def get_sin_generator(self, module = Module.SigAnalyzer_2):
        if self._analyzermap[module][0] == "SignalAnalyzer":
            return SPMSineWaveGenerator(self._spm, self._analyzermap[module][1])
        return None

    def get_lock_in(self, module = Module.SigAnalyzer_2):
        if self._analyzermap[module][0] == "SignalAnalyzer":
            return SPMLockIn(self._spm, self._analyzermap[module][1])
        return None

    def get_channel_multiplexer(self, mux):
        if mux == Module.AnalogHiResOutMux:
            return SPMHiResOutMux(self._spm)
        elif mux == Module.AnalogFastOutMux:
            return SPMFastOutMux(self._spm)
        elif mux == Module.SigAnalyzer_1:
            return SPMLockInMux(self._spm)
        elif mux == Module.SigAnalyzer_2:
            return SPMLockInMux(self._spm)
        else:
            return None

    def get_data_capture(self, capture):
        if capture == Module.CaptureHiRes:
            return SPMCaptureHiRes(self._spm)
        elif capture == Module.CaptureFast:
            return SPMCaptureFast(self._spm)
        else:
            return None

def connect(spm = None, luparsefile = ""):
    if spm is None:
        spm = nanosurf.SPM(luparsefile)
    return SPMController(spm)

