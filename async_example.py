# import datetime
# import asyncio
#
# async def display_date(loop):
#     end_time = loop.time() + 5.0
#     while True:
#         print(datetime.datetime.now())
#         if (loop.time() + 1.0) >= end_time:
#             break
#         await asyncio.sleep(1)
#
#
# loop = asyncio.get_event_loop()
# # Blocking call which returns when the display_date() coroutine is done
# loop.run_until_complete(display_date(loop))
#
# print('this line is after the loop')
# loop.close()

import threading, time

def f():
    print("f started")
    time.sleep(3)
    print("f finished")

threading.Thread(target=f).start()
print('\n this line is after function call')