#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is Peter's from-scratch frankenpaste prototype plotter
#naming standard: thisThing

#this program takes many things that end with ".root" and outputs simulation and reconstruction plots into the folder "Plots"
#the process name in the config file must be the file's name 

import ROOT as r
import pdb
import copy
from array import array
from ROOT import gSystem
from optparse import OptionParser
gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?
rootColors=[1,2,4,28,7] #a presumably color-blind friendly color palette
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

def histogramFiller(hist, plotVar, allData, processName):

    allowNoise= False
    
    if   plotVar == 'simX': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[0])
    elif plotVar == 'simY': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[1])  
    elif plotVar == 'simZ': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[2]) 
    elif plotVar == 'simE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
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


    elif plotVar == 'trigSimX':  #unimplemented
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0])  
     
    elif plotVar == 'trigSimE': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getEdep()) 




    elif   plotVar == 'simZ(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[2]+450,h.getPosition()[0])
    elif plotVar == 'simZ(Y)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[1])            
    elif plotVar == 'simY(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[1],h.getPosition()[0])                 

    elif plotVar == 'simE(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[0],h.getEdep()) 
    elif plotVar == 'simE(Z)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getEdep()) 
    
    elif plotVar == 'recZ(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getXPos()) 
    elif plotVar == 'recZ(Y)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getYPos()) 
    elif plotVar == 'recY(X)': 
        for entry in allData: 
            for ih,h in enumerate(getattr(entry, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getYPos(),h.getXPos()) 
     
    return hist                

    


def main(options):       
    #One element for each plot. Each plot is a list of pairs, each element in the list being a line on the plot. 
    #The pair holds the plotvar, then the file it stems from   
    plotGroups = [
        
        (('simX','Work'),),
        (('simE','Work'),),
        (('simZ(X)','Work'),),
        (('simE(X)','Work'),),
        # (('simZ','e-0.5'),('recZ','e-0.5'),),
        ]         

    plotDict = {
        'simE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':20}, 'dimension' : 1 },
        'simEH1' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
        'simEH2' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
        'simEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
        'simX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'simY' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'simZ' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},
        
        'recE' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':20} , 'dimension' : 1},
        'recENoisy' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
        'recPE' :{'xaxis' : 'Number of Photo-electrons', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
        'recX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'recY' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'recZ' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},        
        
        'trigSimX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
        'trigSimE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':1}, 'dimension' : 1 },
        
        'simZ(X)' :{'xaxis' : 'Penetration depth [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':900, 'min':0, 'max':900}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},                            
        'simZ(Y)' :{'xaxis' : 'Z Distance [mm]', 'yaxis' : 'Y Distance [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':900, 'min':-450, 'max':450}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},        
        'simY(X)' :{'xaxis' : 'Y Distance [mm]', 'yaxis' : 'X Distance [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':2000, 'min':-1000, 'max':1000}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},
        'simE(X)' :{'xaxis' : 'X Distance [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                        'binning1' : {'nBins':2000, 'min':-1000, 'max':1000},  
                        'binning2' : {'nBins':200, 'min':0, 'max':10}}, 
        'simE(Z)' :{'xaxis' : 'Z Distance [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                        'binning1' : {'nBins':1000, 'min':-500, 'max':500},  
                        'binning2' : {'nBins':200, 'min':0, 'max':10}},                                
                        
                        
        'recZ(X)' :{'xaxis' : 'Z Distance [mm]', 'yaxis' : 'X Distance [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':900, 'min':-450, 'max':450}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},
        'recZ(Y)' :{'xaxis' : 'Z Distance [mm]', 'yaxis' : 'Y Distance [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':500, 'min':-450, 'max':450}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},
        'recY(X)' :{'xaxis' : 'Y Distance [mm]', 'yaxis' : 'X Distance [mm]', 'dimension' : 2,
                        'binning1' : {'nBins':2000, 'min':-1000, 'max':1000}, 
                        'binning2' : {'nBins':2000, 'min':-1000, 'max':1000}},
        
        }
   
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
        
        lines=[]
        legend = r.TLegend(0.65,0.75,1.,1.);
        
        for j in plotGroups[plotNumber]: #creates a plot for each variable you are going to plot
            plotVar = var  = j[0]
            fileName = j[1]           

            #tried to make this more efficient by only running it once, but such methods are doomed to fail            
            inFile = r.TFile(fileName+".root","READ")  
            allData = inFile.Get("LDMX_Events")
            # allData.Print("toponly")           
            
            
            if plotDict[j[0]]['dimension'] == 1:
                binning = plotDict[j[0]]['binning']
                hist = r.TH1F(plotVar,plotVar[0:],binning['nBins'],binning['min'],binning['max']) #name, title, nbins, start, finish
                
            elif plotDict[j[0]]['dimension'] == 2:
                binning1 = plotDict[j[0]]['binning1']
                binning2 = plotDict[j[0]]['binning2']
                hist = r.TH2F(plotVar,"Deposit locations",binning1['nBins'],binning1['min'],binning1['max'] #name, title, nbins, start, finish
                    ,binning2['nBins'],binning2['min'],binning2['max']) #nbins, start, finish
                        
                    
            hist.SetYTitle(plotDict[plotVar]['yaxis'])
            hist.SetXTitle(plotDict[plotVar]['xaxis'])
            hist.SetFillStyle(0);
            hist.SetLineColor(rootColors[len(lines)]);
                    
            processName = fileName        
            # processName = "process"       
            hist = histogramFiller(hist, plotVar, allData, processName)                     

            if plotDict[j[0]]['dimension'] == 1:
                hist.SetMinimum(0.5)
                pad.SetLogy()
                try: 
                    hist.Scale(1./hist.Integral()) #normalises
                    hist.SetYTitle("Normalised entries") 
                except: print("didnt normalise")
            
            elif plotDict[j[0]]['dimension'] == 2:
                hist.SetOption("COLZ")
            
            lines.append(copy.deepcopy(hist))          
            # lines[-1].Draw("SAME C")
            # lines[-1].Draw("SAME E2")
            lines[-1].Draw("SAME")
            # lines[-1].Draw("SAME") #add E for error bars
            
            legend.AddEntry(lines[-1],j[0]+" "+j[1],"f");

        legend.SetTextSize(0.03)
        legend.Draw();

       
        label = r.TLatex()
        label.SetTextFont(42)
        label.SetTextSize(0.03)
        label.SetNDC()
        # label.DrawLatex(0,  0.97, "Default: 0.5 GeV e-")

        # canvas.SaveAs("Plots/"+options.particle+str(options.energy)+"GeV"+str(options.angle)+"deg__"+p1+"_vs_"+p2+".png")
        canvas.SaveAs("plots/Plot"+str(plotNumber)+".png")
        canvas.Close() #memory leak killer

if __name__=="__main__":
	parser = OptionParser()	
	parser.add_option('-e','--energy', dest='energy', default = '0.5',help='beam energy in GeV')
	parser.add_option('-p','--particle', dest='particle', default = 'e-',help='type of particle in beam')
	parser.add_option('-a','--angle', dest='angle', default = '0', help='incidence angle')
	parser.add_option('-f','--file', dest='file', default = 'Output', help='Name of the file (without the .root)')
	options = parser.parse_args()[0]
	main(options)