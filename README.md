# FMOS Post-Backup Script to send Backup to NFS
This script can run on FMOS to send automatically generated backup files to a NSF location. 

## Setup
### Create Virtual Environment and Install Libraries
This script a Python Virtual Environment (venv) to be able to run on FMOS.
1. Use the command below to create a venv in PostBackupNFS/.
```console
/usr/lib/firemon/devpackfw/bin/python -m venv PostBackupNFS
```
2. Activate venv.
```console
source ~/PostBackupNFS/bin/activate
```
3. Install pip.
```console
python3 ~/PostBackupNFS/bin/pip install -U pip
```
4. Now we can install the required libraries.
```console
python3 ~/PostBackupNFS/bin/pip install logging pyNfsClient 
```
5. Exit the python virtual environemnt:
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
In the steps going forward use absolute paths, replacing `~/` with the output of `pwd`. If the command examples ahead, assume the output of `pwd` is `/home/admin`.
### Configure the script.
Copy the `PostBackupNFS.py` file to ~`/PostBackupNFS/PostBackupNFS.py`.
Adjust the follwoing configuration varialbe to match your environment.
```python
# NFS Configuration
NFS_SERVER = 'nfs_server_address'
NFS_SHARE = '/path/to/nfs/share'
```
### Test the script by sending a file.
1. Create a file to send named `testfile`.
```consle
echo testdata > testfile
```
2. Run script to send the `testfile`.
```console
/home/admin/PostBackupNFS/bin/python /home/admin/PostBackupNFS/PostBackupNFS.py testfile
```
3. Look for errors in `nfs_transfer.log`.
### Setup FireMon Post-Backup Action
1. Login to the FireMon Server Control Panel usng https on port 55555.
2. Navigate to OS > Backup > Post-Backup Actions.
3. Click the `+` icon under "Run a command on the local machine".
4. In the "Command to run:" field enter the following (be sure to reference the absolue path in your environment).
```console
cd /admin/firemon $$ /home/admin/PostBackupNFS/bin/python /home/admin/PostBackupNFS/PostBackupNFS.py ${BACKUP}
```
5. Click `Stage Changes` then `Apply Configuration`.
6. Test the post-backup action from CLI using the command below.
```console
fmos backup --prune
```
7. Look for errors in `nfs_transfer.log`.
