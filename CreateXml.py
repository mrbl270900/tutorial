import xml.etree.ElementTree as ET
from lxml import etree

platform = ET.Element('platform')
platform.set('version', '4.1')

amount_workers = 5

class Worker:
  def __init__(self, host):
    self.name = host


#setting up main server node
actor = ET.SubElement(platform, "actor")
actor.set('host', 'Server')
actor.set('function', 'master')


#setting up tasks to be done/ arguments for main server node
argument= ET.SubElement(actor, "argument")
argument.set('value', '20')

argument = ET.SubElement(actor, "argument")
argument.set('value', '50000000')

argument = ET.SubElement(actor, "argument")
argument.set('value', '1000000')

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


platform.clear()
platform.set('version', '4.1')

zone = ET.SubElement(platform, "zone")
zone.set('id', 'zone0')
zone.set('routing', 'Full')

host = ET.SubElement(zone, "host")
host.set('id', 'Server')
host.set('speed', '98.095Mf')

#setup hosts and links
for x in range(0, amount_workers):
    temp_worker = Worker("Worker" + str(x))
    host = ET.SubElement(zone, "host")
    host.set('id', temp_worker.name)
    host.set('speed', '98.095Mf')

link = ET.SubElement(zone, "link")
link.set('id', '0')
link.set('bandwidth', '41.279125MBps')
link.set('latency', '59.904us')

for x in range(0, amount_workers):
    link = ET.SubElement(zone, "link")
    link.set('id', str(x+1))
    link.set('bandwidth', '41.279125MBps')
    link.set('latency', '59.904us')

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