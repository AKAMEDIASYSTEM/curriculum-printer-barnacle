#!/usr/bin/env python
from __future__ import print_function
import Adafruit_BBIO.UART as uart
import Adafruit_BBIO.GPIO as gpio
from Adafruit_Thermal import *
import requests
import time
import atexit
import ssd1351 as ssd

BG_COLOR = 0x000000
TEXT_COLOR = 0x99f0f0
button = 'P8_37'
LINEWIDTH = 21 # with this font, we can fit 21 chars on a line
to_print = False
r = ' '

class the_screen(object):

    def __init__(self):
        self.text = 'awaiting update'

    def update_screens(self):
        req = requests.get(curriculum, params=payload)
        # print(r.text)
        resp = req.json()
        print('encoding is',req.encoding)
        keywords = resp['data']['noun_phrase']
        print(keywords)
        # try:
        #     t = keywords.decode('utf-8','ignore')
        # except UnicodeEncodeError:
        #     print(keywords)
        #     print('ERROR IN ABOVE LINE')
        #     t = keywords.encode('utf-8','ignore')

        disp.clear_display()
        disp.fillScreen(BG_COLOR)
        i=3 # initial vertical offset
        # keywords = ["really long sentence with lots of words","short thing", "really long thing again really long hello hello", "cat pajamas"]
        colorweird = False # we differently-color multiline entries
        for p in keywords:
            buff = ""
            # disp.draw_text_bg(5, 5+i, p, TEXT_COLOR, BG_COLOR)
            try:
                p = p.decode('utf-8','ignore')
            except UnicodeEncodeError:
                p = p.encode('utf-8','ignore')
            for j in p.split(' '):
                j += " "
                if len(buff + j) > LINEWIDTH:
                    print('should wrap ', buff+j)
                    disp.draw_text_bg(0, i, buff, TEXT_COLOR+30, BG_COLOR)
                    colorweird = True
                    print(i)
                    i += 10
                    buff = " " + j
                else:
                    buff = buff + j
            if len(buff):
                print(i)
                if colorweird:
                    disp.draw_text_bg(0, i, buff, TEXT_COLOR+30, BG_COLOR)
                    colorweird = False
                else:
                    disp.draw_text_bg(0, i, buff, TEXT_COLOR, BG_COLOR)
                i+=10
            i+=10
        self.text = t

oled = the_screen()

def exit_handler():
    gpio.cleanup()

def ppp(a):
    # print('printing! %s' % r)
    # printer.print(r)
    # printer.print(oled.text)
    # printer.feed(4)
    pass

curriculum = 'http://curriculum.local/api'
payload = {'n':3} # three phrases
# print('about to create disp')
disp = ssd.SSD1351()
atexit.register(exit_handler)
disp.begin()
gpio.setup(button, gpio.IN)
gpio.add_event_detect(button, gpio.FALLING, callback=ppp)
uart.setup('UART1')
# print('just began UART')
printer = Adafruit_Thermal('/dev/ttyO1', 19200, timeout=5)
printer.begin()
keyword = u"" # does this solve the ridic encoding prob




# def update_screens():
#     req = requests.get(curriculum, params=payload)
#     # print(r.text)
#     resp = req.json()
#     print('encoding is',req.encoding)
#     keyword = resp['data']
#     # print(keyword, 'utf-8')
#     try:
#         t = keyword.decode('utf-8','ignore')
#     except UnicodeEncodeError:
#         print(keyword)
#         print('ERROR IN ABOVE LINE')
#         t = keyword.encode('utf-8','ignore')

#     disp.clear_display()
#     disp.fillScreen(BG_COLOR)
#     i=3 # initial vertical offset
#     k = t.split('\n')
#     # a = ["really long sentence with lots of words","short thing", "really long thing again really long hello hello", "cat pajamas"]
#     print(k)
#     colorweird = False # we differently-color multiline entries
#     for p in k:
#         buff = ""
#         # disp.draw_text_bg(5, 5+i, p, TEXT_COLOR, BG_COLOR)
#         for j in p.split(' '):
#             j += " "
#             if len(buff + j) > LINEWIDTH:
#                 print('should wrap ', buff+j)
#                 disp.draw_text_bg(0, i, buff, TEXT_COLOR+30, BG_COLOR)
#                 colorweird = True
#                 print(i)
#                 i += 10
#                 buff = " " + j
#             else:
#                 buff = buff + j
#         if len(buff):
#             print(i)
#             if colorweird:
#                 disp.draw_text_bg(0, i, buff, TEXT_COLOR+30, BG_COLOR)
#                 colorweird = False
#             else:
#                 disp.draw_text_bg(0, i, buff, TEXT_COLOR, BG_COLOR)
#             i+=10
#         i+=10
#     return t



while True:
    oled.update_screens()
    time.sleep(10)