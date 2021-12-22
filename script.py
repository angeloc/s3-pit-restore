import subprocess, json

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
items = data["items"]

# Display the config parameters
outputStr = '''
        Input Parameters
        ------------------------------
        Dry Run:     {dryRun}
        Bucket:      {bucket}
        Timestamp:   {timestamp}
        Items:       {items}
    '''
print(outputStr.format(**locals()))


input = ask_yesno("Continue ? (y/n)")

if input is True: 
    print("user consent. Starting")
    
    # Process the records
    for index, item in enumerate(items, start=1):
        print("------------------------------------------------")
        print("Processing {} of {} , path = {} ".format(index, len(items), item))
        if dryRun:
            subprocess.call(f' python s3-pit-restore -b {bucket} -B {bucket} -p {item} -t "{timestamp}" -v --dry-run', shell=True)
        else:
            subprocess.call(f' python s3-pit-restore -b {bucket} -B {bucket} -p {item} -t "{timestamp}" -v', shell=True)
else:
    print("user denied, Exiting")