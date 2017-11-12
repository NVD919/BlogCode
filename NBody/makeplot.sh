reset
set terminal gif animate delay 10 size 1000,100
set output "animate.gif"
stats 'data.txt' nooutput
set xrange [0:50]
set yrange [0:5]
set palette defined ( 1 "#B0B0B0", 3 "#FF0000")

unset colorbox

set format x ''
set format y ''
do for [i=1:int(STATS_blocks)] {
    plot 'data.txt' index (i-1) using 1:2:3 with points palette pt 7 ps 0.5 notitle
}
set output
quit

