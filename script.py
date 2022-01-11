import subprocess, json
from datetime import datetime

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

# Read input file and parameters
file = open('input.json')
data = json.load(file)

dryRun = data["dryRun"]
bucket = data["bucket"]
timestamp = data["timestamp"]
skipDeletion = data["skipDeletion"]
items = data["items"]
logFileName = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# Display the config parameters
outputStr = '''
        Input Parameters
        ------------------------------
        Dry Run:       {dryRun}
        Skip Deletion: {skipDeletion}
        Bucket:        {bucket}
        Timestamp:     {timestamp}
        Items:         {items}
    '''
print(outputStr.format(**locals()))


input = ask_yesno("Continue ? (y/n)")

if input is True: 
    print("user consent. Starting")
    scriptcmd = f'python s3-pit-restore -b {bucket} -B {bucket} -t "{timestamp}" --avoid-duplicates --logFileName "{logFileName}"'
    
    #Process the records
    for index, item in enumerate(items, start=1):
        itemcmd = f'{scriptcmd} -p {item}'
        optioncmd = itemcmd
        print("------------------------------------------------")
        print(f"Processing {index} of {len(items)} , path = {item}")
        if skipDeletion:
            optioncmd = f'{optioncmd} --skip-deletion'
        if dryRun:
            optioncmd = f'{optioncmd} -v --dry-run'
            
        subprocess.call(optioncmd, shell=True)
else:
    print("user denied, Exiting")