# dependencies

# prerequisite
* Visual C++ Redistributable XXXX , I dont know which, cv2 doesnt work without some DLL
* Python 3.71 - https://www.python.org/downloads/release/python-371/ (make sure do add python to PATH)
* Install tesseract - https://github.com/UB-Mannheim/tesseract/wiki  (add to path as well, C:\Program Files (x86)\Tesseract-OCR)
* replace file eng.traineddata with the one from git repository in "C:\Program Files (x86)\Tesseract-OCR\tessdata"

# Libraries
pip install opencv-python pyautogui pytesseract pillow

# TO:DO
* Simulate mouse and key movement
* Add support for multiple monitors
* Support window being not in focus - screenshotting the process
* Develop some kind of cavebot