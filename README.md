
yasiVers.py  is a utility to automatically create gnuplot displays from FlightGear Yasim
  configuration files. Lift, Drag, L/D plots are created using different Yasim 'Version' 
 specifications so that the effect of version changes in the FDM can be inspected. 
 A menu interface allows for the various key Yasim parameters to be adjusted; such adjustments
 are saved separately from the original yasim xml configuration file. 

The python script depends on Tkinter being available for import and gnuplot should be installed.
 It's a work in process, it's likely the parser will throw errors depending on the line-bt-line 
 form of the input configuration file: most likely the 'wing', 'hstab' and 'vstab' definitions
 will need to be unsplit into single long line definitions. 
 
compVers.py is useful for quickly checking version effects, separate gnuplots for Lift, Drag and LvsD
  are displayed with each plot depicting curves for different Yasim version strings.  

dspdVers.py Displays in addition to Lift, Drag, LiftVsDrag displays as in compVers.py a plot of 
  Drag vs Speed generated from Yasim command option '-d'. 
  
For both compVers.py and dspdVers.py the plotted line styles are chosen to highlight differences
  between Yasim versions: 
  YASIM_VERSION_ORIGINAL data are shown as solid Violet 'line' style 
  YASIM_VERSION_32       data are shown as green 'impulse' style, vertical strokes from Y=0 to datapoints
  YASIM_VERSION_CURRENT  data are shown as 'dot' style seen as asterisks, '*'
  2017.2                 data are shown as 'line-dot' style seen as amber line with small boxes
  
  Versions CURRENT and 2017.2 should match exactly sine 2017.2 is the current version. Any mismatch 
  between the vertical green strokes and amber lines is significant, indicating that the new, 2017.2
  version has a different solution from the previous version. Other deviations from the solid violet line
  highlight changes from Original due to versin 32 fixes. 
 
examples: 
  cd/theClonedDir/772E;  python ../yasiVers.py -f 772E.xml        ( adjust as desired, press 'Plot' ) 
  cd/theClonedDir/772E;  python ../compVers.py -f 772E.xml        ( adjust as desired, press 'Plot' ) 
  cd/theClonedDir/772E;  python ../dspdVers.py -f 772E.xml        ( adjust as desired, press 'Plot' ) 
  cd/theClonedDir/; mkdir MyNewModel; cp ../*Tplt.p .; copy pathTo/Aircraft/MyNewModel/yasimConfig.xml; 
                         python ../dspdVers.py -f yasimConfig.xml ( adjust as desired, press 'Plot' ) 
