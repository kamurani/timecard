#!/usr/bin/python3

'''
TODO 
INTERACTIVE MODE 
- curses based display 
- shows all tasks (can 'pin' favourite ones)
- vim-like keybindings to navigate, can just press one button 'P' to punchin/out (toggles) 
- so could keep the window open in a seperate term and you can switch and just rapidly switch task 


TODO support 'today' or 'yesterday' instead of dates

TODO handle adding a shift that overlaps with another one; i.e. stops you from adding an overlapping shift
-- maybe adding an overlap, just creates one shift (i.e. extends one)


TODO sort shifts within the 'shifts' array in chronological order


TODO set 'alarms' i.e. 'clockout at 3pm today' -- doesn't actually set the shift yet (i.e. can't set things in the future)
but will somehow keep track (server?) and set it later

TODO timecard task rename "Hospital"
        Rename to:  <user input> 
     Renamed Hospital to Orderly Job. 

TODO if only one task left, that is the working task. (i.e. when no ambiguity)


TODO allow for adding shifts 
i.e. timecard add shift --start <time> --end <time> 

vs   

timecard add task "Name"



TODO timecard list:   shows current SELECTED task HIGHLIGHTED. 
                      shows currently ONGOING tasks highlighted, with different colour. 

                      also shows TOTAL HOURS for each task.

                      also shows LAST PUNCH for each task  e.g. 'today, 07:58' 

TODO timecard list --shift:
                    
                    shows a list of all shifts (by task) from the last (DEFAULT TIME) week 
                    i.e. 
                    MONDAY      12:01 - 19:00 
                    WEDNESDAY   07:00 - 17:58
                    THURSDAY
                    FRIDAY
                    etc. 
                    --
                    TOTAL HOURS 7:50
        

TODO timecard settings:     shows toggable settings graphically

                    DISPLAY TIME        24hr    | AM/PM
                    TIMEZONE            DEFAULT | MANUAL

                    SAVE

                
TODO support for:
timecard punch 
<adds punch for current working one> 
BUT, could also do
timecard punch "Taskname" 
# so you don't have to keep switching to it...



'''

# use:  (SHELL VERSION)
# 
# $ timecard "work"
# WORK> punch
# Punched in for WORK at <time>. 
# WORK> punch
# Punched out for WORK at <time>. 
# WORK> q 
# $ timecard "something else"
#


# TODO add ability to add punch in future 
# TODO add ability to add punch in past (i.e. if you forgot to add it)

'''
$ timecard 
 
# starts with last used working task 
Hospital work> punch
Clocked in. 
Hospital work> task 

# lists tasks (colour coded based on if they were done today, in progress, or not in progress)
# can tab through 
Programming     BINFSOC     Gym     

Hospital work> task "Programming"
Change task to "Programming"
Programming> punch
Clocked into Programming at <time>. 

# DEFAULT setting:  when you switch task, it automatically clockpis out of it (if you were already
# clocked in).  Can disable this in settings.
Programming> exit
$ 

'''

'''
Argument version
'''

'''
PUNCH COMMAND
$ timecard punch
Clocked in to <DEFAULT TASK> at <TIME>. 

$ timecard punch [TASK]
'''


# timecard --working-task 
# Current task:  Hospital work 
# timecard add punch 
# Clocked in to Hospital work at <time>. 
# timecard add punch 
# Clocked out of Hospital work at <time>. 
# timecard add shift
# DATE           today
# START TIME     now
# END TIME       - 

# # above are the default values, can use arrow keys to fill it in. 

# timecard add task
# Name: <name of task>
# <other attributes, can think of these later>
# Added '<name of task>' to list of tasks 
# timecard list tasks 
# <prints list of tasks> 
# timecard list shifts "Hospital work"
# <prints list of shifts for task 'Hospital work'> 

# 

# timecard view tasks
# <prints out graphic display of all tasks by month (each block is a day worked or not), or by day (shows blocks as hours worked) 
# can press button to toggle views; and in each view, can scroll back and forth (i.e. by month, or via .....)

from mando import command, main

from datetime import datetime
from datetime import timezone
from datetime import timedelta

import sys
import json


'''
Constants
'''
PROGRAM_NAME = 'timecard'
DEFAULT_COMMAND = 'shell'

OUTPUT_FILE = 'log.json'
METADATA_FILE = 'metadata.json'

DEFAULT_PROMPT = '>'

TASK_NAME = 'name'
TASK_SHIFTS = 'shifts'
TASK_CLOCKIN = 'clockin_time'

COMMAND_PUNCH = "punch"

'''
Metadata
'''
CURRENT_WORKING_TASK = "current_working_task"




'''
TODO make 'timecard task' == 'timecard list' 
'''


'''
Classes
'''

