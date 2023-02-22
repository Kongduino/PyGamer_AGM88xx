# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time, board, sys, keypad, displayio
import adafruit_bme680, busio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_amg88xx

Label = label.Label
ff = "fonts/GoMono-Bold-18.bdf"
GoMonoBold18 = bitmap_font.load_font(ff)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)
# Create the display
display = board.DISPLAY
#display.rotation=180
# Create a bitmap with two colors
bitmap = displayio.Bitmap(64, 64, 50)
myPalette = displayio.Palette(50)
myPalette[0]=0x0000ff
myPalette[1]=0x0014ff
myPalette[2]=0x0029ff
myPalette[3]=0x003eff
myPalette[4]=0x0053ff
myPalette[5]=0x0068ff
myPalette[6]=0x007cff
myPalette[7]=0x0091ff
myPalette[8]=0x00a6ff
myPalette[9]=0x00bbff
myPalette[10]=0x00d0ff
myPalette[11]=0x00e4ff
myPalette[12]=0x00f9ff
myPalette[13]=0x00ffef
myPalette[14]=0x00ffda
myPalette[15]=0x00ffc5
myPalette[16]=0x00ffb0
myPalette[17]=0x00ff9c
myPalette[18]=0x00ff87
myPalette[19]=0x00ff72
myPalette[20]=0x00ff5d
myPalette[21]=0x00ff48
myPalette[22]=0x00ff34
myPalette[23]=0x00ff1f
myPalette[24]=0x00ff0a
myPalette[25]=0x0aff00
myPalette[26]=0x1fff00
myPalette[27]=0x34ff00
myPalette[28]=0x48ff00
myPalette[29]=0x5dff00
myPalette[30]=0x72ff00
myPalette[31]=0x87ff00
myPalette[32]=0x9cff00
myPalette[33]=0xb0ff00
myPalette[34]=0xc5ff00
myPalette[35]=0xdaff00
myPalette[36]=0xefff00
myPalette[37]=0xfff900
myPalette[38]=0xffe400
myPalette[39]=0xffd000
myPalette[40]=0xffbb00
myPalette[41]=0xffa600
myPalette[42]=0xff9100
myPalette[43]=0xff7c00
myPalette[44]=0xff6800
myPalette[45]=0xff5300
myPalette[46]=0xff3e00
myPalette[47]=0xff2900
myPalette[48]=0xff1400
myPalette[49]=0xff0000

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=myPalette)
tile_grid.x = int((display.width/2)-32)
tile_grid.y = int((display.height/2)-32)
feed1_label = Label(GoMonoBold18, text="T°", color=0xE39300)
feed1_label.x = tile_grid.x + 5
feed1_label.y = tile_grid.y + 74
# Create a Group
group = displayio.Group()
# Add the TileGrid to the Group
group.append(tile_grid)
group.append(feed1_label)
# Add the Group to the Display
display.show(group)


while True:
    py = 0
    s = 0.0
    cnt = 0
    tp = 0
    for row in amg.pixels:
        # Pad to 1 decimal place
        px = 0
        for temp in row:
            tp = int(temp)
            if tp<0:
                tp=0
            elif tp>49:
                tp=49
            s += temp
            print(["{0:.1f}".format(temp)])
            for yy in range (0,8):
                for xx in range (0,8):
                    bitmap[px*8+xx, py*8+yy] = tp
            px += 1
            cnt += 1
        py += 1
    print("\n")
    feed1_label.text="{0:.1f}°".format(s/cnt)
    print(feed1_label.text)
    print(f"{tp} --> {myPalette[tp]}")
    c=~myPalette[tp]
    if c<0:
        c=16777215+c
    feed1_label.color=c
    time.sleep(1)
