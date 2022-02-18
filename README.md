# iPadSparkPythonista
Change presets on the Spark 40 amp with only an ipad (no Spark app).    

- Spark.py presents a midi interface over UDP for a midi app like MidiFire. This allows generic Midi control of the Spark amp.   
- Spark2.py connects to a midi bluetooth controller like the Akai LPD8 Wireless.  This allows the controller to control the Spark amp.    

Spark.py requires:
- a midi device of some sort (in my case, an Akai LPD8 wireless)    
- iOS device
- Pythonista app
- MidiFire app

MidiFire send the CoreMIDI message over UDP to the Pythonista app which then communicates to the Spark Amp over BLE.   

## Installation

Purchase Pythonista   
Purchase MidiFire   

Set up MidiFire as follows:

- In Setup select Connect Device to find your bluetooth midi device
- Using the +, select that device
- Using the +, select OSC Exchange module
- Using the +, select Event Monitor module
- Link them as in the diagram - midi device to both OSC Exchange and Event Monitor
- In OSC Exchange, select settting (gear wheel) then UDP Send Port is 5555 and Wrap Data in Sysex is No.

Test this by pressing keys on your device and see MidiFire light each module appropriately, and see the MIDI even in Event Monitor

In Pythonista, copy the code in Spark.py then run it using the run arrow.
Turn on the Spark.
You should see connection messages.

Then all is ready.

The Python code will need to be tweaked for the specific MIDI messages your devce produces.

## Pictures

<p align="center">
  <img src="https://github.com/paulhamsh/iPadSparkPythonista/blob/main/pictures/IMG_0010.PNG" width="700" title="connections">
</p>

<p align="center">
  <img src="https://github.com/paulhamsh/iPadSparkPythonista/blob/main/pictures/IMG_0011.PNG" width="700" title="connections">
</p>

<p align="center">
  <img src="https://github.com/paulhamsh/iPadSparkPythonista/blob/main/pictures/IMG_0012.PNG" width="700" title="connections">
</p>

<p align="center">
  <img src="https://github.com/paulhamsh/iPadSparkPythonista/blob/main/pictures/IMG_0013.PNG" width="700" title="connections">
</p>

<p align="center">
  <img src="https://github.com/paulhamsh/iPadSparkPythonista/blob/main/pictures/IMG_0014.PNG" width="700" title="connections">
</p>
