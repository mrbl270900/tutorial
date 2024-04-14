import xml.etree.ElementTree as ET
from lxml import etree
import random
import os

platform = ET.Element('platform')
platform.set('version', '4.1')

amount_workers = 10

class Worker:
  def __init__(self, host):
    self.name = host


#setting up main server node
actor = ET.SubElement(platform, "actor")
actor.set('host', 'Server')
actor.set('function', 'master')


#setting up tasks to be done/ arguments for main server node
argument= ET.SubElement(actor, "argument")
argument.set('value', '20') # amount of tasks

argument = ET.SubElement(actor, "argument")
argument.set('value', '50000000') # 50 million flop task size 

argument = ET.SubElement(actor, "argument")
argument.set('value', '10000000') # is in bits so 10 million bits comunication cost or 10 megabites

#setting op nodes and add arguments to nodes here also
for x in range(0,amount_workers):
    temp_worker = Worker("Worker" + str(x))
    argument = ET.SubElement(actor, "argument")
    argument.set('value', temp_worker.name)

for x in range(0,amount_workers):
    temp_worker = Worker("Worker" + str(x))
    actor = ET.SubElement(platform, "actor")
    actor.set('host', temp_worker.name)
    actor.set('function', 'worker')

save_path_file = "ServerSetup.xml"

#making xml string and removing binary makings
xml_string = str(ET.tostring(platform))
xml_string = xml_string[2: len(xml_string)-1]

#making the xml have indents and newlines
root = etree.fromstring(xml_string)
Pretty_xml = etree.tostring(root, pretty_print=True).decode()

xml_string = "<?xml version='1.0'?>" + '\n' + '<!DOCTYPE platform SYSTEM "https://simgrid.org/simgrid.dtd">' + "\n" + Pretty_xml

with open(save_path_file, 'w') as f:
    f.write(xml_string)


#=========================================================================
# Here is a list of strings to put in the generated speed txt files
# all of the strings in the three lists follow the conventions listed in the SIMGRID documentation :-D
speedFile_strings = [
    "0 0.5\n2 0.3\n4 0.2\nLOOPAFTER 5",  
    "0 0.2\n2 0.5\n4 0.4\nLOOPAFTER 5",  
    "0 0.3\n2 0.2\n4 0.1\nLOOPAFTER 5"   
    
]
#=========================================================================
# Here is a list of strings to put in the generated state txt files 
stateFile_strings = [
    "0 1\n25 0\nLOOPAFTER 35",  
    "0 1\n10 0\nLOOPAFTER 35",  
    "0 1\n20 0\nLOOPAFTER 45"   
    
]
#=========================================================================
# Here is a list of strings to put in the generated bandwidth txt files
bandwidthFile_strings = [
    "0.0 40000000\n7.0 60000000\nLOOPAFTER 12",  
    "0.0 35000000\n9.0 55000000\nLOOPAFTER 12",  
    "0.0 45000000\n6.0 65000000\nLOOPAFTER 12"   
    
]

# Here we define the folder where we want to save our files
folder_path_speed = "speed-files/"
folder_path_state = "state-files/"
folder_path_bandwidth = "bandwidth-files/"

# Here we make sure not to create the folder agin if it has already been made
if not os.path.exists(folder_path_speed):
    os.makedirs(folder_path_speed)
    
    
if not os.path.exists(folder_path_state):
    os.makedirs(folder_path_state)

if not os.path.exists(folder_path_bandwidth):
    os.makedirs(folder_path_bandwidth)

platform.clear()
platform.set('version', '4.1')

zone = ET.SubElement(platform, "zone")
zone.set('id', 'zone0')
zone.set('routing', 'Full')

host = ET.SubElement(zone, "host")
host.set('id', 'Server')
host.set('speed', '980950.0Mf') #980.95 gigaflpos
#host.set('speed_file', 'availabilityFile.txt') # availability_file (speed_file) attribute :-D 
#host.set('state_file', 'hostState.txt') # state_file attribute :-D 
#the above speed file and state file is only set for the server host. they are generated later in this file.

