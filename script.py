import subprocess, json

file = open('input.json')
data = json.load(file)

dryRun = data["dryRun"]
bucket = data["bucket"]
timestamp = data["timestamp"]
items = data["items"]

for item in items:
    if dryRun:
        subprocess.call(f' python s3-pit-restore -b {bucket} -B {bucket} -p {item} -t "{timestamp}" -v --dry-run', shell=True)
    else:
        subprocess.call(f' python s3-pit-restore -b {bucket} -B {bucket} -p {item} -t "{timestamp}" -v', shell=True)

