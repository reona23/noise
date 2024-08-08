#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Noise Generator
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


class noise_generator(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Noise Generator")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6 # 5e6
        self.noise_gain = noise_gain = int(sys.argv[1])

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
        self.uhd_usrp_sink_0.set_center_freq(2426e6, 0)
        self.uhd_usrp_sink_0.set_gain(noise_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
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


tb = noise_generator()

def sig_handler(sig=None, frame=None):
    tb.stop()
    tb.wait()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

tb.start()
time_start = time.time()
while (True):
    time_end = time.time()
    if time_end - time_start > jikken_time:
        tb.stop()
        tb.wait()
       # sys.exit(0)
        break