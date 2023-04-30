Global Integer Xmax, Xmin, Ymax, Ymin, Zmin, xpos, ypos, gap, radius, x, y, z, u, x1, x2, y1, y2
Global String p$, px1$, px2$, py1$, py2$

Function main
	String indata$(0), receive$
  	Integer i, camX, camY, camZ

	Motor On
	Power High
	Speed 20
	SpeedR 20
	Accel 20, 20
	SpeedS 20
	AccelS 20, 20
	
' going to camera position
  Go Camera_Pos

'  SetNet #201, "192.168.150.2", 2001, CRLF
  SetNet #201, "127.0.0.1", 2001, CRLF
  OpenNet #201 As Server
  Print "Robot ready, listening to network"
  WaitNet #201
  OnErr GoTo ehandle

  Do
   Input #201, receive$
   ParseStr receive$, indata$(), " " ' convert to lower case
   Print "Received message: ", receive$
   
  
   ' if the command is jump3
   If indata$(0) = "jump3" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
	    u = Val(indata$(4))
    
   		Print "Jumping to x=", x, " y=", y, " z=", z
	   	Jump3 Here +Z(50), Here :X(0) :Y(y) :Z(z + 50), Here :X(x) :Y(y) :Z(z) :U(u)
   EndIf
   
   If LCase$(indata$(0)) = "go" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
    
   		Print "Going to x=", x, " y=", y, " z=", z
	   	Go Here :X(x) :Y(y) :Z(z)
   EndIf
   
   If LCase$(indata$(0)) = "m" Then
     	p$ = Trim$(indata$(1))
    
   		Print "Going to ", p$
	   	Go P(PNumber(p$))
   EndIf
   
   If LCase$(indata$(0)) = "p" Then
   		P333 = Here
   		Print "Current location is ", P333
	   	Print #201, P333
   EndIf
   
   If LCase$(indata$(0)) = "local" Then ' map to local coordinate
   		Real px1, py1, px2, py2
     	px1 = Val(Trim$(indata$(1)))
        py1 = Val(Trim$(indata$(2)))
        px2 = Val(Trim$(indata$(3)))
        py2 = Val(Trim$(indata$(4)))
        
   		Print "Mapping world coordinate to local"
   		Print "Blue button:", px1, ",", py1, "  Knob:", px2, ",", px2
		Real ZOffset
		ZOffset = 522
		P332 = Here :X(px1) :Y(py1) :Z(ZOffset) ' blue	
		P333 = Here :X(px2) :Y(py2) :Z(ZOffset) ' knob
		Local 3,(LBB:P332),(LK:P333) ' map those points to Local BB and Local Knob at z=521
   EndIf
   
 
	' --------- tasks -------
	If LCase$(indata$(0)) = "go_click_m5" Then
   		go_click_m5
   	EndIf
   	
	If LCase$(indata$(0)) = "go_press_blue_button" Then
		Speed 50
   		go_press_blue_button
   	EndIf

   	
	If LCase$(indata$(0)) = "go_approach_slider" Then
		Speed 15
		Real starting_pos
		starting_pos = Val(Trim$(indata$(1)))
   		go_approach_slider(starting_pos)
   	EndIf
   	
	If LCase$(indata$(0)) = "go_check_display" Then
		Speed 50
   		go_check_display
   	EndIf
   	
	If LCase$(indata$(0)) = "go_slide" Then
		Speed 20
		Real mm
		mm = Val(Trim$(indata$(1)))
   		go_slide(mm)
   	EndIf
   	
 	If LCase$(indata$(0)) = "go_tool_up" Then
   		go_tool_up
   	EndIf

   	If LCase$(indata$(0)) = "go_approach_plug1" Then
   		go_approach_plug1
   	EndIf
   	
   	If LCase$(indata$(0)) = "go_approach_plug2" Then
   		go_approach_plug2
   	EndIf
   	
   	If LCase$(indata$(0)) = "go_approach_plug3" Then
   		go_approach_plug3
   	EndIf
   	
	If LCase$(indata$(0)) = "go_open_door" Then
   		go_open_door
   	EndIf
   	
	If LCase$(indata$(0)) = "go_probe1" Then
   		go_probe1
   	EndIf
   	
	If LCase$(indata$(0)) = "go_probe2" Then
   		go_probe2
   	EndIf
   	
 	If LCase$(indata$(0)) = "go_probe_drop" Then
   		go_probe_drop
   	EndIf
   	 	
   	If LCase$(indata$(0)) = "go_approach_cable" Then
   		go_approach_cable
   	EndIf

   	If LCase$(indata$(0)) = "go_wind_cable" Then
   		go_wind_cable
   	EndIf

	If LCase$(indata$(0)) = "go_catch_probe" Then
   		go_catch_probe
   	EndIf
   	
	If LCase$(indata$(0)) = "go_stow" Then
   		go_stow
   	EndIf

	If LCase$(indata$(0)) = "go_press_red_button" Then
   		go_press_red_button
   	EndIf
	' --------- end tasks -------
   
   
   
	P777 = Here
	Print #201, P777
	
  Loop

  Exit Function

  ehandle:
	Call ErrFunc
    EResume Next
