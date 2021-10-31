from pylab import *
from numpy import *

def load_data(file):
  data = open(file, "r") #loads file
  data=data.read()       #reads file
  data=data.split("\n")[0:-2]  #turn one giant string into a list of line strings. 
  return data

def numbers(data,TAI=False):



    times=[]
    for line in data:
        if line[line.find("c")+1]=="2":
        # try:     times.append( float(line[line.find("t")+1:-1]) /125000000/4096 - float(data[0][data[0].find("t")+1:-1])) 
            try:
                seconds     = float(line[line.find("t")+1:line.find("n")])
                nanoseconds = float(line[line.find("n")+1:line.find("f")])
                fractions   = float(line[line.find("f")+1:-1])    
                startTime =  seconds + nanoseconds * 8e-9 + fractions * 8e-9 / 4096
                break 
            except: 
                # print("error?")
                pass

    if TAI:
        startTime=TAI


    '''
    line=data[0]
    seconds     = float(line[line.find("t")+1:line.find("n")])
    nanoseconds = float(line[line.find("n")+1:line.find("f")])
    fractions   = float(line[line.find("f")+1:-1])    
    startTime   = 0#( seconds + nanoseconds * 8e-9 + fractions * 8e-9 / 4096)# - startTime) 
'''
    # startTime = float(data[0][data[0].find("t")+1:-1]) /125000000/4096
    for line in data:
        if line[line.find("c")+1]=="2":
        # try:     times.append( float(line[line.find("t")+1:-1]) /125000000/4096 - float(data[0][data[0].find("t")+1:-1])) 
            try:
                seconds     = float(line[line.find("t")+1:line.find("n")])
                nanoseconds = float(line[line.find("n")+1:line.find("f")])
                fractions   = float(line[line.find("f")+1:-1])  
                  
                times.append( seconds + nanoseconds * 8e-9 + fractions * 8e-9 / 4096 - startTime) 
                if seconds + nanoseconds * 8e-9 + fractions * 8e-9 / 4096 - startTime > endTime: break

            except: 
                # print("error?")
                pass
    return times



#define desired time here in UTC
UTC=False

if UTC:
    TAI=UTC+37
else:
    TAI=False





file = 'timestamps.txt'  
data = load_data(file)
data = numbers(data,TAI)

endTime=50

xlim(0,endTime)
binsies = linspace(0,endTime,4000)
hist(data,bins=binsies)
# y=data
# x=linspace(y[0],y[-1],)
# plot(x,y)
xlabel("time [s]")
ylabel("counts")
show()
savefig("Plot.png",dpi=100)
