# PostBackupNFS
FMOS post-backup script to send backup file to NSF location. 

Requires Additiona Python Libraries
```console
pip install pyNfsClient
```

## Setup
This script a Python Virtual Environment (venv) to be able to run on FMOS.
Use the command below to create a venv in PostBackupNFS/.
```console
/usr/lib/firemon/devpackfw/bin/python -m venv PostBackupNFS
```
Activate venv.
```console
source PostBackupNFS/bin/activate
```
Install pip.
```console
python3 PostBackupNFS/bin/pip install -U pip
```
Now we can install the required libraries.
```console
python3 PostBackupNFS/bin/pip install sys os logging pyNfsClient 
```
