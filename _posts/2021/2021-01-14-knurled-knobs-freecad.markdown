---
layout: post
author: Taylor Talkington
title: Knurled Knobs in FreeCAD
date: 2021-01-14 06:20 -0500
---

![knurling](/assets/knurling.png)

## Knurly, Dude!

The 3D Printing adventures continue, and as I find myself designing things I had the question: how can I make knurled surfaces in FreeCAD?

After some research and combining a few different techniques, here's what I came up with.

## Creating Knurling

This technique only works on circular surfaces (cylinders), but that's ok because most knobs and handles are round anyway...

For this example, I made a knob for my 3D Printer's LCD encoder in FreeCAD version 0.18. Actions specified are in the 'Task' pane.

First, create a simple knob:
1. Select Part Design Workbench
2. Create Body
3. Create Sketch (select XY_Plane)
4. Add a cirlce with a radius of 10 mm, snapped to the center origin  
    ![circle](/assets/knurling_1.png)
5. Close the sketch
6. Pad it by 10 mm  
    ![cylinder](/assets/knurling_2.png)
7. Select the top edge  
    ![fillet](/assets/knurling_3.png)
8. Fillet 2 mm  
    ![fillet2](/assets/knurling_4.png)
9. Select the bottom face
10. Create Sketch
11. Add a circle with a radius of 7 mm, anchored to the origin  
    ![pocket1](/assets/knurling_5.png)
12. Pocket 9 mm
13. Select the new inner face  
    ![pocket2](/assets/knurling_6.png)
14. Create Sketch
15. Create two circles, both centered on the origin
    - One with a radius of 4 mm
    - One with a radius of 3.05 (6.1 / 2 - the LCD encoder shaft is 6mm in diameter)
    ![circles](/assets/knurling_7.png)
16. Add 2 vertical lines near the top of the circles, connecting them
    - Attach the endpoints of each line to both circles (*Fix Point onto an Object* constraint)
    - Give both lines a vertical constraint
    - Give both lines equali1ty constraint (select both and select the '=' constraint)
    - Constrain the lines to be 1 mm apart horizontally
        1. Select the top vertex of each line
        2. Shift-H
        3. Specify 1 mm
    ![lines](/assets/knurling_8.png)
17. Use the Trim Edge tool to remove the portion of the circles between the lines: ![trim_edge](/assets/knurling_9.png)  
    ![sketch2](/assets/knurling_10.png)
18. Pad by 8 mm

So that's a simple knob. Now on to the knurling:
1. Select Part Workbench
2. Part->Create Primitives
    1. Select Helix
    2. Radius is the same as the knob (10 mm)
    3. Height is the same as the knob (10 mm)
    4. Pitch 10 x height (100 mm)
    5. Click Create
    6. Click Close
    ![helix1](/assets/knurling_11.png)
3. Select Part Design Workbench
4. Select the helix
5. Part Design->Create Body
6. Create Sketch
7. Select XY_Plane001
8. Hide the knob for now (Select 'Body' in the Model pane and press space)
9. Draw a triangle near the base of the helix:
    1. One point constrained to the x axis
    2. The angle at that point constrained to 90 degrees
    3. Constrain the two connecting segments to be equal length
    3. Constrain that point to be 9 mm from the y axis
    4. Constrain one of the other points to be 10.5 mm from the y axis
    5. Constrain the far edge to be vertical
    6. Close sketch
    ![helix_sketch](/assets/knurling_12.png)
10. Additive Pipe
    1. Under 'Path to sweep along' click Object
    2. Select the helix
    3. Select 'Frenet' for Orientation Mode
11. Make the knob visible again (Select 'Body' in the Model pane and press space)  
    ![helix_pipe](/assets/knurling_13.png)
12. Select Draft Workbench
13. Select the helix pipe (Body001) in the Model Pane
14. Modification->Array Tools->Polar Array
    1. Number of elements = 20
    2. Click Reset point and verifty X, Y, Z = 0
    3. Click OK
    ![array_1](/assets/knurling_14.png)
15. Copy the array
    1. Select the array (Array) in the Model pane and press Ctrl-C
    2. Leave all objects selected and click OK
    3. Press Ctrl-V
16. Change the new helix to left-handed
    1. Select the copied helix (Helix001)
    2. In the properties panel below, change local coord to 'Left Handed'
    ![copy helix](/assets/knurling_15.png)
17. Cut the helixes from the knob
    1. Select Part Workbench
    2. Select the knob (Body)
    3. Hold Ctrl and select Array
    4. Part->Boolean->Cut
    5. Select Cut
    6. Hold Ctrl and Select Array001
    7. Part->Boolean->Cut
    ![cutting](/assets/knurling_16.png)

There! A knurled knob. I didn't quite like it yet, though. But, tweaking it is easy since FreeCAD is parametric.

I ended up tweaking the helixes a bit:
1. Select Helix in the Model Pane
2. Change Pitch to 75 mm
3. Change Height to 9.25 mm
4. Select Helix001 and repeat 2 & 3

That's better, I think:
![final](/assets/knurling_17.png)