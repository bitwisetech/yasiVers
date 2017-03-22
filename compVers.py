#!/usr/bin/env python
#
## compVers.py tix menu driven yasim version explorer with gnuplot displays
#    takes a given yasim config file, runs cmdline yasim with different versions specified
#    gnuplots are yasim version's Lift, Drag, Lift vs Drag in separate plots  
import getopt, os, shlex, subprocess, sys, Tix
import Tkinter as tk
from collections import OrderedDict 
# default yasim config under test
def normArgs(argv):
  global ycIpFid
  ycIpFid   = 'yasimCfg.xml'
  global ycIpNam
  ycIpNam = ycIpFid.find('.xml')
  ycIpNam = ycIpFid[0:ycIpNam]
  global ycOpFid
  ycOpFid   = 'ytixOutp.xml'
  global yDatFid
  yDatFid   = "ytixData.txt"
  # template gnuplot spec files for 2, 3 variables plot
  global spc2Fid
  spc2Fid   = '2argTplt.p'
  global spc3Fid
  spc3Fid   = '3argTplt.p'
  global tpltFid
  tpltFid   = 'compTplt.p'
  global vbl2Fid
  vbl2Fid   = '2argSpec.p'
  global vbl3Fid
  vbl3Fid   = '3argSpec.p'
  global allvLiftFid
  allvLiftFid  = 'allvLift.p'
  global allvDragFid
  allvDragFid  = 'allvDrag.p'
  global allvLvsDFid
  allvLvsDFid = 'allvLvsD.p'
  # get yasim config FileID from args
  try:
    opts, args = getopt.getopt(argv, "f:", "file=")
  except getopt.GetoptError:
     print 'sorry, I need -f or file= yasim config  fileID '
     sys.exit(2)
    #
  for opt, arg in opts:
    if   opt in ("-f", "--file"):
      ycIpFid = arg
      ycIpNam = ycIpFid.find('.xml')
      ycIpNam = ycIpFid[0:ycIpNam]

##
# Scan template yasim cfig and extract numeric elements, copy for tix menu
#
def vblsFromTplt():
  global ycIpFid, ycIpNam, ycOpFid, yDatFid
  global spc2Fid, spc3Fid, vbl2Fid, vbl3Fid
  global Va, Aa, Ka, Ra, Fa                                    # Approach  parms
  global Vc, Hc, Kc, Rc                                        # Cruise    parms 
  global Cw, Iw, Aw, Ww, Pw, Lw, Dw, Lr, Dr                    # Wing/Ailr parms
  global Ch, Ih, Ah, Wh, Ph, Lh, Dh                            # Hstab     parms
  global Cv, Iv, Av, Wv, Pv, Lv, Dv                            # Vstab     parms 
  global Sp, Rp, Ap, Pp, Wp, Mp                                # Prop      parms 
  global Hy, Vy                                                # Solver    parms
#
  # extracted text fields for saved parameter values 
  global textVa, textAa, textKa, textRa, textFa
  global textVc, textHc, textKc,  textRc
  global textCw, textIw, textAw,  textWw, textPw, textLw, textDw, textLr, textDr  
  global textCh, textIh, textAh,  textWh, textPh, textLh, textDh
  global textCv, textIv, textAv,  textWv, textPv, textLv, textDv
  global txtZa,  txtZZa, txtZZZa, txtZc,  txtZZc
  global txtZw,  txtZZw, txtZZZw, txtZh,  txtZZh, txtZZZh
  global txtZv,  txtZZv, txtZZZv, txtZZp, txtZZZp
  global txtZr,  txtSp,  txtRp,   txtZp,  txtAp,  txtPp, txtWp, txtMp
#  
  # flags indicate parsing has detected various sections of yasim config 
  apprFlag   = 0
  cruzFlag   = 0
  wingFlag   = 0
  hstabFlag  = 0
  vstabFlag  = 0
  propFlag   = 0
#
  Vy = 180
  Hy = 2000
  Va = Aa = Ka = Ra = Fa = Vc = Hc = Kc = Rc = 0
  Cw = Iw = Aw = Ww = Pw = Lw = Dw = Lr = Dr = 0
  Ch = Ih = Ah = Wh = Ph = Lh = Dh = Cv = Iv = Av = Wv = Pv = Lv = Dv = 0
  Sp = Rp = Ap = Rp = Wp = Mp = 0
