# UNDER DEVELOPMENT
# dependencies

# Libraries
pip install opencv-python pyautogui pytesseract pillow 

# Other
AHK script included to keep window of choice on top with (ctrl + space)

# TO:DO
* Set default values for healing etc, force 0 if no value.
* Move mana pot to heal pot if statement? add check for hp before using mana pot
* Load / Save settings
* Add support for multiple monitors
* Support window being not in focus - screenshotting the process
* Develop some kind of cavebot


# prerequisite for ocr stuff
* Visual C++ Redistributable XXXX 
* Python 3.71 - https://www.python.org/downloads/release/python-371/ (make sure do add python to PATH)
* Install tesseract - https://github.com/UB-Mannheim/tesseract/wiki  (add to path as well, C:\Program Files (x86)\Tesseract-OCR)
* replace file eng.traineddata with the one from git repository in "C:\Program Files (x86)\Tesseract-OCR\tessdata"