class Task(dict):

    name = ""
    shifts = []
    clockin_time = None     # None if not currently clocked in

    def __init__(self, name, shifts=[], clockin_time=None):
        self.name = name
        self.shifts = shifts
        self.clockin_time = clockin_time

    def get_name(self):
        return self.name
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def add_shift(self, shift): 
        self.shifts.append(shift)
    
    def get_clockin_time(self):
        return self.clockin_time

    def is_current(self):
        return self.clockin_time is not None

        '''TODO maybe let class handle the clockin 'is current' checks?'''

    def clockin(self):
        self.clockin_time = datetime.now()

        
    def clockout(self):
        # Store shift, then reset clockin_time
        clockout_time = datetime.now()

        shift = Shift(self.clockin_time, clockout_time)
        self.add_shift(vars(shift))
        self.clockin_time = None



class Shift(dict):


    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def get_duration(self):
            duration = self.end - self.start 
            return duration

    

'''
class shift(dict):

    def __init__(self, start, end=None):
        self.start = start
        self.end = end
    
    def __getattr__(self, attr):
        return self[attr]

    def get_delta(self):

        duration = self.end - self.start
        duration = datetime.now()
        return divmod(duration.total_seconds(), 3600)[0] 
'''

''' TODO
class Foo(dict):
    def __init__(self):
        pass
    def __getattr__(self, attr):
        return self[attr]
'''


# UTIL FUNCTIONS
# -------------------------------

'''
Write to file
'''
def write_shift(data):

    
    json.dumps(data, indent=4)

'''
Get most recent working task TODO
'''
def get_last_task():
    return None






def get_default_task():
    return "Task"


def make_task_from_dict(task_dict):
    
    name = task_dict[TASK_NAME]
    clockin_time = task_dict[TASK_CLOCKIN]
    shifts = task_dict[TASK_SHIFTS]

    task = Task(name, shifts, clockin_time)
    return task






'''
Global variables
'''
tasks = {}
metadata = {}
current_task = get_last_task()


'''
Get current task
'''
def current_task():
    global metadata

    if CURRENT_WORKING_TASK in metadata: 
        return metadata[CURRENT_WORKING_TASK] 

     
    return None

def set_current_task(task):
    global metadata
    metadata[CURRENT_WORKING_TASK] = task

'''
Initialise
'''
def initialise():
    global tasks
    global metadata

    with open(OUTPUT_FILE, "r") as read_file:
        tasks = json.load(read_file, object_hook=object_hook)
    
    with open(METADATA_FILE, "r") as read_file:
        metadata = json.load(read_file)

    

'''
Save data 
'''
def finish():
    
    write_tasks()
    write_metadata()


'''
Encoder for datetime
'''
def default(obj):
    if isinstance(obj, datetime):
        return { '_isoformat': obj.isoformat() }
    raise TypeError('...')

'''
Decoder for datetime
'''
def object_hook(obj):
    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return datetime.fromisoformat(_isoformat)
    return obj

'''
Save edits to file
'''
def write_tasks():

    global tasks
    with open(OUTPUT_FILE, "w") as write_file:
        json.dump(tasks, write_file, default=default)

'''
Save metadata to file
'''
def write_metadata():
    global metadata 
    with open(METADATA_FILE, "w") as write_file:
        json.dump(metadata, write_file)


@command
def punch(task):
    '''Clock in or out of a task at the current time.

    Add new punch for a task at the current time.  The punch is added for the current working task by default if no task name is specified.

    :param task: Name of task to add punch for.
    '''
    
    initialise()
    global metadata
    global tasks

    if task is None:
        task = current_task()

    elif task not in tasks:
        print ('No task called {}.'.format(task))
        return
    
    #task.addPunch()
    #task.print_punch()

    # task.clock_in()
    # or 
    # task.clock_out()
    '''
    TODO make more robust object types for 'task'
    '''

    name = task

    if name is None:
        print ("No selected task.")
        return

    '''
    print ("TASKS:")
    print (tasks)
    print ("NAME")
    print (name)
    '''

    task_dict = tasks[name]

    '''
    print ("TASK DICT:")
    print (task_dict)
    '''


    ''' TODO Make Task object from dict '''
    task = make_task_from_dict(task_dict)       # TODO avoid doing this
    
    #print ('TASK:')
    #print (vars(task))

    # Check if we are currently clocked out
    if task.is_current():
        # Clock out
        direction = 'out'
        task.clockout()

        task.add_shift


    else:
        # Clock in
        direction = 'in'
        task.clockin() 

        '''TODO: put this in the Task() class; i.e. just do 'task.punch' '''

    '''  
    print ("AFTER...")
    print ("TASK:")
    print (vars(task))
    '''

    tasks[name] = vars(task)

    '''
    print ("tasks[name]: ")
    print (tasks[name])
    '''
    


    now = datetime.now()
    current_time = now.strftime("%H:%M")
    punchtime = current_time

    print ('{}: Clocked {} at {}.'.format(task.get_name(), direction, punchtime))

    finish()

    # punch.print()


@command
def undo():
    '''Undo recent punch.

    Removes last punch made (clock in / out).

    '''
    pass

@command
def list():
    '''List all tasks.

    Shows list of all tasks.
    '''
    initialise()
    global tasks

    if tasks:
        print("TASKS")
        print("-------------------")



        for key in tasks.keys():
            
            indent = " > " if key == current_task() else "   "
            print (indent + key)
        '''
        TODO more elegant way of printing this.
        TODO highlight (with curses) the selected task
        TODO can press tab to cycle through and then press enter to select; or Q to quit without selecting anything
        '''
    else:
        print("No tasks.")


