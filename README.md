  cd/theDownloadedDir;  python yasiVers.py -f c310.xml  ( aadjust as desired, press 'Plot' ) 

yasiVers.py  is a utility to automatically create gnuplot displays from FlightGear Yasim
  configuration files. Lift, Drag, L/D plots are created using different Yasim 'Version' 
  specifications so that the effect of version changes in the FDM can be inspected. 
 A menu interface allows for the various key Yasim parameters to be adjusted; such adjustments
are saved separately from the original yasim xml configuration file. 

 The python script depends on Tkinter being available for import and gnuplot should be installed.
 It's a work in process, it's likely the parser will throw errors depending on the line-bt-line 
 form of the input configuration file. 
 
