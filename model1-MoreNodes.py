from pulp import *
import math
import random
import matplotlib.pyplot as plt
import numpy as np

numberofBTSs=30
#Click on the green circles, your first click is the source of the first flow
#Your second click is the destination of that first flow
#Your third click is the source of the second flow
#Your Fourth Click is the destination of that second flow.
#Then, close the graph window, the optimization problem gets solved then.
flows={1:[1,4],2:[3,2]} #flow_ID:[source,destination]
L_star=[40,40] # Maximum length of the line accpetable for transferring the load. The actual length must be calculated
Dmax=10  #maximum distance a BTS can access the nodes
############END OF INPUTS

fig = plt.figure()

#RANDOM BTSs and plot them
bts={1:[0,0]}
for x in range(1, numberofBTSs):
    bts[x]=[random.randint(0,20),random.randint(0,20)]
    plt.plot([bts[x][0]],[bts[x][1]],'go',picker=5,label=x)
    
#SELECT SOURCES AND DESTINATIONS

myIndex=0
def onpick(event):
    global myIndex    
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    btsNo = thisline.get_label()
    ind = event.ind
    print('onpick points:', xdata,ydata,btsNo)
    if myIndex==0:
        flows[1][0]=int(btsNo)
        myIndex=myIndex+1
        plt.plot(xdata,ydata,'r^',label=x)
    elif myIndex==1:
        flows[1][1]=int(btsNo)
        myIndex=myIndex+1
        plt.plot(xdata,ydata,'b^',label=x)
    elif myIndex==2:
        flows[2][0]=int(btsNo)
        myIndex=myIndex+1
        plt.plot(xdata,ydata,'rs',label=x)
    elif myIndex==3:
        flows[2][1]=int(btsNo)
        myIndex=myIndex+1
        plt.plot(xdata,ydata,'bs',label=x)
    
fig.canvas.mpl_connect('pick_event', onpick)
plt.show()



SrcDest = [[0 for x in range(2)] for y in range(2)]#I had to do this! Sorry, not a neat code now! :)
SrcDest[0][0]=flows[1][0]
SrcDest[0][1]=flows[1][1]
SrcDest[1][0]=flows[2][0]
SrcDest[1][1]=flows[2][1]
#Lets calculate the intersection of two lines, exactly an imaginary place where the the flows pass in an intersection
o=[(((bts[SrcDest[0][0]][0]*bts[SrcDest[0][1]][1]-bts[SrcDest[0][0]][1]*bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][0]-bts[SrcDest[1][1]][0]))-((bts[SrcDest[0][0]][0]-bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][0]*bts[SrcDest[1][1]][1]-bts[SrcDest[1][0]][1]*bts[SrcDest[1][1]][0])))/(((bts[SrcDest[0][0]][0]-bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][1]-bts[SrcDest[1][1]][1]))-((bts[SrcDest[0][0]][1]-bts[SrcDest[1][1]][0])*(bts[SrcDest[1][0]][0]-bts[SrcDest[1][1]][0]))),(((bts[SrcDest[0][0]][0]*bts[SrcDest[0][1]][1]-bts[SrcDest[0][0]][1]*bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][1]-bts[SrcDest[1][1]][1]))-((bts[SrcDest[0][0]][1]-bts[SrcDest[0][1]][1])*(bts[SrcDest[1][0]][0]*bts[SrcDest[1][1]][1]-bts[SrcDest[1][0]][1]*bts[SrcDest[1][1]][0])))/(((bts[SrcDest[0][0]][0]-bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][1]-bts[SrcDest[1][1]][1]))-((bts[SrcDest[0][0]][1]-bts[SrcDest[1][1]][0])*(bts[SrcDest[1][0]][0]-bts[SrcDest[1][1]][0])))]
(((bts[SrcDest[0][0]][0]-bts[SrcDest[0][1]][0])*(bts[SrcDest[1][0]][1]-bts[SrcDest[1][1]][1]))-((bts[SrcDest[0][0]][1]-bts[SrcDest[1][1]][0])*(bts[SrcDest[1][0]][0]-bts[SrcDest[1][1]][0])))
###############H:We should know all distances between every couple BTSs
BTSCount=len(bts.keys())
d = [[0 for x in range(BTSCount)] for y in range(BTSCount)]
for i in bts.keys():
    for j in bts.keys():
        d[i-1][j-1]=math.sqrt(((bts[i][0]-bts[j][0])**2)+((bts[i][1]-bts[j][1])**2))
        #print(d[i-1][j-1])
###############
###############H:We should know all distances between every node and the conjunction
print("TTTTTTTTTTTTTTTTTTTTT")
BTSCount=len(bts.keys())
dToConj = [0 for x in range(BTSCount)]
for i in bts.keys():
    dToConj[i-1]=math.sqrt(((bts[i][0]-o[0])**2)+((bts[i][1]-o[1])**2))
    #print(dToConj[i-1])
###############
h1_var=LpVariable.dicts("H1",[1],0,100)
h2_var=LpVariable.dicts("H2",[1],0,100)
l_var=LpVariable.dicts("Li_f",[(i,f) for i in flows.keys() for f in flows[i]],0,100)
a_var=LpVariable.dicts("A_i",[(i) for i in bts.keys()],0,1,LpBinary)
b_var=LpVariable.dicts("B_i",[(i) for i in bts.keys()],0,1,LpBinary)

#prob=LpProblem("Facility",LpMinimize)
prob=LpProblem("Facility",LpMaximize)

prob+=h1_var[1]+h2_var[1]
######################################### constriant 1    
for i in flows.keys():
    t=h1_var[1]+h2_var[1]+lpSum(l_var[(i,f)] for f in flows[i])<=L_star[i-1]
    #print (t)
    prob+=t
