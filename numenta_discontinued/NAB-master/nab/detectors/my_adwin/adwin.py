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


from pyadwin import Adwin as ad

#from outliers import smirnov_grubbs as grubbs



class MyadwinDetector(AnomalyDetector):


    #### Control variables
    dataset_size_to_keep = 24*(2/1)*60
    window_size= 24*2
    start_evaluation = 2*window_size

    #### OTHER Variables
    first = True
    dataset = None
    pointnumb = 0;
    adwin = ad()
    anomalyScore = None






    def handleRecord(self, inputData):

        if(self.pointnumb >= self.start_evaluation):
            if (self.adwin.update(inputData['value'])):
                self.anomalyScore = 1
            else:
                self.anomalyScore = 0

        else:
            self.adwin.update(inputData['value'])
            self.anomalyScore = 0


        self.pointnumb += 1
        if self.anomalyScore == 1:
            print("anomaly score is one...")
            print(inputData['timestamp'])

        ###Return detection result
        if self.anomalyScore == None:
            return (0, )
        else:
            return(self.anomalyScore, )
