reset
set terminal jpeg
set output "redispipeline.jpg"
set style fill solid 1.00 border 0
set style histogram
set style data histogram
set xtics rotate by -45
set grid ytics linestyle 1
set yrange [0:12500]
set xlabel "Approach" font "bold"
set ylabel "Rate (/s)" font "bold"
plot "redispipeline.dat" using 2:xtic(1) ti "Redis Transfers (/s)" linecolor rgb "#000033"
