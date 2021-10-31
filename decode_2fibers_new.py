import ROOT as r
from sys import argv
from math import floor
from itertools import chain
import numpy as np

import glob

def ADCtoQ(ADC):
  if ADC <= 0: return -16;
  if ADC >= 255: return 350000;
  nbins_= [0, 16, 36, 57, 64];
  sense_ = [3.1,   6.2,   12.4,  24.8, 24.8, 49.6, 99.2, 198.4, 198.4, 396.8, 793.6, 1587, 1587, 3174, 6349, 12700];
  edges_ = [-16,   34,    158,    419,    517,   915,
                      1910,  3990,  4780,   7960,   15900, 32600,
                      38900, 64300, 128000, 261000, 350000];
  gain_ = 1                    
  rr = int(ADC // 64);  # range
  v1 = ADC % 64;  # temp. var
  ss = 0;         # sub range

  for i in range (1,4):# to get the subrange
    if v1 > nbins_[i]: ss += 1;
  
  cc = 64 * rr + nbins_[ss];
  temp = edges_[4 * rr + ss] + (v1 - nbins_[ss]) * sense_[4 * rr + ss] +  sense_[4 * rr + ss] / 2;
  return temp / gain_;


class qie_frame:

    def __init__(self,label):
        self.label=label
        self.adcs=[]
        self.tdcs=[]
        self.capid=0
        self.ce=0
        self.bc0=0

    def decode(self,frame):
        if len(frame) != 22 :
            # print("[[qie_frame]]  ERROR: was expecting 22 characters")
            return
        else :
            self.capid = (int(frame[:2],16)>>2)&3
            self.ce = (int(frame[:2],16)>>1)&1
            self.bc0 = (int(frame[:2],16))&1
            for i in range(8):
                temp_adc=int(frame[(i+1)*2:(i+2)*2],16)
                self.adcs.append(temp_adc)
            tdc_bytes_03=int(frame[-4:-2],16)
            tdc_bytes_48=int(frame[-2:],16)
            for i in range(3,-1,-1):
                temp_tdc=(tdc_bytes_03>>(i*2))&3
                self.tdcs.append(temp_tdc)
            for i in range(3,-1,-1):
                temp_tdc=(tdc_bytes_48>>(i*2))&3
                self.tdcs.append(temp_tdc)

    def printer(self):
        print('-----QIE FRAME-------')
        print(self.label)
        print('CADID: {0} CE: {1} BC0: {2}'.format(self.capid,self.ce,self.bc0))
        print('adcs: ',' '.join(map(str,self.adcs)))
        print('tdcs: ',' '.join(map(str,self.tdcs)))

    def trigger(self):
        nzero=0
        for adc,tdc in zip(self.adcs,self.tdcs):
            if (adc > 50 and adc < 255) :
                # print('[[qie_frame]] Trigger')
                # self.printer()
                return
            if adc==0 :
                nzero=nzero+1
        if nzero>3 :
            # print('[[qie_frame]] Trigger')
            # self.printer()
            return
        
hist_pulse=[]
for i in range(16):
    hist_pulse.append(r.TH2F("pulse_ch{0}".format(i),"pulse_ch{0};time sample;ADC".format(i),64,-0.5,63.5,64,-0.5,63.5))

hist_adc_tdc=[]
for i in range(16):
    hist_adc_tdc.append(r.TH2F("adc_tdc{0}".format(i),"adc_tdc{0};TDC;ADC".format(i),4,-0.5,3.5,256,-0.5,255.5))

hist_adc=[]
for i in range(16):
    hist_adc.append(r.TH1F("adc{0}".format(i),"adc{0};ADC;Arbitrary".format(i),50,-0.5,49.5))

hist_charge=[]
# Bins, quadtratic, st max bin is at ~1000
#charge_bins = np.array([(i*33./30.)**2 for i in range(31)])  # 0, 5, 10, ... , 400, 500, 600, 800, 1000
charge_bins = np.array([i for i in np.linspace(0,800,800)])  # linear bining
# charge_bins = np.array([ADCtoQ(i) for i in np.linspace(0,100,200)])
for i in range(16):
    #hist_charge.append(r.TH1F("charge{0}".format(i),"charge{0};Charge [fC?];Arbitrary".format(i),50,-0.5,1000))
    # NEW:  Add variable binning
    hist_charge.append(r.TH1F("charge{0}".format(i),"charge{0};Charge [fC?];Arbitrary".format(i),len(charge_bins)-1,charge_bins))

hist_tdc=[]
for i in range(16):
    hist_tdc.append(r.TH1F("tdc{0}".format(i),"tdc{0};ADC;Arbitrary".format(i),3,-0.5,3.5))
    
def clean_kchar(data):
    return data.replace('F7FB','')

def clean_BC7C(data):
    return data.replace('BC7C','')

def remove_partial_events(data):
    return  data[data.find('BC'):data.rfind('BC')]

def read_string_from_file(filename):
    data=""
    with open(filename) as f:
        data+= ''.join(f.readlines())
    return data.split('192.168.1.30')

def load_data(file):
  data = open(file, "r") #loads file
  data=data.read()       #reads file
  data=data.split("\n") #turn one giant string into a list of line strings. The last line is "" and drops it.
  return data

def sort_into_events(data):
  processed_data=[]
  processed_event=[]
  for line in data:
    try:
      if line[0] == 'r':
        processed_data.append(processed_event)
        # print("appended", 1)
        processed_event=[]
      if line[0] != 's' and line[:4] != 'recv' and line[0] != '\r':
        processed_event.append(line) 
    except: pass #blank lines in data that would otherwise crash program
  return processed_data

######### = = = = = = = = = = = = = = = = = 

#data = load_data('data/'+argv[1]+'.txt')

# filepath = '../data/*oct_28_2{}*.txt'
# filepath = '../data/15gev_hadrons_oct_29_1947_2021.txt'
filepath = 'data/2gev_electrons_oct_29_2209_2021.txt'
filepath = 'data/4gev_electrons_oct30_1406_2021.txt'

samples_summed=10

# for data_file in glob.glob(filepath.format('2')) + glob.glob(filepath.format('3')):
for data_file in [filepath]:
    print("Reading file", data_file)
    data = load_data(data_file)
    data = sort_into_events(data)
    data = list(chain.from_iterable(data))

    events=[]
    start_index=0
    for i in range(len(data)):
        if i+1 >= len(data):
            break
        if data[i]== 'FFFFFFFFFFFFFFFF':# and data[i+1] == 'FFFFFFFFFFFFFFFF':
            if i != 0 :
                events.append(data[start_index:i-1])
            start_index=i+2
    # print(events)

    ievent=-1
    for event in events:
        # print("did it run?")
        ievent = ievent+1
        # print('=========== NEW EVENT {0} ========'.format(ievent))
        fiber2=""
        fiber1=""
        event = event[1:]
        for word in event:
            fiber1+=word[:8]
            fiber2+=word[8:]

        fiber1 = clean_kchar(fiber1)
        fiber1 = clean_BC7C(fiber1)
        #fiber1 = remove_partial_events(fiber1)
        fiber2 = clean_kchar(fiber2)
        fiber2 = clean_BC7C(fiber2)
        #fiber2 = remove_partial_events(fiber2)
            
        fiber1 = fiber1.split('BC')
        fiber2 = fiber2.split('BC')
        
        sum_charge = [0,0,0,0,0,0,0,0]
        for i,z in enumerate(zip(fiber1,fiber2)):
            if i>20: break#print(i)
            # print('---------- NEW TIME SAMPLE ({0}) ----------'.format(i))
            # print(z)
            f1 = qie_frame('fiber 1')
            f1.decode(z[0])
            
            for j,codes in enumerate(zip(f1.adcs,f1.tdcs)):
                #hist_pulse[(ievent-1)*16+j].Fill(i,codes[0])
                # print(j)
                sum_charge[j]+= ADCtoQ(codes[0])
                if i%samples_summed==samples_summed-1:
                    hist_pulse[j].Fill(i,codes[0])
                    hist_adc[j].Fill(codes[0])
                    # hist_charge[j].Fill(ADCtoQ(codes[0]))
                    
                    hist_tdc[j].Fill(codes[1])
                    hist_adc_tdc[j].Fill(codes[1],codes[0])


                    hist_charge[j].Fill(sum_charge[j])
                    sum_charge[j]= 0


            f1.trigger()
            #f1.printer()
            f2 = qie_frame('fiber 2')
            f2.decode(z[1])
            for j,codes in enumerate(zip(f2.adcs,f2.tdcs)):
                #hist_pulse[(ievent-1)*16+j+8].Fill(i,codes[0])
                hist_pulse[j+8].Fill(i,codes[0])
                hist_adc[j+8].Fill(codes[0])
                hist_charge[j+8].Fill(ADCtoQ(codes[0]))
                hist_tdc[j+8].Fill(codes[1])
                hist_adc_tdc[j+8].Fill(codes[1],codes[0])
            f2.trigger()
            #f2.printer()
        

# Normalize charge histo:
for hist in hist_charge:
    for i in range(30):
        hist.SetBinContent(i, hist.GetBinContent(i) / hist.GetBinWidth(i))

can = r.TCanvas('can','can',1000,500)
# for i,h in enumerate(hist_pulse):
#     print(i,h)
#     h.Draw("colz")
#     can.SaveAs('plots/'+argv[1]+'pulse_ch{0}.png'.format(i))
# for i,h in enumerate(hist_adc):
#     h.Draw()
#     can.SetLogy()
#     can.SaveAs('plots/'+argv[1]+'adc{0}.png'.format(i))
for i,h in enumerate(hist_charge):
    h.Draw()
    can.SetLogy()
    can.SaveAs('alldata_'+'charge{0}.png'.format(i))    
# for i,h in enumerate(hist_tdc):
#     h.Draw()
#     can.SaveAs('plots/'+argv[1]+'tdc{0}.png'.format(i))
# can.SetLogy(False)
# for i,h in enumerate(hist_adc_tdc):
#     h.Draw()
#     can.SaveAs('plots/'+argv[1]+"adc_tdc{0}.png".format(i))
