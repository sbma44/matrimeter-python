import math, sys
from settings import *

def draw_lines(points, closed=True, **kwargs):

    out = ''
    attributes = ''
    for (k,v) in kwargs.items():
        attributes += '%s="%s" ' % (k,v)

    extra = 0
    if closed and points[0]!=points[-1]:
        extra = 1
    
    for i in range(0,len(points) + extra):
        x1 = points[i % len(points)][0]
        y1 = points[i % len(points)][1]
        x2 = points[(i+1) % len(points)][0]
        y2 = points[(i+1) % len(points)][1]
    
        out += '<line x1="%f%s" y1="%f%s" x2="%f%s" y2="%f%s" %s />' % (x1, MEASUREMENT_UNIT, y1, MEASUREMENT_UNIT, x2, MEASUREMENT_UNIT, y2, MEASUREMENT_UNIT, attributes)    

    
    out += ' />'
    
    return out
    
def translate_points(points, x, y):
    new_points = []
    for p in points:
        new_points.append((p[0] + x, p[1] + y))
    return new_points
    
# I wish I was a better programmer. But I'm going to write code for each edge.
def draw_square(x, y, width, height, finger_joint=(0, 0, 0, 0), kerf=0):
    points = []
    
    k = kerf / 2
    
    points.append((x-k,y-k))
    
    # top edge    
    if finger_joint[0]==0:
        points.append((x+width+k, y-k))
    else:
        num_fit = math.floor(width / MATERIAL_WIDTH)
        if num_fit%2==0:
            num_fit -= 1
        leftover_change = width - (MATERIAL_WIDTH * num_fit)
        current_x = x + (leftover_change/2.0) + MATERIAL_WIDTH + ((math.fabs(finger_joint[0])-1) * MATERIAL_WIDTH)
        fj = finger_joint[0] / math.fabs(finger_joint[0])
        i = 0
        while current_x < (x+width-(leftover_change/2.0)-((math.fabs(finger_joint[0])-1) * MATERIAL_WIDTH)):
            if (i%2)==0:
                points.append((current_x+k, y - k))
                points.append((current_x+k, y - k + (fj * MATERIAL_WIDTH)))
            else:                
                points.append((current_x-k, y - k + (fj * MATERIAL_WIDTH)))
                points.append((current_x-k, y - k))
            current_x += MATERIAL_WIDTH
            i += 1                
        points.append((x+width+k, y-k))
    
    # right edge
    if finger_joint[1]==0:
        points.append((x+width+k, y+width+k))
    else:
        num_fit = math.floor(height / MATERIAL_WIDTH)
        if num_fit%2==0:
            num_fit -= 1
        leftover_change = height - (MATERIAL_WIDTH * num_fit)
        current_y = y + (leftover_change/2.0) + MATERIAL_WIDTH + ((math.fabs(finger_joint[1])-1) * MATERIAL_WIDTH)
        fj = finger_joint[1] / math.fabs(finger_joint[1])
        i = 0
        while current_y < (y+height-((leftover_change/2.0)+((math.fabs(finger_joint[1])-1) * MATERIAL_WIDTH))):
            if (i%2)==0:
                points.append((x+width+k, current_y+k))
                points.append((x+width+k+(-1 * fj * MATERIAL_WIDTH), current_y+k))
            else:                
                points.append((x+width+k+(-1 * fj * MATERIAL_WIDTH), current_y-k))
                points.append((x+width+k, current_y-k))
            current_y += MATERIAL_WIDTH
            i += 1    
        points.append((x+width+k, y+height+k))
        
    # bottom edge
    if finger_joint[2]==0:
        points.append((x-k, y+height+k))
    else:
        num_fit = math.floor(height / MATERIAL_WIDTH)
        if num_fit%2==0:
            num_fit -= 1        
        leftover_change = width - (MATERIAL_WIDTH * num_fit)
        current_x = x + width - ((leftover_change/2.0) + MATERIAL_WIDTH) - ((math.fabs(finger_joint[2])-1) * MATERIAL_WIDTH)
        fj = finger_joint[2] / math.fabs(finger_joint[2])
        i = 0
        while current_x > (x+(leftover_change/2.0)+((math.fabs(finger_joint[2])-1) * MATERIAL_WIDTH)):
            if (i%2)==0:
                points.append((current_x+k, y+height+k))
                points.append((current_x+k, y+height+k+(-1 * fj * MATERIAL_WIDTH)))
            else:                
                points.append((current_x-k, y+height+k+(-1 * fj * MATERIAL_WIDTH)))
                points.append((current_x-k, y+height+k))
            current_x -= MATERIAL_WIDTH
            i += 1                
        points.append((x-k, y+height+k))
    
    
    # right edge
    if finger_joint[3]==0:
        points.append((x-k,y-k))
    else:
        num_fit = math.floor(height / MATERIAL_WIDTH)
        if num_fit%2==0:
            num_fit -= 1        
        leftover_change = height - (MATERIAL_WIDTH * num_fit)
        current_y = y + height - ((leftover_change/2.0) + MATERIAL_WIDTH + ((math.fabs(finger_joint[3])-1) * MATERIAL_WIDTH))
        fj = -1 * finger_joint[3] / math.fabs(finger_joint[3])
        i = 0
        while current_y > (y+((leftover_change/2.0)+((math.fabs(finger_joint[3])-1) * MATERIAL_WIDTH))):
            if (i%2)==0:
                points.append((x-k, current_y-k))
                points.append((x-k+(-1 * fj * MATERIAL_WIDTH), current_y-k))
            else:                
                points.append((x-k+(-1 * fj * MATERIAL_WIDTH), current_y+k))
                points.append((x-k, current_y+k))
            current_y -= MATERIAL_WIDTH
            i += 1    
        points.append((x-k,y-k))
    
    return points
        
        
