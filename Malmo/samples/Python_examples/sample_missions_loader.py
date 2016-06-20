# --------------------------------------------------------------------------------------------------------------------
# Copyright (C) Microsoft Corporation.  All rights reserved.
# --------------------------------------------------------------------------------------------------------------------
# Sample mission loader
# Used to check the mission repository

import MalmoPython
import os
import sys
import time
import random

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

# -- set up the mission -- #
#mission_file_no_ext = '../Sample_missions/default_world_1'                 # Survive and find gold, diamond or redstone!
#mission_file_no_ext = '../Sample_missions/default_flat_1'                  # Move to a wooden hut in a snow tempest!
mission_file_no_ext = '../Sample_missions/tricky_arena_1'                  # Mind your step to the redstone! 
#mission_file_no_ext = '../Sample_missions/eating_1'                        # Eat a healthy diet! 
#mission_file_no_ext = '../Sample_missions/cliff_walking_1'                 # Burning lava! 

#mission_file_no_ext = '../Sample_missions/mazes/maze_1'                    # Get a-mazed! A simple maze.
#mission_file_no_ext = '../Sample_missions/mazes/maze_2'                    # Get more a-mazed! A complex maze.

#mission_file_no_ext = '../Sample_missions/classroom/basic'                 # Grab the treasure! Single small room
#mission_file_no_ext = '../Sample_missions/classroom/obstacles'             # The apartment! Some rooms
#mission_file_no_ext = '../Sample_missions/classroom/simpleRoomMaze'        # Some rooms making a maze (not with maze decorator)
#mission_file_no_ext = '../Sample_missions/classroom/attic'                 # Lava, libraries, incomplete staircase, goal is in the attic
#mission_file_no_ext = '../Sample_missions/classroom/vertical'              # Need to go up
#mission_file_no_ext = '../Sample_missions/classroom/complexity_usage'      # Big rooms generator with doors, pillars, a house
#mission_file_no_ext = '../Sample_missions/classroom/medium'                # Hotel California: big rooms with doors, ladders....
#mission_file_no_ext = '../Sample_missions/classroom/hard'                  # Buckingham Palace: big rooms with doors, easy to get lost, ...


agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)
if agent_host.receivedArgument("test"):
    exit(0) # TODO: discover test-time folder names

mission_file = mission_file_no_ext + ".xml"
with open(mission_file, 'r') as f:
    print "Loading mission from %s" % mission_file
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    
# Attempt to start a mission and set the recording:
launchedMission=False
while not launchedMission:
    try:
        # Set up a recording 
        my_mission_record = MalmoPython.MissionRecordSpec(mission_file_no_ext + ".tgz")
        my_mission_record.recordRewards()
        my_mission_record.recordMP4(24,400000)
        # And attempt to start the mission:
        agent_host.startMission(my_mission, my_mission_record )
        launchedMission=True
    except RuntimeError as e:
        print "Error starting mission:",e
        exit(1)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",

total_reward = 0.0

# main loop:
while world_state.is_mission_running:
    try:
        # For manual commands on the keyboard
        #  nb = raw_input('Enter command: ')
        #  agent_host.sendCommand(nb)
        
        # Hardwired moves
        agent_host.sendCommand("move " + str(0.5*(random.random()*2-0.5)) )
        agent_host.sendCommand("pitch " + str(0.2*(random.random()*2-1)) )
#        agent_host.sendCommand("pitch -1")
#        agent_host.sendCommand("jump 1")
#        agent_host.sendCommand("attack 1")
#         agent_host.sendCommand("drop")
        agent_host.sendCommand( "turn " + str(0.5*(random.random()*2-1)) )
    except RuntimeError as e:
        print "Failed to send command:",e
        pass
    time.sleep(0.5)
    world_state = agent_host.getWorldState()
    print "video,observations,rewards received:",world_state.number_of_video_frames_since_last_state,world_state.number_of_observations_since_last_state,world_state.number_of_rewards_since_last_state
    for reward in world_state.rewards:
        print "Summed reward:",reward.value
        total_reward += reward.value
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
print "Total reward = " + str(total_reward)