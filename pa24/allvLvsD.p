# Gnuplot script file for "outpData.txt"
 # This file is based on tplt3arg.p
 set   autoscale                        # scale axes automatically
 unset log                              # remove any log-scaling
 unset label                            # remove any previous labels
 #
  set term qt size 360, 229
 # set term wxt size 240, 200
 # set term wxt size 380, 150
 # set term wxt size 500, 180
 set xtic auto                          # set xtics automatically
 set ytic auto                          # set ytics automatically
 set  grid xtics ytics
 show grid
 set title "dspdVers.py pa24 All Versions : 180kTAS at 2000ft" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag', \
#      "outpData.txt" every ::155::210 using 1:4 with lines title 'LD'
plot"pa24-vdat-vOrig.txt" every 4::2        using 1:4 with line title 'LvsD vOrig', \
    "pa24-vdat-vNone.txt" every 4::2        using 1:4 with line title 'LvsD vNone', \
    "pa24-vdat-v32.txt" every 4::2        using 1:4 with impulses title 'LvsD v32', \
    "pa24-vdat-v2017-2.txt" every 4::2        using 1:4 with linespoints title 'LvsD v2017-2', \
