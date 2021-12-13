#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is Peter's from-scratch frankenpaste prototype plotter
#naming standard: thisThing

#this program takes many things that end with ".root" and outputs simulation and reconstruction plots into the folder "plots"
#the process name in the config file must be the file's name 
#now available on github


from Histograms import *
from numpy import *
import ROOT as r
import pdb
import copy
from array import array
from ROOT import gSystem
from optparse import OptionParser
gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window


# rootColors=[1,2,4,28,7] #a presumably color-blind friendly color palette
# rootColors=[28,2,4] #a three-compare color-blind friendly color palette
# rootColors=[4,2] #a -v+ comparison
rootColors=[1,2,3,4,5,6,7,8,9] #Colorblind unfriendly for comparing many things
rootMarkers=[4,26,32] #this is getting out of hand


def unabbreviate(str):
    if str == "rec": return "reconstruction"
    elif str == "sim": return "simulation"
    elif str == "e-0.5": return "500 MeV electrons"
    elif str == "e+0.5": return "500 MeV positrons"
    else: return str

def createCanvas():
    return r.TCanvas( 'c1', 'Histogram Drawing Options',1000,1000 )

def createPad(plotDimension):
    pad = r.TPad( 'pad', 'The pad with the histogram', 0,0,1,1 )
    pad.Draw()
    pad.cd()
    pad.SetGridx()
    pad.SetGridy()
    pad.SetLogy()  
    pad.GetFrame().SetFillColor( 18 ) 
    if plotDimension == 1:
        pad.SetRightMargin(0.05)
        pad.SetLeftMargin(0.1)  
    elif plotDimension == 2:
        pad.SetRightMargin(0.12)
        pad.SetLeftMargin(0.14)
    return pad

def createLegend():
    legend = r.TLegend(0.0,0.9,0.2,1)
    legend.SetTextSize(0.03)  
    return legend    

def createInfoBox():
     #sets what the top right box should say. "" for nothing.
    r.gStyle.SetOptStat("ne")  

def createLabel():
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.03)
    label.SetNDC()
    return label
    # label.DrawLatex(0,  0.97, "Default: 0.5 GeV e-")

def drawLine(plotDimension,lines):
    # hist.SetOption("")
    if plotDimension == 1:
        lines[-1].Draw("HIST SAME")
        # lines[-1].Draw("SAME E")
    if plotDimension == 2:
        lines[-1].Draw("COLZ SAME")  


