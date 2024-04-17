# Copyright (c) 2010-2022. The SimGrid Team. All rights reserved.          

# This program is free software; you can redistribute it and/or modify it
# under the terms of the license (GNU LGPL) which comes with this package. 

# ##################################################################################
# Take this tutorial online: https://simgrid.org/doc/latest/Tutorial_Algorithms.html
# ##################################################################################

from simgrid import Actor, Engine, Host, Mailbox, this_actor
import time
import sys

# task obj
class Task:
  def __init__(self, tasknr, computing_cost, communication_cost, time_started = None):
    self.tasknr = tasknr
    self.computing_cost = computing_cost
    self.communication_cost = communication_cost
    self.time_pased = time_started
    self.time_started = time_started if time_started is not None else time.time()
  def set_time_pased(self, time_pased):
    self.time_pased = time_pased


class Request_For_Task: #can add data about node here
   def __init__(self, mailbox):
      self.mailbox = mailbox
      this_actor.info("Request_For_Task instance created with mailbox: " + str(mailbox))

class Request_With_Task_Done:
   def __init__(self, mailbox, task): 
      self.mailbox = mailbox
      self.task = task # as the class task



# master-begin
def master(*args):
  assert len(args) > 3, f"Actor master requires 3 parameters plus the workers' names, but got {len(args)}"
  tasks_count = int(args[0])
  compute_cost = int(args[1])
  communicate_cost = int(args[2])
  pending_comms = []
  tasks = []
  sent_tasks = []
  server_mailbox = Mailbox.by_name(this_actor.get_host().name)
  server_mailbox.set_receiver(Actor.self())

  this_actor.info("Server started")
  this_actor.info(str(tasks_count))

  #make task obj's
  for i in range(0, tasks_count):
     tasks.append(Task(i, compute_cost, communicate_cost))

  this_actor.info("tasks preprosesed x")

  mailbox = Mailbox.by_name("Worker0")
  mailbox.put_init(tasks[0], 0).detach()


  while len(tasks) > 0 or len(sent_tasks) > 0:
    #this_actor.info(f"One of the following tasks or sent_tasks is larger than 0") #i am used for debugging
    if len(tasks) > 0:
      #this_actor.info(f"the length of tasks is larger than 0") #i am also used for debugging
      #if server_mailbox.ready:
      this_actor.info("mailbox ready")
      data = server_mailbox.get()
      this_actor.info(str(data))
      worker_mailbox = Mailbox.by_name(str(data.mailbox))
      this_actor.info("sending " + tasks[0].tasknr + " to:" + str(data.mailbox))
      comm = worker_mailbox.put_async(tasks[0], tasks[0].communication_cost)
      tasks[0].set_time_pased(time.time())
      sent_tasks.append(tasks[0])
      pending_comms.append(comm)
      tasks.remove(tasks[0])

    #check if task sent is done or has waited to long
    if(len(sent_tasks) > 0): # async?
       current_time = time.time()
       for task in sent_tasks:
          #this_actor.info("is tasks sent not done?")
          if current_time - task.time_started > 60: # wait time is 60 secunds
             tasks.append(task)
             sent_tasks.remove(task)

  this_actor.info("all taskes done?")

  for comm in pending_comms:
    comm.wait()

  this_actor.info("all taskes done")
# master-end

# worker-begin
def worker(*args):
  assert len(args) == 0, "The worker expects to not get any argument"
  this_actor.info("worker starting")
  this_actor.info(str(this_actor.get_host().name))
  testVariable = str(this_actor.get_host().name)
  mailbox = Mailbox.by_name(testVariable)
  mailbox.set_receiver(Actor.self())
  this_actor.info("worker mail box done")
  server_mailbox = Mailbox.by_name("Server")
  this_actor.info("server mail box done")
  done = False
  while not done:
    this_actor.info("asking for task")
    

    try:
        #if server_mailbox.ready:
        this_actor.info("I'm trying to send a request for a task'")
        comm = server_mailbox.put_async(Request_For_Task(mailbox), 50)
        this_actor.info("asked for task")
        comm.wait()
        #else:
            #this_actor.info("The server mailbox is not ready yet")
    except Exception as e:
        this_actor.info(f"An error occurred while putting async task: {e}")

    
    this_actor.info("waiting for task")
    if mailbox.ready:
      this_actor.info("task ready")
      task = mailbox.get()
      if task.computing_cost > 0: # If compute_cost is valid, execute a computation of that cost 
        this_actor.info("running:" + str(task.tasknr))
        this_actor.execute(task.computing_cost)
        #server_mailbox.put_async(Request_With_Task_Done(mailbox, task))
      else: # Stop when receiving an invalid compute_cost
        done = True
        this_actor.info("Exiting now.")

#worker-end

# main-begin
if __name__ == '__main__':
    assert len(sys.argv) > 2, f"Usage: python app-masterworkers.py platform_file deployment_file"

    e = Engine(sys.argv)

    # Register the classes representing the actors
    e.register_actor("master", master)
    e.register_actor("worker", worker)

    # Load the platform description and then deploy the application
    e.load_platform(sys.argv[1])
    e.load_deployment(sys.argv[2])

    # Run the simulation
    e.run()

    this_actor.info("Simulation is over")
# main-end