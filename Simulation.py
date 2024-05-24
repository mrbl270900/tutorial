# Copyright (c) 2010-2022. The SimGrid Team. All rights reserved.          

# This program is free software; you can redistribute it and/or modify it
# under the terms of the license (GNU LGPL) which comes with this package. 

# ##################################################################################
# Take this tutorial online: https://simgrid.org/doc/latest/Tutorial_Algorithms.html
# ##################################################################################

from simgrid import Actor, Engine, Mailbox, this_actor, Link, Host
import time
import sys
import random

# task obj
class Task:
  def __init__(self, tasknr, computing_cost, communication_cost, can_data_split, time_started = None):
    self.tasknr = tasknr
    self.computing_cost = computing_cost
    self.communication_cost = communication_cost
    self.time_pased = 0
    self.time_started = time_started
    self.can_data_split = can_data_split
  def set_time_pased(self):
    self.time_pased = e.clock - self.time_started
  def set_time_started(self):
    self.time_started = e.clock

def sort_full_size(val):
  return val.computing_cost + val.communication_cost

class Request_For_Task: #can add data about node here
   def __init__(self, mailbox, speed, link_speed,):
      self.mailbox = mailbox
      self.speed = speed
      self.link_speed = link_speed

class Request_With_Task_Done:
   def __init__(self, mailbox, task, speed, link_speed,): 
      self.mailbox = mailbox
      self.task = task # as the class task
      self.speed = speed
      self.link_speed = link_speed

class Request_With_Task_Done_No_New_Task:
  def __init__(self, mailbox, task):
    self.mailbox = mailbox
    self.task = task # as the class task

class Time:
  def get_time():
    return e.clock

def computing_cost_sort(e):
  return e.computing_cost

def tasknr(e):
  return e.tasknr

def get_task(data, alg, sent_tasks, tasks, low_low, med_low, high_low, low_med, med_med, high_med, low_high, med_high, high_high):
  if alg == "catagory":
    this_actor.info("data.speed "+ str(data.speed) + "  data.link_speed " + str(data.link_speed))
    #logic for chosing task for worker
    #find right task if avalibul if not give close task
    task = None
    done = False
    while not done:
      if data.link_speed < 30000001 and data.speed < 4700000001 and len(low_low) > 0:
        this_actor.info("lowlow")
        task = low_low[0]
        low_low.remove(low_low[0])
        done = True
      elif data.link_speed < 30000001 and data.speed < 5200000001 and len(med_low) > 0:
        this_actor.info("medlow")
        task = med_low[0]
        med_low.remove(med_low[0])
        done = True
      elif data.link_speed < 30000001 and data.speed > 5200000000 and len(high_low) > 0:
        this_actor.info("highlow")
        task = high_low[0]
        high_low.remove(high_low[0])
        done = True
      elif data.link_speed < 65000001 and data.speed < 4700000001 and len(low_med) > 0:
        this_actor.info("lowmed")
        task = low_med[0]
        low_med.remove(low_med[0])
        done = True
      elif data.link_speed < 65000001 and data.speed < 5200000001 and len(med_med) > 0:
        this_actor.info("medmed")
        task = med_med[0]
        med_med.remove(med_med[0])
        done = True
      elif data.link_speed < 65000001 and data.speed > 5200000000 and len(high_med) > 0:
        this_actor.info("highmed")
        task = high_med[0]
        high_med.remove(high_med[0])
        done = True
      elif data.link_speed > 65000000 and data.speed < 4700000001 and len(low_high) > 0:
        this_actor.info("lowhigh")
        task = low_high[0]
        low_high.remove(low_high[0])
        done = True
      elif data.link_speed > 65000000 and data.speed < 5200000001 and len(med_high) > 0:
        this_actor.info("medhigh")
        task = med_high[0]
        med_high.remove(med_high[0])
        done = True
      elif data.link_speed > 65000000 and data.speed > 5200000000 and len(high_high) > 0:
        this_actor.info("highhigh")
        task = high_high[0]
        high_high.remove(high_high[0])
        done = True
      else:
        if data.link_speed < 30000001 and data.speed < 4700000001 and len(low_low) == 0:
          data.speed = 5200000000
        elif data.link_speed < 30000001 and data.speed < 5200000001 and len(med_low) == 0:
          data.speed = 5500000001
        elif data.link_speed < 30000001 and data.speed > 5200000000 and len(high_low) == 0:
          data.link_speed = 65000000
          data.speed = 4700000000
        elif data.link_speed < 65000001 and data.speed < 4700000001 and len(low_med) == 0:
          data.speed = 5200000000
        elif data.link_speed < 65000001 and data.speed < 5200000001 and len(med_med) == 0:
          data.speed = 5500000001
        elif data.link_speed < 65000001 and data.speed > 5200000000 and len(high_med) == 0:
          data.link_speed = 90000000
          data.speed = 4700000000
        elif data.link_speed > 65000000 and data.speed < 4700000001 and len(low_high) == 0:
          data.speed = 5200000000
        elif data.link_speed > 65000000 and data.speed < 5200000001 and len(med_high) == 0:
          data.speed = 5500000001
        elif data.link_speed > 65000000 and data.speed > 5200000000 and len(high_high) == 0:
          data.link_speed = 30000000
          data.speed = 4700000000
    tasks.remove(task)
    task.set_time_started()
    sent_tasks.append(task)
  else:
    task = tasks[0]
    task.set_time_started()
    sent_tasks.append(task)
    tasks.remove(task)

  return task

