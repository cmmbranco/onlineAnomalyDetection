import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import re
from cycler import cycler
import numpy as np
import matplotlib as mpl
import seaborn as sns; sns.set()



import sys, getopt

def main(argv):
    inputfile = ''
    outputdir = ''
    detector = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","odir=","detector="])
    except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputdir> -d <detector>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'dataset_plot.py -i <inputfile> -o <outputdir>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--odir"):
         outpudir = arg
      elif opt in ("-d", "--detector"):
         detector = arg
    # print('Input file is '+  inputfile)
    # print('Output dir is ' + outputdir)


    inputsplit = os.getcwd()+inputfile
    inputsplit = str(inputfile).split('/')
    datasetname =  str(inputsplit[len(inputsplit)-2]) + '/' +str(inputsplit[len(inputsplit)-1]).strip('.csv')


    outputdir = os.getcwd()+ '/' + outpudir

    inputpath = os.getcwd()+'/' + inputfile
    imgdir =  outpudir + str(inputsplit[len(inputsplit)-2])


    print("Datasetname is: " + datasetname)

    ### Get current workpath
    ### Create if needed

    if not os.path.exists(imgdir):
       os.makedirs(imgdir)



    anomaliepath = str(inputpath).split('/')

    concatanomaliepath = ''
    pos = 0;
    for arg in anomaliepath:
        concatanomaliepath +=  arg+ '/'
        if(pos == len(anomaliepath)-4):
            break
        pos += 1

    labels_json = str(concatanomaliepath) + 'labels/combined_labels.json'

    ## Extract anomalous timepoints and respective values
    my_results = str(concatanomaliepath) + 'results/' +detector+ '/' + str(inputsplit[len(inputsplit)-2]) + '/' + ''+detector+'_' + str(inputsplit[len(inputsplit)-1])

    print('\n')
    print("Filepath is: \n" + inputpath )
    print("Outputdir dir is: \n" + imgdir)
    print("Anomaly path is: \n" + my_results)


    #### Extract my issued labels

    data_after_detect = pd.read_csv(my_results)

    ## Extract anomaly points with value and position
    res = data_after_detect.loc[data_after_detect['anomaly_score'] == 1]
    anomaly_list = res['timestamp'].tolist()

    ## Padding for ploting
    mark_every_error = []
    #anomaly_ys = []
    for i in range(len(anomaly_list)):
       mark_every_error.append(data_after_detect.index[data_after_detect['timestamp'] == anomaly_list[i]].tolist()[0])

    #### Prepare Ground truth labels
    ground_truth = []
    with open(labels_json) as f:
     anomalies = json.load(f)

     for anomaly in anomalies[datasetname+'.csv']:
         ground_truth.append(re.sub(r'\.0+','', anomaly))

    mark_every_label = []

    #anomaly_ys = []
    for i in range(len(ground_truth)):
        mark_every_label.append(data_after_detect.index[data_after_detect['timestamp'] == ground_truth[i]].tolist()[0])


    sns.set(rc={'figure.figsize':(10, 4)})


    seriesdir = outputdir + '/' + str(inputsplit[len(inputsplit)-2]) + '/'


    f, ax = plt.subplots(1)


    data_after_detect2 = data_after_detect.set_index('timestamp')
    data_after_detect2.index = pd.to_datetime(data_after_detect2.index)
    ax.margins(x=0)

    ### Plot time series with errors marked

    #print("Every error is:")
    #print(mark_every_error)

    ax.plot(data_after_detect2.index, data_after_detect2['value'], '-D', markerfacecolor='r' ,markevery = mark_every_error)
    ax.plot(data_after_detect2.index, data_after_detect2['value'], 'D', markerfacecolor='y' ,markevery = mark_every_label)

    plt.title(datasetname +" with errors")
    plt.ylabel("Value")
    plt.xlabel("Date Time")
    plt.tight_layout()
    #plt.savefig(seriesdir + 'experiment_plot')
    plt.show()




if __name__ == "__main__":
   main(sys.argv[1:])
