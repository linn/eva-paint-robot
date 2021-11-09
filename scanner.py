#!/usr/bin/env python3

# Mostly lifted from https://gist.github.com/michalfapso/1755e8a35bb83720c2559ce8ffde5f85

# Tested with `SC-8110-2D-B` 1d & 2d barcode scanner
#
# Inspired by https://github.com/julzhk/usb_barcode_scanner
# which was inspired by https://www.piddlerintheroot.com/barcode-scanner/
# https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100
# from 'brechmos' - thank-you!
#
# This implementation doesn't directly decode hidraw stream, but uses
# evdev and grabs the device, so the code arrives only in this script
# and not in any active input window.
#
# Also, it uses a list of USB vendor:product to identify the device,
# so that you don't have to set the dev path.

import evdev
import logging
import os

logging.basicConfig(filename='eva.log', encoding='utf-8', level=logging.DEBUG)

ERROR_CHARACTER = '?'
VALUE_UP = 0
VALUE_DOWN = 1

# USB VENDOR & PRODUCT list of 2d scanners
VENDOR_PRODUCT = [
        [0x05ac,0x0221], # [vendor, product]
        [0x05ac,0x0220],
        [0x05f9,0x2216],
        ]

CHARMAP = {
        evdev.ecodes.KEY_1: ['1', '!'],
        evdev.ecodes.KEY_2: ['2', '@'],
        evdev.ecodes.KEY_3: ['3', '#'],
        evdev.ecodes.KEY_4: ['4', '$'],
        evdev.ecodes.KEY_5: ['5', '%'],
        evdev.ecodes.KEY_6: ['6', '^'],
        evdev.ecodes.KEY_7: ['7', '&'],
        evdev.ecodes.KEY_8: ['8', '*'],
        evdev.ecodes.KEY_9: ['9', '('],
        evdev.ecodes.KEY_0: ['0', ')'],
        evdev.ecodes.KEY_MINUS: ['-', '_'],
        evdev.ecodes.KEY_EQUAL: ['=', '+'],
        evdev.ecodes.KEY_TAB: ['\t', '\t'],
        evdev.ecodes.KEY_Q: ['q', 'Q'],
        evdev.ecodes.KEY_W: ['w', 'W'],
        evdev.ecodes.KEY_E: ['e', 'E'],
        evdev.ecodes.KEY_R: ['r', 'R'],
        evdev.ecodes.KEY_T: ['t', 'T'],
        evdev.ecodes.KEY_Y: ['y', 'Y'],
        evdev.ecodes.KEY_U: ['u', 'U'],
        evdev.ecodes.KEY_I: ['i', 'I'],
        evdev.ecodes.KEY_O: ['o', 'O'],
        evdev.ecodes.KEY_P: ['p', 'P'],
        evdev.ecodes.KEY_LEFTBRACE: ['[', '{'],
        evdev.ecodes.KEY_RIGHTBRACE: [']', '}'],
        evdev.ecodes.KEY_A: ['a', 'A'],
        evdev.ecodes.KEY_S: ['s', 'S'],
        evdev.ecodes.KEY_D: ['d', 'D'],
        evdev.ecodes.KEY_F: ['f', 'F'],
        evdev.ecodes.KEY_G: ['g', 'G'],
        evdev.ecodes.KEY_H: ['h', 'H'],
        evdev.ecodes.KEY_J: ['j', 'J'],
        evdev.ecodes.KEY_K: ['k', 'K'],
        evdev.ecodes.KEY_L: ['l', 'L'],
        evdev.ecodes.KEY_SEMICOLON: [';', ':'],
        evdev.ecodes.KEY_APOSTROPHE: ['\'', '"'],
        evdev.ecodes.KEY_BACKSLASH: ['\\', '|'],
        evdev.ecodes.KEY_Z: ['z', 'Z'],
        evdev.ecodes.KEY_X: ['x', 'X'],
        evdev.ecodes.KEY_C: ['c', 'C'],
        evdev.ecodes.KEY_V: ['v', 'V'],
        evdev.ecodes.KEY_B: ['b', 'B'],
        evdev.ecodes.KEY_N: ['n', 'N'],
        evdev.ecodes.KEY_M: ['m', 'M'],
        evdev.ecodes.KEY_COMMA: [',', '<'],
        evdev.ecodes.KEY_DOT: ['.', '>'],
        evdev.ecodes.KEY_SLASH: ['/', '?'],
        evdev.ecodes.KEY_SPACE: [' ', ' '],
        }

def barcode_reader_evdev(dev):
    barcode_string_output = ''
    # barcode can have a 'shift' character; this switches the character set
    # from the lower to upper case variant for the next character only.
    shift_active = False
    for event in dev.read_loop():

        #print('categorize:', evdev.categorize(event))
        #print('typeof:', type(event.code))
        #print("event.code:", event.code)
        #print("event.type:", event.type)
        #print("event.value:", event.value)
        #print("event:", event)

        if event.code == evdev.ecodes.KEY_ENTER and event.value == VALUE_DOWN:
            #print('KEY_ENTER -> return')
            # all barcodes end with a carriage return
            return barcode_string_output
        elif event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
            #print('SHIFT')
            shift_active = event.value == VALUE_DOWN
        elif event.value == VALUE_DOWN:
            ch = CHARMAP.get(event.code, ERROR_CHARACTER)[1 if shift_active else 0]
            #print('ch:', ch)
            # if the charcode isn't recognized, use ?
            barcode_string_output += ch

def list_devices():
    # This tickles asyncio in some way that prevents Python from exploding when ctrl+c has been pressed
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    print("--------------------------------------------------")
    for device in devices:
        print('device:', device)
        print('info  :', device.info)
        print('path  :', device.path)
        print('name  :', device.name)
        print('phys  :', device.phys)
        print("--------------------------------------------------")
        # print(VENDOR_PRODUCT)
        for vp in VENDOR_PRODUCT:
            # print("vp1 is " + str(vp[1]))
            # print("device.info.product is " + str(device.info.product))
            if device.info.vendor == vp[0] and device.info.product == vp[1]:
                print("Returning scanning devices")
                return device
    print("No input device found")
    return None

def wait_for_input():
    dev = evdev.InputDevice(os.environ['BARCODEREADER1'])
    dev.grab()

    try:
        while True:
            upcnumber = barcode_reader_evdev(dev)
            print("Scanned number is : " + upcnumber)
            return upcnumber
    except KeyboardInterrupt:
        logging.debug('Keyboard interrupt')
    except Exception as err:
        logging.error(err)
    dev.ungrab()

def main():
    # reader = BarcodeReader()
    list_devices()

    dev = evdev.InputDevice(os.environ['BARCODEREADER1'])
    print("Capturing from", dev.path)
    dev.grab()

    try:
        while True:
            print("here?")
            upcnumber = barcode_reader_evdev(dev)
            print("Scanned number is : " + upcnumber)
    except KeyboardInterrupt:
        logging.debug('Keyboard interrupt')
    except Exception as err:
        print("wtf")
        logging.error(err)

    dev.ungrab()

if __name__ == '__main__':
    main()
