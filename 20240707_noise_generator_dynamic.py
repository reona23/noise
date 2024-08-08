#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dynamic Noise Generator
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

jikken_time = 3600 * 3
phase_1_time = int(sys.argv[2]) ##1回目の干渉時間の設定
phase_2_time = int(sys.argv[3]) ##2回目の干渉時間の設定
phase_3_time = jikken_time - (phase_1_time + phase_2_time)

class noise_generator(gr.top_block):

    def __init__(self, noise_gain):
        gr.top_block.__init__(self, "Dynamic Noise Generator")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.noise_gain = noise_gain =int(sys.argv[1])

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(2402e6, 0)
        self.uhd_usrp_sink_0.set_gain(noise_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.uhd_usrp_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_bandwidth(self.samp_rate, 0)

    def get_noise_gain(self):
        return self.noise_gain

    def set_noise_gain(self, noise_gain):
        self.noise_gain = noise_gain
        self.uhd_usrp_sink_0.set_gain(self.noise_gain, 0)

    def set_center_freq(self, freq):
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("Usage: python3 your_script_name.py <noise_gain>")
    #     sys.exit(1)

    noise_gain = int(sys.argv[1])
    tb = noise_generator(noise_gain)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    time_start = time.time()
    while True:
        time_elapsed = time.time() - time_start
        if time_elapsed < phase_1_time:
            tb.set_center_freq(2402e6)
        elif time_elapsed < phase_1_time + phase_2_time:
            tb.set_center_freq(2480e6)
        else:
            tb.set_center_freq(2426e6)
        
        if time_elapsed > jikken_time:
            tb.stop()
            tb.wait()
            break
        time.sleep(1)  # Add a small sleep to reduce CPU usage