Fend
Function ErrFunc

  Print ErrMsg$(Err(0))
  Select Err(0)
   Case 2902
     OpenNet #201 As Server
     WaitNet #201

   Case 2910
     OpenNet #201 As Server

     WaitNet #201

   Default
     Error Err(0)

  Send
Fend

Function drawCircle
	Arc3 Here -X(radius), Here -X(radius) +Y(radius) CP
	Arc3 Here +X(radius), Here +X(radius) -Y(radius) CP
Fend
	
Function go_click_m5
	Go Approach_M5
	Go Click_M5
	Wait (0.2)
	Go Approach_M5
Fend
Function go_press_buttons
	Go Approach_Button
	Go Press_Blue
	Wait (0.5)
	Go Approach_Button
	Go Press_Red
	Wait (0.5)
	Go Approach_Button
Fend
Function go_press_blue_button
	Go Approach_Button
	Go Press_Blue
	Wait (0.2)
	Go Approach_Button
Fend
Function go_open_door
	Go Approach_Door_OrginalPos
	Go Door_Orginal_Pick
	Go DOor_Open1
	Go Door_Open2 CP
	Go Door_Open3 CP
	Go Door_Open4 CP
	Go Door_Open5 CP
	Go Door_Open6
	Go Door_Open7 CP
	Go Door_Open8
	Go Door_Finished
Fend
Function go_probe1
	' make sure gripper is open g0
	Go Approach_probe
	Go Probe_Pick0
	' close the gripper here
Fend
Function go_probe2
	Go probe_pick1
	Go probe_pick2
	Go probe_pick3
	Go probe_pick4
	Go probe_pick5
	Wait (2)
	Go probe_pick6
	Wait (1)
	Go Probe_Pick7
	Go probe_pick4
	Go probe_place1
	Go probe_place2
	Go probe_place3
Fend
Function go_probe_drop
	Go probe_place1
	Go probe_place2
	Go probe_place3
Fend
Function go_approach_plug1
    Go Approach_Plug_orginalPos
	Go Plug_OrginalPos
	'Close the Gripper
	
Fend
Function go_approach_plug2
	Go Unplug_OrginalPos
	Go Approach_Plug_DestinationPos
	Go Plug_DestinationPos
	Go Plug_DestinationTurn
	' Open the Gripper
Fend
Function go_approach_plug3
	Go Plug_FinishedUp
Fend
	
Function go_approach_cable
	' must open g50
	Go Approach_Cable
	Go Approach_Grabbing_Cable
Fend
Function go_wind_cable
	Go Cable1
	Go Cable2
	Go Cable3
	Go Cable4
	Go Cable5
	Go Cable6
	Go Cable7
	Go Cable8
	Go Cable9
	Go Cable10
	Go Cable11
	Go Cable12
	Go Cable4
	Go Cable5
	Go Cable6
	Go Cable7
	Go Cable8
	Go Cable9
	Go Cable10
	Go Cable11
	'Go Cable12
	'Go Cable4
	'Go Cable5
	'Go Cable6
	'Go Cable7
	'Go AlignProbe1
	'Go AlignProbe2
	'Go AlignProbe3
	' open g70 from here and continue with catch probe
Fend
Function go_catch_probe
	'Go CatchProbe1
	'Go CatchProbe2
	' close g80 here and continue with stow
Fend
Function go_stow
	Go Stow1
	Go Stow2
	Go Stow3
	Go Stow4
	Go Stow5
	'Go Stow6
	'Wait (1)
	'Go Stow7
	' open g0
Fend
Function go_press_red_button
	' make sure gripper is closed g80
	Go Stow_Finished
	Go Approach_Button
	Go Press_Red
	Wait (0.5)
	Go Approach_Button
Fend
Function go_slide(distance As Real)
	Real d
	If distance >= 0 And distance <= 31 Then
		For d = distance - 2 To distance + 3
			Go Slider_StartPos +X(d) CP
			Wait (0.3)
		Next
		Go Slider_StartPos
	EndIf
Fend
Function go_check_display
	Go Display_Pic
Fend
Function go_approach_slider(StartPoint As Real)
	' make sure gripper is open
	If StartPoint >= 0 And StartPoint < 31 Then
		Go Approach_Slider +X(StartPoint)
		Wait (1)
		Go Approach_Slider +X(StartPoint) -Z(26.5)
	EndIf
Fend
Function go_tool_up
	' make sure the gripper is open 
		Go Here +Z(26.5)
Fend