# master-begin
def master(*args):
  assert len(args) > 3, f"Actor master requires 3 parameters plus the workers' names, but got {len(args)}"
  tasks_count = int(args[0])
  compute_cost = int(args[1])
  communicate_cost = int(args[2])
  tasks = []
  sent_tasks = []
  server_mailbox = Mailbox.by_name(this_actor.get_host().name)
  server_mailbox.set_receiver(Actor.self())
  last_run_sent_tasks_check = Time.get_time()
  sending_comms = []
  not_done = True
  alg = "random"
  chunck = 3
  low_low = []
  med_low = []
  high_low = []
  low_med = []
  med_med = []
  high_med = []
  low_high = []
  med_high = []
  high_high = []

  this_actor.info("Server started")
  this_actor.info(str(tasks_count))

  #make task obj's
  for i in range(0, tasks_count):
     task_count = i + 3
     task = args[task_count].split(",")
     tasks.append(Task(int(task[0]), int(task[1]), int(task[2]), bool(task[3])))

  if alg == "small first":
    this_actor.info("alg = small first")
    tasks.sort(reverse=True ,key=sort_full_size)
  elif alg == "big first":
    this_actor.info("alg = big first")
    tasks.sort(key=sort_full_size)
  elif alg == "catagory":
    this_actor.info("alg = catagory")

    for task in tasks:
      if task.computing_cost == 1000000000 and task.communication_cost == 5000000:
        low_low.append(task)
      elif task.computing_cost == 2500000000 and task.communication_cost == 5000000:
        med_low.append(task)
      elif task.computing_cost == 5000000000 and task.communication_cost == 5000000:
        high_low.append(task)
      elif task.computing_cost == 1000000000 and task.communication_cost == 10000000:
        low_med.append(task)
      elif task.computing_cost == 2500000000 and task.communication_cost == 10000000:
        med_med.append(task)
      elif task.computing_cost == 5000000000 and task.communication_cost == 10000000:
        high_med.append(task)
      elif task.computing_cost == 1000000000 and task.communication_cost == 20000000:
        low_high.append(task)
      elif task.computing_cost == 2500000000 and task.communication_cost == 20000000:
        med_high.append(task)
      elif task.computing_cost == 5000000000 and task.communication_cost == 20000000:
        high_high.append(task)
        
  else:
    this_actor.info("alg = random sorting")
    random.shuffle(tasks)


  this_actor.info("tasks preprosesed")

  while not_done: #len(tasks) > 0 or len(sent_tasks) > 0 or len(sending_comms) > 0:
    try:
      if Time.get_time() - last_run_sent_tasks_check > 10:
        last_run_sent_tasks_check = Time.get_time()
        #check for the tasks that have been issued if not done in 60 secunds
        for task in sent_tasks:
          task.set_time_pased()
          if task.time_pased > 59:
            this_actor.info(str(task.tasknr) + " removing from sent and adding to tasks")

            if alg == "small first":
              tasks.append(task)
              tasks.sort(reverse=True ,key=sort_full_size)
            elif alg == "big first":
              tasks.append(task)
              tasks.sort(key=sort_full_size)
            elif alg == "catagory":
              tasks.append(task)
              if task.computing_cost == 1000000000 and task.communication_cost == 5000000:
                low_low.append(task)
              elif task.computing_cost == 2500000000 and task.communication_cost == 5000000:
                med_low.append(task)
              elif task.computing_cost == 5000000000 and task.communication_cost == 5000000:
                high_low.append(task)
              elif task.computing_cost == 1000000000 and task.communication_cost == 10000000:
                low_med.append(task)
              elif task.computing_cost == 2500000000 and task.communication_cost == 10000000:
                med_med.append(task)
              elif task.computing_cost == 5000000000 and task.communication_cost == 10000000:
                high_med.append(task)
              elif task.computing_cost == 1000000000 and task.communication_cost == 20000000:
                low_high.append(task)
              elif task.computing_cost == 2500000000 and task.communication_cost == 20000000:
                med_high.append(task)
              elif task.computing_cost == 5000000000 and task.communication_cost == 20000000:
                high_high.append(task)
            else:
              tasks.append(task)
              random.shuffle(tasks)

            sent_tasks.remove(task)

      if len(sending_comms) > 0:
        for comm in sending_comms:
          if comm.state_str == "FINISHED":
            this_actor.info(str(comm.state_str))
            sending_comms.remove(comm)
      
      comm_get = server_mailbox.get_async()
      comm_get.wait()
      
      if comm_get.test():
        data = comm_get.get_payload()
        this_actor.info(str(data))

        if len(tasks) > 0 and type(data) == Request_For_Task:
          worker_mailbox = Mailbox.by_name(str(data.mailbox)[8:-1])
          this_actor.info(str(worker_mailbox))
          task_chunks = []
          for x in range(0, chunck):
            task = get_task(data, alg, sent_tasks, tasks, low_low, med_low, high_low, low_med, med_med, high_med, low_high, med_high, high_high)
            this_actor.info("sending " + str(task.tasknr) + " to:" + str(data.mailbox)[8:-1])
            task_chunks.append(task)
          sending_comms.append(worker_mailbox.put_async(task_chunks, task.communication_cost))

        elif len(tasks) > 0 and type(data) == Request_With_Task_Done:
          worker_mailbox = Mailbox.by_name(str(data.mailbox)[8:-1])
          if data.task in sent_tasks:
            sent_tasks.remove(data.task)
          task_chunks = []
          for x in range(0, chunck):
            task = get_task(data, alg, sent_tasks, tasks, low_low, med_low, high_low, low_med, med_med, high_med, low_high, med_high, high_high)
            this_actor.info("sending " + str(task.tasknr) + " to:" + str(data.mailbox)[8:-1])
            task_chunks.append(task)
          sending_comms.append(worker_mailbox.put_async(task_chunks, task.communication_cost))

        elif len(tasks) == 0 and len(sent_tasks) > 0 and type(data) == Request_With_Task_Done:
          worker_mailbox = Mailbox.by_name(str(data.mailbox)[8:-1])
          if data.task in sent_tasks:
            sent_tasks.remove(data.task)
          this_actor.info("sending wait to:" + str(data.mailbox)[8:-1])
          sending_comms.append(worker_mailbox.put_async("wait", 50))

        elif type(data) == Request_With_Task_Done_No_New_Task:
          if data.task in sent_tasks:
            sent_tasks.remove(data.task)

        elif len(tasks) == 0 and len(sent_tasks) > 0:
          worker_mailbox = Mailbox.by_name(str(data.mailbox)[8:-1])
          this_actor.info("sending wait to:" + str(data.mailbox)[8:-1])
          sending_comms.append(worker_mailbox.put_async("wait", 50))

        else:
          Actor.kill_all()
          not_done = False
      else:
        this_actor.sleep_for(0.1)

    except Exception as e:
        test = "test"
        this_actor.info(f"An error occurred in server: {e}")

  this_actor.info("all taskes and workers done")
