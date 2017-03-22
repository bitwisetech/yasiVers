# Gnuplot script file for "outpData.txt"
 # This file is based on tplt3arg.p
 set   autoscale                        # scale axes automatically
 unset log                              # remove any log-scaling
 unset label                            # remove any previous labels
 #
  set term qt size 480, 320
 # set term wxt size 240, 200
 # set term wxt size 380, 150
 # set term wxt size 500, 180
 set xtic auto                          # set xtics automatically
 set ytic auto                          # set ytics automatically
 set  grid xtics ytics
 show grid
 set title "compVers.py J3Cub All Versions : 180kTAS at 2000ft" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag', \
#      "outpData.txt" every ::155::210 using 1:4 with lines title 'LD'
plot"J3Cub-datvOrig.txt" every 4::2        using 1:4 with line title 'LvsD vOrig', \
    "J3Cub-datv32.txt" every 4::2        using 1:4 with impulses title 'LvsD v32', \
    "J3Cub-datvCurr.txt" every 4::2        using 1:4 with points title 'LvsD vCurr', \
    "J3Cub-datv2017-2.txt" every 4::2        using 1:4 with linespoints title 'LvsD v2017-2', \