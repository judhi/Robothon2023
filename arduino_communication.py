import serial

class ArduinoCommunication:
    def __init__(self, port, baudrate):
        # Open serial port
        self.ser = serial.Serial(port, baudrate)

        # Flush serial buffer
        self.ser.flushInput()
        self.ser.flushOutput()
        
        while 1:
            response = self.ser.readline().decode().strip()
            print(response)
            if (response == "Ready"):
                print("Arduino is ready")
                break

    def readline(self):
        # Wait for response from Arduino
        response = self.ser.readline().decode().strip()

        return response
    
    def communicate(self, message):
        # Send data to Arduino
        self.ser.write(message.encode())

        # Wait for response from Arduino
        response = self.ser.readline().decode().strip()

        return response

    def close(self):
        # Close serial port
        self.ser.close()
