# Gnuplot script file for "outpData.txt"
 # This file is based on tplt3arg.p
 set   autoscale                        # scale axes automatically
 unset log                              # remove any log-scaling
 unset label                            # remove any previous labels
 #
  set term qt size 400, 320
 # set term wxt size 240, 200
 # set term wxt size 380, 150
 # set term wxt size 500, 180
 set xtic auto                          # set xtics automatically
 set ytic auto                          # set ytics automatically
 set  grid xtics ytics
 show grid
 set title "compVers.py 772Z All Versions : 210kTAS at 10ft" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag', \
#      "outpData.txt" every ::155::210 using 1:4 with lines title 'LD'
plot"772Z-datv2017-2.txt" every ::2        using 1:2 with lines title 'Lift v2017-2', \
    "772Z-datvOrig.txt" every ::2        using 1:2 with lines title 'Lift vOrig', \
    "772Z-datvCurr.txt" every ::2        using 1:2 with lines title 'Lift vCurr', \
    "772Z-datv32.txt" every ::2        using 1:2 with lines title 'Lift v32', \
