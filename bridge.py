import asyncio
from bleak import BleakScanner, BleakClient
from pythonosc import dispatcher
from pythonosc import osc_server
import atexit

ble_address = 'E1486812-63D0-45C7-A263-D7021401C6AB'
write_characteristics = [
  '19B10001-E8F2-537E-4F6C-D104768A1214',
  '19B10002-E8F2-537E-4F6C-D104768A1215',
  '19B10003-E8F2-537E-4F6C-D104768A1216',
  '19B10004-E8F2-537E-4F6C-D104768A1217',
  '19B10005-E8F2-537E-4F6C-D104768A1218',
]
values = [
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
]
num_servos = 5
# on_value = bytearray(0)
# off_value = bytearray([0x0])
# servoUp = False

def servo(newVal, index):
  global values
  values[index] = bytearray([int(hex(newVal), 16)])  

def servo0 (unused_addr, val):
  servo(val, 0)

def servo1 (unused_addr, val):
  servo(val, 1)

def servo2 (unused_addr, val):
  servo(val, 2)

def servo3 (unused_addr, val):
  servo(val, 3)

def servo4 (unused_addr, val):
  servo(val, 4)

async def sendToBoard():
  devices = await BleakScanner.discover(10)
  for device in devices:
    print(device)
  device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
  dispatch = dispatcher.Dispatcher()
  dispatch.map('/slider0', servo0)
  dispatch.map('/slider1', servo1)
  dispatch.map('/slider2', servo2)
  dispatch.map('/slider3', servo3)
  dispatch.map('/slider4', servo4)

  server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", 57121), dispatch, asyncio.get_event_loop())
  transport, protocol = await server.create_serve_endpoint()
  def exitHandler():
    transport.close()
  atexit.register(exitHandler)
  print(device)
  async with BleakClient(device) as client:
    while True:
      for i in range(num_servos):
        print("servo" + str(i) + " value: " + str(values[i]))
        await client.write_gatt_char(write_characteristics[i], values[i], False)
      await asyncio.sleep(0.1)


async def main():
  await sendToBoard()


          




      # for service in client.services:
      #   print("" + str(service) + str(service.uuid) + str(service.description))
      #   for char in service.characteristics:
      # dispatch = dispatcher.Dispatcher()
      # dispatch.map("/fred", servo)
      # server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 57121), dispatch)
      # arduinoLoop = asyncio.get_event_loop()
      # arduinoLoop.run_until_complete(sendToBoard())
      # server.serve_forever()
      # print("server running")

      # while True:
      #   if (servoUp):
      #     await client.write_gatt_char(write_characteristic, off_value, False)
      #   else:
      #     await client.write_gatt_char(write_characteristic, on_value, False)
      #   await asyncio.sleep(0.1)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# servoUp = False

# async def sendBluetoothMessages(client):

# dispatch = dispatcher.Dispatcher()
# dispatch.map("/fred", servo)
# server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 57121), dispatch)

# loop.run_until_complete(sendBluetoothMessages(client))
# server.serve_forever()

