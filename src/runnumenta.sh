#!/bin/bash



cd ../numenta_discontinued/NAB-master


##### No space between anything otherwise it wont work
variable_start=16
variable_step=1
variable_end=25



#touch './todel.txt'

#while [ $(bc<<<"$variable_start < $variable_end") -eq 1 ]
#do
  rm exp_settings.txt
  touch exp_settings.txt

  echo "[my-config]" > exp_settings.txt

  echo "dataset_size_to_keep=20" >> exp_settings.txt
  #echo "dataset_size_to_keep=${variable_start}" >> exp_settings.txt
  echo "window_size=2" >> exp_settings.txt


  #echo "dataset_size_to_keep =  8*window_size" >> exp_settings.txt

  echo "probabilistic_version = 0" >> exp_settings.txt

  echo "discord_sim_Threshold = 0.96" >> exp_settings.txt

  echo "fourier_on=1" >> exp_settings.txt
  echo "min_dist_on=0" >> exp_settings.txt

  echo "start_evaluation = dataset_size_to_keep - 1" >> exp_settings.txt
  echo "decay_rate = 1" >> exp_settings.txt
  echo "ttl = 48" >> exp_settings.txt
  echo "n_Discords_extract = 3" >> exp_settings.txt
  echo "n_Discords_keep = 207" >> exp_settings.txt
  echo "ex_zone = window_size/4" >> exp_settings.txt


  #### For Motifs
  echo "n_Motifs_keep = 1000" >> exp_settings.txt
  echo "motif_ttl = 1000" >> exp_settings.txt
  echo "motif_sim_Threshold = 0.95" >> exp_settings.txt
  echo "motif_ex_zone = math.floor(window_size/2)" >> exp_settings.txt


  #-m pdb
  python run_mine.py -d my --numCPUs 1 --windowsFile labels/combined_windows_tiny_machine.json # >> './todel.txt'

  cd results/my/

  #echo "matrixbegin" #  >> '1../../prob_test_declives.txt'
  #cat my_standard_scores.csv  # >> '../../prob_test_declives.txt'
  #echo "matrixend" # >> '../../prob_test_declives.txt'

  #cd ../../../../src

  cd ../../

  sleep 2
  #python calconfusionmatrix.py  >> './results_four099.txt'


  # python dataset_plot_afterdetect.py -i ../numenta_discontinued/NAB-master/data/realKnownCause/nyc_taxi.csv -o ./output -d my

  ## Bc needed for floating point operations in bash
  variable_start=$( echo "$variable_start + $variable_step" | bc )

  # echo $variable_start

    #####
    ##### EXAMPLE COMMANDS TO RETRIEVE THE RESULTS
    #####
    #cat final_095_4x.txt | grep "Final score for 'my' detector on 'standard' profile"
    #grep 'my,standard' ./final_095_4x.txt
#done