######################################### constriant 2    
for i in bts.keys():
    cando=1
    for f in flows.keys():
        if i in flows[f]:
            cando=0
            break
    if cando:
        t=a_var[i]+b_var[i]<=1
        #print (t)
        prob+=t
######################################### constriant 3
t=lpSum(a_var[(i)] for i in bts.keys())==1
#print (t)
prob+=t
######################################### constriant 4
t=lpSum(b_var[(i)] for i in bts.keys())==1
#print(t)
prob+=t
######################################### constriant 5_1
t=lpSum(a_var[(i)]*d[SrcDest[0][0]-1][i-1] for i in bts.keys())==l_var[1,SrcDest[0][0]]
#print(t)
prob+=t
######################################### constriant 5_2
t=lpSum(a_var[(i)]*d[i-1][SrcDest[1][1]-1] for i in bts.keys())==l_var[2,SrcDest[1][1]]
#print(t)
prob+=t
######################################### constriant 6_1
t=lpSum(b_var[(i)]*d[i-1][SrcDest[0][1]-1] for i in bts.keys())==l_var[1,flows[1][1]]
#print(t)
prob+=t
######################################### constriant 6_2
t=lpSum(b_var[(i)]*d[SrcDest[1][0]-1][i-1] for i in bts.keys())==l_var[2,flows[2][0]]
#print(t)
prob+=t
######################################### constriant 7_1
t=lpSum(a_var[(i)]*dToConj[i-1] for i in bts.keys())==h1_var
#print(t)
prob+=t
print("*************")
######################################### constriant 7_2
t=lpSum(b_var[(i)]*dToConj[i-1] for i in bts.keys())==h2_var
#print(t)
prob+=t


######################################### constriant 8
# I JUST ADDED The following CONSTRAINT: If any of the nodes might be the source or destination, it has to be excluded from the intermediate nodes selected. So. A_i for i=1,2,3,4 shall be all zero
# I JUST ADDED The following CONSTRAINT: If any of the nodes might be the source or destination, it has to be excluded from the intermediate nodes selected. So. B_i for i=1,2,3,4 shall be all zero
t=lpSum(a_var[(i)] for i in flows[1])+lpSum(a_var[(i)] for i in flows[2])==0
#print (t)
prob+=t
t=lpSum(b_var[(i)] for i in flows[1])+lpSum(b_var[(i)] for i in flows[2])==0
#print (t)
prob+=t

######################################### constriant 9
#each node can just find an intermediate node within its access range (Dmax)
for i in flows.keys():
    for j in flows[i]:
        t=l_var[(i,j)]<=Dmax
        print (t)
        prob+=t

#################print THE PROBLEM#####################
print(prob)

#################SOLVE#####################
prob.writeLP("model0.lp")
prob.solve()
print("Status:", LpStatus[prob.status])
for vv in prob.variables():
    print(vv.name, "=", vv.varValue, "\tReduced Cost =",vv.dj)
print("objective=", value(prob.objective))
print("\nSensitivity Analysis\nConstraint\t\tShadow Price\tSlack")
for name, cc in list(prob.constraints.items()):
    print(name, ":", cc, "\t", cc.pi, "\t\t", cc.slack)


if LpStatus[prob.status]!="Optimal":
    exit(0)

#START PLOTTING ALL THE RESULTS

for x in range(1, numberofBTSs):
    if x==flows[1][0]:
        plt.plot([bts[x][0]],[bts[x][1]],'r^',label=x)
    elif x==flows[1][1]:
        plt.plot([bts[x][0]],[bts[x][1]],'r^',label=x)
    elif x==flows[2][0]:
        plt.plot([bts[x][0]],[bts[x][1]],'bs',label=x)
    elif x==flows[2][1]:
        plt.plot([bts[x][0]],[bts[x][1]],'bs',label=x)
    else:
        plt.plot([bts[x][0]],[bts[x][1]],'go',label=x)

if LpStatus[prob.status]=="Optimal":
    print("dfss")

#Find an intermesiate node that has A_i=1 and B_i=1
for vv in prob.variables():
    if (vv.name[:2]=="A_" and vv.varValue==1):
        a_ii=int(vv.name[4:len(vv.name)])
        plt.plot([bts[a_ii][0]],[bts[a_ii][1]],'yo',markersize=10)

for vv in prob.variables():
    if (vv.name[:2]=="B_" and vv.varValue==1):
        b_ii=int(vv.name[4:len(vv.name)])
        plt.plot([bts[b_ii][0]],[bts[b_ii][1]],'ro',markersize=10)
        
#plot the lines

#plt.plot(bts[flows[1][0]],bts[a_i])
plt.plot([bts[flows[1][0]][0],bts[a_ii][0]],[bts[flows[1][0]][1],bts[a_ii][1]])

#plt.plot(bts[a_ii],bts[flows[2][1]])
plt.plot([bts[a_ii][0],bts[flows[2][1]][0]],[bts[a_ii][1],bts[flows[2][1]][1]])


#plt.plot(bts[a_ii],bts[b_ii])
plt.plot([bts[a_ii][0],bts[b_ii][0]],[bts[a_ii][1],bts[b_ii][1]])


#plt.plot(bts[b_ii],bts[flows[1][1]])
plt.plot([bts[b_ii][0],bts[flows[1][1]][0]],[bts[b_ii][1],bts[flows[1][1]][1]])

#plt.plot(bts[b_ii],bts[flows[2][0]])
plt.plot([bts[b_ii][0],bts[flows[2][0]][0]],[bts[b_ii][1],bts[flows[2][0]][1]])

#plt.plot([1,1],[20,20])    
plt.show()

