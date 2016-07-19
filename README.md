## S3 Browser [![Build Status](https://travis-ci.org/andrewgross/s3browser.svg?branch=master)](https://travis-ci.org/andrewgross/s3browser) [![Coverage Status](https://coveralls.io/repos/github/andrewgross/s3browser/badge.svg?branch=master)](https://coveralls.io/github/andrewgross/s3browser?branch=master)


S3Browser is a tool to help you browse your S3 Buckets like a local filesystem.  It features `cd`, `ls`, and `pwd` for now, with some added bonuses around showing rollups for directory sizes and the most recently modified file.  For now it is read only, though if you want any features feel free to suggest them.


### Installation

```
pip install s3browser
```

### Usage

You can pass access keys to `s3browser` directly, or just let it pick them up from your environment.  It uses `boto` under the hood so you can use an existing configurations for that.

```
usage: s3browser [-h] [--access-key-id ACCESS_KEY_ID]
                 [--secret-access-key SECRET_ACCESS_KEY]

Run S3Browser

optional arguments:
  -h, --help            show this help message and exit
  --access-key-id ACCESS_KEY_ID
                        AWS_ACCESS_KEY_ID used by Boto
  --secret-access-key SECRET_ACCESS_KEY
                        AWS_SECRET_ACCESS_KEY used by Boto
```

Once you are in the CLI, it will automatically load a list of all of your available S3 buckets.  You can use the `help` command to get detailed information for each of the commands.


### Gotchas

`s3browser` is written in Python, so it is not the most efficient.  For really large buckets be prepared to wait a while for it to complete.  S3 requires us to page through all the files to retrieve them, and currently that is done serially in chunks of 1000.  Additionally, the internal representation of each S3 Key is ~800 Bytes, once you use `refresh` on a bucket with millions of keys, expect some memory pressure.

I have successfully browsed ~15mm keys on my dev machine with 16GB of RAM, of which python used ~12GB.  If key retrieval speed or memory usage are big issues for you, feel free to open a ticket and we can spend the time to find better ways to implement the internal structures so they are more compact!
