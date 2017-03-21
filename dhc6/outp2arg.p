# Gnuplot script file for "outpData.txt"
 # This file is based on tplt2arg.p
 set   autoscale                        # scale axes automatically
 unset log                              # remove any log-scaling
 unset label                            # remove any previous labels
 # 
 set term qt size 360, 240
 # set term wxt size 240, 200
 # set term wxt size 380, 150
 # set term wxt size 500, 180
 set xtic auto                          # set xtics automatically
 set ytic auto                          # set ytics automatically
 set  grid xtics ytics
 show grid
 set title "dhc6v32\nAp:73.0 6.0 0.5 0.3 0.0\n Cr:176.0 10000.0 0.8 1.0\nWi:2.0 0.0 10.0 6.0 1.5 1.6 3.2 1.2 1.2\nHs:0 1 17.0 6.0 1.5 1.7 1.5\nVs:0 1 16.0 4.0 0 0.0 0.0Ys:100 20" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag'
 plot "dhc6-datv32.txt" every ::2        using 1:2 with lines title 'lift', \
      "dhc6-datv32.txt" every ::2        using 1:3 with lines title 'drag'