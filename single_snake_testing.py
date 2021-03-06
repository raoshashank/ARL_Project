import sim
import sys
import IPython
import numpy as np
import math
import time
sim.simxFinish(-1)
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID == -1:
    sys.exit("Couldn't connect to CSim server")
else:
    print("Connected to Sim Server")


num_units = 4
t=0
speed=[5,5]
ampitude_h=[0.0,15.0]
ampitude_v=[20.0,15.0]
phase_v=[120.0,0.0]
phase_h=[60.0,0.0]
phase_cam=[180.0,180.0]
#Inputs for the function control (in radians) (also 2 sets)
A_H=[ampitude_h[0]*math.pi/180.0,ampitude_h[1]*math.pi/180.0]
A_V=[ampitude_v[0]*math.pi/180.0,ampitude_v[1]*math.pi/180.0]
P_V=[phase_v[0]*math.pi/180.0,phase_v[1]*math.pi/180.0]
P_H=[phase_h[0]*math.pi/180.0,phase_h[1]*math.pi/180.0]
P_C=[phase_cam[0]*math.pi/180.0,phase_cam[1]*math.pi/180.0]
s=0 # if s=0 we use the first set of parameters, if s=1 we use the second set of parameters


#IPython.embed()
#error_code_cam,joint_cam_handle=sim.simxGetObjectHandle(clientID,'snake_joint_cam',sim.simx_opmode_oneshot_wait)
joints_h_handles=np.zeros([num_units,1])
joints_v_handles=np.zeros([num_units,1])
#distance_measurement_handles = np.zeros([num_snakes,1])

#for snake in range(num_snakes):
#error_code_dist,distance_measurement_handles[snake] =  sim.simxGetDistanceHandle(clientID,'snake'+str(snake)+'_goal',sim.simx_opmode_blocking)
for i in range(1,num_units+1):
    error_code_h, joints_h_handles[i-1] = sim.simxGetObjectHandle(clientID,'snake_joint_h'+str(i),sim.simx_opmode_oneshot_wait)
    error_code_v, joints_v_handles[i-1] = sim.simxGetObjectHandle(clientID,'snake_joint_v'+str(i),sim.simx_opmode_oneshot_wait)
    if error_code_h!=0 or error_code_v!=0:# or error_code_cam!=0:
        print("Problem!")
#IPython.embed()
_,snake_handle = sim.simxGetObjectHandle(clientID,'snake',sim.simx_opmode_oneshot_wait)
sim.simxRemoveModel(clientID,snake_handle,sim.simx_opmode_blocking)
input()
sim.simxLoadModel(clientID,'/home/raoshashank/Downloads/CopellaSim/models/robots/mobile/snake_no_child_script.ttm',True,sim.simx_opmode_blocking)  
   

#if (t>10) then -- Here we do a transition from one movement type to the other movement type (between time=10 and time=11):
s=0.0
#    if (s>1) then
#        s=1
#    end
#end
t_const = 0.050000000745058
distances = np.zeros([3,1])
#for snake in range(num_snakes):
t = 0.0

while True:
    t = t+t_const
    time.sleep(t_const)
    #print(t)

    for i in range(1,5):
        h_cmd = (A_H[0]*(1-s)+A_H[1]*s)*math.cos(t*(speed[0]*(1-s)+speed[1]*s)+i*(P_H[0]*(1-s)+P_H[1]*s))
        err_code_h = sim.simxSetJointTargetPosition(clientID,joints_h_handles[i-1],h_cmd,sim.simx_opmode_oneshot)
        v_cmd =(A_V[0]*(1-s)+A_V[1]*s)*math.sin(t*(speed[0]*(1-s)+speed[1]*s)+i*(P_V[0]*(1-s)+P_V[1]*s))
        err_code_v = sim.simxSetJointTargetPosition(clientID,joints_v_handles[i-1],v_cmd,sim.simx_opmode_oneshot)

    print("Distances:")
    
    if t>=5.0:
        break
    print("---")    

#sim.setJointTargetPosition(joint_cam[1],(A_V[1]*(1-s)+A_V[2]*s)/2*math.sin(t*(speed[1]*(1-s)+speed[2]*s)+(P_V[1]*(1-s)+P_V[2]*s)+(P_C[1]*(1-s)+P_C[2]*s)))
#end 