#setup hosts and links
for x in range(0, amount_workers):
    temp_worker = Worker("Worker" + str(x))
    host = ET.SubElement(zone, "host")
    host.set('id', temp_worker.name)
    host.set('speed', '4215.0Mf') #4.215 gigaflops  
    speedFile = os.path.join(folder_path_speed, f"{temp_worker.name}-speed_file.txt")
    #speedFile = f"{temp_worker.name}-speed_file.txt"  #code to add speed_file attribute with a generated txt file for each host tags 
    host.set('speed_file', speedFile )
    speedfile_string = random.choice(speedFile_strings) # here we randomly choose a string from the list of strings
    with open(speedFile, 'w') as f:
        f.write(speedfile_string)
    
    stateFile = os.path.join(folder_path_state, f"{temp_worker.name}-state_file.txt")  #code to add state_file attribute with a generated txt file for each host tags 
    host.set('state_file', stateFile )
    statefile_string = random.choice(stateFile_strings) # here we randomly choose a string from the list of strings
    with open(stateFile, 'w') as f:
        f.write(statefile_string)
    

link = ET.SubElement(zone, "link")
link.set('id', '0')
link.set('bandwidth', '100MBps')
link.set('latency', '59.904us')
#link.set('bandwidth_file', 'bandwidth.txt' )

for x in range(0, amount_workers):
    link = ET.SubElement(zone, "link")
    link.set('id', str(x+1))
    link.set('bandwidth', '65MBps')
    link.set('latency', '9.0ms')
    bandWidthFile = os.path.join(folder_path_bandwidth, f"link{x+1}-bandWidth_file.txt")  #code to add bandwidth file attribute with a generated txt file for each host tags 
    link.set('bandwidth_file', bandWidthFile )
    bandWidthFile_string = random.choice(bandwidthFile_strings) # here we randomly choose a string from the list of strings
    with open(bandWidthFile, 'w') as f: 
        f.write(bandWidthFile_string)

route = ET.SubElement(zone, "route")
route.set('src', 'Server')
route.set('dst', 'Server')
link_ctn1 = ET.SubElement(route, "link_ctn")
link_ctn1.set('id', '0')
for x in range(0, amount_workers):
    route = ET.SubElement(zone, "route")
    route.set('src', 'Server')
    route.set('dst', 'Worker' + str(x))
    link_ctn1 = ET.SubElement(route, "link_ctn")
    link_ctn1.set('id', str(x+1))

#=============================================
#Creating txt files for host availability 
# availability_string = worker starts with a 100% power available the after 1 second it drops to 50% and then after 2 seconds drop to 20%.

availabilityFile = "availabilityFile.txt"
availability_string = "1 1\n2 0.5\n4 0.2\nLOOPAFTER 5"
with open(availabilityFile, 'w') as f:
    f.write(availability_string)
#=============================================
#=============================================
#Creating txt files for host state
# state_string = worker that is available initially and then becomes unavailable after 3 seconds.

hostStateFile = "hostState.txt"
state_string = "1 1\n4 0\nLOOPAFTER 5"
with open(hostStateFile, 'w') as f:
    f.write(state_string)
#=============================================
#=============================================
#Creating txt files for link bandwidth
#At time t = 4, the bandwidth is 40 Mb/s. At time t = 8, it raises to 60 Mb/s. At time t = 24, it drops at 40 MBps again
bandwidthFile = "bandwidth.txt"
bandwidth_string = "4.0 40000000\n8.0 60000000\nLOOPAFTER 12.0"
with open(bandwidthFile, 'w') as f:
    f.write(bandwidth_string)
#=============================================

save_path_file = "NetworkSetup.xml"

#making xml string and removing binary markings
xml_string = str(ET.tostring(platform))
xml_string = xml_string[2: len(xml_string)-1]

#making the xml have indents and newlines
root = etree.fromstring(xml_string)
Pretty_xml = etree.tostring(root, pretty_print=True).decode()

xml_string = "<?xml version='1.0'?>" + '\n' + '<!DOCTYPE platform SYSTEM "http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd">' + "\n" + Pretty_xml

with open(save_path_file, 'w') as f:
    f.write(xml_string)