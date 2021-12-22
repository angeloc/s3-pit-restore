# Script for S3 Restore
This script restores several AWS-S3 folders at once using the S3-pit-restore library.
For refrence, here is the official documentation of [s3-pit-restore](./script_README.md).

We must give data in the `input.json` file, that will be used by the script.
You can run the script by simply running this command:
```bash
$ python script.js
```
- - -

## Installing
- clone the repository
```bash
$ git clone https://github.com/yashijain1998/s3-pit-restore.git
```

- Go to the repository:
```bash
$ cd s3-pit-restore
```

- Run the script:
```bash
$ python script.js
```
- - -

## Data for input.json
We need to provide values in `input.json`.

![input-data](https://user-images.githubusercontent.com/86454870/147052865-32f7bd10-1db9-41e1-8994-c87838407357.png)

- dryRun 
  - If true, it will display a list of files that will be restored but will not perform any actual operations in AWS S3.
  - If false, it will restore the folders in AWS S3 according to the timestamp.

- bucket - The name of the AWS S3 bucket in which the restore operation will be performed.

- timestamp - The date and time at which the folder will be restored. The timestamp format is **MM-DD-YYYY HH:MM:SS +UTC**. Note: The timestamp must include the timezone offset.

- items - list the folders which will be restored.

## Output 
When -v [verbose] param is passed, the output is logged in console in the format 

[timestamp] [versionId] [size] [storage class] [file name]

![with verbose](https://user-images.githubusercontent.com/86454870/147057112-778b5ecd-0dff-4182-973c-73d5079f12c7.png)

Without verbose, the output is only the *file name* that is restored.

![without verbose](https://user-images.githubusercontent.com/86454870/147058015-20997348-abcb-47fd-996e-43c4bb1ee13a.png)

