# ----------------------------------------------------------------------
# Copyright (C) 2015, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
This detector establishes a baseline score by recording a constant value for all
data points.
"""

from nab.detectors.base import AnomalyDetector

from matrixprofile import *
from discords import discords
from motifs import motifs
#from matrixprofile.motifs import motifs
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import sys
import os

from scipy import spatial
from scipy.fftpack import fft
from ConfigParser import SafeConfigParser

import scipy.stats

#import pdb; pdb.set_trace()


#from outliers import smirnov_grubbs as grubbs
#
# import inspect
#
# print(inspect.getmodule(discords).__file__)





class Sequence():

    def __init__(self):
        self.values = []

    def add(self, value):
        self.values.append(value)

    def getSeq(self):
        return self.values


    def compare(self,valseq):

        #### Direct similarity
        # equal = 0
        # for idx,val in enumerate(valseq.getSeq()):
        #     if(val == self.values[idx]):
        #         equal += 1

        #result = equal/len(valseq.getSeq())
        #return result


        ### Cosine similarity

        #print("hue")
        result = 1 - spatial.distance.cosine(self.values, valseq.getSeq())

        #print(result)
        return result





class MyDetector(AnomalyDetector):



    configParser = SafeConfigParser()
    settingspath  = str(os.getcwd())+ '/exp_settings.txt'
    configParser.read(settingspath)


    probabilistic_version = eval(configParser.get('my-config', 'probabilistic_version'))
    window_size = eval(configParser.get('my-config', 'window_size'))
    dataset_size_to_keep = eval(configParser.get('my-config','dataset_size_to_keep'))

    ttl = eval(configParser.get('my-config', 'ttl'))
    decay_rate = eval(configParser.get('my-config', 'decay_rate'))
    start_evaluation = eval(configParser.get('my-config', 'start_evaluation'))
    n_Discords_keep = eval(configParser.get('my-config', 'n_Discords_keep'))
    n_Discords_extract = eval(configParser.get('my-config', 'n_Discords_extract'))
    discord_sim_Threshold = eval(configParser.get('my-config', 'discord_sim_Threshold'))
    ex_zone = eval(configParser.get('my-config', 'ex_zone'))
    n_Motifs_keep = eval(configParser.get('my-config', 'n_Motifs_keep'))
    motif_ttl = eval(configParser.get('my-config', 'motif_ttl'))
    motif_sim_Threshold = eval(configParser.get('my-config', 'motif_sim_Threshold'))
    motif_ex_zone = eval(configParser.get('my-config', 'motif_ex_zone'))
    fourier_on = eval(configParser.get('my-config', 'fourier_on'))
    min_dist_on = eval(configParser.get('my-config', 'min_dist_on'))

    print("Experiment settings are...")
    print("dataset_size_to_keep: " + str(dataset_size_to_keep))
    print("window_size: " + str(window_size))
    print("ttl: " + str(ttl))
    print("decay_rate: " + str(decay_rate))
    print("start_evaluation: " + str(start_evaluation))
    print("n_Discords_keep: " + str(n_Discords_keep))
    print("n_Discords_extract: " + str(n_Discords_extract))
    print("discord_sim_Threshold: " + str(discord_sim_Threshold))
    print("ex_zone: " + str(ex_zone))
    print('\n')


    #### OTHER Variables
    algo_min = 8
    first = True
    second = True
    first_four = True
    second = True
    dataset = None
    pointnumb = 0

    maxdist = None

    # exclude up to a day on the left and right side
    # ex_zone = 0

    motif_columns = ["motif","last_seen", "count", "ttl"]
    motif_list = pd.DataFrame(columns = motif_columns)
    # motif_sim_Threshold = 0.99
    # n_Motifs_keep = 1000
    # motif_ttl = 1000

    discord_columns = ["discord", "last_seen", "count", "ttl"]
    discord_list = pd.DataFrame(columns = discord_columns)

    anomalyScore = None
    sample_interval = None
    old_scores = []
    distance_vector = None
    slopes = []
    prev = None
    anom2First = True

    def mean_confidence_interval(self,data, confidence=0.99):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h


    def maintain_dataset(self, inputData):
        ###Init dataset
        if self.first:

            self.first_ts = inputData['timestamp']

            ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([inputData['value']], columns = ["value"], index=[ts])
            self.dataset = new_row

            self.first = False



        ### Maintain dataset
        else:

            if (self.second):
                self.second = False
                self.second_ts = inputData['timestamp']

                self.delta_time = self.second_ts - self.first_ts


            #### Maintain dataset
            if(len(self.dataset.index) == self.dataset_size_to_keep):


                # print("########")
                # print("dataset before:")
                # print(len(self.dataset.index))
                # print(inputData['timestamp'])
                ### Drop oldest record to make space for the new one
                self.dataset = self.dataset.drop(self.dataset.index[[0]])
                # print("after_drop:")
                # print(len(self.dataset.index))
                ##Add new value to dataset
                ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([inputData['value']], columns = ["value"], index=[ts])
                # print("new row:")
                # print(new_row)

                self.dataset = pd.concat([self.dataset, pd.DataFrame(new_row)], ignore_index=True)
                self.dataset.reset_index(drop=True)

                # print("dataset after:")
                # print(len(self.dataset.index))



            else:
                ### Simply add new record as there is space
                ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([inputData['value']], columns = ["value"], index=[ts])
                self.dataset = pd.concat([self.dataset, pd.DataFrame(new_row)], ignore_index=True)
                self.dataset.reset_index(drop=True)
                # print(self.dataset.shape)


    def maintain_motifs(self, motif_list, ts ,inputData):

        print("Maintaining motifs")

        anomscore = 0
        # print("Maintain motifs: ")
        # print(motif_list)
        clean_motifs = []

        for nest1 in motif_list[0]:

            for value in nest1:
                clean_motifs.append(value)


        ### Fetch value sequence

        for pos in clean_motifs:
            motifseq = Sequence()

            for i in range(self.window_size):
                motifseq.add(self.dataset.iloc[pos+i]['value'])



            if self.motif_list.empty :
                print("First motif....trivial insertion")
                df_to_add = pd.DataFrame([[motifseq,ts,ts,1,self.motif_ttl]], columns=self.motif_columns)
                self.motif_list = pd.concat([self.motif_list,df_to_add],ignore_index=True)
                self.motif_list = self.motif_list.reset_index(drop=True)

            else:
                refreshed1 = False

                for row_idx1,cur_seq1 in self.motif_list.iterrows():
                    ## If its similar, refresh last seen and add count
                    # print(motifseq.compare(cur_seq1['motif']))
                    if motifseq.compare(cur_seq1['motif']) >= self.motif_sim_Threshold:
                        #print("Anom refresh: hit with score " + str(seq.compare(cur_seq['discord'])))
                        self.motif_list.loc[row_idx1,'last_seen'] = ts
                        self.motif_list.loc[row_idx1,'count'] += 1
                        self.motif_list.loc[row_idx1,'ttl'] = self.motif_ttl
                        #print(self.discord_list)

                        refreshed1 = True



                #### If no entry was refreshed add discord
                if not refreshed1:
                    ### New anomalous pattern found....this timepoint will be anomalous
                    anomscore = 1
                    print("Motif did not refresh: ")
                    print(inputData['timestamp'])

                    ###  Check if anomaly list is full....choose one to replace
                    if (self.motif_list.shape[0] >= self.n_Motifs_keep):

                        ### Drop oldest based on ttl
                        #print("Implement replace anomaly")
                        print("Motif replaced \n")

                        idx_to_drop = self.motif_list.ttl.idxmin()
                        #print("Dropping: " + str(self.discord_list.iloc[idx_to_drop].discord.getSeq()))

                        self.motif_list.drop(self.motif_list.index[idx_to_drop],inplace=True)

                        #print("Adding: " + str(seq.getSeq()))
                        df_to_add = pd.DataFrame([[motifseq,ts,ts,1,self.motif_ttl]], columns=self.motif_columns)
                        self.motif_list = pd.concat([self.motif_list,df_to_add],ignore_index=True)
                        self.motif_list=self.motif_list.reset_index(drop=True)
                        #print(self.motif_list)


                    ### If not full simply add
                    else:
                        print("Motif added \n")

                        df_to_add = pd.DataFrame([[motifseq,ts,ts,1,self.motif_ttl]], columns=self.motif_columns)
                        self.motif_list = pd.concat([self.motif_list,df_to_add],ignore_index=True)
                        self.motif_list=self.motif_list.reset_index(drop=True)
                        #print(self.motif_list)

        return anomscore;

    def evaluate_anom(self,inputData):


        if(len(self.dataset.index) == self.start_evaluation):

            if(self.min_dist_on):
                print("Minimum distance ON")
            else:
                print("Minimum distance OFF")

            if (self.fourier_on):


                #Number of sample points
                rfftval = np.abs(np.fft.rfft(self.dataset.value.values-self.dataset.values.mean()))

                xf = np.linspace(0, len(rfftval), len(rfftval))/60.0/60.0/len(rfftval)

                final = int(1/xf[np.argmax(rfftval)]/3600)*2


                self.window_size = final
                self.ex_zone = int(self.window_size/4)

                print("Fourier ON: window size is " + str(self.window_size))

                # print(N)
                # print(inputData['timestamp'])

            else:
                print("Fourier Off")



        ### Number after which we start evaluating...in this case two windows


        if (len(self.dataset.index) > self.start_evaluation):

            ## get values
            a = self.dataset.values.squeeze()


            try:

                ## Calculate scrimp
                results = matrixProfile.scrimp_plus_plus(a,self.window_size)



                temp_df = self.dataset.copy()
                temp_df['profile'] = np.append(results[0],np.zeros(self.window_size-1)+np.nan)
                temp_df['profile_index'] = np.append(results[1], np.zeros(self.window_size - 1) + np.nan)



                # we look for the 5 events specified in the data explaination
                found_anoms = discords(temp_df['profile'], self.ex_zone, k=self.n_Discords_extract)

                if((self.maxdist == None) and self.min_dist_on):
                    self.maxdist = temp_df.iloc[found_anoms[0]]['profile']

                    print("Minimum Distance Found:")
                    print(self.maxdist)

                else:
                    pass





                ####
                ####    Motif detection, other code must be uncommented
                ####
                #found_motifs = motifs(ts=self.dataset.values.squeeze(), mp=results, max_motifs=3, ex_zone=self.motif_ex_zone)
                #self.maintain_motifs(found_motifs, ts, inputData)


                ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")


                filtered_anoms = filter(lambda x : x != sys.maxsize, found_anoms)
                filtered_anoms = np.unique(filtered_anoms)

                final_anoms = []



                if(self.min_dist_on):
                    ### FIlter anomalies based on minimum distance required
                    for anom in filtered_anoms:

                        if(temp_df['profile'].get(anom) > self.maxdist):
                            final_anoms.append(anom)

                    filtered_anoms = final_anoms

                # print(filtered_anoms)
                # print("Anomalies are: \n")
                # print(filtered_anoms)
                # print(temp_df.iloc[filtered_anoms])

                ####
                #### This section manages anomalies found and their storage
                ####

                self.discord_list['ttl'] -= self.decay_rate
                # self.motif_list['ttl'] -= self.decay_rate


                ### Remove anomalies with ttl <= 0
                torem =  self.discord_list['ttl']>=0
                self.discord_list = self.discord_list[torem].reset_index(drop=True)

                torem =  self.motif_list['ttl']>=0
                self.motif_list = self.motif_list[torem].reset_index(drop=True)




                self.anomalyScore = 0;
                ### Grab anomaly sequences to compare with existing ones
                for pos in filtered_anoms:

                    #print("Considering: " + str(pos))

                    seq = Sequence()

                    ### Fetch value sequence

                    for i in range(self.window_size):
                        seq.add(temp_df.iloc[pos+i]['value'])


                    if self.discord_list.empty:

                        # print("Discord list empty...adding")


                        df_to_add = pd.DataFrame([[seq,ts,1,self.ttl]], columns=self.discord_columns)
                        self.discord_list = pd.concat([self.discord_list,df_to_add],ignore_index=True)
                        self.discord_list=self.discord_list.reset_index(drop=True)
                        print("discord was empty")




                    else:
                        refreshed = False

                        for row_idx,cur_seq in self.discord_list.iterrows():

                            ## If its similar, refresh last seen and add count
                            # print(seq.compare(cur_seq['discord']))
                            if seq.compare(cur_seq['discord']) >= self.discord_sim_Threshold:
                                #print("Anom refresh: hit with score " + str(seq.compare(cur_seq['discord'])))
                                self.discord_list.loc[row_idx,'last_seen'] = ts
                                self.discord_list.loc[row_idx,'count'] += 1
                                self.discord_list.loc[row_idx,'ttl'] = self.ttl
                                #print(self.discord_list)

                                refreshed = True



                        #### If no entry was refreshed add discord
                        if not refreshed:
                            ### New anomalouinputDatas pattern found....this timepoint will be anomalous
                            print("Input Data: ")
                            print(inputData['timestamp'])

                            self.anomalyScore = 1
                            ###  Check if anomaly list is full....choose one to replace
                            if (self.discord_list.shape[0] >= self.n_Discords_keep):

                                ### Drop oldest based on ttl
                                #print("Implement replace anomaly")
                                #print("Anomaly replaced \n")

                                idx_to_drop = self.discord_list.ttl.idxmin()
                                #print("Dropping: " + str(self.discord_list.iloc[idx_to_drop].discord.getSeq()))

                                self.discord_list.drop(self.discord_list.index[idx_to_drop],inplace=True)

                                #print("Adding: " + str(seq.getSeq()))
                                df_to_add = pd.DataFrame([[seq,ts,1,self.ttl]], columns=self.discord_columns)
                                self.discord_list = pd.concat([self.discord_list,df_to_add],ignore_index=True)
                                self.discord_list=self.discord_list.reset_index(drop=True)

                                #print(self.discord_list)


                            ### If not full simply add
                            else:
                                #print("Anomaly added \n")

                                # print(inputData['timestamp'])
                                # print(filtered_anoms)
                                # print(seq.getSeq())
                                # print(self.dataset.values)
                                # exit()
                                df_to_add = pd.DataFrame([[seq,ts,1,self.ttl]], columns=self.discord_columns)
                                self.discord_list = pd.concat([self.discord_list,df_to_add],ignore_index=True)
                                self.discord_list=self.discord_list.reset_index(drop=True)


            except Exception as e:

                print(e)
                print("GOT ERROR")
                print(self.window_size)
                print(self.dataset.size)
                #input()
                return (0, )




            # print(self.discord_list)
            # print("\n")
            # print(self.motif_list)

        #self.pointnumb +=1


        ####  Detect Drift


        #print(grubbs.test(self.dataset.values, alpha=0.05))
        #if self.anomalyScore == 1:
            #print("anomaly score is one...")
            #print(ts)

        ###Return detection result
        if self.anomalyScore == None:
            return (0, )

        else:

            #if self.anomalyScore == 1:
                # print("Input Data: ")
                # print(inputData['timestamp'])

            return(self.anomalyScore, )


    def evaluate_anom1(self,inputData):

        self.anomalyScore = 0;


        if(len(self.dataset.index) == self.start_evaluation):

            if(self.min_dist_on):
                print("Minimum distance ON")
            else:
                print("Minimum distance OFF")


        ### Number after which we start evaluating...in this case two windows


        if (len(self.dataset.index) > self.start_evaluation):


            ## get values
            a = self.dataset.values.squeeze()



            ## Calculate scrimp
            results = matrixProfile.scrimp_plus_plus(a,self.window_size)

            temp_df = self.dataset.copy()
            temp_df['profile'] = np.append(results[0],np.zeros(self.window_size-1)+np.nan)
            temp_df['profile_index'] = np.append(results[1], np.zeros(self.window_size - 1) + np.nan)



            # we look for the 5 events specified in the data explaination
            found_anoms = discords(temp_df['profile'], self.ex_zone, k=self.n_Discords_extract)

            if((self.maxdist == None) and self.min_dist_on):
                self.maxdist = temp_df.iloc[found_anoms[0]]['profile']

                print("Minimum Distance Found:")
                print(self.maxdist)
                self.distance_vector=[]

            else:
                pass

            ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")


            filtered_anoms = filter(lambda x : x != sys.maxsize, found_anoms)
            filtered_anoms = np.unique(filtered_anoms)

            final_anoms = []
            final_dist = []




            if(self.min_dist_on):
                ### FIlter anomalies based on minimum distance required
                for anom in filtered_anoms:

                    if(temp_df['profile'].get(anom) > self.maxdist):
                        final_anoms.append(anom)

                filtered_anoms = final_anoms


            #####
            ##### IMPLEMENT LOG LIKELIHOOD OF THE DISTANCES
            for pos in filtered_anoms:

                if ((not self.distance_vector) or len(self.distance_vector) < 3):
                        #print("Considering: " + str(pos))
                        val = temp_df.iloc[pos]['profile']
                        self.distance_vector.append(val)

                else:
                    a,b,c = self.mean_confidence_interval(self.distance_vector)
                    val = temp_df.iloc[pos]['profile']


                    if (val < c):
                        pass

                    else:
                        res = val-a

                        if (self.anomalyScore < res):
                            self.anomalyScore = res

                    self.distance_vector.append(val)

            #return (self.anomalyScore, )


        if self.anomalyScore == None:
            return(0, )

        else:

            if self.anomalyScore > 0:
                #print(self.anomalyScore)
                self.old_scores.append(self.anomalyScore)
                #print("normalized value: " +  str(self.anomalyScore / np.max(self.old_scores) ))
                self.anomalyScore = self.anomalyScore / np.max(self.old_scores)

                return(self.anomalyScore, )

            else:

                return(self.anomalyScore, )
        #return(self.anomalyScore, )


        print("SHOULD NOT GET HERE!!!!")



    def evaluate_anom2(self,inputData):


        self.anomalyScore = 0;


        if (len(self.dataset.index) > self.start_evaluation):

            ## get values
            a = self.dataset.values.squeeze()



            ## Calculate scrimp
            results = matrixProfile.scrimp_plus_plus(a,self.window_size)


            #self.slopes = []
            #prev = None
            #for val in results:
            #    if (not self.slopes):
            #        self.slopes.append(0)
            #        prev = val
            #    else:
            #        slope = val - prev
            #        prev = val
            #        self.slopes.append(slope)

            temp_df = self.dataset.copy()
            temp_df['profile'] = np.append(results[0],np.zeros(self.window_size-1)+np.nan)
            temp_df['profile_index'] = np.append(results[1], np.zeros(self.window_size - 1) + np.nan)



            # we look for the 5 events specified in the data explaination
            found_anoms = discords(temp_df['profile'], self.ex_zone, k=self.n_Discords_extract)

            if((self.maxdist == None) and self.min_dist_on):
                self.maxdist = temp_df.iloc[found_anoms[0]]['profile']

                print("Minimum Distance Found:")
                print(self.maxdist)

            else:
                pass

            ts = pd.to_datetime(inputData['timestamp'], format="%Y-%m-%d %H:%M:%S")


            filtered_anoms = filter(lambda x : x != sys.maxsize, found_anoms)
            filtered_anoms = np.unique(filtered_anoms)

            final_anoms = []
            final_dist = []




            if(self.min_dist_on):
                ### FIlter anomalies based on minimum distance required
                for anom in filtered_anoms:

                    if(temp_df['profile'].get(anom) > self.maxdist):
                        final_anoms.append(anom)

                filtered_anoms = final_anoms


            #####
            ##### IMPLEMENT LOG LIKELIHOOD OF THE DISTANCES
            for pos in filtered_anoms:
                prev = temp_df.iloc[pos-1]['profile']
                val = temp_df.iloc[pos]['profile']


                slope = val-prev

                if (not(self.slopes) or (len(self.slopes)<3)):
                    self.slopes.append(slope)

                else:

                    a,b,c = self.mean_confidence_interval(self.slopes)
                    self.slopes.append(slope)

                    if ((slope > c) or (slope < b)):
                        if (slope/np.max(slope) > self.anomalyScore):
                            self.anomalyScore = slope/np.max(slope)




        if(self.anomalyScore > 0):
            print(inputData['timestamp'])
            print(self.anomalyScore)

        return (self.anomalyScore, )





    def handleRecord(self, inputData):


        self.maintain_dataset(inputData);

        # print(self.motif_list)
        # print(self.dataset.size)
        #print(inputData['timestamp'])

        if (self.probabilistic_version == 1):
            return self.evaluate_anom1(inputData);

        if (self.probabilistic_version == 2):
            return self.evaluate_anom2(inputData);

        else:
            return self.evaluate_anom(inputData);
