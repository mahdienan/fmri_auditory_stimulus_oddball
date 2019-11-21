#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written by mahdi@unimaas 2019
# audio library support: ['sounddevice', 'pyo', 'pygame', ]

import time, random, math
from datetime import datetime
from psychopy import sound, gui, visual, core, data, event, logging, clock


# create logfile
filename = "logfile_{}.txt".format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
logfile = open(filename, "a+")

# define variables
TRIAL_SIZE = 60
BLOCK_SIZE = 5
STIMULUS_DURATION = 0.05
INTER_BLOCK_INTERVAL = 0.5
INTER_STIMULUS_INTERVAL = 0.15

TR_LENGTH = 1.5

STANDARD_SEQ = "AAAAA"
DEVIANT_SEQ = "AAAAB"

# generate auditory blocks and randomize their order 
condition1 = [[STANDARD_SEQ]*BLOCK_SIZE for i in range(int(TRIAL_SIZE*0.8))] + [[STANDARD_SEQ]*(BLOCK_SIZE-1) + [DEVIANT_SEQ] for i in range(int(TRIAL_SIZE*0.2))]
condition2 = [[DEVIANT_SEQ]*BLOCK_SIZE for i in range(int(TRIAL_SIZE*0.8))] + [[DEVIANT_SEQ]*(BLOCK_SIZE-1) + [STANDARD_SEQ] for i in range(int(TRIAL_SIZE*0.2))]
random.shuffle(condition1)
random.shuffle(condition2)

# execute a sequence of 5 sounds.
def execute_block(sound_seq):
    start_time = time.time()
    msg = "[{}] block='".format(datetime.now().strftime("%d_%m_%Y_%H:%M:%S:%f"))
    for block in range(BLOCK_SIZE):
        msg += "{}".format(sound_seq[block])
        for tone in sound_seq[block]:
            if tone is "A":
                sound.Sound(500, secs=STIMULUS_DURATION).play()
            elif tone is "B":
                sound.Sound(1000, secs=STIMULUS_DURATION).play()
            core.wait(INTER_STIMULUS_INTERVAL)
        core.wait(INTER_BLOCK_INTERVAL)
    end_time = time.time()
    duration = end_time - start_time
    msg += "' duration={}\n".format(time.time() - start_time)
    print(msg)
    logfile.write(msg)
    block_tick = math.floor(duration/TR_LENGTH)
    return block_tick


def run_condition(cond):
    counter = 0
    block_i = 0
    seq_i = 0

    while True:
        #event.waitKeys(keyList=['5'])
        core.wait(1.5) # simulate scanner triggers.
        counter += 1

        if counter % 10 == 0:
            block_tick = execute_block(cond[block_i])
            counter += block_tick

            block_i += 1
            block_msg = "end of block #{}\n".format(str(block_i))
            logfile.write(block_msg)
            print(block_msg)

            logfile.write("Inter-block Interval of 8.25s...\n")
            core.wait(INTER_BLOCK_INTERVAL)
            if block_i == TRIAL_SIZE:
                break


############# START OF EXECUTION #############

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=False, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0],
    blendMode='avg', useFBO=True, 
    units='height')

# create and draw fixation
fixation = visual.GratingStim(win=win, mask="cross", size=0.025, pos=[0,0], sf=0, rgb=-1)
fixation.draw()
win.flip()

# Initial delay before presenating the stimulus
#core.wait(2)

# Start the stimulus presentation
logfile.write("START OF CONDITION 1\n")
run_condition(cond=condition1)
for tick in range(6):
    event.waitKeys(keyList=['5'])
logfile.write("START OF CONDITION 2\n")
run_condition(cond=condition2)
for tick in range(6):
    event.waitKeys(keyList=['5'])
logfile.write("START OF CONDITION 1\n")
run_condition(cond=condition1)
for tick in range(6):
    event.waitKeys(keyList=['5'])
logfile.write("START OF CONDITION 2\n")
run_condition(cond=condition2)
for tick in range(6):
    event.waitKeys(keyList=['5'])

# close logfile, window and quit core module
logfile.close()
win.close()
core.quit()
