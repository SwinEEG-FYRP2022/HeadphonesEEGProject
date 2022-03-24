import os
import matplotlib
import matplotlib.pyplot as plt

import argparse
import time
import numpy as np
import pandas as pd
import brainflow
import scipy.fftpack
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = "COM3"

    board = BoardShim(1, params)
    board.prepare_session()
    # board.start_stream () # use this for default options
    board.start_stream()
    time.sleep(10)
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()

    
    print(data)
    
    y1 = data[ 1, :]
    y2 = data[ 2, :]
    y3 = data[ 3, :]
    y4 = data[ 4, :]
   
    #x = d[ 0, :] - 100
    x = np.arange(len(y1)) / BoardShim.get_sampling_rate(1) # make array from 0 to end of y1 and divide by sampling rate
    fig, axs = plt.subplots(2)


    #plt.plot( x[1:190], y[1:190] )
    axs[0].plot( x, y1 )
    axs[0].plot( x, y2 )
    axs[0].plot( x, y3 )
    axs[0].plot( x, y4 )

    axs[0].set(xlabel="Time (s)")
    axs[0].set(ylabel="microVolts (uV)")

    y1_fft = np.absolute(np.fft.fft(y1)) # Does FFT of y1 and take magnitude of each complex number
    y2_fft = np.absolute(np.fft.fft(y2))
    y3_fft = np.absolute(np.fft.fft(y3))
    y4_fft = np.absolute(np.fft.fft(y4))
    x_fft = np.fft.fftfreq(len(y1_fft), 1.0/BoardShim.get_sampling_rate(1)) # Calculates x axis scale from sampling rate
    
    axs[1].plot(x_fft, y1_fft)
    axs[1].plot(x_fft, y2_fft)
    axs[1].plot(x_fft, y3_fft)
    axs[1].plot(x_fft, y4_fft)
    axs[1].set(xlabel="Frequency (Hz)")
    axs[1].set(ylabel="Magnitude")           
    plt.show()

    
    df = pd.DataFrame(np.transpose(data))
    print(df)
    df.to_csv('./brainy_data.csv')

if __name__ == "__main__":
    main()
