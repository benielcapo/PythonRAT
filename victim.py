import requests
import json
import time
import subprocess

endPoint = "YOUR_END_POINT"

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