#
  ## # open auto yasim config file
  ## ycOpHndl  = open(ycOpFid, 'w', 0)
  # Phase 1 open base yasim config file and parse elements
  with open(ycIpFid, 'r') as ycIpHndl:
  # step each line in template yasim config file
    for line in ycIpHndl:
      # flag on appr section
      if '<approach' in line:
        apprFlag = 1
      if '</approach' in line:
        apprFlag = 0
      # flag on cruise section
      if '<cruise' in line:
        cruzFlag = 1
      if '</cruise' in line:
        cruzFlag = 0
      # flag on wing section
      if '<wing' in line:
        wingFlag = 1
      if '</wing' in line:
        wingFlag = 0
      # flag on hstab section
      if '<hstab' in line:
        hstabFlag = 1
      if '</hstab' in line:
        hstabFlag = 0
      if '<vstab' in line:
        vstabFlag = 1
      if '</vstab' in line:
        vstabFlag = 0
      ### appr section parse approach speed and AoA elements
      if (apprFlag == 1):
        #in appr section, find elements
        if ('approach speed' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textVa = line[0:(sepsList[0]+1)]
          Va     = float ( (line[(sepsList[0]+1):(sepsList[1])]))
          textAa = line[(sepsList[1]):(sepsList[2]+1)]
          Aa     = float(line[(sepsList[2]+1):(sepsList[3])])
          textKa = line[(sepsList[3]):(sepsList[4]+1)]
          Ka     = float(line[(sepsList[4]+1):(sepsList[5])])
          txtZa  = line[(sepsList[5]):]
          line   = textVa + str(Va) + textAa + str(Aa) + textKa + str(Ka)   \
                 + txtZa
        if ('throttle' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textRa = line[0:(sepsList[2]+1)]
          Ra     = float ( (line[(sepsList[2]+1):(sepsList[3])]))
          txtZZa = line[(sepsList[3]):]
          line   = textRa + str(Ra) + txtZZa
        if ('flaps' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textFa  = line[0:(sepsList[2]+1)]
          Fa      = float ( (line[(sepsList[2]+1):(sepsList[3])]))
          txtZZZa = line[(sepsList[3]):]
          line    = textFa + str(Fa) + txtZZZa
        ###
      ### cruise section parse cruise speed element
      if (cruzFlag == 1):
        #in cruise section, find element
        if ('cruise speed' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textVc = line[0:(sepsList[0]+1)]
          Vc     = float ( (line[(sepsList[0]+1):(sepsList[1])]))
          textHc = line[(sepsList[1]):(sepsList[2]+1)]
          Hc     = float ( (line[(sepsList[2]+1):(sepsList[3])]))
          textKc = line[(sepsList[3]):(sepsList[4]+1)]
          Kc     = float ( (line[(sepsList[4]+1):(sepsList[5])]))
          txtZc  = line[(sepsList[5]):]
          line   = textVc + str(Vc) + textHc + str(Hc) + textKc + str(Kc)   \
                 + txtZc
        if ('throttle' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textRc = line[0:(sepsList[2]+1)]
          Rc     = float ( (line[(sepsList[2]+1):(sepsList[3])]))
          txtZZc = line[(sepsList[3]):]
          line   = textRc + str(Rc) + txtZZc
        ###
      ### wing section parse camber and induced drag elements
      # Be Sure length, chord ... camber, idrag elements are on a single line
      if (wingFlag == 1):
        #in wing section, find elements
        if ('camber' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textCw = line[0:(sepsList[8]+1)]
          Cw     = float ( (line[(sepsList[8]+1):(sepsList[9])]))
          textIw = line[(sepsList[9]):(sepsList[10]+1)]
          Iw     = float(line[(sepsList[10]+1):(sepsList[11])])
          txtZw  = line[(sepsList[11]):]
          # overwrite line with substituted elements
          line   = textCw + str(Cw) + textIw + str(Iw) + txtZw
        ###
        #in wing section, find stall elements
        if ('stall' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textAw = line[0:(sepsList[0]+1)]
          Aw     = float ( (line[(sepsList[0]+1):(sepsList[1])]))
          textWw = line[(sepsList[1]):(sepsList[2]+1)]
          Ww     = float(line[(sepsList[2]+1):(sepsList[3])])
          textPw = line[(sepsList[3]):(sepsList[4]+1)]
          Pw     = float(line[(sepsList[4]+1):(sepsList[5])])
          txtZZw = line[(sepsList[5]):]
          line   = textAw + str(Aw) + textWw + str(Ww) + textPw + str(Pw)  \
                 + txtZZw
        ###
        #in wing section, find flap0 elements
        if ('flap0' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textLw = line[0:(sepsList[4]+1)]
          Lw     = float ( (line[(sepsList[4]+1):(sepsList[5])]))
          textDw = line[(sepsList[5]):(sepsList[6]+1)]
          Dw     = float( line[(sepsList[6]+1):(sepsList[7])])
          txtZZZw = line[(sepsList[7]):]
          line    = textLw + str(Lw) + textDw + str(Dw) + txtZZZw
        if ('flap1' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textLr = line[0:(sepsList[4]+1)]
          Lr     = float ( (line[(sepsList[4]+1):(sepsList[5])]))
          textDr = line[(sepsList[5]):(sepsList[6]+1)]
          Dr     = float( line[(sepsList[6]+1):(sepsList[7])])
          txtZr  = line[(sepsList[7]):]
          line    = textLr + str(Lr) + textDr + str(Dr) + txtZr
      ### hstab section parse camber, idrag, stall and flap0 elements
      if (hstabFlag == 1):
        ### hstab section parse camber and induced drag elements if present
        #    If camber element is present then idrag dflt 1 must be present
        # Be Sure length,chord...camber, idrag are in order on a single line
        if ('camber' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textCh = line[0:(sepsList[8]+1)]
          Ch     = float ( (line[(sepsList[8]+1):(sepsList[9])]))
          textIh = line[(sepsList[9]):(sepsList[10]+1)]
          Ih     = float(line[(sepsList[10]+1):(sepsList[11])])
          txtZh  = line[(sepsList[11]):]
          # overwrite line with substituted elements
          line   = textCh + str(Ch) + textIh + str(Ih) + txtZh
        else:
          # camber is not specified so deflt values to satisfy menu
          Ch = 0
          Ih = 1
        #in hstab section, find stall elements
        if ('stall' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textAh = line[0:(sepsList[0]+1)]
          Ah     = float ( (line[(sepsList[0]+1):(sepsList[1])]))
          textWh = line[(sepsList[1]):(sepsList[2]+1)]
          Wh     = float(line[(sepsList[2]+1):(sepsList[3])])
          textPh = line[(sepsList[3]):(sepsList[4]+1)]
          Ph     = float(line[(sepsList[4]+1):(sepsList[5])])
          txtZZh = line[(sepsList[5]):]
          line   = textAh + str(Ah) + textWh + str(Wh) + textPh + str(Ph)    \
                 + txtZZh
        #in hstab section, find flap0 elements
        if ('flap0' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textLh = line[0:(sepsList[4]+1)]
          Lh     = float ( (line[(sepsList[4]+1):(sepsList[5])]))
          textDh = line[(sepsList[5]):(sepsList[6]+1)]
          Dh     = float( line[(sepsList[6]+1):(sepsList[7])])
          txtZZZh = line[(sepsList[7]):]
          line   = textLh + str( Lh) + textDh + str(Dh) + txtZZZh
      ### vstab section parse camber, idrag, stall and flap0 elements
      if (vstabFlag == 1):
        ### vstab section parse camber and induced drag elements if present
        #    If camber element is present then idrag dflt 1 must be present
        # Be Sure length,chord...camber, idrag are in order on a single line
        if ('camber' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textCv = line[0:(sepsList[8]+1)]
          Cv     = float ( (line[(sepsList[8]+1):(sepsList[9])]))
          textIv = line[(sepsList[9]):(sepsList[10]+1)]
          Iv     = float(line[(sepsList[10]+1):(sepsList[11])])
          txtZv  = line[(sepsList[11]):]
          # overwrite line with substituted elements
          line   = textCv + str(Cv) + textIv + str(Iv) + txtZv
        else:
          # camber is not specified so deflt values to satisfy menu
          Cv = 0
          Iv = 1
        #in vstab section, find stall elements
        if ('stall' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textAv = line[0:(sepsList[0]+1)]
          Av     = float ( (line[(sepsList[0]+1):(sepsList[1])]))
          textWv = line[(sepsList[1]):(sepsList[2]+1)]
          Wv     = float(line[(sepsList[2]+1):(sepsList[3])])
          textPv = line[(sepsList[3]):(sepsList[4]+1)]
          Ph     = float(line[(sepsList[4]+1):(sepsList[5])])
          txtZZv  = line[(sepsList[5]):]
          line   = textAv + str(Av) + textWv + str(Wv) + textPv + str(Pv)    \
                 + txtZZv
        #in vstab section, find flap0 elements
        if ('flap0' in line):
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          textLv = line[0:(sepsList[4]+1)]
          Lv     = float ( (line[(sepsList[4]+1):(sepsList[5])]))
          textDv = line[(sepsList[5]):(sepsList[6]+1)]
          Dv     = float( line[(sepsList[6]+1):(sepsList[7])])
          txtZZZv = line[(sepsList[7]):]
          line   = textLv + str( Lv) + textDv + str(Dv) + txtZZZv
  #close and sync file
    ycIpHndl.flush
    os.fsync(ycIpHndl.fileno())
  ycIpHndl.close
##
# After tix menu changes, create temp yasim config file with new elements
#
def autoFromVbls():
  global ycIpFid, ycIpNam, ycOpFid, yDatFid
  global spc2Fid, spc3Fid, vbl2Fid, vbl3Fid
  global Va, Aa, Ka, Ra, Fa                                    # Approach  parms
  global Vc, Hc, Kc, Rc                                        # Cruise    parms 
  global Cw, Iw, Aw, Ww, Pw, Lw, Dw, Lr, Dr                    # Wing/Ailr parms
  global Ch, Ih, Ah, Wh, Ph, Lh, Dh                            # Hstab     parms
  global Cv, Iv, Av, Wv, Pv, Lv, Dv                            # Vstab     parms 
  global Sp, Rp, Ap, Pp, Wp, Mp                                # Prop      parms 
  global Hy, Vy                                                # Solver    parms
#
  # extracted text fields for saved parameter values 
  global textVa, textAa, textKa, textRa, textFa
  global textVc, textHc, textKc,  textRc
  global textCw, textIw, textAw,  textWw, textPw, textLw, textDw, textLr, textDr  
  global textCh, textIh, textAh,  textWh, textPh, textLh, textDh
  global textCv, textIv, textAv,  textWv, textPv, textLv, textDv
  global txtZa,  txtZZa, txtZZZa, txtZc,  txtZZc
  global txtZw,  txtZZw, txtZZZw, txtZh,  txtZZh, txtZZZh
  global txtZv,  txtZZv, txtZZZv, txtZZp, txtZZZp
  global txtZr,  txtSp,  txtRp,   txtZp,  txtAp,  txtPp, txtWp, txtMp
#
  apprFlag   = 0
  cruzFlag   = 0
  wingFlag   = 0
  hstabFlag  = 0
  vstabFlag  = 0
  ycOpFid  = ycIpNam + '-tix.xml'
  yDatFid  = ycIpNam + '-tix.txt'
  ## # open auto yasim config file
  ycOpHndl  = open(ycOpFid, 'w', 0)
  # Phase 3 write auto file via yconfig template and subsVbls from Tix
  with open(ycIpFid, 'r') as ycIpHndl:
  # step each line in template yasim config file
    for line in ycIpHndl:
      # flag on appr section
      if '<approach' in line:
        apprFlag = 1
      if '</approach' in line:
        apprFlag = 0
      # flag on cruise section
      if '<cruise' in line:
        cruzFlag = 1
      if '</cruise' in line:
        cruzFlag = 0
      # flag on wing section
      if '<wing' in line:
        wingFlag = 1
      if '</wing' in line:
        wingFlag = 0
      # flag on hstab section
      if '<hstab' in line:
        hstabFlag = 1
      if '</hstab' in line:
        hstabFlag = 0
      if '<vstab' in line:
        vstabFlag = 1
      if '</vstab' in line:
        vstabFlag = 0
      ### in each section write saved text fields and updated element values
      if (apprFlag == 1):
        if ('approach speed' in line):
          line   = textVa + str(Va) + textAa + str(Aa) + textKa + str(Ka)   \
                 + txtZa
        if ('throttle' in line):
          line   = textRa + str(Ra) + txtZZa
        if ('flaps' in line):
          line    = textFa + str(Fa) + txtZZZa
      if (cruzFlag == 1):
        if ('cruise speed' in line):
          line   = textVc + str(Vc) + textHc + str(Hc) + textKc + str(Kc)   \
                 + txtZc
        if ('throttle' in line):
          line   = textRc + str(Rc) + txtZZc
      if (wingFlag == 1):
        if ('camber' in line):
          line   = textCw + str(Cw) + textIw + str(Iw) + txtZw
        if ('stall' in line):
          line   = textAw + str(Aw) + textWw + str(Ww) + textPw + str(Pw)  \
                 + txtZZw
        if ('flap0' in line):
          line    = textLw + str(Lw) + textDw + str(Dw) + txtZZZw
        if ('flap1' in line):
          line    = textLr + str(Lr) + textDr + str(Dr) + txtZr
      if (hstabFlag == 1):
        if ('camber' in line):
          line   = textCh + str(Ch) + textIh + str(Ih) + txtZh
        if ('stall' in line):
          line   = textAh + str(Ah) + textWh + str(Wh) + textPh + str(Ph)    \
                 + txtZZh
        if ('flap0' in line):
          line   = textLh + str( Lh) + textDh + str(Dh) + txtZZZh
      if (vstabFlag == 1):
        if ('camber' in line):
          line   = textCv + str(Cv) + textIv + str(Iv) + txtZv
        if ('stall' in line):
          line   = textAv + str(Av) + textWv + str(Wv) + textPv + str(Pv)    \
                 + txtZZv
        if ('flap0' in line):
          line   = textLv + str( Lv) + textDv + str(Dv) + txtZZZv
      # Write unchanged/modified line into auto.xml
      ycOpHndl.write(line)
    #close and sync files
    ycOpHndl.flush
    os.fsync(ycOpHndl.fileno())
    ycOpHndl.close
    ycIpHndl.flush
    os.fsync(ycIpHndl.fileno())
  ycIpHndl.close

##
# Call yasim data and gnuplot with auto-created config and plot spec files
def callPlot():
  global ycIpFid, ycIpNam, ycOpFid, yDatFid
  global spc2Fid, spc3Fid, vbl2Fid, vbl3Fid
  global allvLiftFid, allvDragFid, allvLvsDFid
  global Va, Aa, Ka, Ra, Fa                                    # Approach  parms
  global Vc, Hc, Kc, Rc                                        # Cruise    parms 
  global Cw, Iw, Aw, Ww, Pw, Lw, Dw, Lr, Dr                    # Wing/Ailr parms
  global Ch, Ih, Ah, Wh, Ph, Lh, Dh                            # Hstab     parms
  global Cv, Iv, Av, Wv, Pv, Lv, Dv                            # Vstab     parms 
  global Sp, Rp, Ap, Pp, Wp, Mp                                # Prop      parms 
  global Hy, Vy                                                # Solver    parms
#
  # extracted text fields for saved parameter values 
  global textVa, textAa, textKa, textRa, textFa
  global textVc, textHc, textKc,  textRc
  global textCw, textIw, textAw,  textWw, textPw, textLw, textDw, textLr, textDr  
  global textCh, textIh, textAh,  textWh, textPh, textLh, textDh
  global textCv, textIv, textAv,  textWv, textPv, textLv, textDv
  global txtZa,  txtZZa, txtZZZa, txtZc,  txtZZc
  global txtZw,  txtZZw, txtZZZw, txtZh,  txtZZh, txtZZZh
  global txtZv,  txtZZv, txtZZZv, txtZZp, txtZZZp
  global txtZr,  txtSp,  txtRp,   txtZp,  txtAp,  txtPp, txtWp, txtMp
#
  # dictinary of versions in Yasim configuration strings Be Sure vOrig Is First 
  versDict =             OrderedDict([ ('YASIM_VERSION_ORIGINAL', 'vOrig'), \
                                      ('YASIM_VERSION_32', 'v32'),         \
                                      ('YASIM_VERSION_CURRENT', 'vCurr'),  \
                                      ('2017.2',                'v2017-2') ])
  #create common annotation test parsed / menu-altered values
  commNota = ' set title "' + ycIpNam + 'All Versions Parms:\\nAp:' + str(Va) \
    + ' ' + str(Aa) + ' ' + str(Ka) + ' ' + str(Ra) + ' ' + str(Fa) +'\\n'    \
    + ' Cr:'  + str(Vc) + ' ' + str(Hc) + ' ' + str(Kc) + ' '                 \
    + str(Rc) + '\\nWi:' + str(Cw) + ' ' + str(Iw) + ' ' + str(Aw)            \
    + ' ' + str(Ww) + ' ' + str(Pw) + ' ' + str(Lw) + ' ' + str(Dw)           \
    + ' ' + str(Lr) + ' ' + str(Dr)                                           \
    + '\\nHs:' + str(Ch) + ' ' + str(Ih) + ' ' + str(Ah)                      \
    + ' ' + str(Wh) + ' ' + str(Ph) + ' '   + str(Lh) + ' ' + str(Dh)         \
    + '\\nVs:' + str(Cv) + ' ' + str(Iv) + ' ' + str(Av)                      \
    + ' ' + str(Wv) + ' ' + str(Pv) + ' '   + str(Lv) + ' ' + str(Dv)         \
    + 'Ys:'+ str(Vy) + ' ' + str(Hy) + '" \n'
  # uncomment line below to supress parms legend
  commNota = ' set title "compVers.py ' + ycIpNam + ' All Versions : ' + Vy + 'kTAS at ' + Hy + 'ft" \n'
  #setup write handles for three separate gnuplot spec files     
  liftHndl  = open(allvLiftFid, 'w', 0)
  dragHndl  = open(allvDragFid, 'w', 0)
  lvsdHndl  = open(allvLvsDFid, 'w', 0)
  # partially create gnuplot config files up until plot specifications 
  # use comp template 
  with open(tpltFid, 'r') as tplt:
    plotFlag = 0
    for line in tplt:
      # set flag near end when 'plot' string is found
      if (' plot ' in line ): plotFlag = 1
      # find the title line in template config
      if ('set title' in line ):
        #create title using parsed / substituted values
        line = commNota
      if ( plotFlag < 1):
        # Write line into each gnuplot template
        liftHndl.write(line)
        dragHndl.write(line)
        lvsdHndl.write(line)
  # flag to indicate first entry in dict 
  versIter = 0 
  ## Iterate dictionary; for each version create yasim.xml file and gnuplot line specs 
  for versKywd in versDict.keys():
    versSfix = versDict[versKywd]
    vcfgFid  = ycIpNam + versSfix + '.xml'
    vdatFid  = ycIpNam +  '-dat' + versSfix + '.txt'
    ##
    ## # open auto yasim config file
    vcfgHndl  = open(vcfgFid, 'w', 0)
    # Phase 3 write auto file via yconfig template and subsVbls from Tix
    with open(ycIpFid, 'r') as ycIpHndl:
    # step each line in template yasim config file
      for line in ycIpHndl:
        if '<airplane mass="' in line:
          # make an index list of double quotes in the line
          sepsList = []
          sepsChar = '"'
          lastIndx = 0
          while (lastIndx > -1):
            sepsIndx = line.find( sepsChar, (lastIndx +1))
            if (sepsIndx > 0) :
              sepsList.append(sepsIndx)
            lastIndx = sepsIndx
          # Use index list to split line into text and numbers
          lineMass = line[0:(sepsList[1]+1)]
          line = lineMass + ' version="' + versKywd + '">'
        # Write unchanged/modified line into auto.xml
        vcfgHndl.write(line)
      #close and sync files
      vcfgHndl.flush
      os.fsync(vcfgHndl.fileno())
      vcfgHndl.close
      ycIpHndl.flush
      os.fsync(ycIpHndl.fileno())
    ycIpHndl.close
    # resume gnuplot spec file 
    # At EOF of gnuplot specification file append plot lines version's data file name
    ## Iterate through each version in dictionary
    # 'plot' only at first filespec, set linestyle for visibility
    line = '    '  
    if ( versSfix == 'vOrig') :
      line = 'plot'
      styl = 'line'
    if ( versSfix == 'v32') :
      styl = 'impulses'
    if ( versSfix == 'vCurr') :
      styl = 'points'
    if ( versSfix == 'v2017-2') :
      styl = 'linespoints'
    line = line + '"' + vdatFid +'" every 6::2        using '            \
       + '1:2 with ' + styl + ' title \'Lift ' + versSfix + '\', \\\n'
    liftHndl.write(line)
    line = '    '  
    if ( versSfix == 'vOrig') :
      line = 'plot'
      styl = 'line'
    if ( versSfix == 'v32') :
      styl = 'impulses'
    if ( versSfix == 'vCurr') :
      styl = 'points'
    if ( versSfix == 'v2017-2') :
      styl = 'linespoints'
    line = line + '"' + vdatFid +'" every 6::2        using '            \
       + '1:3 with ' + styl + ' title \'Drag ' + versSfix + '\', \\\n'
    dragHndl.write(line)
    line = '    '  
    if ( versSfix == 'vOrig') :
      line = 'plot'
      styl = 'line'
    if ( versSfix == 'v32') :
      styl = 'impulses'
    if ( versSfix == 'vCurr') :
      styl = 'points'
    if ( versSfix == 'v2017-2') :
      styl = 'linespoints'
    line = line + '"' + vdatFid +'" every 6::2        using '            \
       + '1:4 with ' + styl + ' title \'LvsD ' + versSfix  + '\', \\\n'
    lvsdHndl.write(line)
    versIter += 1
    # run yasim external process to show console output
    command_line = 'yasim ' + vcfgFid + ' -a ' + str(Hy) + ' -s ' + str(Vy)
    args = shlex.split(command_line)
    p = subprocess.Popen(args)
    p.communicate()
    p.wait()
    #
    # run yasim external process for auto dataset, name used in .p spec
    yDatHndl = open(yDatFid, 'w')
    command_line = 'yasim ' + vcfgFid + ' -g -a ' + str(Hy) + ' -s ' + str(Vy)
    args = shlex.split(command_line)
    p = subprocess.Popen(args, stdout=yDatHndl)
    yDatHndl.close
    p.wait()
    #
    # run yasim external process for saved dataset file
    vDatHndl = open(vdatFid, 'w')
    command_line = 'yasim ' + vcfgFid + ' -g -a '+ str(Hy) + ' -s ' + str(Vy)
    args = shlex.split(command_line)
    p = subprocess.Popen(args, stdout=vDatHndl)
    vDatHndl.close
    p.wait()
    #
  #end step through version dictionary
  liftHndl.close
  dragHndl.close
  lvsdHndl.close
  tplt.close
  #
  ##
  # run gnuplot with all versions Lift command file to plot dataset
  command_line = "gnuplot -p " + allvLiftFid
  args = shlex.split(command_line)
  DEVNULL = open(os.devnull, 'wb')
  p = subprocess.Popen(args, stdout=DEVNULL, stderr=DEVNULL)
  p.communicate()
  DEVNULL.close()
  #
  # run gnuplot with all versions Drag command file to plot dataset
  command_line = "gnuplot -p " + allvDragFid
  args = shlex.split(command_line)
  DEVNULL = open(os.devnull, 'wb')
  p = subprocess.Popen(args, stdout=DEVNULL, stderr=DEVNULL)
  p.communicate()
  DEVNULL.close()
  #
  # run gnuplot with all versions LvsDD command file to plot dataset
  command_line = "gnuplot -p " + allvLvsDFid
  args = shlex.split(command_line)
  DEVNULL = open(os.devnull, 'wb')
  p = subprocess.Popen(args, stdout=DEVNULL, stderr=DEVNULL)
  p.communicate()
  DEVNULL.close()
#

##
# Tix Interface Menu #
##
class PropertyField:
  def __init__(self, parent, prop, label):
    self.prop = prop
    self.field = Tix.LabelEntry( parent, label=label,
       options='''
       label.width 12
       label.anchor e
       entry.width 12
       ''' )
    self.field.pack( side=Tix.TOP, padx=8, pady=2 )

  # Pull numeric vals from menu entries and store into variables
  def eval_field(self):
    global Va, Aa, Ka, Ra, Fa                                    # Approach  parms
    global Vc, Hc, Kc, Rc                                        # Cruise    parms 
    global Cw, Iw, Aw, Ww, Pw, Lw, Dw, Lr, Dr                    # Wing/Ailr parms
    global Ch, Ih, Ah, Wh, Ph, Lh, Dh                            # Hstab     parms
    global Cv, Iv, Av, Wv, Pv, Lv, Dv                            # Vstab     parms 
    global Sp, Rp, Ap, Pp, Wp, Mp                                # Prop      parms 
    global Hy, Vy                                                # Solver    parms
    #
    #
    val = self.field.entry.get()
    lbl = self.field.label.cget('text')
    self.prop = val
    if 'ApprSpd'    in lbl: Va = val
    if 'ApprAoA'    in lbl: Aa = val
    if 'ApprFuel'   in lbl: Ka = val
    if 'ApprThrt'   in lbl: Ra = val
    if 'ApprFlap'   in lbl: Fa = val
    if 'SolveAtSpd' in lbl: Vy = val
    if 'SolveAtAlt' in lbl: Hy = val
    if 'CruiseSpd'  in lbl: Vc = val
    if 'CruiseAlt'  in lbl: Hc = val
    if 'CruiseFuel' in lbl: Kc = val
    if 'CruiseThrt' in lbl: Rc = val
    if 'WingCambr'  in lbl: Cw = val
    if 'WingIDrag'  in lbl: Iw = val
    if 'WingStAoA'  in lbl: Aw = val
    if 'WingStWid'  in lbl: Ww = val
    if 'WingStlPk'  in lbl: Pw = val
    if 'WFlapLift'  in lbl: Lw = val
    if 'WFlapDrag'  in lbl: Dw = val
    if 'AilrnLift'  in lbl: Lr = val
    if 'AilrnDrag'  in lbl: Dr = val
    if 'HstbCambr'  in lbl: Ch = val
    if 'HstbIDrag'  in lbl: Ih = val
    if 'HstbStAoA'  in lbl: Ah = val
    if 'HstbStWid'  in lbl: Wh = val
    if 'HstbStlPk'  in lbl: Ph = val
    if 'HFlapLift'  in lbl: Lh = val
    if 'HFlapDrag'  in lbl: Dh = val
    if 'VstbCambr'  in lbl: Ch = val
    if 'VstbIDrag'  in lbl: Ih = val
    if 'VstbStAoA'  in lbl: Ah = val
    if 'VstbStWid'  in lbl: Wh = val
    if 'VstbStlPk'  in lbl: Ph = val
    if 'VFlapLift'  in lbl: Lh = val
    if 'VFlapDrag'  in lbl: Dh = val

  def update_field(self):
    val = self.prop
    self.field.entry.delete(0,'end')
    self.field.entry.insert(0, val)

class PropertyPage(Tix.Frame):
  def __init__(self,parent):
    Tix.Frame.__init__(self,parent)
    #self.fgfs = fgfs
    self.pack( side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1 )
    self.fields = []

  def addField(self, prop, label):
    f = PropertyField(self, prop, label)
    self.fields.append(f)

  def eval_fields(self):
    for f in self.fields:
      f.eval_field()

  def update_fields(self):
    for f in self.fields:
      #f.update_field(self.fgfs)
      f.update_field()
      Tix.Frame.update(self)

class ycTix(Tix.Frame):
  def __init__(self,root=None):
    Tix.Frame.__init__(self,root)
    z = root.winfo_toplevel()
    z.wm_protocol("WM_DELETE_WINDOW", lambda self=self: self.quitcmd())
    #self.fgfs = fgfs
    self.pack()
    self.pages = {}
    self.after_id = None
    self.createWidgets()
    self.update()

  def createWidgets(self):
    self.nb = Tix.NoteBook(self)
    self.nb.add( 'appr', label='APPR',
           raisecmd= lambda self=self: self.update_page() )
    self.nb.add( 'cruz', label='CRUISE',
           raisecmd= lambda self=self: self.update_page() )
    self.nb.add( 'wing', label='WING',
           raisecmd= lambda self=self: self.update_page() )
    self.nb.add( 'hstb', label='HSTAB',
           raisecmd= lambda self=self: self.update_page() )
    self.nb.add( 'vstb', label='VSTAB',
           raisecmd= lambda self=self: self.update_page() )
    #
    page = PropertyPage( self.nb.appr )
    self.pages['appr'] = page
    page.addField( Va,    'ApprSpd:')
    page.addField( Aa,    'ApprAoA:')
    page.addField( Ka,    'ApprFuel:')
    page.addField( Ra,    'ApprThrt:')
    page.addField( Fa,    'ApprFlap:')
    page.addField( Vy,  'SolveAtSpd:')
    page.addField( Hy,  'SolveAtAlt:')
    #
    page = PropertyPage( self.nb.cruz )
    self.pages['cruz'] = page
    page.addField( Vc,    'CruiseSpd:')
    page.addField( Hc,    'CruiseAlt:')
    page.addField( Kc,   'CruiseFuel:')
    page.addField( Rc,   'CruiseThrt:')
    #
    page = PropertyPage( self.nb.wing )
    self.pages['wing'] = page
    page.addField( Cw,    'WingCambr:')
    page.addField( Iw,    'WingIDrag:')
    page.addField( Aw,    'WingStAoA:')
    page.addField( Ww,    'WingStWid:')
    page.addField( Pw,    'WingStlPk:')
    page.addField( Lw,    'WFlapLift:')
    page.addField( Dw,    'WFlapDrag:')
    page.addField( Lr,    'AilrnLift:')
    page.addField( Dr,    'AilrnDrag:')
    #
    page = PropertyPage( self.nb.hstb )
    self.pages['hstb'] = page
    page.addField( Ch,    'HstbCambr:')
    page.addField( Ih,    'HstbIDrag:')
    page.addField( Ah,    'HstbStAoA:')
    page.addField( Wh,    'HstbStWid:')
    page.addField( Ph,    'HstbStlPk:')
    page.addField( Lh,    'HFlapLift:')
    page.addField( Dh,    'HFlapDrag:')
    #
    page = PropertyPage( self.nb.vstb )
    self.pages['vstb'] = page
    page.addField( Cv,    'VstbCambr:')
    page.addField( Iv,    'VstbIDrag:')
    page.addField( Av,    'VstbStAoA:')
    page.addField( Wv,    'VstbStWid:')
    page.addField( Pv,    'VstbStlPk:')
    page.addField( Lv,    'VFlapLift:')
    page.addField( Dv,    'VFlapDrag:')
    #
    self.nb.pack( expand=1, fill=Tix.BOTH, padx=5, pady=5, side=Tix.TOP )

    self.QUIT = Tix.Button(self)
    self.QUIT['text'] = 'Quit'
    self.QUIT['command'] = self.quitCmd
    self.QUIT.pack({"side": "right"})

    self.PLOT = Tix.Button(self)
    self.PLOT['text'] = 'Plot'
    self.PLOT['command'] = self.plotCmd
    self.PLOT.pack({"side": "left"})
  #
  def plotCmd(self):
    page = self.pages[ self.nb.raised() ]
    ##for k in self.pages.keys():
      ##p = self.pages[k]
      ##print ('p: ', p)
      ##p.eval_fields()
    page.eval_fields()
    autoFromVbls()
    callPlot()
  #
  def quitCmd(self):
    if self.after_id:
      self.after_cancel(self.after_id)
    self.quit()
    self.destroy()
  #
  def update_page(self):
    page = self.pages[ self.nb.raised() ]
    page.update_fields()
    self.update()
    ###self.after_id = self.after( 1000, lambda self=self: self.update_page() )
#
def main():
  normArgs(sys.argv[1:])
  root = Tix.Tk()
  vblsFromTplt()
  app = ycTix( root )
  app.mainloop()

if __name__ == '__main__':
  main()

##### ycTixPlot Ends
