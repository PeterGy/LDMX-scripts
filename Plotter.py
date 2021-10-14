#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is Peter's from-scratch frankenpaste prototype plotter
#naming standard: thisThing

#this program takes many things that end with ".root" and outputs simulation and reconstruction plots into the folder "Plots"
#the process name in the config file must be the file's name 
#now available on github

from numpy import *
import ROOT as r
import pdb
import copy
from array import array
from ROOT import gSystem
from optparse import OptionParser
gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?
# rootColors=[1,2,4,28,7] #a presumably color-blind friendly color palette
# rootColors=[28,2,4] #a three-compare color-blind friendly color palette
# rootColors=[4,2] #a -v+ comparison
rootColors=[1,2,3,4,5,6,7,8,9] #Colorblind unfriendly for comparing many things
rootMarkers=[4,26,32] #this is getting out of hand
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

def unabbreviate(str):
    if str == "rec": return "reconstruction"
    elif str == "sim": return "simulation"
    elif str == "e-0.5": return "500 MeV electrons"
    elif str == "e+0.5": return "500 MeV positrons"
    else: return str

def histogramFiller(hist, plotVar, allData, processName, minEDeposit=0, maxEDeposit=float('inf')):

    allowNoise= False
    # print("Only deposits between "+str(minEDeposit)+" and "+str(maxEDeposit))
    
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
    
                    #h.getID() repeats even in rec mode
                    # print("rec id",h.getID()-4026e5)
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
                    hist.Fill(h.getPosition()[2]+450,h.getPosition()[1])            
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
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos()+450,h.getXPos()) 
    elif plotVar == 'recY(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos()+450,h.getYPos()) 
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
    elif plotVar == 'trigBarID': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getID()) 
                # hist.Fill(h.bar()) 

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

    return hist                




def depositionAnalyser(plotVar, allData, fileName): #Analyses energy depostions in Z plane   
    if plotVar == 'simE(Z)':
        bins = arange(0,1000) #1000 bins, each representing a mm along the detector
      
        binCount    = [0 for i in bins] #number of hits that bin got
        binSum      = [0 for i in bins] #sum of energies that bin got
        binCumSum   = [0 for i in bins] #cumulative sum of energies that bin got
        binAvg      = [0 for i in bins] #average energy that bin got
        binCumAvg   = [0 for i in bins] #cumulative average energy that bin got
        

        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+fileName)):
                #I move the hcal 500 mm back so plt doesn't go mad from negative indices and show bad stuff
                binCount[int(h.getPosition()[2])+500] += 1 
                binSum[int(h.getPosition()[2])+500] += h.getEdep()
        
        for i in bins: #finds averages
            if binCount[i] > 0: binAvg[i]  = binSum[i]/binCount[i]
                
        for i in arange(1,1000): #finds cumulatives
            binCumAvg[i]=binCumAvg [i-1]+binAvg[i]
            binCumSum[i]=binCumSum [i-1]+binSum[i]
            

        
        
        #plotting
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        # plt.figure("hits")
        # plt.yscale("log")
        # plt.title("Number of depositions  (1000 muons)")
        # plt.ylabel("Deposit count")
        # plt.xlabel("Detector depth [mm]")
        # plt.plot(bins,binCount)
        # plt.savefig('plots/1_Hits.png')
        
        # plt.figure("energy")
        # plt.yscale("log")
        # plt.title("Total energy deposited (1000 muons)")
        # plt.ylabel("Energy [MeV]")
        # plt.xlabel("Detector depth [mm]")
        # plt.ylim((5e-3,5e3))
        # plt.plot(bins,binSum)
        # plt.savefig('plots/2_EnergyDeposited.png')
        
        plt.figure("cum")
        plt.title("Total energy deposited (1000 muon sim)")
        plt.ylabel("Energy [MeV]")
        plt.xlabel("Detector depth [mm]")
        plt.plot(bins,binCumSum)
        plt.savefig('plots/3_CumEnergyDeposited.png')
        
        
        binCumSumAvg = [i/1000 for i in binCumSum]
        
        plt.figure("cumAverage")
        plt.title("Total energy deposited by an average 2 GeV muon into scintillators only")
        plt.ylabel("Energy [MeV]")
        plt.xlabel("Detector depth [mm]")
        plt.plot(bins,binCumSumAvg)
        plt.savefig('plots/4_CumEnergyDepositedAverage.png')
        
        # plt.figure("remain")
        # plt.title("Remaining energy of a single muon (1000 muon sim)")
        # plt.ylabel("Energy [MeV]")
        # plt.xlabel("Detector depth [mm]")
        
        # loss_factor=8.2        
        # binCumRem= [  -i*loss_factor/1000+500  for i in binCumSum]
        # print(binCumRem[-1])
        # plt.plot(bins,binCumRem)
        # plt.savefig('plots/3.5_Remains.png')
        
        
        
        print("total energy deposited",sum(binSum))

