#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is Peter's from-scratch frankenpaste prototype plotter
#naming standard: thisThing

#this program takes many things that end with ".root" and outputs simulation and reconstruction plots into the folder "plots"
#the process name in the config file must be the file's name 
#now available on github


from Histograms import *
from HistogramFiller import *
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

             

def barName(id):
    if id is False: return "Machine"
    if id <20: return "bar"+str(id) #it means it is TS
    shortID = id-402654208
    layer = int(shortID/1024)
    bar = shortID%1024
    return "layer"+str(layer)+"_bar"+str(bar)




def createCanvas():
    return r.TCanvas( 'c1', 'Histogram Drawing Options',1000,1000 )

def createPad(plotDimension):
    pad = r.TPad( 'pad', 'The pad with the histogram', 0,0,1,1 )
    pad.Draw()
    pad.cd()
    pad.SetGridx()
    pad.SetGridy()
      
    pad.GetFrame().SetFillColor( 18 ) 
    if plotDimension == 1:
        pad.SetRightMargin(0.05)
        pad.SetLeftMargin(0.1)  
        # pad.SetLogy()
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




def createLabel(fwhm=None):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.03)
    label.SetNDC()    
    if fwhm: label.DrawLatex(0,  0.005, "FWHM:  "+str(round(fwhm,6)))
    return label


def drawLine(plotDimension,lines):
    # hist.SetOption("")
    if plotDimension == 1:
        lines[-1].Draw("HIST SAME")
        # lines[-1].Draw("SAME E")
    if plotDimension == 2:
        lines[-1].Draw("COLZ SAME")  




  
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

def getPlotBars(plotNumber):
    plot = plotGroups[plotNumber]
    line = plot[0]
    plotType = line[0]    
    try: bars = plotDict[plotType]['bars']
    except: bars = [False]
    return bars   

def normaliseHist():
    if plotDimension == 1: 
        try: 
            hist.Scale(1./hist.Integral()) #normalises
            hist.SetYTitle("Normalised entries")
            hist.SetMaximum(1)                    
        except: print("didnt normalise")

def main():       
    for plotNumber in range(len(plotGroups)): #creates a plot
        plotDimension =  getPlotDimension(plotNumber)
        barIDs = getPlotBars(plotNumber)
        for id in barIDs:
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
                
                if plotVar == 'Energy as a function of the incoming particle angle':
                    angles = [angle for angle in range(0,50,10)]
                    inFiles= [r.TFile('e-1GeV'+str(angle)+"deg.root","READ")  for angle in angles ]
                    allDatas=[f.Get("LDMX_Events")  for f in inFiles]
                    for i in range(len(angles)): 
                        filledHist = fillHist(hist, plotVar, allDatas[i],angle=angles[i])

                else:
                    filledHist = fillHist(hist, plotVar, allData, barID=id)
                
                #normaliseHist(plotDimension)                                        
                lines.append(copy.deepcopy(filledHist.hist))                  
                drawLine(plotDimension,lines) 
                legend.AddEntry(lines[-1],fileName,"f")
        
            if plotDimension == 1 or 2: legend.Draw();
            if hasattr(filledHist, 'fwhm'): 
                createLabel(fwhm=filledHist.fwhm)
                del filledHist.fwhm



            canvas.SaveAs("plots/Plot"+str(plotNumber)+"____"+barName(id)+".png")
            # canvas.SaveAs("plots/"+str(plotNumber)+".png")
            canvas.Close() #memory leak killer



#aaah the implementation

# barIDs = hcalBarIDs()
# barIDs = range(0,12) #trigScintBarIDs

# if badIDs != "machine":
# for id in barIDs:
#         main(id)

# else: main(id)
main()