def construct_polygon(num_sides):
    points = []
    
    polygon_size = 0.25 * VIEWPORT_WIDTH
    points = []
    for i in range(0, num_sides):
        r = 2 * math.pi * (i / (1.0 * num_sides))
        r_next = 2 * math.pi * (((i+1) % num_sides) / (1.0 * num_sides))

        x1 = (polygon_size * math.cos(r)) + (VIEWPORT_WIDTH / 2)
        y1 = (polygon_size * math.sin(r)) + (VIEWPORT_HEIGHT / 2)

        points.append((x1, y1))
    
    return points
    

def main(html=True):
    print """<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""

    if html:
        print '<html>'

    print '<svg width="%d%s" height="%d%s">' % (VIEWPORT_WIDTH, MEASUREMENT_UNIT, VIEWPORT_HEIGHT, MEASUREMENT_UNIT)

    print """<defs>
        <style type="text/css"><![CDATA[
          line {
            stroke:black;
            stroke-width:%f%s;
          }
          polygon {
            stroke:black;
            strong-width:%f%s;
          }
        ]]></style>
    </defs>""" % (STROKE_WIDTH, MEASUREMENT_UNIT, STROKE_WIDTH, MEASUREMENT_UNIT)
    
    #points = construct_polygon(polygon_sides=int(sys.argv[1]))
    points_kerfless = draw_square(10, 10, 78, 78, (0, 1, -4, 1), kerf=0)
    points_kerf = draw_square(10, 10, 78, 78, (0, 1, -4, 1), kerf=2)
    print draw_lines(points_kerfless, style="stroke:black")
    print draw_lines(points_kerf, style="stroke:red")
    
    # points = draw_square(10, 10, 78, 78, (0, 0, 0, 0))
    # print draw_lines(points, False)



    print '</svg>'

    if html:
        print '</html>'

if __name__ == '__main__':
    main(html=('--html' in sys.argv))