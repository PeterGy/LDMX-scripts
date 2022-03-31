#a program that maps the testbeam channels to the sipms.
#so far untested, mapping will likely have to be tweaked

import sys
import ROOT
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TStyle, TTree, TH1D, TH2D, TLegend, TGraph, TGraphErrors
from ROOT import gROOT, gStyle, gSystem, gPad
ROOT.gROOT.SetBatch(1); 
gSystem.Load("libFramework.so")
inputFile=TFile(sys.argv[1], "read")

#converts the 'real' channel into a 3 vector that describes the SiPM really well
def realChannel_to_SipM(c):#[layer,bar,side]  
    if c == None: return None      
    for i in range(1,10):
        if 0 <= c and c <= 3: return [i,c,0]
        if 4 <= c and c <= 7: return [i,c-4,1]
        if 8 <= c and c <= 11: return [i,c-4,0]
        if 12 <= c and c <= 15: return [i,c-8,1]
        c-=16
    for i in range(10,20): 
        if 0 <= c and c <= 3: return [i,c,0]
        if 4 <= c and c <= 7: return [i,c-4,1]
        if 8 <= c and c <= 11: return [i,c-4,0]
        if 12 <= c and c <= 15: return [i,c-8,1]
        if 16 <= c and c <= 19: return [i,c-8,0]
        if 20 <= c and c <= 23: return [i,c-12,1]
        c-=24   
    return 'too many layers'    

# converts the link-channel provided by the HGCROC into a 'real' channel: goes from 1 to 384, representing a SiPM each
def FpgaLinkChannel_to_realChannel(FpgaLinkChannel):
    channel = FpgaLinkChannel[2]-1
    if 0 <= channel and channel <= 7:  realChannel = channel
    elif 9 <= channel and channel <= 16:  realChannel = channel-1
    elif 19 <= channel and channel <= 26:  realChannel = channel-3
    elif 28 <= channel and channel <= 35:  realChannel = channel-4
    else: realChannel = None

    if realChannel != None: realChannel+=FpgaLinkChannel[1]*32
    if realChannel != None: realChannel+=FpgaLinkChannel[0]*32*6

    return realChannel


allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #alldata
c=ROOT.TCanvas('t','The canvas of anything', 1100, 900)
c.cd()
hist = ROOT.TH2F('Map', "Mapped SiPM ADCs", 40, 1, 40, 12, 0, 12)

for t in allData : #for event in alldata
    # if t.fpga != 0:print(t.fpga)
    realChannel = FpgaLinkChannel_to_realChannel([t.fpga+1,t.link,t.channel])
    if realChannel != None:
        LayerBarSide = realChannel_to_SipM(realChannel)
        if LayerBarSide[2]==1: LayerBarSide[0] +=20
        hist.Fill(LayerBarSide[0],LayerBarSide[1],t.adc) 

#link is the chip halves, channel is just the channel
hist.SetYTitle('Bar number')
hist.SetXTitle('Layer number')


hist.Draw("COLZ")
c.SaveAs("map.png")  