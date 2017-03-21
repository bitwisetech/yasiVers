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
 set title "cit2v32\nAp:86.0 15.0 0.2 0.3 1.0\n Cr:331.0 36000.0 0.87 1.0\nWi:2.5 -3.0 15.0 18.0 1.5 1.5 1.7 1.2 1.1\nHs:0 1 18.0 5.0 1.5 1.6 1.1\nVs:0 1 16.0 5.0 0 1.4 1.2Ys:100 5000" 
# set xlabel "AoA (Deg)"
# set ylabel "Force (G)"
#plot  "outpData.txt" every ::155::210 using 1:2 with lines title 'lift', \
#      "outpData.txt" every ::155::210 using 1:3 with lines title 'drag'
 plot "cit2-datv32.txt" every ::2        using 1:2 with lines title 'lift', \
      "cit2-datv32.txt" every ::2        using 1:3 with lines title 'drag'