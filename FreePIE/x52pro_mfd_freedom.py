# This is a script for FreePIE (http://andersmalmgren.github.io/FreePIE/)
#
# It binds the MFD buttons on the x52pro to output keypad button presses.

if starting:
  x52pro = joystick[1]

class mfd():
  LeftRollerClick = x52pro.getDown(31)
  LeftRollerUp = x52pro.getDown(34)
  LeftRollerDown = x52pro.getDown(35)
  RightRollerClick = x52pro.getDown(38)
  RightRollerUp = x52pro.getDown(36)
  RightRollerDown = x52pro.getDown(37)
  StartStop = x52pro.getDown(32)
  Reset = x52pro.getDown(33)

keyboard.setKey(Key.NumberPad4, mfd.LeftRollerClick)
keyboard.setKey(Key.NumberPad7, mfd.LeftRollerUp)
keyboard.setKey(Key.NumberPad1, mfd.LeftRollerDown)
keyboard.setKey(Key.NumberPad6, mfd.RightRollerClick)
keyboard.setKey(Key.NumberPad8, mfd.RightRollerUp)
keyboard.setKey(Key.NumberPad3, mfd.RightRollerDown)
keyboard.setKey(Key.NumberPad2, mfd.Reset)
keyboard.setKey(Key.NumberPad5, mfd.StartStop)
