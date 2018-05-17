#!/bin/bash
#
# This bash script is a tool for plot all data file with GNUPLOT

declare -r kGnuPlotProfileName='plot_final_pattern.gnu'
declare -r kPlotPictureKind='png'
declare -r kWindowLength='1280'

#**** Plot and Save the Data Pattern ****
echo ' '
echo '-------------------- PLOT BEGIN --------------------'
echo '[bash]> Make Sure you have already installed' 
echo '[bash]>   the GNUPLOT software...'
echo '[bash]>'

plot_num=0
plot_failed_num=0
for plot_file_name in $(ls *'.dlaplot')
do
  plot_file_name=${plot_file_name%'.'*}

  canvas_size=${plot_file_name%%'-'*}
  canvas_length=${canvas_size%%'X'*}
  canvas_width=${canvas_size##*'X'}
  ((window_width=kWindowLength*canvas_width/canvas_length))

cat > ${kGnuPlotProfileName} << EOF
set term ${kPlotPictureKind} size ${kWindowLength},${window_width}
#set title "DlaPlot"
unset key
unset xtics
unset ytics
set output "${plot_file_name}.png" 
plot "${plot_file_name}.dlaplot" using 2:1 with points pt 9 ps 0.1 lc 'black'
EOF

  gnuplot ${kGnuPlotProfileName}
  if [ -e  ${plot_file_name}.png ]
  then
    echo "[bash]> CREATED: ${plot_file_name}.png"
    ((plot_num++))
  else
    echo "[bash]> CREAT FAILED : ${plot_file_name}.png"
    ((plot_failed_num++))
  fi
  
done
echo '[bash]>'
echo "[bash]> ${plot_num} Picture are Plot Successfully, ${plot_failed_num} Failed"
echo '------------------ PLOT FINISHED -------------------'
echo ' '

rm ${kGnuPlotProfileName}
echo '------------------ FILE LIST -------------------'
ls -1 *'X'*'-'*'-'*'-['*'periodic].'*
echo '--------------------- END ----------------------'
echo ' '
