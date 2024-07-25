import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pyNfsClient import NFSv3

# NFS Configuration
NFS_SERVER = 'nfs_server_address'
NFS_SHARE = '/path/to/nfs/share'

# Log Configuration
LOG_FILE = 'nfs_transfer.log'
LOG_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3  # Keep up to 3 backup log files

# Setup logging with rotation
handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.info('Starting file transfer to NFS share.')

def send_file_to_nfs(local_file_path):
    try:
        # Connect to the NFS server
        nfs = NFSv3(NFS_SERVER, port=2049, mount_path=NFS_SHARE)
        logger.info(f'Connected to {NFS_SERVER}.')

        # Open local file
        with open(local_file_path, 'rb') as local_file:
            file_data = local_file.read()
            remote_file_path = os.path.join(NFS_SHARE, os.path.basename(local_file_path))

            # Write data to NFS share
            nfs.write(remote_file_path, file_data, overwrite=True)
            logger.info(f'File {local_file_path} transferred to {remote_file_path} on {NFS_SERVER}.')

    except Exception as e:
        logger.error(f'Failed to transfer file: {e}')
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: uploadNFS.py <backup_file_path>")
        sys.exit(1)

    backup_file_path = sys.argv[1]
    if not os.path.isfile(backup_file_path):
        print(f"Error: File {backup_file_path} does not exist.")
        sys.exit(1)

    send_file_to_nfs(backup_file_path)
    logger.info('File transfer completed.')
