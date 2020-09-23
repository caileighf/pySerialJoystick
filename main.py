'''
pySerialJoystick main.py

Author: Caileigh Fitzgerald <cfitzgerald@whoi.edu>
(c) 2019 Woods Hole Oceanographic Institution
'''
import traceback
import os
import sys
import threading
import argparse
import time

# to add more controllers check out config.py
from config import (supported_controllers, block_print, enable_print)
# 
# SUPRESS PYGAME STARTUP PRINT MESSAGE 
# (it prints the version # and that gets printed in debug mode anyways)
#
block_print()
import pygame
enable_print()

class TestController(object):
    """docstring for TestController"""
    def __init__(self):
        super(TestController, self).__init__()
        pygame.init()
        pygame.joystick.init()
        # grabs first joystick
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def joystick_info(self):
        info  = 'Name:      {}\n'.format(self.joystick.get_name())
        info += '# Axes:    {}\n'.format(self.joystick.get_numaxes())
        info += '# Buttons: {}\n'.format(self.joystick.get_numbuttons())
        info += '# Hats:    {}\n'.format(self.joystick.get_numhats())
        return(info)

    def stop(self):
        pass

    def try_controls(self):
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                    else:
                        print(event)
        except KeyboardInterrupt:
            pass

class Controller(object):
    """ Class to interface with a Joystick """
    def __init__(self, config,
                       handle_printing=True,
                       joy_index=0, 
                       debug=True):
        pygame.init()
        pygame.joystick.init()
        self._shutdown = False
        self.handle_printing = handle_printing
        # there can be multiple joysticks connected
        # .. Controller uses the name to identify them and the config name MUST match
        self.joystick = pygame.joystick.Joystick(joy_index)
        self.joystick.init()

        self.debug = debug
        if self.debug:
            self.print_to_stream('pygame version: {}'.format(pygame.__version__))
            self.print_to_stream(self.joystick_info())
        
        # make sure connected controller's name matches the passed config
        if config['name'] != self.joystick.get_name():
            raise ValueError('\"{}\"" was not found!'.format(config['name']))

        # populate controls lists
        self._init_controls(config)
        self._init_event_map()

    def _init_event_map(self):
        # map for event to general callback
        self.controller_event_map = {
            pygame.JOYBUTTONDOWN: self.on_press,
            pygame.JOYBUTTONUP:   self.on_release,
            pygame.JOYAXISMOTION: self.on_axis_motion,
            pygame.JOYHATMOTION:  self.on_dpad,
        }

    def _init_controls(self, config):
        try:
            # make sure config has all these keys
            self.button_controls = config['button_controls']
            self.joystick_controls = config['joystick_controls']
            self.hat_controls = config['hat_controls']
        except KeyError as e:
            raise ValueError('config parameter is missing a key!\n{}'.format(e))

    def print_to_stream(self, output, end='\r\n'):
        if self.handle_printing:
            # probably not needed up maybe there will be more formatting
            # .. either way, that can happen now
            print(output, end=end)

    def joystick_info(self):
        info  = 'Name:      {}\n'.format(self.joystick.get_name())
        info += '# Axes:    {}\n'.format(self.joystick.get_numaxes())
        info += '# Buttons: {}\n'.format(self.joystick.get_numbuttons())
        info += '# Hats:    {}\n'.format(self.joystick.get_numhats())
        return(info)

    def on_press(self, event):
        output = None
        for button in self.button_controls:
            if event.button == button.index:
                if button.print_on_press != None:
                    button.handle_event(event)
                    output = button.format_output(on_press=True)
                    if output != None: break 
        if output != None:
            self.print_to_stream(output)

    def on_release(self, event):
        output = None
        for button in self.button_controls:
            if event.button == button.index:
                if button.print_on_release != None:
                    button.handle_event(event)
                    output = button.format_output(on_press=False)
                    if output != None: break 
        if output != None:
            self.print_to_stream(output)

    def on_axis_motion(self, event):
        output = None
        axis = event.axis

        for joystick in self.joystick_controls:
            if joystick.print_attr_on_change != None:
                try:
                    joystick.set_val(axis=axis, val=event.value)
                except ValueError:
                    # set_val throws a value error if the event that triggered
                    # .. on_axis_motion isn't connected to THIS joystick.
                    continue
                else:
                    joystick.handle_event(event)
                    output = joystick.format_output(axis=axis)
                    if output != None: break 
        if output != None:
            self.print_to_stream(output)

    def on_dpad(self, event):
        output = None
        dpad = self.hat_controls[event.hat]
        
        if dpad != None:
            dpad.set_val(event.value)
            dpad.handle_event(event)
            if event.value == (0, 0):
                if dpad.print_on_release != None:
                    output = dpad.format_output(on_press=False)
            else:
                if dpad.print_on_press != None:
                    output = dpad.format_output(on_press=True)

        if output != None:
            self.print_to_stream(output)

    def start_polling(self, freq=60):
        self.freq = freq
        self.thread_ = threading.Thread(target=self.loop)
        self.thread_.start()

    def is_shutdown(self):
        return(self._shutdown)

    def stop(self):
        self._shutdown = True

    def kill(self):
        sys.exit(0)

    def loop(self):
        try:
            while not self.is_shutdown():
                # loop through events and handle
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._shutdown = True
                        continue

                    elif event.type in self.controller_event_map:
                        try:
                            self.controller_event_map[event.type](event)
                        except:
                            if self.debug: self.print_to_stream(traceback.format_exc())
                    else:
                        if self.debug: self.print_to_stream('Unrecognized event: {}'.format(event.type))
        finally:
            pygame.quit()
            self.kill()

def handle_test_controller(controller):
    print('=================================================================')
    print('= Press buttons and joysticks to get info about this controller =')
    print('=================================================================')
    print(controller.joystick_info())
    controller.try_controls()
    return(0)

def handle_controller(controller):
    # start controller thread 
    controller.start_polling()
    # loop until controller has been shutdown
    while not controller.is_shutdown():
        time.sleep(0.1)
    return(0)

def main(args, controller):
    if isinstance(controller, TestController):
        rc = handle_test_controller(controller)
    elif isinstance(controller, Controller):
        rc = handle_controller(controller)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--controller-name', help='Controller name', default='MY-POWER CO.,LTD. 2In1 USB Joystick')
    parser.add_argument('--debug',action="store_true", help="print debug messages to stderr")
    args = parser.parse_args()

    if 'test' in args.controller_name:
        controller = TestController()
    else:
        controller = Controller(config=supported_controllers[args.controller_name], debug=args.debug)

    rc = None
    try:
        rc = main(args=args, controller=controller)
    except KeyboardInterrupt:
        pass
    except Exception:
        if args.debug: traceback.print_exc()
    finally:
        controller.stop()
        if args.debug: print('\n\n\tEnding...\n')
        exit(rc)