#!/usr/bin/python3

import evdev
import sys
from requests import post

#does the api call
def call_ha(command, authorization):
    url = "http://docker.lan:8123" + command
    headers = {
        "Authorization": authorization,
        "content-type": "application/json",
    }

    response = post(url, headers=headers)
    print(response.text)


# API Call to Key Bindings
bindings = {
    evdev.ecodes.KEY_SPACE: "/api/services/script/togglelight",
    evdev.ecodes.KEY_UP: "/api/services/script/brightnessup",
    evdev.ecodes.KEY_DOWN: "/api/services/script/brightnessdown",
    evdev.ecodes.KEY_ENTER: "/api/services/script/bed"
}

device = evdev.InputDevice('/dev/input/event0')
print(device)

if len(sys.argv) < 2:
    print("Missing authorization key")
    exit()

authorization = sys.argv[1]

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
        print(evdev.categorize(event))
        print(event.code)

        if event.code in bindings:
            call_ha(bindings[event.code], authorization)




        
