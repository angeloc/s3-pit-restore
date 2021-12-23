# Script for S3 Restore
This script restores several AWS-S3 folders at once using the S3-pit-restore library.
For refrence, here is the official documentation of [s3-pit-restore](./script_README.md).

We must give data in the `input.json` file, that will be used by the script.
You can run the script by simply running this command:
```bash
$ python script.js
```
- - -

## Prerequisitex

  * Python 3
  * AWS credentials available in the environment
	* This can be accomplished in various ways:
		* Environment Variables:
			* AWS_ACCESS_KEY_ID
			* AWS_SECRET_ACCESS_KEY
			* AWS_DEFAULT_REGION
		* Your `~/.aws/ files`
			* Configured with `aws configure`

## Installing
- clone the repository
```bash
$ git clone https://github.com/yashijain1998/s3-pit-restore.git
```

- Go to the repository:
```bash
$ cd s3-pit-restore
```

- Install s3-pit-restore dependency
```bash
$ pip3 install s3-pit-restore
``` 

- Run the script:
```bash
$ python script.js
```
- - -

## Data for input.json
We need to provide values in `input.json`.

```
{
	"dryRun": false,
	"bucket": "ms-versioning-bucket",
	"timestamp": "12-23-2021 15:25:00 +5:30",
	"items": [
		 "level1/level2-1/"
	]
}
```

- dryRun 
  - If true, it will display a list of file/folder that will be restored but will not perform any actual operations in AWS S3.
  - If false, it will restore the file/folder in AWS S3 according to the timestamp.

- bucket - The name of the AWS S3 bucket in which the restore operation will be performed.

- timestamp - The date and time at which the folder will be restored. The timestamp format is **MM-DD-YYYY HH:MM:SS +UTC**. Note: The timestamp must include the timezone offset.

- items - list the folders which will be restored. Multiple folders/files can be passed

## Output 
The output is logged in console in the format 

[creation timestamp] [versionId] [size] [storage class] [file name]

* creation timestamp - The time when the version of the file/folder was created.
* versionId - The version Id of the restored file/folder.
* size - The file/folder folder's size.
* storage class - The storage class of bucket.
* file name - The restored or deleted file/folder.

![Script output](https://i.ibb.co/zN8c7SK/image.png)
