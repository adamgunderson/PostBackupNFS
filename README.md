# PostBackupNFS
FMOS post-backup script to the send backup file to a NSF location. 

## Setup
### Create Virtual Environment and Install Libraries
This script a Python Virtual Environment (venv) to be able to run on FMOS.
Use the command below to create a venv in PostBackupNFS/.
```console
/usr/lib/firemon/devpackfw/bin/python -m venv PostBackupNFS
```
Activate venv.
```console
source ~/PostBackupNFS/bin/activate
```
Install pip.
```console
python3 ~/PostBackupNFS/bin/pip install -U pip
```
Now we can install the required libraries.
```console
python3 ~/PostBackupNFS/bin/pip install logging pyNfsClient 
```
Exit the python virtual environemnt:
```console
deactivate
```
Identify the absolut path where `~/PostBackupNFS/PostBackupNFS.py` exists. Absolute path is required when setting up the post-backup action in FireMon.
```console
cd ~
```
```console
pwd
```
In the steps going forward use absolute paths, replacing `~/` with the output of `pwd`.
### Configure the script.
Copy the `PostBackupNFS.py` file to ~`/PostBackupNFS/PostBackupNFS.py`.
Adjust the follwoing configuration varialbe to match your environment.
```python
# NFS Configuration
NFS_SERVER = 'nfs_server_address'
NFS_SHARE = '/path/to/nfs/share'
```
Test the script by sending a file.

### Setup FireMon Post-Backup Action
Login to the FireMon Server Control Panel usng https on port 55555.
Navigate to OS > Backup > Post-Backup Actions.
Click the `+` icon under "Run a command on the local machine"
In the "Command to run:" field enter the following (be sure to reference the absolue path in your environment).
```console
cd /home/firemon $$ /home/firemon/PostBackupNFS/bin/python /home/firemon/PostBackupNFS/PostBackupNFS.py ${BACKUP}
```
Click `Stage Changes` then `Apply Configuration`.
Test the post-backup action from CLI using the command below.
```console
fmos backup --prune
```
Look for errors in `nfs_transfer.log`.
