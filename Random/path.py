import sys, os
if getattr(sys, 'frozen', False): # we are running in a bundle
    bundle_dir = sys._MEIPASS # This is where the files are unpacked to
else: # normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

print ('Location : ' + bundle_dir) # Where the base file exists

file = bundle_dir + '\\test.txt'
print ('File is at: ' + os.path.abspath(file)) # Absolute path of target file
if os.path.isfile(file):
    with open(file, "r") as f:
        print ('Contents:\n' + f.read()) # Print contents of file if it exists
else:
    print ('Created a new file') # Create a file if it doesn't exist

with open(file, "a") as f:
    f.write('New Line\n') # Add a new line to see if is there next time

input() # Block to keep terminal alive
