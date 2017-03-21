# Gnuplot script file for "outpData.txt"
 # This file is based on tplt2arg.p
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
 set title "c310v32\nAp:70.0 16.0 1.0 0.4 1.0\n Cr:223.0 20000.0 1.0 1.0\nWi:0.8 0.1 16.0 4.0 1.5 1.5 1.2 1.3 1.2\nHs:0 1 16.0 4.0 1.5 1.68 1.2\nVs:0 1 16.0 4.0 0 1.3 1.2Ys:100 5000" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag'
 plot "c310-datv32.txt" every ::2        using 1:2 with lines title 'lift', \
      "c310-datv32.txt" every ::2        using 1:3 with lines title 'drag'