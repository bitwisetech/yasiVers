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
 set title "dspdVers.py 752P All Versions : 180kTAS at 2000ft" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag', \
#      "outpData.txt" every ::155::210 using 1:4 with lines title 'LD'
plot"752P-vdat-vOrig.txt" every 4::2        using 1:3 with line title 'Drag vOrig', \
    "752P-vdat-vNone.txt" every 4::2        using 1:3 with line title 'Drag vNone', \
    "752P-vdat-v32.txt" every 4::2        using 1:3 with impulses title 'Drag v32', \
    "752P-vdat-v2017-2.txt" every 4::2        using 1:3 with linespoints title 'Drag v2017-2', \
