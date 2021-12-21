import subprocess, json, argparse
 
parser=argparse.ArgumentParser()

parser.add_argument('-b', '--bucket', help='s3 bucket to restore from', required=True)
parser.add_argument('-i', '--input', help='input file', required=True)

args=parser.parse_args()

f = open(args.input)
data = json.load(f)

for d in data:
    print(d['prefix'])
    subprocess.call(f' python s3-pit-restore -b {args.bucket} -B {args.bucket} -p {d["prefix"]} -t "{d["timestamp"]}"', shell=True)
