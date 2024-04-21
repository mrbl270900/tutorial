# Copyright (c) 2010-2022. The SimGrid Team. All rights reserved.          

# This program is free software; you can redistribute it and/or modify it
# under the terms of the license (GNU LGPL) which comes with this package. 

# ##################################################################################
# Take this tutorial online: https://simgrid.org/doc/latest/Tutorial_Algorithms.html
# ##################################################################################

from simgrid import Actor, Engine, Host, Mailbox, this_actor, ActivitySet
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

  pending_comms = ActivitySet()

  this_actor.info("Server started")
  this_actor.info(str(tasks_count))

  #make task obj's
  for i in range(0, tasks_count):
     tasks.append(Task(i, compute_cost, communicate_cost))

  this_actor.info("tasks preprosesed")

  while len(tasks) > 0:
    try:
      this_actor.info("mailbox ready")
      data = server_mailbox.get_async()
      data.wait_for(2)
      this_actor.info(str(data))
      worker_mailbox = Mailbox.by_name(str(data.sender.host))
      this_actor.info("sending " + str(tasks[0].tasknr) + " to:" + str(data.sender.host))
      task = tasks[0]
      tasks.remove(tasks[0])
      comm = worker_mailbox.put_init(task, task.communication_cost)
      comm.detach()


    except Exception as e:
        this_actor.info(f"An error occurred in server: {e}")

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
  not_asked_for_task = True
  while not done:
    try:
      if not_asked_for_task:
        this_actor.info("I'm trying to send a request for a task'")
        comm = server_mailbox.put_init(Request_For_Task(str(mailbox)), 50)
        comm.detach()
        not_asked_for_task = False
        this_actor.info("asked for task")
        
      else:
        this_actor.info("getting task")
        task = mailbox.get()
        this_actor.info("task got")
        if task.computing_cost > 0: # If compute_cost is valid, execute a computation of that cost 
          this_actor.info("running:" + str(task.tasknr))
          this_actor.execute(task.computing_cost)
          not_asked_for_task = True
          this_actor.info("done with task:" + str(task.tasknr))
          #add code for done task to server here
          
        else: # Stop when receiving an invalid compute_cost
          done = True
          this_actor.info("Exiting now.")

    except Exception as e:
        this_actor.info(f"An error occurred in worker: {e}")

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