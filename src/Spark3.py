import cb
#import socket

class SparkManager (object):
    def __init__(self):
        self.spark_peripheral = None
        self.midi_peripheral = None
        self.spark_control_peripheral = None

        self.spark_send_char = None
        self.spark_recv_char = None
        self.midi_recv_char = None
        self.spark_control_recv_char = None

        self.midi_value = None
        self.spark_control_value = None

    def did_discover_peripheral(self, p):
        if p.name and 'Spark 40 BLE' in p.name and not self.spark_peripheral:
            self.spark_peripheral = p
            print('Connecting Spark')
            cb.connect_peripheral(p)

        if p.name and 'SKC50S-4 v3.0.1 9E02' in p.name and not self.spark_control_peripheral:
            self.spark_control_peripheral = p
            self.midi_peripheral = p
            print('Connecting Spark Control')
            cb.connect_peripheral(p)
 
        if p.name and 'Akai LPD8 Wireles' in p.name and not self.midi_peripheral:
            self.midi_peripheral = p
            print('Connecting Midi controller')
            cb.connect_peripheral(p)

    def did_connect_peripheral(self, p):
        #print('Connected:', p.name)
        #print('Discovering services...')
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print('Failed to connect: %s' % (error,))

    def did_disconnect_peripheral(self, p, error):
        print('Disconnected, error: %s' % (error,))
        self.spark_peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            print(s.uuid)
            if s.uuid == 'FFC0' or s.uuid == '03B80E5A-EDE8-4B33-A751-6CE34EC4C700' or s.uuid == '7BDB8DC0-6C95-11E3-981F-0800200C9A66':
                p.discover_characteristics(s)
            
    def did_discover_characteristics(self, s, error):
        print('Did discover characteristics...')
        for c in s.characteristics:

            if c.uuid == 'FFC2' and self.spark_recv_char == None:
                self.spark_recv_char = c
                self.spark_peripheral.set_notify_value(c, True)

            if c.uuid == 'FFC1' and self.spark_send_char == None:
                self.spark_send_char = c
                
            if c.uuid == '7772E5DB-3868-4112-A1A9-F2669D106BF3' and self.midi_recv_char == None:
                self.midi_recv_char = c
                self.midi_peripheral.set_notify_value(c, True)

            if c.uuid == '362F71A0-6C96-11E3-981F-0800200C9A66' and self.spark_control_recv_char == None:
                print('Got spark control')
                self.spark_control_recv_char = c
                self.spark_control_peripheral.set_notify_value(c, True)
               

    def did_update_value(self, c, error):
        if c.uuid == '7772E5DB-3868-4112-A1A9-F2669D106BF3':
            self.midi_value = c.value

        if c.uuid == '362F71A0-6C96-11E3-981F-0800200C9A66':
            self.spark_control_value = c.value
      
 
    def send_bytes(self, data):
        if self.spark_send_char != None:
           self.spark_peripheral.write_characteristic_value(self.spark_send_char, data, False)
           #print("Sent ", data)
        
    def get_midi_value(self):
        val = self.midi_value
        self.midi_value = None
        return val

    def get_spark_control_value(self):
        val = self.spark_control_value
        self.spark_control_value = None
        return val         

mngr = SparkManager()
cb.set_central_delegate(mngr)
print('Scanning for peripherals...')
cb.scan_for_peripherals()

tone1="01fe000053fe1a000000000000000000f00124000138000000f7"
tone2="01fe000053fe1a000000000000000000f00123010138000001f7"
tone3="01fe000053fe1a000000000000000000f00125020138000002f7"
tone4="01fe000053fe1a000000000000000000f00120030138000003f7"

tone1b=bytes.fromhex(tone1)
tone2b=bytes.fromhex(tone2)
tone3b=bytes.fromhex(tone3)
tone4b=bytes.fromhex(tone4)

print("Starting...")
while True:
    val = mngr.get_midi_value()
    if val != None:
        if (val[2] == 0x90) or (val[2] == 0xb0 and val[4] == 0x7f):
            param = val[3]
            if param in [0x18, 0x40]:  
                mngr.send_bytes(tone1b)
                print("[MIDI] Preset 1")
            elif param in [0x1a, 0x42]:
                mngr.send_bytes(tone2b)
                print("[MIDI] Preset 2")
            elif param in [0x1c, 0x41]:
                mngr.send_bytes(tone3b)
                print("[MIDI] Preset 3")
            elif param in [0x1d, 0x43]:
                mngr.send_bytes(tone4b)
                print("[MIDI] Preset 4")

    val = mngr.get_spark_control_value()
    if val != None:
        param = val[0]
        if param == 0x01:
            mngr.send_bytes(tone1b)
            print("[SC] Preset 1")
        elif param == 0x04:
            mngr.send_bytes(tone2b)
            print("[SC] Preset 2")
        elif param == 0x02:    
            mngr.send_bytes(tone3b)
            print("[SC] Preset 3")   
        elif param == 0x08:
            mngr.send_bytes(tone4b)
            print("[SC] Preset 4")
