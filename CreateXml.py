import xml.etree.ElementTree as ET
from lxml import etree
import random
import os

platform = ET.Element('platform')
platform.set('version', '4.1')

amount_workers = 10

amount_tasks = 1000

#host: string

class Worker:
  def __init__(self, host):
    self.name = host

#nr: string
#task_size: int
#comunication_size: int
#can_split_data: bool
#can_split_comunication: bool

class Task:
    def __init__(self, nr, task_size, comunication_size, can_split_data, can_split_comunication):
        self.nr = nr
        self.task_size = task_size
        self.comunication_size = comunication_size
        self.can_split_data = can_split_data
        self.can_split_comunication = can_split_comunication

    def get_string(self):
        return self.nr + "," + str(self.task_size) + "," + str(self.comunication_size) + "," + str(self.can_split_data) + "," + str(self.can_split_comunication)

#setting up main server node
actor = ET.SubElement(platform, "actor")
actor.set('host', 'Server')
actor.set('function', 'master')


#setting up tasks to be done/ arguments for main server node
argument= ET.SubElement(actor, "argument")
argument.set('value', str(amount_tasks)) # amount of tasks

argument = ET.SubElement(actor, "argument")
argument.set('value', '25000000000') # 25.000 million flop task size should tak around 12 sec for a node 

argument = ET.SubElement(actor, "argument")
argument.set('value', '10000000') # is in bits so 10 million bits comunication cost or 10 megabites

#setting op nodes and add arguments to nodes here also
for x in range(0,amount_tasks):
    temp_task = Task(str(x), 25000000000, 10000000, False, False)
    argument = ET.SubElement(actor, "argument")
    argument.set('value', temp_task.get_string())

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
# Here i want to create a list of tuples that contains the number of cores, the GFLOPS pr core and the probability weight
# This list is based on the data from Seti@home the probability weights in the the tuples are calculated based on the number of computers that have the individual specs.

computer_data = [
    ('6.00','6,29',0.0009755304447),
    ('16.00','6,18',0.001219413056),
    ('16.00','6,09',0.0008129420372),
    ('8.00','5,99',0.005690594261),
    ('4.00','5,92',0.001625884074),
    ('4.00','5,83',0.003089179741),
    ('6.00','5,73',0.00284529713),
    ('4.00','5,71',0.001463295667),
    ('8.00','5,58',0.0009755304447),
    ('8.00','5,53',0.005690594261),
    ('6.00','5,51',0.002764002927),
    ('8.00','5,47',0.00349565076),
    ('16.00','5,46',0.004308592797),
    ('31.45','5,42',0.004715063816),
    ('8.00','5,42',0.005934476872),
    ('8.00','5,4',0.003658239168),
    ('6.00','5,4',0.0008129420372),
    ('8.00','5,4',0.002194943501),
    ('12.00','5,38',0.002032355093),
    ('6.00','5,35',0.003089179741),
    ('16.00','5,35',0.001544589871),
    ('15.65','5,34',0.01154377693),
    ('23.42','5,32',0.01073083489),
    ('4.00','5,29',0.001544589871),
    ('4.00','5,28',0.001463295667),
    ('4.00','5,28',0.004471181205),
    ('6.00','5,27',0.001951060889),
    ('23.00','5,26',0.0009755304447),
    ('8.00','5,26',0.000894236241),
    ('15.66','5,26',0.006259653687),
    ('17.17','5,22',0.01056824648),
    ('16.00','5,2',0.001138118852),
    ('12.00','5,18',0.00284529713),
    ('11.87','5,15',0.007722949354),
    ('16.00','5,11',0.001788472482),
    ('16.00','5,09',0.001056824648),
    ('16.00','5,07',0.000894236241),
    ('4.00','5,05',0.003333062353),
    ('6.00','5,01',0.003251768149),
    ('7.98','5',0.0195919031),
    ('32.00','4,99',0.001707178278),
    ('11.82','4,98',0.002764002927),
    ('12.00','4,96',0.0008129420372),
    ('6.00','4,95',0.0008129420372),
    ('16.00','4,87',0.001219413056),
    ('6.00','4,87',0.005609300057),
    ('15.93','4,87',0.01585236973),
    ('4.00','4,87',0.002276237704),
    ('4.00','4,86',0.001463295667),
    ('11.96','4,86',0.02528249736),
    ('4.00','4,85',0.004471181205),
    ('8.00','4,84',0.002520120315),
    ('4.00','4,82',0.001625884074),
    ('12.00','4,82',0.003983415982),
    ('12.00','4,79',0.001463295667),
    ('11.95','4,79',0.02804650028),
    ('6.00','4,78',0.0008129420372),
    ('12.00','4,77',0.002194943501),
    ('12.00','4,77',0.00130070726),
    ('8.00','4,76',0.000894236241),
    ('16.00','4,75',0.0008129420372),
    ('7.71','4,74',0.001951060889),
    ('7.88','4,74',0.01877896106),
    ('6.00','4,73',0.00414600439),
    ('19.00','4,72',0.0008129420372),
    ('8.00','4,7',0.002357531908),
    ('4.00','4,7',0.004715063816),
    ('20.00','4,7',0.001219413056),
    ('4.00','4,7',0.005040240631),
    ('15.20','4,69',0.001219413056),
    ('19.55','4,68',0.001788472482),
    ('12.00','4,68',0.002438826112),
    ('12.00','4,67',0.003170473945),
    ('4.00','4,66',0.002520120315),
    ('8.00','4,66',0.0009755304447),
    ('23.09','4,64',0.001869766686),
    ('6.00','4,63',0.01138118852),
    ('11.86','4,6',0.003414356556),
    ('15.75','4,6',0.002601414519),
    ('4.05','4,58',0.006828713113),
    ('7.98','4,55',0.02731485245),
    ('11.95','4,54',0.009186245021),
    ('58.00','4,53',0.00130070726),
    ('31.48','4,53',0.007153889928),
    ('4.00','4,52',0.006828713113),
    ('7.96','4,49',0.02024225673),
    ('16.00','4,48',0.005609300057),
    ('7.98','4,46',0.003333062353),
    ('4.00','4,46',0.006910007316),
    ('18.55','4,45',0.000894236241),
    ('4.00','4,44',0.002276237704),
    ('16.00','4,43',0.0008129420372),
    ('4.00','4,42',0.001788472482),
    ('7.60','4,41',0.0008129420372)


]

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
    "0 1\n25 1\nLOOPAFTER 35",  
    "0 1\n10 1\nLOOPAFTER 35",  
    "0 1\n20 1\nLOOPAFTER 45"   
    
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
host.set('speed', '980950.0Mf') #980.95 gigaflpos pr core (would very likely be a lot lower)
host.set('core', '32') #number of cores for the server host
#host.set('speed_file', 'availabilityFile.txt') # availability_file (speed_file) attribute :-D 
#host.set('state_file', 'hostState.txt') # state_file attribute :-D 
#the above speed file and state file is only set for the server host. they are generated later in this file.

#setup hosts and links
for x in range(0, amount_workers):
    temp_worker = Worker("Worker" + str(x))
    host = ET.SubElement(zone, "host")
    host.set('id', temp_worker.name)
    # Here i want to randomly select a tuple from the computer_data list based on the probabilities
    selected_cores, selected_gflops, weight = random.choices(computer_data)[0]
    host.set('speed', selected_gflops) #4the GFLOPS from the random tuple
    host.set('core', selected_cores) #number of cores from the random tuple 
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
link.set('bandwidth_file', 'bandwidth.txt' )

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