'''
TODO: avoid having to use flags to signify; e.g. should intelligently understand if you give it an integer, you mean how many days back. 
'''
@command
def shift(task, start=None, end=None, back=None, all=False):
    '''Display shifts.
    
    Shows previous shifts logged for a particular task in the specified range.  Default is the last 7 days. 

    :param task: Name of task to show shifts for. 
    :param -s, --start: Start date for range of shifts.
    :param -e, --end: End date for range of shifts.
    :param -b, --back: Number of days in the past to show shifts from.
    :param -a, --all: Show shifts for all tasks.  
    '''

    

    if start is None:

        # Ignore start times 
        pass

    else:

        if back:

            time_back = back

    



    # TODO can say '7 days' or '7d' to show shifts just since then. 
    




# TODO archive the task (not lost forever)
# TODO autocomplete the names of tasks 
# TODO make 'task' and 'all' mutually exclusive 
@command
def remove(task, all=False):
    '''Remove a task. 

    :param task: Name of task to be removed.
    :param -a, --all: Remove all tasks.
    '''

    global tasks 
    initialise()

    if not tasks:
        print("No tasks to remove.")

    elif all:
        tasks.clear()
        print ('Removed all tasks.')
        set_current_task(None)
    elif task is not None: 
        
        if (task in tasks):
            tasks.pop(task)
            print ('Removed {}.'.format(task))

            curr = current_task()
            if curr == task:
                set_current_task(None)
        else:
            print ('No task called {}.'.format(task))
       
    
    finish()





@command
def shell(arg=False, verbose=False):
    prompt = DEFAULT_PROMPT
    print (prompt)

'''
TODO add more elgant way of doing 'timecard add shift' vs 'timecard add task' 
TODO allow for argument-only input for adding a shift (with datetime syntax); but also
allow for prompting 
i.e. 

$ timecard add -s -i
Adding shift to <working task name>:
START
---------
YEAR 2021
MONTH ---
DAY 

END
---------
YEAR 2021
MONTH --
DAY 
''' 

@command
def add(name, start=None, end=None):
    '''Add a new task to track.

    Add a new task to be logged.

    :param name: Name of task to be added. 
    :param -s, --start: Start time of shift to be added.
    :param -e, --end: End time of shift to be added.
    '''

    global tasks
    initialise()


    #print (datetime.today())

    '''
    shift = Shift("s", "a")

    print(shift.start)
    print(shift.end)
    '''

    if start: 

        # Add new shift
        if name in tasks:
            
            task = tasks[name]
            task = make_task_from_dict(task) 
            
            shift = Shift(start, end)
                        
            task.add_shift(vars(shift))
            #task['shifts'].append(vars(shift))

            #print ('TASK:')
            #print (vars(task))

            print('{}: Added shift from {} to {}.'.format(name, start, end))

        else:
            print('Task {} does not exist.'.format(name))

    else:


        # Add new task
        if name in tasks:
            print ('Task "{}" already exists.'.format(name))
            return
        else:
            task = Task(name)
            tasks[name] = vars(task)

    # DEBUG
    finish()
    

    


    

'''
TODO just typing 'task' will show list of tasks
'''
@command
def task(name, new=False):
    '''Switch task.

    Change to a different working task. 

    :param name: Name of the task
    :param -n, --new: Create new task and switch to it
    '''

    # timecard task "Taskname"
    # No task "Taskname". 
    # timecard task -n "Taskname"
    # creates task and then switches to it

    global tasks
    global metadata
    initialise()

    if name in tasks:

        if name == current_task():
            print ("Already on task {}.".format(name)) 
        else:
            print ("Switched task to {}.".format(name))
            metadata[CURRENT_WORKING_TASK] = name

    else:
        if new:
            ''' TODO '''
            print ("Creating new task...")
        else:
            print ('No task called "{}".  Create it using {} add "{}".'.format(name, PROGRAM_NAME, name))
        

    finish()
    


    





@command
def status(task):
    '''Show status of a given task.

    Show status of a given task.  The task shown is the current working task by default if no task name is specified. 

    :param task: Name of task to show status for. 

    '''

    pass 
    #TODO

'''
$ timecard view --ongoing 
# just show all tasks that are currently on
'''
@command
def view():
    '''Graphically display tracked tasks.

    Graphically display tracked tasks.  Can be specified to show only tasks that are currently active. 
    Can show tasks by month or by day, and can be scrolled. 

    '''

'''
Handle command line arguments
'''
'''
Default command
'''
# If no command specified, run default command (shell)
if not sys.argv[1:]:
    sys.argv.append(DEFAULT_COMMAND)


# 'punch' without task name should add punch for current working task
if sys.argv[1] == COMMAND_PUNCH:
    
    if not sys.argv[2:]:
        sys.argv.append(current_task())


'''
Main function
'''


if __name__ == "__main__":
    main()
