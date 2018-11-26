# S3 point in time restore

This is the repository for s3-pit-restore, a point in time restore tool
for Amazon S3.

The typical scenario in which you may need this tool is when you have
enabled versioning on an S3 bucket and want to restore some or all of
the files to a certain point in time, to local file system, same s3 bucket or different s3 bucket.

Doing this with the web interface is time consuming: Amazon S3 web management
gui doesn't offer a simple way to do that on a massive scale.

With this tool you can easily restore a repository to a point in time
with a simple command like:

	* To local file-system:-
		`$ s3-pit-restore -b my-bucket -d restored-bucket-local -t "06-17-2016 23:59:50 +2"`
	* To s3 bucket:-
		`$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -t "06-17-2016 23:59:50 +2"`

Choosing the correct time and date to restore at is simply a matter of getting
that information clicking the *Versions: Show* button from the S3 web gui
and navigating through the, now appeared, versions timestamps. 

## Installing

With pip install:

`$ pip3 install s3-pit-restore`

or clone the repository and launch:

`$ python3 setup.py install`

## Usage

`s3-pit-restore` can do a lot of interesting things. The base one is restoring an entire bucket to a previous state:

### Restore to local file-system

	* Restore to local file-system directory `restored-bucket-local`
		`$ s3-pit-restore -b my-bucket -d restored-bucket-local -t "06-17-2016 23:59:50 +2"`

### Restore to s3 bucket

	* Restore to same bucket:-
		`$ s3-pit-restore -b my-bucket -B my-bucket -t "06-17-2016 23:59:50 +2"`

	* Restore to different bucket:-
		`$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -t "06-17-2016 23:59:50 +2"`

	* Restore to s3 bucket with custom virtual prefix [restored object(src_obj) will have key as `new-restored-path/src_obj["Key"]`]
		`$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -P new-restored-path -t "06-17-2016 23:59:50 +2"`

### Other common options for both the cases

(explained using `Restore to local file-system` case)

	* Another thing it can do is to restore a subfolder (*prefix*) of a bucket:
		`$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -t "06-17-2016 23:59:50 +2"`

	* You can also speedup the download if you have bandwidth using more parallel workers:
		`$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -t "06-17-2016 23:59:50 +2" --max-workers 100`

	* If want to restore a well defined time span, you can use a starting and ending timestamp (a month in this example):
		`$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -f "05-01-2016 00:00:00 +2" -t "06-01-2016 00:00:00 +2"`

## Command line options

```
usage: s3-pit-restore [-h] -b BUCKET [-B DEST_BUCKET] [-d DEST]
                      [-P DEST_PREFIX] [-p PREFIX] [-t TIMESTAMP]
                      [-f FROM_TIMESTAMP] [-e] [-v] [--dry-run] [--debug]
                      [--test] [--max-workers MAX_WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                        s3 bucket to restore from
  -B DEST_BUCKET, --dest-bucket DEST_BUCKET
                        s3 bucket where recovering to
  -d DEST, --dest DEST  path where recovering to on local
  -p PREFIX, --prefix PREFIX
                        s3 path to restore from
  -P DEST_PREFIX, --dest-prefix DEST_PREFIX
                        s3 path to restore to
  -t TIMESTAMP, --timestamp TIMESTAMP
                        final point in time to restore at
  -f FROM_TIMESTAMP, --from-timestamp FROM_TIMESTAMP
                        starting point in time to restore from
  -e, --enable-glacier  enable recovering from glacier
  -v, --verbose         print verbose informations from s3 objects
  --dry-run             execute query without transferring files
  --debug               enable debug output
  --test                s3 pit restore testing
  --max-workers MAX_WORKERS
                        max number of concurrent download requests
```

## Docker Usage

```bash
# make a new local dir in your current path
mkdir restore

# restore a point in time copy under the restore dir you just created
docker run -ti --rm --name=s3pit -v {$PWD}/restore:/tmp -e AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID] -e AWS_SECRET_ACCESS_KEY=[AWS_ACCESS_KEY_ID] avatarnewyork/s3-pit-restore:latest s3-pit-restore -b [Bucket] -p [Prefix] -d /tmp -t "01-25-2018 10:59:50 +2"
```

## Testing

s3-pit-restore comes with a testing suite. You can run it with:

### Restore to local file-system test cases:
	`$ ./s3-pit-restore -b my-bucket -d /tmp/ --test`

### Restore to s3 bucket test cases:
	`$ ./s3-pit-restore -b my-bucket -B restore-bucket-s3 -P restore-path --test` (make sure you have s3 bucket `restore-bucket-s3`)

### Run all the test cases:
	`$ ./s3-pit-restore -b my-bucket -B restore-bucket-s3 -d /tmp/ -P restore-path --test`
