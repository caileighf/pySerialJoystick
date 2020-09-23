# pySerialJoystick

### USB Controller
_currently only tested on the following USB controller:_

TTX PS3 Wired USB Controller - Blue - PlayStation 3 https://www.amazon.com/dp/B07255847K/ref=cm_sw_r_cp_api_fab_pXLAFbTA0BJ8Y

See `config.py` if you want to add mapping for a different controller

### Setting up your environment and running for the first time
```
$ virtualenv -p python3 /path-to-venv
$ source /path-to-venv/bin/activate
$ pip install -r requirements.txt

$ python main.py
```

### Running with output piped to single stream
```
$ python main.py # stdout
$ python main.py >> tee joystick_output.txt
$ python main.py >> /dev/ttyUSB0
```

### Running with output piped to stdout AND file descriptor
_the `-u` is for unbuffered mode. tee will not work with out it_
```
$ python -u main.py | tee joystick_output.txt
$ python -u main.py | tee /dev/ttyUSB0
```

### Getting info about another USB controller
if you pass `--controller-name test` to main it will create a controller that spits out values it's getting from buttons. It's one way to create a controller map like the one in `config.py`
```
$ python main.py --controller-name test

=================================================================
= Press buttons and joysticks to get info about this controller =
=================================================================
Name:      MY-POWER CO.,LTD. 2In1 USB Joystick
# Axes:    4
# Buttons: 12
# Hats:    1

<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.06183050019837031})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.5154576250495926})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 1.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 1.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 1.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.7732169560838649})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.37113559373760185})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.010284737693411055})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.010284737693411055})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.10309152500991851})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 2, 'value': 0.0})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.15463728751487776})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.18555253761406293})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.17523728141117587})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.14432203131199073})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.020599993896298106})>
<Event(7-JoyAxisMotion {'joy': 0, 'axis': 3, 'value': 0.0})>
```

### Example output with the values in `config.py`
```
$ python main.py

$LEFT_JOY,v,0.0
$LEFT_JOY,v,-0.030945768608661155
$LEFT_JOY,v,-0.195898312326426
$LEFT_JOY,h,0.0
$LEFT_JOY,v,-0.22681356242561113
$LEFT_JOY,h,-0.2165288247322001
$LEFT_JOY,v,0.0
$LEFT_JOY,v,0.0
$LEFT_JOY,h,-1.000030518509476
$LEFT_JOY,h,-0.7217017120883816
$LEFT_JOY,h,-0.3402203436384167
$LEFT_JOY,h,-0.030945768608661155
$LEFT_JOY,h,0.0
$CIRCLE,pressed
$CIRCLE,released
$SQAURE,pressed
$SQAURE,released
$TRIANGLE,pressed
$TRIANGLE,released
$RIGHT_TOP,pressed
$RIGHT_TOP,released
$RIGHT_TOP,pressed
$RIGHT_TOP,released
$RIGHT_TRIG,pressed
$RIGHT_TRIG,released
$LEFT_TRIG,pressed
$LEFT_TRIG,released
$LEFT_TRIG,pressed
$LEFT_TRIG,released
$DPAD,up
$DPAD,up
$DPAD,up
$DPAD,up
$DPAD,down
$DPAD,right
$START,pressed
$START,released
$SELECT,pressed
$SELECT,released
$RIGHT_JOY,h,0.0
$RIGHT_JOY,h,0.24741355632190923
$RIGHT_JOY,h,0.4226813562425611
$RIGHT_JOY,h,0.5257728812524797
$RIGHT_JOY,h,0.5154576250495926
$RIGHT_JOY,h,0.4329966124454482
$RIGHT_JOY,h,0.030915250099185155
$RIGHT_JOY,h,0.0
```