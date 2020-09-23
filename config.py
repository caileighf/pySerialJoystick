'''
Order of operations for controls:

    1. call: control_inst.handle_event(pygame::event) --> sets values and calls on_action callable (if any)
    2. call: control_inst.format_output(args) ----------> returns formatted output string (see class for examples)

'''
import os, sys
# for suppressing pygame output
def block_print():
    sys.stdout = open(os.devnull, 'w')

# for turning back on after suppressing pygame output
def enable_print():
    sys.stdout = sys.__stdout__

# 
# SUPRESS PYGAME STARTUP PRINT MESSAGE 
# (it prints the version # and that gets printed in debug mode anyways)
#
block_print()
import pygame
enable_print()

JOYSTICK_EVENT = [
            pygame.JOYBUTTONDOWN,
            pygame.JOYBUTTONUP,
            pygame.JOYAXISMOTION,
            pygame.JOYHATMOTION,
        ]

class ButtonControl(object):
    """docstring for ButtonControl

    possible output formats:
        1. prefix + print_on_press
        2. print_on_press --> default prefix (empty str) gets you this
        3. prefix + print_on_release
        4. print_on_release --> default prefix (empty str) gets you this

    """
    def __init__(self, index,
                       name,
                       prefix='',
                       value=None,
                       print_on_press=None, 
                       print_on_release=None, 
                       on_press=None, 
                       on_release=None):
        super(ButtonControl, self).__init__()
        self.index = index
        self.name = name
        self.prefix = prefix
        self.value = value
        self.print_on_press = print_on_press
        self.print_on_release = print_on_release
        self.on_press = on_press
        self.on_release = on_release

    def set_val(self, val):
        self.value = val

    def format_output(self, on_press=True):
        if on_press:
            if self.print_on_press == None:
                return(None)
            return('{}{}'.format(self.prefix, self.print_on_press))

        if self.print_on_release == None:
            return(None)
        return('{}{}'.format(self.prefix, self.print_on_release))

    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if callable(self.on_press):
                self.on_press(event)
        elif event.type == pygame.JOYBUTTONUP:
            if callable(self.on_release):
                self.on_release(event)

class DPadControl(object):
    """docstring for DPadControl
    
    possible output formats:
        1. prefix + print_on_press + print_on_up
        2. prefix + print_on_up --> default prefix (empty str) gets you this
        3. prefix + print_on_release + print_on_down
        4. prefix + print_on_down --> default prefix (empty str) gets you this 

    """
    def __init__(self, name, 
                       value=None,
                       prefix='',
                       print_on_press='', 
                       print_on_release=None,
                       print_on_up='up',
                       print_on_down='down',
                       print_on_left='left',
                       print_on_right='right',
                       on_press=None, 
                       on_release=None,
                       up=(0, 1), 
                       down=(0, -1), 
                       left=(-1, 0), 
                       right=(1, 0)):
        super(DPadControl, self).__init__()
        self.name = name
        self.value = value
        self.prefix = prefix
        self.print_on_press = print_on_press
        self.print_on_release = print_on_release
        self.print_on_up = print_on_up
        self.print_on_down = print_on_down
        self.print_on_left = print_on_left
        self.print_on_right = print_on_right
        self.on_press = on_press
        self.on_release = on_release
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def set_val(self, val):
        self.value = val
        
    def format_output(self, on_press=True):
        direction = self.value
        if on_press:
            output = '{}{}'.format(self.prefix, self.print_on_press)
        else:
            if self.print_on_release == None:
                return(None)
            output = '{}{}'.format(self.prefix, self.print_on_release)
            return(output)

        if self.value == self.up:
            output += self.print_on_up
        elif self.value == self.down:
            output += self.print_on_down
        elif self.value == self.left:
            output += self.print_on_left
        elif self.value == self.right:
            output += self.print_on_right
        else:
            return(None)
        return(output)

    def handle_event(self, event, on_press=True):
        if event.type == pygame.JOYHATMOTION:
            self.set_val(event.value)

            if on_press:
                if callable(self.on_press):
                    self.on_press(event)
            else:
                if callable(self.on_release):
                    self.on_release(event)

