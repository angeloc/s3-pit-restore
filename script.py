import subprocess, json, sys
from datetime import datetime
from pathlib import Path

# Function to ask user confirmation
def ask_yesno(question):
    yes = {'yes', 'y'}
    no = {'no', 'n'}

    done = False
    print(question)
    while not done:
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond by yes or no.") 

# Check python version 
if sys.version_info[0] < 3:
    print('Script is supported only for python 3 version')
    sys.exit()

# Read input file and parameters
file = open('input.json')
data = json.load(file)

dryRun = data["dryRun"]
bucket = data["bucket"]
deletionMode = data["deletionMode"]
timestamp = data["timestamp"]
items = data["items"]
logFileName = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
delimiter = data["delimiter"]
ignoreList = data["ignoreList"]

# Display the config parameters
outputStr = '''
        Input Parameters
        ------------------------------
        Dry Run:       {dryRun}
        Deletion Mode: {deletionMode}
        Bucket:        {bucket}
        Timestamp:     {timestamp}
        Items:         {items}
        Delimiter:     {delimiter}
        Ignore List:   {ignoreList}
    '''
print(outputStr.format(**locals()))


input = ask_yesno("Continue ? (y/n)")

if input is True: 
    print("user consent. Starting")
    pycmd = Path(sys.executable).stem
    scriptcmd = f'{pycmd} s3-pit-restore -b {bucket} -B {bucket} -t "{timestamp}" --avoid-duplicates --logFileName "{logFileName}" --delimiter "{delimiter}" --ignore-list "{ignoreList}" --deletion-mode "{deletionMode}"'
    
    #Process the records
    for index, item in enumerate(items, start=1):
        itemcmd = f'{scriptcmd} -p {item}'
        optioncmd = itemcmd
        print("------------------------------------------------")
        print(f"Processing {index} of {len(items)} , path = {item}")
        if dryRun:
            optioncmd = f'{optioncmd} -v --dry-run'
            
        subprocess.call(optioncmd, shell=True)
else:
    print("user denied, Exiting")
