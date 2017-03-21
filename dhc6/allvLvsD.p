# Gnuplot script file for "outpData.txt"
 # This file is based on tplt3arg.p
 set   autoscale                        # scale axes automatically
 unset log                              # remove any log-scaling
 unset label                            # remove any previous labels
 #
  set term qt size 360, 200
 # set term wxt size 240, 200
 # set term wxt size 380, 150
 # set term wxt size 500, 180
 set xtic auto                          # set xtics automatically
 set ytic auto                          # set ytics automatically
 set  grid xtics ytics
 show grid
 set title "dhc6All Versions Parms:\nAp:73.0 6.0 0.5 0.3 0.0\n Cr:176.0 10000.0 0.8 1.0\nWi:2.0 0.0 10.0 6.0 1.5 1.6 3.2 1.2 1.2\nHs:0 1 17.0 6.0 1.5 1.7 1.5\nVs:0 1 16.0 4.0 0 0.0 0.0Ys:80 15" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag', \
#      "outpData.txt" every ::155::210 using 1:4 with lines title 'LD'
plot"dhc6-datv2017-2.txt" every ::2        using 1:4 with lines title 'LvsD v2017-2', \
    "dhc6-datvOrig.txt" every ::2        using 1:4 with lines title 'LvsD vOrig', \
    "dhc6-datvCurr.txt" every ::2        using 1:4 with lines title 'LvsD vCurr', \
    "dhc6-datv32.txt" every ::2        using 1:4 with lines title 'LvsD v32', \
