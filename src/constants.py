TARGET_FRAMERATE = 60
#Old Z Axis range = (1 - (-1)) = 2
#New Z Axis range = (1 - 0) = 1
#Range ratio = 1/2
#New val = (old val - old zaxis min) * range ratio
OLD_ZAXIS_MIN = -1
RANGE_RATIO = 0.5

#Drag force = 0.5 * coefficient of drag * frontal area * air density * speed^2
#The drag force below is without the speed^2 as that varies however the rest stays consistent therefore we can save some computational power here
#Drag force without speed^2 (drag coeff)= 0.5 * 0.27 * 1.85 * 1.29
DRAG_COEFF = 0.32
#Rolling resitance is apparently 30 times drag force
RR_FORCE = 9.6

GRAVITY = 9.81

RADS_to_RPM = 60/(2*3.14) 
RPM_to_RADS = (2*3.14)/60


#WALL OF TEXT
#Total force = tractive force - drag - roll res
#tractive force = u * engine force
#drag = cd * velV * velM
#roll res = crr * velV

#From there we can calculate acceleration
#a = F/m
#v = v + dt*a
#p = p + dt*v
