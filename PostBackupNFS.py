import sys
import logging
from logging.handlers import RotatingFileHandler
from pyNfsClient import (Portmap, Mount, NFSv3, MNT3_OK, NFS_PROGRAM, NFS_V3, NFS3_OK, DATA_SYNC)

#########################
## BEGIN CONFIGURATION ##
#########################

NFS_HOST = "192.168.1.100"
MOUNT_PATH = "/nfsshare"

# Authentication configuration
AUTH_FLAVOR = 1  # The authentication flavor numbers are managed by IANA. Here is the official table: http://www.iana.org/assignments/rpc-authentication-numbers/rpc-authentication-numbers.xml
AUTH_MACHINE_NAME = "host1"
AUTH_UID = 0
AUTH_GID = 0

# Logging Configuration
LOG_FILE = 'post_backup_nfs.log'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

#######################
## END CONFIGURATION ##
#######################








logger = logging.getLogger('PostBackupNFS')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

AUTH = {
    "flavor": AUTH_FLAVOR,
    "machine_name": AUTH_MACHINE_NAME,
    "uid": AUTH_UID,
    "gid": AUTH_GID,
    "aux_gid": list(),
}
def main(file_path):
    logger.info("Starting NFS backup process")

    portmap = None
    mount = None
    nfs3 = None

    try:
        portmap = Portmap(NFS_HOST, timeout=3600)
        portmap.connect()
        logger.info("Connected to Portmap")

        mnt_port = portmap.getport(Mount.program, Mount.program_version)
        mount = Mount(host=NFS_HOST, port=mnt_port, timeout=3600)
        mount.connect()
        logger.info("Connected to Mount")

        mnt_res = mount.mnt(MOUNT_PATH, AUTH)
        if mnt_res["status"] == MNT3_OK:
            logger.info("Mount successful")
            root_fh = mnt_res["mountinfo"]["fhandle"]
            
            nfs_port = portmap.getport(NFS_PROGRAM, NFS_V3)
            nfs3 = NFSv3(NFS_HOST, nfs_port, 3600)
            nfs3.connect()
            logger.info("Connected to NFSv3")

            file_name = file_path.split('/')[-1]
            lookup_res = nfs3.lookup(root_fh, file_name, AUTH)
            if lookup_res["status"] == NFS3_OK:
                fh = lookup_res["resok"]["object"]["data"]
                with open(file_path, 'rb') as f:
                    content = f.read()
                write_res = nfs3.write(fh, offset=0, count=len(content), content=content, stable_how=DATA_SYNC, auth=AUTH)
                if write_res["status"] == NFS3_OK:
                    logger.info("File written successfully to NFS")
                else:
                    logger.error("Write failed")
            else:
                logger.error("Lookup failed")
        else:
            logger.error("Mount failed")

    except Exception as e:
        logger.exception("An error occurred during the NFS backup process")
    finally:
        if nfs3:
            nfs3.disconnect()
        if mount:
            mount.umnt(MOUNT_PATH, AUTH)
            mount.disconnect()
        if portmap:
            portmap.disconnect()
        logger.info("NFS backup process completed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python PostBackupNFS.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
