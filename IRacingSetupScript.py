#V1.0

import os
import fnmatch
import datetime
import tkinter as tk
from tkinter import filedialog

downloadPath = ""
iRacingPath = ""



root = tk.Tk()
root.withdraw()
root.update()
movedSetups = 0

now = datetime.datetime.now()

# (removes ->) create log.txt
if not os.path.exists("log.txt"):
    with open("log.txt","w") as f:                                                                                                                                                          
        f.close()

else:
    with open("log.txt","a") as f:
        f.write("\n")
        f.write("\n")
        f.write(str(now.day) + str(now.month) + ": New execute \n")




#if configfile doesnt exists
if not os.path.exists("config.txt"):                                                                                                                                                    
    print("Select your download folder!")
    #open explorer for setting up downloadpath
    downloadPath = filedialog.askdirectory()                                                                                                                                            

    print('Please select your "iRacing/setups" folder!')
    #open explorer for setting up iracing/setups path
    iRacingPath = filedialog.askdirectory()                                                                                                                                             

    #save paths in configfile
    with open("config.txt","w") as f:                                                                                                                                                   
        f.write(downloadPath + "\n")
        f.write(iRacingPath)

else:
    #load paths from config.txt
    with open("config.txt","r") as f:                                                                                                                                                   
        configfile = f.read().split("\n")
        downloadPath = configfile[0]
        iRacingPath = configfile[1]


#get all setups out of "downloads"
files = fnmatch.filter(os.listdir(downloadPath), "*.sto")                                                                                                                               


#filter for matching carsetupfolder
def filteriRacingcars(carName):                                                                                                                                                         
    filteredCars = fnmatch.filter(os.listdir(iRacingPath), "*" + carName + "*")
    if filteredCars:
        return filteredCars


#for each setup in downloadfolder
for carsetup in files:                                                                                                                                                                  

    #split up the setupfilename by the first 5 "_"
    currentCar = carsetup.split("_", 4)                                                                                                                                                 


    #for each split of setupfilename
    for filepart in currentCar:                              
        
        #search for matching carsetupfolder                                                                                                                           
        if filteriRacingcars(filepart):                                                                                                                                                 
            setupfolder = filteriRacingcars(filepart)

            #Move setup to Iracing folder with changed name when already exists (day+month at the end)
            #File does already exists
            if os.path.exists(iRacingPath + "\\" + setupfolder[0] + "\\" + carsetup):
                os.rename(downloadPath + "\\" + carsetup, iRacingPath + "\\" + setupfolder[0] + "\\" + carsetup[0:len(carsetup)-4] + "_" + str(now.day) + "-" + str(now.month) + ".sto")
            
            #file does not exist
            else:
                os.rename(downloadPath + "\\" + carsetup, iRacingPath + "\\" + setupfolder[0] + "\\" + carsetup)  
            
            movedSetups = movedSetups + 1                                                             
            

            #logging moved setups
            with open("log.txt","a") as f:                                       
                #log moved files                                           
                f.write(carsetup + "\t\t\t\t" + " moved from:" + downloadPath + "\\" + carsetup + "\t\t\t\t" + " to: " + iRacingPath + "\\" + setupfolder[0] + "\\" + carsetup[0:len(carsetup)-4] + "_" + str(now.day) + "-" + str(now.month) + ".sto" + "\n")                                                                                                                                                                      #breaks when setupfolder found
        

#log amount of moved setups
with open("log.txt","a") as f:                                                                                                                                                          
    f.write("Moved setups: " + str(movedSetups))