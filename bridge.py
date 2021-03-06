import asyncio
from logging import error
from bleak import BleakScanner, BleakClient
from pythonosc import dispatcher
from pythonosc import osc_server
import atexit

def bytes_to_int(bytes):
  return int.from_bytes(bytes, 'big')

# ble_address = 'D1316A97-230E-45B8-9BA0-9A308A11D4AD'
write_characteristics = [
  '7c962495-dd04-496a-87a8-2f837bc3eedd',
  '84e1e552-67a4-4a29-8553-b597c731554f',
  '9bb9e2bc-5799-49ce-a1cf-8385de906f7f',
  '577f2be7-5c69-4591-87bc-67fbf914aeb4',
  'c614f8b8-f751-4197-9eda-53652d882deb',
]
notify_characteristic = 'b28cbce8-06b0-44d0-8e94-2ece7b9526f3'

values = [
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
  bytearray([int(hex(0), 16)]),
]

prevValues = values.copy()
num_servos = 5

client = -1

def servo(newVal, index):
  global client
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

def callback(sender: int, data: bytearray):
    print(f"{sender}: {data}")

dispatch = dispatcher.Dispatcher()
dispatch.map('/slider0', servo0)
dispatch.map('/slider1', servo1)
dispatch.map('/slider2', servo2)
dispatch.map('/slider3', servo3)
dispatch.map('/slider4', servo4)


async def getBLEDevice():
  print ("Scanning for ServoCallback")
  while True:
    devices = await BleakScanner.discover(5)
    for device in devices:
      if device.name == "ServoCallback":
        print("ServoCallback found")
        return device
    "ServoCallback not found, rerunning scanner"

async def sendToBoard():
  device = await getBLEDevice()
  print(device)

  server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", 57121), dispatch, asyncio.get_event_loop())
  transport, protocol = await server.create_serve_endpoint()
  def exitHandler():
    transport.close()
  atexit.register(exitHandler)
  async with BleakClient(device) as client:
    # print(client.get_services)
    print("Awaiting supercollider commands...")

    # await client.start_notify(notify_characteristic, callback)

    isConnected = client.is_connected
    while isConnected:
      for i in range(num_servos):
        if (client.is_connected):
          if (prevValues[i] != values[i]):
            print("servo" + str(i) + " value: " + str(bytes_to_int(values[i])))
            await client.write_gatt_char(write_characteristics[i], values[i], False)
            prevValues[i] = values[i]
          await asyncio.sleep(0.01)
        else:
          isConnected = False
    print("ServoCallback disconnected, reestablishing connection")
    transport.close()
    atexit.unregister(exitHandler)


async def main():
  while True:
    await sendToBoard()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# servoUp = False
