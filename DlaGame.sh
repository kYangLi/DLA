#!/bin/bash
#
# This bash script is the start program of DLA...

#**** Parameter List
declare -r kGnuPlotProfileName='plot_final_pattern.gnu'
declare -r kPlotPictureKind='png'
declare -r kWindowLength='1280'
set -a file_name_before


#**** Program Perpare **** 
## Read the file list into a array before program begin
ls_index=0
for file_name_before_element in $(ls)
do 
file_name_before[${ls_index}]=${file_name_before_element}
((ls_index++))
done

#**** Program Execution ****
./version-1.2.0.py

### PLOT METHOD I ###
### PLOT THE CHANGE DATA FILE ###
#**** Get the Date File Name Need to be Plot ****
echo '---------------- BASH EXECUTE ----------------'
echo '[bash]> Using GNUPLOT to plot the data file...'

## Compare the difference between the file list before and after the program's execution
new_file_name=''
for file_name_after_element in $(ls)
do
  is_new_data_file=true

  for file_name_before_element in ${file_name_before[@]}
  do
    ls_file_name_after_element=${file_name_after_element%%'['*}${file_name_after_element##*'['}
    ls_file_name_after_element=${ls_file_name_after_element%%']'*}
    ls_file_name_before_element=${file_name_before_element%%'['*}${file_name_before_element##*'['}
    ls_file_name_before_element=${ls_file_name_before_element%%']'*}

    if [[ ${ls_file_name_after_element} = ${ls_file_name_before_element} ]]
    then
      is_new_data_file=false
      break
    fi
  done

  if ${is_new_data_file} && [[ ${file_name_after_element} = *'X'*'-'*'-'*'-['*'periodic].dla'* ]]
  then  # if the file name is a new one and its name can be recognized as a data file one  
    new_file_name=${file_name_after_element}
    new_file_name=${new_file_name%'.'*}
    ls_new_file_name=${new_file_name%%'['*}'\'${new_file_name##*'-'}
    ls_new_file_name=${ls_new_file_name%%']'*}'\]' 

    for file_name_after_element in $(ls ${ls_new_file_name}*)
    do   
      if [[ ${file_name_after_element##*'.'} != ${kPlotPictureKind} ]]
      then # if the file's extension is not 'png'  
        continue
      fi
      # if the data file do not plot to a 'png' picture file 
      #   then the command here will never be executed
      is_new_data_file=false  
      break 
      
    done
    
    if ${is_new_data_file}
    then # if this data file has not been plot yet
      break
    fi
  fi
done

if [[ ${new_file_name} = '' ]]
then
  ### PLOT METHOD II ###
  ### PLOT ALL THE DATA FILE ###
  ./PlotAllDataFile.sh 
else
  #**** Plot Picture ****
  # Get the Canvas' size 
  canvas_size=${new_file_name%%'-'*}
  canvas_length=${canvas_size%%'X'*}
  canvas_width=${canvas_size##*'X'}
  ((window_width=kWindowLength*canvas_width/canvas_length))
  # Set the GNUPLOT profile
cat > ${kGnuPlotProfileName} << EOF
set term ${kPlotPictureKind} size ${kWindowLength},${window_width}
#set title "DlaPlot"
unset key
unset xtics
unset ytics
set output "${new_file_name}.png" 
plot "${new_file_name}.dlaplot" using 2:1 with points pt 9 ps 0.1 lc 'black'
EOF
  #plot picture with gnuplot
  gnuplot ${kGnuPlotProfileName}

  if [ -e  ${new_file_name}.png ]
    then
      echo '[bash]>'
      echo "[bash]> ${new_file_name}.png is created!"
      echo '[bash]>'
    else
      echo "[bash]> CREAT FAILED : ${new_file_name}.png"
      echo '[bash]> Make Sure you have already installed'
      echo '[bash]>   the GNUPLOT software...'
    fi

  echo '------------------ BASH END ------------------'
  echo ' '

  rm ${kGnuPlotProfileName}
fi
