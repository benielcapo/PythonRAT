import requests
import json
import time
import subprocess
import io
import pyautogui

endPoint = "http://localhost:8080"

def GetScreenBytes():
    screenShot = pyautogui.screenshot()
    imgBytes = io.BytesIO()
    screenShot.save(imgBytes, "PNG")
    imgBytes.seek(0)
    return imgBytes

def GetScreen():
    imgBytes = GetScreenBytes()
    fileData = {"file": ("screenshot.png", imgBytes, "image/png")}
    requests.post(endPoint + "/upload", files=fileData)


requiredLibraries = ["numpy", "pyautogui"]

def InstallLibraries():
    for library in requiredLibraries:
        try:
            subprocess.run("pip install " + library, shell=True)
        except Exception as err:
            print("error while installing library " + library + ", error: " + err)

def GetInstructions():
    instructions = None
    try:
        response = requests.get(endPoint)
        instructions = response.json()
    except Exception as e:
        print(f"Error while fetching: {e}")
    if not instructions:
        return []
    return instructions

def ExecuteInstructions(instructions):
    for instruction in instructions:
        print("executing instruction: " + instruction)
        try:
            exec(instruction)
        except Exception as e:
            print(f"Error executing instruction: {e}")

def main():
    instructions = GetInstructions()
    ExecuteInstructions(instructions)

InstallLibraries()

while True:
    main()
    time.sleep(0.5)
