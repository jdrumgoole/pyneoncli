# pyneoncli

A python package and command line tool for interaction with the [Neon](https://neon.tech) Serverless Postgres [API](https://api-docs.neon.tech/reference/getting-started-with-neon-api).

This is a work in progress and this version is incomplete. 

This version only supports the Neon V2 API. 

The program can read the NEON_API_KEY from the environment or it can he loaded from a .env field in the current working directory.

# Operation
```
usage: neoncli [-h] [--apikey APIKEY] [--version] [--nocolor] [-f FIELDFILTER]
               {project,branch} ...

neoncli - python neon api client

positional arguments:
  {project,branch}      Neon commands
    project             maninpulate Neon projects
    branch              manuinplate Neon branches

options:
  -h, --help            show this help message and exit
  --apikey APIKEY       Specify NEON API Key (env NEON_API_KEY)
  --version             show program's version number and exit
  --nocolor             Turn off Color output
  -f FIELDFILTER, --fieldfilter FIELDFILTER
                        Enter field values to filter results on

Version : 0.0.6a
```