# S3 point in time restore

This is the repository for s3-pit-restore, a point in time restore tool
for Amazon S3.

The typical scenario in which you may need this tool is when you have
enabled versioning on an S3 bucket and want to restore some or all of
the files to a certain point in time.

Doing this with the web interface is time consuming: Amazon S3 web management
gui doesn't offer a simple way to do that on a massive scale.

With this tool you can easly restore a repository to a point in time
with a simple command like this:

`:~$ s3-pit-restore -b my-bucket -d my-restored-bucket -t "06-17-2016 23:59:50 +2"`

Choosing the correct time and date to restore at is simply a matter of getting
that information clicking the *Versions: Show* button from the S3 web gui
and navigating through the, now appeared, versions timestamps. 

## Installing

With pip install:

`:~# pip3 install s3-pit-restore`

or clone the repository and launch:

`:~# python3 setup.py install`