def fillHist(hist, plotVar, allData, processName="process" , minEDeposit=0, maxEDeposit=float('inf')):
    allowNoise= False
    if   plotVar == 'simX': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[0])                  
    elif plotVar == 'simY': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[1])  
    elif plotVar == 'simZ': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2]) 
    elif plotVar == 'simE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getEdep()) 
                # print("Sim id",h.getID()-4026e5)               
    elif plotVar == 'simEH1': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getPosition()[2] < 0: hist.Fill(h.getEdep())              
    elif plotVar == 'simEH2': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getPosition()[2] > 0: hist.Fill(h.getEdep()) 


    elif plotVar == 'simEBar': 
        for entry in allData: 
            bars={}
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                try: bars[h.getID()]+=h.getEdep()
                except: bars[h.getID()]=h.getEdep()                            
            for bar in bars:
                hist.Fill(bars[bar])
        print(bars) 
                
       

    elif plotVar == 'recEBar': 
        for entry in allData: 
            bars={}
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                try: bars[h.getID()]+=h.getPE()
                except: bars[h.getID()]=h.getPE()                           
            for bar in bars:
                hist.Fill(bars[bar]) 

    elif plotVar == 'recEventBar': 
        for entry in allData: 
            bars={}
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                hist.Fill(h.getID())
                #402654211:402668549

    elif plotVar == 'recBarEvent': 
        bars={}
        for entry in allData:             
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                try: bars[h.getID()]+=1
                except: bars[h.getID()]=1
        barOrder=[]                               
        for bar in bars:
            barOrder.append(bar)
        barOrder.sort()      
        hist = r.TH1F(plotVar,"Event counts in each bar", len(bars) ,0,len(bars)) 
        for i in range(len(barOrder)):
            hist.Fill(i,bars[barOrder[i]])

        hist.SetYTitle('counts')
        hist.SetXTitle('bar ranking in bar ID')

    elif plotVar == 'recE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: 
                    hist.Fill(h.getEnergy()) 
  
    elif plotVar == 'recENoisy': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                    hist.Fill(h.getEnergy()) 
  
    elif plotVar == 'recX': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getXPos()) 
    elif plotVar == 'recY': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getYPos()) 
    elif plotVar == 'recZ': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos()) 


    elif plotVar == 'Total number of hits per event': 
        for event in allData: 
            totalCount=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalCount+=1
            hist.Fill(totalCount) 
        hist.BufferEmpty() #figures out the xrange        
        minX = hist.GetXaxis().GetBinLowEdge(1)
        maxX = hist.GetXaxis().GetBinLowEdge(11)
        hist.SetBins(int(maxX - minX),minX,maxX) #makes it so there is one bin per event


    elif plotVar == 'Sum of pulse height per event': 
        for event in allData: 
            totalAmplitude=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalAmplitude+=h.getAmplitude()
            hist.Fill(totalAmplitude) 
        hist.BufferEmpty() #figures out the xrange        
        minX = hist.GetXaxis().GetBinLowEdge(1)
        maxX = hist.GetXaxis().GetBinLowEdge(11)
        hist.SetBins(int(maxX - minX),minX,maxX) #makes it so there is one bin per ns



    elif plotVar == 'Total number of hits per run': 
        totalAmplitude=0
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalAmplitude+=1
                # totalAmplitude+=h.getAmplitude()
        hist.Fill(totalAmplitude) 

    elif plotVar == 'recAmp': 
        entryCount=0
        for entry in allData: 
            entryCount+=1
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getAmplitude()) 

                    #h.getID() repeats even in rec mode
                    # print("rec id",h.getID()-4026e5)
        print(entryCount)            
    elif plotVar == 'recPE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getPE()) 

    #the whole hcal F(x) thing is wrong, be careful
    elif plotVar == 'simX(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getPosition()[0])
                # hist.Fill(h.getPosition()[2],h.getPosition()[0])
    elif plotVar == 'simY(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getPosition()[1])            
    elif plotVar == 'simY(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[1],h.getPosition()[0])                 

    elif plotVar == 'simE(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[0],h.getEdep()) 
    elif plotVar == 'simE(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getEdep()) 
    
    elif plotVar == 'recX(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getXPos()) 
    elif plotVar == 'recY(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getYPos()) 
    elif plotVar == 'recY(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getYPos(),h.getXPos()) 

    elif plotVar == 'trigSimX':  #unimplemented
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0])       
    elif plotVar == 'trigSimE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getEdep())      
                
    #trig f(x) works               
    elif plotVar == 'trigSimX(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[0])   
    elif plotVar == 'trigSimY(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[1])            
    elif plotVar == 'trigSimY(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0],h.getPosition()[1])                 
    elif plotVar == 'trigSimE(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0],h.getEdep()) 
    elif plotVar == 'trigSimE(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getEdep()) 


    # elif plotVar == 'trigRecX': 
        # for entry in allData: 
            # for ih,h in enumerate(getattr(entry, "trigScintRecHitsUp_"+processName)):
                # print(h.getYPos())
                # hist.Fill(h.getXPos()) 
                # print(h.items()) 

    elif plotVar == 'trigRecT': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() ==6: hist.Fill(h.getTime()) 
                # print(h.getBarID())
                # print(h.items()) 

    elif plotVar == 'Distribution of number of hits for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID())

    elif plotVar == 'Distribution of signal amplitude for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID(),h.getAmplitude())

    elif plotVar == 'Time difference between TS and HCal': 
        for event in allData: #I define time difference based on the first event's time
            trigTimes=[]
            hcalTimes=[]
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                trigTimes.append(h.getTime())
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hcalTimes.append(h.getTime())
            hist.Fill(min(hcalTimes)-min(trigTimes))

    return hist                

  