def main(options):       
    #One element for each plot. Each plot is a list of pairs, each element in the list being a line on the plot. 
    #The pair holds the plotvar, then the file it stems from   
    plotGroups = [


        # (('trigSimX','Trigger_0.5e-'),),
        # (('trigRecX','Trigger_0.5e-'),),
        (('trigRecT','Trigger_0.5e-'),),
        # (('trigSimX(Z)','Trigger_0.5e-'),),
        # (('trigSimY(Z)','Trigger_0.5e-'),),
        # (('trigSimY(X)','Trigger_0.5e-'),),
        # (('trigSimE','Trigger_0.5e-'),),

        ]         

    barBinsX = range(-1000,1001,50)
    barBinsY = range(-1000,1001,50)
    barBinsZ = [] #binning based on layout of bars
    for i in range(0,19):
        barBinsZ.append(-465.5 + i*49)
        barBinsZ.append(-465.5 + i*49+25)

    plotDict = {
        'simE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
        'simEH1' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
        'simEH2' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
        'simEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
        'simX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'simY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        # 'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},
        'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : barBinsZ, 'dimension' : 1},
        
        'recE' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':0.2} , 'dimension' : 1},
        'recENoisy' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
        'recPE' :{'xaxis' : 'Number of Photo-electrons', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
        'recX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'recY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'recZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},        
        
        
        
        'simX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,   
                        # 'binningX' : {'nBins':40, 'min':-00, 'max':900}, 
                        # 'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
                        # 'binningX' : {'nBins':1000, 'min':-465.5, 'max':465.5},                      
                        # 'binningY' : {'nBins':1000, 'min':-465.5, 'max':465.5}},       
                        'binningX' : barBinsZ,                         
                        'binningY' : barBinsX},                         
        'simY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':40, 'min':0, 'max':900}, 
                        'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},        
        'simY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':40, 'min':-1000, 'max':1000}, 
                        'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
        'simE(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                        'binningX' : {'nBins':2000, 'min':-1000, 'max':1000},  
                        'binningY' : {'nBins':200, 'min':0, 'max':0.1}}, 
        'simE(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                        'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                        'binningY' : {'nBins':200, 'min':0, 'max':10}},                                
                        
                        
        'recX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':40, 'min':0, 'max':900}, 
                        'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
        'recY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':40, 'min':0, 'max':900}, 
                        'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
        'recY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':40, 'min':-1000, 'max':1000}, 
                        'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
        'recE(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                        'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                        'binningY' : {'nBins':200, 'min':0, 'max':10}},    
 
        'trigSimX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':80, 'min':-40, 'max':40}, 'dimension' : 1},
        'trigRecX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':80, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'trigRecT' :{'xaxis' : 'Time [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':20, 'min':0, 'max':10}, 'dimension' : 1}, #machine has a resolution of 0.5 ns apparently
        'trigSimE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':1}, 'dimension' : 1 },
        
        'trigSimX(Z)' :{'xaxis' : 'Penetration depth [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                        # 'binningY' : {'nBins':200, 'min':-20, 'max':20}},    
                        # 'binningX' : {'nBins':100, 'min':-400, 'max':900}, 
                        'binningY' : {'nBins':200, 'min':-20, 'max':20}},                         
        'trigSimY(Z)' :{'xaxis' : 'Penetration depth [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                        'binningY' : {'nBins':200, 'min':-20, 'max':20}},         
        'trigSimY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                        'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                        'binningY' : {'nBins':200, 'min':-20, 'max':20}},  
        'trigBarID'   :{'xaxis' : 'ID', 'yaxis' : 'Counts', 'binning' : {'nBins':50, 'min':0, 'max':50}, 'dimension' : 1 },                      
        }
    
   
    minEDeposit = 0
    maxEDeposit = float('inf')
    # maxEDeposit = 0.1
    allDatas = {}   
    for plotNumber in range(len(plotGroups)):
        canvas = r.TCanvas( 'c1', 'Histogram Drawing Options',1000,1000 )
        pad = r.TPad( 'pad', 'The pad with the histogram', 0,0,1,1 )
        pad.Draw()
        pad.cd()
        pad.SetGridx()
        pad.SetGridy()
        # pad.SetLogy()  
        pad.GetFrame().SetFillColor( 18 )
        
        r.gStyle.SetOptStat("n");
        

        pad.SetRightMargin(0);
        # pad.SetLeftMargin(0);
        # pad.SetTopMargin(0);
        
        lines=[]
        legend = r.TLegend(0.7,0.8,1,1);
        legend.SetTextSize(0.03)
        
        # inFile = r.TFile(fileName+".root","READ")  
        # allData = inFile.Get("LDMX_Events")
        
        for j in plotGroups[plotNumber]: #creates a plot for each variable you are going to plot
            plotVar = var  = j[0]
            fileName = j[1]           

            #tried to make this more efficient by only running it once, but such methods are doomed to fail            
            inFile = r.TFile(fileName+".root","READ")  
            allData = inFile.Get("LDMX_Events")
            # allData.Print("toponly")           
            
            
            if plotDict[j[0]]['dimension'] == 1:
                # histTitle = 'Deposit locations'
                # histTitle = ''
                histTitle = unabbreviate(j[0][0:3]) + ' deposits'      
                binning = plotDict[j[0]]['binning']                
                if type(binning) == type({}):                     
                    hist = r.TH1F(plotVar,histTitle,binning['nBins'],binning['min'],binning['max']) #name, title, nbins, start, finish          
                elif type(binning) == type([]):
                    hist = r.TH1F(plotVar,histTitle, len(binning)-1, array('f',binning)) #name, title, nbins, binlayout
                
            elif plotDict[j[0]]['dimension'] == 2:
                histTitle = 'Deposit locations ('+ unabbreviate(j[1]) +') '+unabbreviate(j[0][0:3])
                
                
                binningX = plotDict[j[0]]['binningX']
                binningY = plotDict[j[0]]['binningY']           
                
                if type(binningX) == type({}):
                    hist = r.TH2F(plotVar,histTitle,binningX['nBins'],binningX['min'],binningX['max'] #name, title, nbins, start, finish
                    ,binningY['nBins'],binningY['min'],binningY['max']) #nbins, start, finish
                elif type(binningX) == type([]):    
                    hist = r.TH2F(plotVar,histTitle, len(binningX)-1, array('f',binningX) #name, title, nbins, start, finish
                    , len(binningY)-1, array('f',binningY)) #nbins, start, finish
                    
                    
                pad.SetRightMargin(0.12);
                pad.SetLeftMargin(0.14);        
                    
            hist.SetYTitle(plotDict[plotVar]['yaxis'])
            hist.SetXTitle(plotDict[plotVar]['xaxis'])
            # hist.SetFillStyle(0);
            # hist.SetMarkerStyle(rootMarkers[len(lines)]) 
            # hist.SetMarkerColor(rootColors[len(lines)])
            # hist.SetMarkerSize(3)
            hist.SetLineColor(rootColors[len(lines)])
                    
            # processName = fileName        
            processName = "process"       
            hist = histogramFiller(hist, plotVar, allData, processName,minEDeposit=minEDeposit,maxEDeposit=maxEDeposit) 

            
            # depositionAnalyser(plotVar, allData, fileName)

            if plotDict[j[0]]['dimension'] == 1:
                hist.SetMinimum(0.5)
                pad.SetLogy()
                
                # try: 
                    # hist.Scale(1./hist.Integral()) #normalises
                    # hist.SetYTitle("Normalised entries")
                    # hist.SetMaximum(1)                    
                # except: print("didnt normalise")
            
            
            lines.append(copy.deepcopy(hist))          

            # hist.SetOption("")
            
            if plotDict[j[0]]['dimension'] == 1:
                lines[-1].Draw("HIST SAME")
                # lines[-1].Draw("SAME E")
            if plotDict[j[0]]['dimension'] == 2:
                lines[-1].Draw("COLZ SAME")    

            
            legend.AddEntry(lines[-1],j[0]+" "+j[1],"f");


        
        if plotDict[j[0]]['dimension'] == 1: legend.Draw();

       
        label = r.TLatex()
        label.SetTextFont(42)
        label.SetTextSize(0.03)
        label.SetNDC()
        # label.DrawLatex(0,  0.97, "Default: 0.5 GeV e-")

        # canvas.SaveAs("Plots/"+options.particle+str(options.energy)+"GeV"+str(options.angle)+"deg__"+p1+"_vs_"+p2+".png")
        canvas.SaveAs("plots/Plot"+str(plotNumber)+".png")
        # canvas.SaveAs("plots/Plot"+str(plotNumber)+"-MAX"+str(maxEDeposit)+"-MeV.png")
        canvas.Close() #memory leak killer

if __name__=="__main__":
	parser = OptionParser()	
	parser.add_option('-e','--energy', dest='energy', default = '0.5',help='beam energy in GeV')
	parser.add_option('-p','--particle', dest='particle', default = 'e-',help='type of particle in beam')
	parser.add_option('-a','--angle', dest='angle', default = '0', help='incidence angle')
	parser.add_option('-f','--file', dest='file', default = 'Output', help='Name of the file (without the .root)')
	options = parser.parse_args()[0]
	main(options)