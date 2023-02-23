import time, board, sys, keypad, displayio
import adafruit_bme680, busio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_amg88xx # from the adafruit bundle
from colorsys import hls_to_rgb # from the adafruit bundle

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
myWidth = int(display.height/8)
halfWidth = int(myWidth/2)
#print(f"myWidth: {myWidth}, halfWidth: {halfWidth}")
bitmap = displayio.Bitmap(myWidth*8, myWidth*8, 50)

def rainbow_color_stops(n=10, end=2/3):
  return [hls_to_rgb(end * i/(n-1), 0.5, 1) for i in range(n)]

stops = 100
myPalette = displayio.Palette(stops)
a = rainbow_color_stops(stops, 1.0)
ix = 0
for x in a:
  print(x)
  r, g, b = x
  #print(f"r = {r}, g = {g}, b = {b}")
  myPalette[ix] = (r*65536+g*256+b)
  ix += 1

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=myPalette)
tile_grid.x = int((display.width-myWidth*8)/2)
tile_grid.y = 0
feed1_label = Label(GoMonoBold18, text="T°", color=0xE39300)
feed1_label.x = tile_grid.x + 2
feed1_label.y = display.height-9
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
            elif tp>=stops:
                tp=stops-1
            s += temp
            #print(["{0:.1f}".format(temp)])
            for yy in range (0, myWidth):
                for xx in range (0, myWidth):
                    bitmap[px*myWidth+xx, py*myWidth+yy] = tp
            px += 1
            cnt += 1
        py += 1
    feed1_label.text="{0:.1f}°".format(s/cnt)
    #print(feed1_label.text)
    #print(f"{tp} --> {myPalette[tp]}")
    c=~myPalette[tp]
    if c<0:
        c=16777215+c
    feed1_label.color=c
    time.sleep(1)
