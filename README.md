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

* To local file-system:
	```
	$ s3-pit-restore -b my-bucket -d restored-bucket-local -t "06-17-2016 23:59:50 +2"
	```
* To s3 bucket:-
	```
	$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -t "06-17-2016 23:59:50 +2"
	```

Choosing the correct time and date to restore at is simply a matter of getting
that information clicking the *Versions: Show* button from the S3 web gui
and navigating through the, now appeared, versions timestamps.

## Installing

With pip install:

`$ pip3 install s3-pit-restore`

or clone the repository and launch:

`$ python3 setup.py install`

## Requirements

  * Python 3
  * AWS credentials available in the environment
	* This can be accomplished in various ways:
		* Environment Variables:
			* AWS_ACCESS_KEY_ID
			* AWS_SECRET_ACCESS_KEY
			* AWS_DEFAULT_REGION
		* Your `~/.aws/ files`
			* Configured with `aws configure`

## Usage

`s3-pit-restore` can do a lot of interesting things. The base one is restoring an entire bucket to a previous state:

### Restore to local file-system

* Restore to local file-system directory `restored-bucket-local`
	```
	$ s3-pit-restore -b my-bucket -d restored-bucket-local -t "06-17-2016 23:59:50 +2"
	```
	* `-b` gives the source bucket name to be restored from
	* `-d` gives the local folder to restore to (if it doesn't exist it will be created)
	* `-t` gives the target date to restore to. Note: The timestamp must include the timezone offset. 

### Restore to s3 bucket

* Restore to same bucket:
	```
	$ s3-pit-restore -b my-bucket -B my-bucket -t "06-17-2016 23:59:50 +2"
	```
	* `-B` gives the destination bucket to restore to. Note: Use the same bucket name to restore back to the source bucket.

* Restore to different bucket:-
	```
	$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -t "06-17-2016 23:59:50 +2"
	```

* Restore to s3 bucket with custom virtual prefix [restored object(src_obj) will have key as `new-restored-path/src_obj["Key"]`] (Using `-P` flag)
	```
	$ s3-pit-restore -b my-bucket -B restored-bucket-s3 -P new-restored-path -t "06-17-2016 23:59:50 +2"
	```

### Other common options for both the cases

* Another thing it can do is to restore a subfolder (*prefix*) of a bucket:
	```
	$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -t "06-17-2016 23:59:50 +2"
	```
	* `-p` gives a prefix to isolate when checking the _source_ bucket (`-P` is used when deal with the _destination_ bucket/folder)

* You can also speedup the download if you have bandwidth using more parallel workers (`--max-workers` flag):
	```
	$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -t "06-17-2016 23:59:50 +2" --max-workers 100
	```

* If want to restore a well defined time span, you can use a starting (`-f`) and ending (`-t`) timestamp (a month in this example):
	```
	$ s3-pit-restore -b my-bucket -d my-restored-subfolder -p mysubfolder -f "05-01-2016 00:00:00 +2" -t "06-01-2016 00:00:00 +2"
	```

## Command line options

```
usage: s3-pit-restore [-h] -b BUCKET [-B DEST_BUCKET] [-d DEST] [-p PREFIX] [-P DEST_PREFIX] [-t TIMESTAMP] [-f FROM_TIMESTAMP] [-e] [-v] [-u ENDPOINT_URL] [--dry-run] [--debug] [--test] [--max-workers MAX_WORKERS]
                      [--sse {AES256,aws:kms}]

options:
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
  -u ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        use another endpoint URL for s3 service
  --dry-run             execute query without transferring files
  --debug               enable debug output
  --test                s3 pit restore testing
  --max-workers MAX_WORKERS
                        max number of concurrent download requests
  --sse {AES256,aws:kms}
                        Specify server-side encryption
```

## Docker Usage

```bash
# make a new local dir in your current path
mkdir restore

# restore a point in time copy under the restore dir you just created
docker run -ti --rm --name=s3-pit-restore -v {$PWD}/restore:/tmp -e AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID] -e AWS_SECRET_ACCESS_KEY=[AWS_ACCESS_KEY_ID] angelocompagnucci/s3-pit-restore -b [Bucket] -p [Prefix] -d /tmp -t "01-25-2018 10:59:50 +2"
```

## Testing

s3-pit-restore comes with a testing suite. You can run it with:

### Restore to local file-system test cases:
	`$ ./s3-pit-restore -b my-bucket -d /tmp/ --test`

### Restore to s3 bucket test cases:
	`$ ./s3-pit-restore -b my-bucket -B restore-bucket-s3 -P restore-path --test` (make sure you have s3 bucket `restore-bucket-s3`)

### Run all the test cases:
	`$ ./s3-pit-restore -b my-bucket -B restore-bucket-s3 -d /tmp/ -P restore-path --test`


## Point-in-time restore strategy

Restoring an S3 bucket to a given point in time means traversing all object
versions and delete markers to determine which ones were the latest at the given
time.

The overall strategy is fairly simple, since it's a matter of comparing
timestamps of versions and delete markers, and restoring the one that's closest
in time to the given point-in-time.

### S3 API details

The source of versions and delete markers in an S3 bucket is the
ListObjectVersions API call. The response is paged with a maximum of 1000
entries per page. Each page may have a list of up to 1000 versions and/or a
separate list of up to 1000 delete markers.

The versions and delete markers are returned in order of key name and recency
(newest first). As S3 iterates over these, it appends versions and delete
markers to separate lists and responds with a page when it reaches the requested
page size (1000 by default).

For reference, [here's how localstack implements it](https://github.com/localstack/localstack/blob/v2.3.2/localstack/services/s3/v3/provider.py#L1491).

Examples:

* If there are 1001 versions of a given key, then the first page contains only a
  list of versions, and that list has the most recent 1000 versions of the
  object. The next page has 1 version (the oldest) of that same object.

* If there are 1001 versions and 1001 delete markers for a given key, then:

  * If all the delete markers were placed after the versions, then:

    * Page 1: 1000 delete markers

    * Page 2: 1 delete marker, 999 versions

    * Page 3: 2 versions

  * If the delete markers and versions are mixed in time, say if an object is
    deleted and written over and over, then:

    * Page 1: 500 versions, 500 delete markers

    * Page 2: 500 versions, 500 delete markers

    * Page 3: 1 version, 1 delete marker

The number of versions or delete markers for a key can easily span two or more
pages, so they must be tracked between pages. Only when a new key name is
observed can we be sure that we have seen all versions or delete markers for a
key.

### Ordering

Since S3 has 1-second granularity on the LastModified timestamp, multiple
versions and/or delete markers may end up having the same timestamp.

To determine which version or delete marker is newest when they all have the
same LastModified timestamp:

* If the IsLatest attribute is true, then this object is the newest.

* For previous versions where neither is the latest, assume that S3's order is
  correct and use the first of the two versions as the most recent one.

* For previous delete markers, it doesn't really matter: They both represent a
  deletion anyway.

* For a previous version vs a delete marker, it is impossible to say which is
  the most recent one since they are kept in different lists. In this case, the
  version takes precedence over the delete marker.