class JoystickControl(object):
    """docstring for JoystickControl

    possible output formats (see note on val):
        1. prefix + val
        2. val --> default prefix (empty str) gets you this
        3. prefix + horizontal_prefix + val
        4. horizontal_prefix + val --> default prefix (empty str) gets you this

    note on val:
        the val is determined by the 'print_attr_on_change' attr.
        if 'print_attr_on_change' is the default ('value')
        we have to take an additional step of figuring out which axis 'value' we want

    ** you can create another attr and use that as the value for all axes
    """
    def __init__(self, name, 
                       horizontal_axis, 
                       vertical_axis,
                       prefix='',
                       print_attr_on_change='value',
                       horizontal_prefix='h,',
                       vertical_prefix='v,',
                       horizontal_value=0.0, 
                       vertical_value=0.0, 
                       on_axis_motion=None):
        super(JoystickControl, self).__init__()
        self.name = name
        self.prefix = prefix
        self.horizontal_axis = horizontal_axis
        self.vertical_axis = vertical_axis
        self.print_attr_on_change = print_attr_on_change
        self.horizontal_prefix = horizontal_prefix
        self.vertical_prefix = vertical_prefix
        self.horizontal_value = horizontal_value
        self.vertical_value = vertical_value
        self.on_axis_motion = on_axis_motion

    def set_val(self, axis, val):
        if axis == self.horizontal_axis:
            self.horizontal_value = val
        elif axis == self.vertical_axis:
            self.vertical_value = val
        else:
            raise ValueError('Axis passed is not connected to this joystick')

    def get_horizontal_output(self):
        if self.print_attr_on_change != 'value':
            return(getattr(self, self.print_attr_on_change))
        return(self.horizontal_value)

    def get_vertical_output(self):
        if self.print_attr_on_change != 'value':
            return(getattr(self, self.print_attr_on_change))
        return(self.vertical_value)

    def format_output(self, axis):
        if axis == self.horizontal_axis:
            return('{}{}{}'.format(self.prefix, 
                                   self.horizontal_prefix,
                                   self.get_horizontal_output()))
        elif axis == self.vertical_axis:
            return('{}{}{}'.format(self.prefix, 
                                   self.vertical_prefix,
                                   self.get_vertical_output()))
        else:
            raise ValueError('Requested axis is not connected to this joystick')

    def handle_event(self, event):
        if event.type == pygame.JOYAXISMOTION:
            self.set_val(axis=event.axis, val=event.value)

            if callable(self.on_axis_motion):
                self.on_axis_motion(event)


supported_controllers = {
    'MY-POWER CO.,LTD. 2In1 USB Joystick': {
        'name': 'MY-POWER CO.,LTD. 2In1 USB Joystick',
        'button_controls': [
            # example with current params
            # $TRIANGLE,pressed
            # $TRIANGLE,released

            # SYMBOL BUTTONS
            ButtonControl(name='TRIANGLE', index=0, prefix='$TRIANGLE,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='CIRCLE',   index=1, prefix='$CIRCLE,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='CROSS',    index=2, prefix='$CROSS,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='SQUARE',   index=3, prefix='$SQAURE,', print_on_press='pressed', print_on_release='released'),
            # TRIGGER BUTTONS
            ButtonControl(name='R_TOP',  index=5, prefix='$RIGHT_TOP,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='R_TRIG', index=7, prefix='$RIGHT_TRIG,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='L_TOP',  index=4, prefix='$LEFT_TOP,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='L_TRIG', index=6, prefix='$LEFT_TRIG,', print_on_press='pressed', print_on_release='released'),
            # SELECT AND START
            ButtonControl(name='SELECT', index=8, prefix='$SELECT,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='START',  index=9, prefix='$START,', print_on_press='pressed', print_on_release='released'),
            # JOYSTICK MO BUTTONS
            ButtonControl(name='L_JOY_BUTTON', index=10, prefix='$LEFT_JOY_BUTTON,', print_on_press='pressed', print_on_release='released'),
            ButtonControl(name='R_JOY_BUTTON', index=11, prefix='$LEFT_JOY_BUTTON,', print_on_press='pressed', print_on_release='released'),
        ],
        'joystick_controls': [
            # example with current params
            # $LEFT_JOY,v,-0.05157628101443525
            # $LEFT_JOY,h,-0.05157628101443525
            JoystickControl(name='LEFT_JOYSTICK', 
                            prefix='$LEFT_JOY,', 
                            horizontal_axis=0, 
                            vertical_axis=1,),
            JoystickControl(name='RIGHT_JOYSTICK', 
                            prefix='$RIGHT_JOY,', 
                            horizontal_axis=2, 
                            vertical_axis=3,),
        ],
        'hat_controls': [
            # if controller has more dpads, keep in my the order of this list 
            # .. is used to pick the correct dpad
            # ... event.hat == index for this list

            # example with current params
            # $DPAD,up
            # $DPAD,down
            # $DPAD,left
            # $DPAD,right
            DPadControl(name='DPAD', prefix='$DPAD,'),
        ],
    }
}