def createHist(plotDict,plotVar):
    if plotDict[plotVar]['dimension'] == 1:     
        # histTitle = 'Event counts in each bar'     
        histTitle = ''     
        binning = plotDict[plotVar]['binning']                
        if type(binning) == type({}):                     
            hist = r.TH1F(plotVar,histTitle,binning['nBins'],binning['min'],binning['max']) #name, title, nbins, start, finish          
        elif type(binning) == type([]):
            hist = r.TH1F(plotVar,histTitle, len(binning)-1, array('f',binning)) #name, title, nbins, binlayout   
        hist.SetMinimum(0.5)      

    elif plotDict[plotVar]['dimension'] == 2:
        histTitle = ""               
        binningX = plotDict[plotVar]['binningX']
        binningY = plotDict[plotVar]['binningY']                           
        if type(binningX) == type({}):
            hist = r.TH2F(plotVar,histTitle,binningX['nBins'],binningX['min'],binningX['max'] #name, title, nbins, start, finish
            ,binningY['nBins'],binningY['min'],binningY['max']) #nbins, start, finish
        elif type(binningX) == type([]):    
            hist = r.TH2F(plotVar,histTitle, len(binningX)-1, array('f',binningX) #name, title, nbins, start, finish
            , len(binningY)-1, array('f',binningY)) #nbins, start, finish                    
  
    # elif plotDict[plotVar]['dimension'] == "bar":
    #     binLabelsEvtType = ["Nothing hard","1n","2n","#geq 3n","1#pi","2#pi", "1#pi_{0}", "1#pi 1N", "1p","2N","exotics","multi-body"]
    #     hist.GetXaxis().SetBinLabel(b+1, binLabelsEvtType[b])

    hist.SetYTitle(plotDict[plotVar]['yaxis'])
    hist.SetXTitle(plotDict[plotVar]['xaxis'])
    # hist.SetLineColor(rootColors[len(lines)])
    # hist.SetFillStyle(0);
    # hist.SetMarkerStyle(rootMarkers[len(lines)]) 
    # hist.SetMarkerColor(rootColors[len(lines)])
    # hist.SetMarkerSize(3)    
    return hist

def loadData(fileName): #can't even make it into a function why is ROOT so awful?
    #tried to make this more efficient by only running it once, but such methods are doomed to fail            
    inFile = r.TFile(fileName+".root","READ")  
    allData = inFile.Get("LDMX_Events")
    # allData.Print("toponly")
    print(allData)   
    return allData

def getPlotDimension(plotNumber):
    plot = plotGroups[plotNumber]
    line = plot[0]
    plotType = line[0]    
    dimension = plotDict[plotType]['dimension']
    return dimension

def normaliseHist():
    if plotDimension == 1: 
        try: 
            hist.Scale(1./hist.Integral()) #normalises
            hist.SetYTitle("Normalised entries")
            hist.SetMaximum(1)                    
        except: print("didnt normalise")

# def main():       
for plotNumber in range(len(plotGroups)): #creates a plot
    plotDimension =  getPlotDimension(plotNumber)
    canvas = createCanvas()
    createInfoBox()
    pad = createPad(plotDimension)      
    legend = createLegend()        
    lines=[]     
    for j in plotGroups[plotNumber]: #creates a line for each variable in the plot
        plotVar = var  = j[0]
        fileName = j[1]           
        inFile = r.TFile(fileName+".root","READ")  
        allData = inFile.Get("LDMX_Events")                   
        hist = createHist(plotDict,plotVar)                               
        hist = fillHist(hist, plotVar, allData) 
        #normaliseHist(plotDimension)                                        
        lines.append(copy.deepcopy(hist))                  
        drawLine(plotDimension,lines) 
        legend.AddEntry(lines[-1],fileName,"f")
   
    if plotDimension == 1: legend.Draw();
    canvas.SaveAs("plots/Plot"+str(plotNumber)+".png")
    canvas.Close() #memory leak killer


# if __name__=="__main__":
#     main()