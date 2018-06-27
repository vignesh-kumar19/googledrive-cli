# edrive-cl, 

drivecli, a program which makes cli lovers to manage their google drive photos, videos or files in command line.  
Only one time authentication, no need to login to your account every time like GUI
It can perform tasks like search, download or upload photos, videos or files

---

## Prerequisites

* Need python 3
* Create project in [google developer console](https://console.developers.google.com/flows/enableapi?apiid=drive)

---

## Install
```
1. Clone the repo
2. cd googledrive-cli
2. pip install -e .
```
*** 

## Examples

### To create and authenticate with google drive

```
$ drivecli
```

### List files in your drive

```
$ drivecli search-file --all
+--------------------------+---------+---------------------+-----------------+
|       modifiedTime       |   size  |         name        |     mimeType    |
+--------------------------+---------+---------------------+-----------------+
| 2018-06-26T07:09:28.788Z |    3    |         build        |    text/plain   |
| 2018-06-12T18:29:44.456Z | 1560010 |   Getting started   | application/pdf |
| 2018-06-12T18:29:43.099Z |  109658 | crypto_currency.png |    image/png    |
+--------------------------+---------+---------------------+-----------------+
```

### Download file from drive

```
$ drivecli download-file --exact=build --localpath=/tmp/
Downloading build
Download 100%.
```

### Upload a file to drive

```
drivecli upload-file --filepath=/tmp/testfile --filetype=plain
Upload Complete!
```
