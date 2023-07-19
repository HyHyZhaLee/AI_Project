

relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

def setPumpOn(self):
    print("PUMP is ON")
    self.rs485.modbus485_send(self.relay2_ON)
    return


def setPumpOff(self):
    print("PUMP is OFF")
    self.rs485.modbus485_send(self.relay2_OFF)
    return

setPumpOn()