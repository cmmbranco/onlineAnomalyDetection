import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import re
import seaborn as sns; sns.set()



import sys, getopt

def main(argv):
    inputfile = ''
    outputdir = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","odir="])
    except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputdir>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'dataset_plot.py -i <inputfile> -o <outputdir>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--odir"):
         outpudir = arg
    # print('Input file is '+  inputfile)
    # print('Output dir is ' + outputdir)

    outputdir = os.getcwd()+ '/' + outpudir


    inputsplit = os.getcwd()+inputfile


    ### Get current workpath
    dirpath = os.getcwd()+'/' + inputfile

    if not os.path.exists(outputdir):
       os.makedirs(outputdir)


    machine_data_path = dirpath
    data = pd.read_csv(machine_data_path)

    ## Extract anomaly points with value and position



    sns.set(rc={'figure.figsize':(11, 4)})


    ## Plot Timeseries
    #print("Anomaly dates: " + str(anomaly_list) + '\n')
    #print("Anomaly indexes: " + str(mark_every) + '\n')
    #print("Anomaly value at index: " + str(anomaly_ys) + '\n')


    data.plot(x='value', y='acc')
    plt.title("Value v Acc")
    plt.xlabel("Size")
    plt.ylabel("Accuracy Achieved")

    plt.xticks(fontsize=8)
    seriesdir = outputdir
    plt.savefig(seriesdir + '/accuracy_plot')




    #plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])
