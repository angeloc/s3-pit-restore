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
	"dryRun": true,
	"skipDeletion": true,
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

- skipDeletion 
  - If true, it will skip deletion of objects created after the mentioned timestamp while restoring
  - If false, it will delete the objects created after the mentioned timestamp while restoring

- bucket - The name of the AWS S3 bucket in which the restore operation will be performed.

- timestamp - The date and time at which the folder will be restored. The timestamp format is **MM-DD-YYYY HH:MM:SS +UTC**. Note: The timestamp must include the timezone offset.

- items - list the folders which will be restored. Multiple folders/files can be passed

## Output 
The output is logged in console and in the log file created under directory `/logs`

### Sample Logs

With **Dry Run** set to **True**: 

[Log Timestamp] [Log Level] [File Path] [Current Version] [Restore Version] [Version Timestamp] [Change Type]

```
2022-01-03 11:33:30,928 INFO "manpreet/file1.json" "nzstzGyhRjf8ptjEbgAvTj.pcEr3IEu_" "OVE5ZRkM4kNT9VpzpjN7PG.EUvVNRgsd" "2021-12-29 09:59:48+00:00" "modified" 
2022-01-03 11:33:31,139 INFO "manpreet/file3.json" "6rc2V8JLgz_cxOrtZd6niX4RQUBGOlWm" "MZFt6mt7Ffbx_Qho0ITQRD4lxdN8oiT_" "2021-12-29 09:59:48+00:00" "modified" 
2022-01-03 11:33:31,249 INFO "manpreet/file6.json" "nq2ofbnPcci6IqH_cWHNiJux25eY3qbF" "" "2021-12-29 11:56:15+00:00" "created" 
```

With **Dry Run** set to **False**: 

[Log Timestamp] [Log Level] [File Path]

```
2022-01-03 11:49:00,293 INFO manpreet/file1.json
2022-01-03 11:49:00,381 INFO manpreet/file3.json
2022-01-03 11:49:00,439 INFO manpreet/file6.json
```
