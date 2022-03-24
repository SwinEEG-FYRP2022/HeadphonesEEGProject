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
    

    #plt.plot( x[1:190], y[1:190] )
    plt.plot( x, y1 )
    plt.plot( x, y2 )
    plt.plot( x, y3 )
    plt.plot( x, y4 )

    plt.xlabel("Time (s)")
    plt.ylabel("microVolts (uV)")
    
    plt.show()

    
    df = pd.DataFrame(np.transpose(data))
    print(df)
    df.to_csv('./brainy_data.csv')

if __name__ == "__main__":
    main()