# master-end

# worker-begin
def worker(*args):
  assert len(args) == 1, "The worker expects to not get any argument"
  workers_dweel_time = int(args[0])
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
  time_started = Time.get_time()
  while not done:
    try:
      if time_started < Time.get_time() - workers_dweel_time:
        this_actor.info(str(this_actor.get_host().name) + " turning off")
        this_actor.sleep_for(30)
        time_started = Time.get_time()

      if not_asked_for_task:
        this_actor.info("I'm trying to send a request for a task")
        worker_number = Host.current().name[6: len(Host.current().name)]
        comm = server_mailbox.put_init(Request_For_Task(str(mailbox), this_actor.get_host().speed, Link.by_name(str(int(worker_number) + 1)).bandwidth), 50)
        comm.wait_for(5)
        not_asked_for_task = False
        
      else:
        comm_get = mailbox.get_async()
        comm_get.wait_for(5)
        chunked_task = comm_get.get_payload()
        this_actor.info("task got: " + str(chunked_task))

        if chunked_task == "wait":
          not_asked_for_task = True
          this_actor.sleep_for(10)

        elif chunked_task[0].computing_cost > 0: # If compute_cost is valid, execute a computation of that cost
          for task in chunked_task:
            if time_started < Time.get_time() - workers_dweel_time:
              this_actor.info(str(this_actor.get_host().name) + " turning off")
              this_actor.sleep_for(30)
              time_started = Time.get_time()
              break
            this_actor.info("running:" + str(task.tasknr))
            this_actor.execute(task.computing_cost)
            this_actor.info("done with task:" + str(task.tasknr))
            if time_started < Time.get_time() - workers_dweel_time:
              this_actor.info(str(this_actor.get_host().name) + " turning off")
              this_actor.sleep_for(30)
              time_started = Time.get_time()
              break
            worker_number = Host.current().name[6: len(Host.current().name)]
            if task == chunked_task[len(chunked_task)]:
              comm = server_mailbox.put_init(Request_With_Task_Done(str(mailbox), task, this_actor.get_host().speed, Link.by_name(str(int(worker_number) + 1)).bandwidth), 50)
              comm.wait_for(5)
              this_actor.info("asked for task")
            else:
              comm = server_mailbox.put_init(Request_With_Task_Done_No_New_Task(str(mailbox), task), 50)
              comm.wait_for(5)
            
        else: # Stop when receiving an invalid compute_cost
          done = True
          this_actor.info("Exiting now.")

    except Exception as e:
        not_asked_for_task = True
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