#IfWinActive, Tibia
SetMouseDelay, -1
SetKeyDelay, 1
SetDefaultMouseSpeed, 2

WheelLeft::
WheelRight::
    Mousegetpos,x,y
    Send {Shift down}
    Send {Click 1145,520, right}
    Send {Click 1245,520, right}
    Send {Click 1345,520, right}
    Send {Click 1145,620, right}
    Send {Click 1245,620, right}
    Send {Click 1345,620, right}
    Send {Click 1145,720, right}
    Send {Click 1245,720, right}
    Send {Click 1345,720, right}
    Send {Shift up}

    MouseMove, %x%, %y%
return

^Esc::ExitApp