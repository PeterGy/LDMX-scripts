def hcalBinning():
    num_layers=9+10
    layer_thickness=45
    dz=num_layers * layer_thickness
    first_layer_zpos=-dz/2
    absorber_thickness=20
    bar_mounting_plate_thickness=3
    scint_adhesive_thickness=0.5
    scint_thickness=20
    binning=[]
    for i in range(num_layers):    
        binning.append(i*layer_thickness + first_layer_zpos + absorber_thickness + bar_mounting_plate_thickness + scint_adhesive_thickness )
        binning.append(i*layer_thickness + first_layer_zpos + absorber_thickness + bar_mounting_plate_thickness + scint_adhesive_thickness + scint_thickness +0.0001)
    return binning

#One element for each plot. Each plot is a list of pairs, each element in the list being a line on the plot. 
#The pair holds the plotvar, then the file it stems from   

testbeamPlotGroups = [

    #1.3
    (('Total number of hits per event',"electron"),),
    (('Sum of pulse height per event',"electron"),),    
    #1.4
    (('Distribution of number of hits for TS bars',"electron"),), 
    (('Distribution of signal amplitude for TS bars',"electron"),), 
    #1.5
    (('Time difference between TS and HCal',"electron"),), 

]
plotGroups = [

    (('Time difference between TS and HCal',"electron"),), 
    #(('trigSimX','Trigger_0.5e-'),),
    # (('simX',"Muons0.5"),),
    #(('recPE',"muon"),),
    # (('simEBar',"muon"),),
    # (('recEBar',"muon"),),
    # (('recX(Z)',"muon"),),
    # (('simX',"muon"),),
    # (('simY',"muon"),),
    # (('simZ',"muon"),),
    # (('simE',"muon"),),
    # (('simEBar',"muon"),),
    # (('simEBar',"sim"),),
    # (('recX',"sim"),('recX',"fakerun"),),
    # (('recY',"sim"),('recY',"fakerun"),),
    # (('recZ',"sim"),('recZ',"fakerun"),),
    # (('recE',"sim"),('recE',"fakerun"),),
    # (('recAmp',"electron"),),


    # (('recAmp',"sim"),('recAmp',"fakerun"),),

    # (('simX(Z)',"muon"),),
    # (('simY(Z)',"muon"),),
    # (('simY(X)',"muon"),),
    # (('simE(X)',"muon"),),
    # (('simE(Z)',"muon"),),
    
    # (('simX(Z)',"muon"),),
    # (('simY(Z)',"muon"),),

    # (('recX(Z)',"muon"),),
    # (('recY(Z)',"muon"),),


    # (('simEBar',"muon"),),
    # (('recEBar',"muon"),),
    # (('recEventBar',"muon"),),
    # (('recBarEvent',"muon"),),

    # (('recY(X)',"muon"),),
    # (('recE(Z)',"muon"),),
    
    # (('trigRecX','Trigger_0.5e-'),),
    # (('trigRecT','Trigger_0.5e-'),),
    # (('trigSimX(Z)','Trigger_0.5e-'),),
    # (('trigSimY(Z)','Trigger_0.5e-'),),
    # (('trigSimY(X)','Trigger_0.5e-'),),
    # (('trigSimE','Trigger_0.5e-'),),
    # (('simX','mu'),),

    ]         

barBinsX = range(-1000,1001,50)
barBinsY = range(-1000,1001,50)
barBinsZ = hcalBinning()

plotDict = {
    'Total number of hits per event'   :{'xaxis' : 'Hits', 'yaxis' : 'Counts', 'binning' : {'nBins':10, 'min':0, 'max':0}, 'dimension' : 1 }, #0,0 min-max makes the xrange automatic. nbins must be 10 so my program can manually set nbins to be the value it should really be automatically
    'Sum of pulse height per event' :{'xaxis' : 'Pulse height [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':10, 'min':0, 'max':0}, 'dimension' : 1 },


    'simE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'simEH1' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
    'simEH2' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
    'simEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'recEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'simX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'simY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    # 'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},
    'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : barBinsZ, 'dimension' : 1},
    
    # 'recEventBar':{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':402654210, 'max':402668549}, 'dimension' : 1},
    'recEventBar':{'xaxis' : 'Bar ID', 'yaxis' : 'Counts', 'binning' : {'nBins':402672650-402656200, 'min':402656200, 'max':402672650}, 'dimension' : 1},
    
    'recBarEvent':{'xaxis' : 'Bar number', 'yaxis' : 'Counts', 'binning' : {'nBins':19, 'min':-0.5, 'max':18.5}, 'dimension' : 1},



    'recE' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recENoisy' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recPE' :{'xaxis' : 'Number of Photo-electrons', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'recY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'recZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},        
    'recAmp' :{'xaxis' : 'Amplitude [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':140, 'min':0, 'max':14}, 'dimension' : 1},        
    
    
    
    # 'simX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,   
    #                 'binningX' : barBinsZ,                         
    #                 'binningY' : barBinsX},                         
    # 'simY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsZ, 
    #                 'binningY' : barBinsY},        
    # 'simY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsX, 
    #                 'binningY' : barBinsY},
    'simE(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                    'binningX' : {'nBins':2000, 'min':-1000, 'max':1000},  
                    'binningY' : {'nBins':200, 'min':0, 'max':0.1}}, 
    'simE(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':200, 'min':0, 'max':10}},                                
                    


    # 'recX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,   
    #                 'binningX' : barBinsZ,                         
    #                 'binningY' : barBinsX},                         
    # 'recY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsZ, 
    #                 'binningY' : barBinsY},        
    # 'recY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsX, 
    #                 'binningY' : barBinsY},

    'simX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'simY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'simY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':40, 'min':-1000, 'max':1000}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},

    'recX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'recY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
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

    'Distribution of number of hits for TS bars':{'xaxis' : 'Bar ID', 'yaxis' : 'Counts', 'binning' : {'nBins':12, 'min':0, 'max':12}, 'dimension' : 1},
    'Distribution of signal amplitude for TS bars':{'xaxis' : 'Bar ID', 'yaxis' : 'Signal Amplitude', 'binning' : {'nBins':12, 'min':0, 'max':12}, 'dimension' : 1},
    'Time difference between TS and HCal':{'xaxis' : 'Time difference [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':50, 'min':0, 'max':50}, 'dimension' : 1},

    }    