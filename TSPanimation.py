import pygame
import re
import random
import geopy.distance

def plotSchools(schools):

    for school in schools:
        list1 = school.split()
        
        x = (10.9855 + float(list1[2])) * 120.8333
        y = (55.546 - float(list1[1])) * 210.1322

        pygame.draw.rect(dis, red, [x, y, 4, 4])

def plotpaths(droneDict):
    pass


class Drone:
    def __init__(self,schoolsDict, droneDict,generation):
        Long = 53.3842125238019
        Lat = -6.60088967821164
        self.droneDict = droneDict
        self.schoolsDict = schoolsDict
        self.X = float(Lat)
        self.Y = float(Long)
        self.originPlotX = (10.9855 + float(Lat)) * 120.8333
        self.originPlotY = (55.546 - float(Long)) * 210.1322
        self.plotX = (10.9855 + float(Lat)) * 120.8333
        self.plotY = (55.546 - float(Long)) * 210.1322
        self.route = [0]
        self.totalDist = 0  
        self.generation = generation 

    def goto(self):
        
        newX = (10.9855 + float(self.X)) * 120.8333
        newY = (55.546 - float(self.Y)) * 210.1322
        
        if(abs(newX -self.plotX)<10 and abs(newY -self.plotY)<10):
            if(self.schoolsDict != {}):
               
                scoreDict = {}
                for i in self.schoolsDict:
                    dist = droneDict[str(self.route[-1]) + "to" + str(i)][0]
                    feramon = droneDict[str(self.route[-1]) + "to" + str(i)][1]
                    
                    if(dist != 0):
                        alpha = 2 *0.9**self.generation
                        beta = 0.00001 *1.01**self.generation
                        scoreDict[i] = (1/dist)*alpha+(feramon*beta)
                       

                values = scoreDict.values()
                Sum = sum(values)
                num = random.random()*Sum
                count = 0

                for x in scoreDict:
                    count += scoreDict[x]
                    if(count>num):
                        break
                    
                self.X = self.schoolsDict[x][1]
                self.Y = self.schoolsDict[x][0]
                self.route.append(x)
                self.plotX = newX
                self.plotY = newY
                self.originPlotX = newX
                self.originPlotY = newY
                del self.schoolsDict[x]
                self.totalDist = self.totalDist+droneDict[str(self.route[len(self.route)-2]) +"to" + str(self.route[len(self.route)-1])][0]

            
        else:
            self.plotX = self.plotX +(newX-self.originPlotX)*0.040
            self.plotY = self.plotY +(newY-self.originPlotY)*0.040

    def plot (self):
            pygame.draw.rect(dis, black, [self.plotX, self.plotY, 3, 3])


file1 = open('/home/user/Desktop/TSP/chn31.txt', 'r')
schools = file1.readlines()


schoolsDict = {}

for x in schools.copy():
    x = x.split()
    schoolsDict[x[0]] = [x[1],x[2]]


droneDict = {}

for i in schoolsDict:
    for j in schoolsDict:
        
        droneDict[str(i)+"to"+ str(j)] = [geopy.distance.geodesic((float(schoolsDict[i][0]),float(schoolsDict[i][1])), (float(schoolsDict[j][0]),float(schoolsDict[j][1]))).km,0]
    


mastercopySchoolsDict = schoolsDict.copy()
ants = [Drone(schoolsDict.copy(),droneDict,1) for x in range(120)]



shortestDistance = 10000
genAverage = 11000
bestPath = []

generation = 0

pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

width,height = 725,904
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Drone Optimization')
ireland_map = pygame.image.load('/home/user/Desktop/TSP/ireland_map.png')
ireland_map = pygame.transform.scale(ireland_map,(width,height))

game_over = False

clock = pygame.time.Clock()
 
while not game_over:
    dis.blit(ireland_map,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    

    

    plotSchools(schools)
 
    for ant in ants:

        ant.goto()
        ant.plot()

    
    ended = [x.schoolsDict == {} for x in ants]
    
    if(all(ended)):
        generation+=1
        
        for ant in ants:
            for i in range(len(ant.route)-1):
                path = droneDict[str(ant.route[i]) +"to" + str(ant.route[i+1])][1]
                temp = ant.totalDist
                if(temp<0):
                    temp = 1
                elif(temp>shortestDistance*(1+(0.5*0.998**generation))): #temp>7000*0.997**generation
                    temp = 0 
                else:
                    temp = (-1/(shortestDistance*(1+(0.5*0.998**generation)))*temp)+1 # temp = (-1/(7000*0.997**generation)*temp)+1
                droneDict[str(ant.route[i]) +"to" + str(ant.route[i+1])][1]+=temp
                
                

            if(len(ant.route)>=120):
                genAverage += ant.totalDist

        
            if(ant.totalDist<shortestDistance and len(ant.route)>120):
                shortestDistance = ant.totalDist
                bestPath = ant.route

        genAverage = genAverage/120

        for path in droneDict:
            droneDict[path][1] = droneDict[path][1]*0.9

        print("overall Best: ",shortestDistance, "generation Average: " ,genAverage, "generation: ", generation)
        ants = []
        for x in range(120): 
            ants.append(Drone(mastercopySchoolsDict.copy(),droneDict,generation))

    if(shortestDistance/genAverage>0.99):
        game_over = True



    
    pygame.display.update()
 
    clock.tick(10*0.9*generation)
 
pygame.quit()
bestPath.append('0')
print(bestPath)
quit()



