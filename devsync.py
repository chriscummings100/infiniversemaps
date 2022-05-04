import subprocess
import os

#script that can only be run by devs to push an exported data folder to the public servers


subprocess.call("gsutil -m rsync -r d:/dev/domains/ftl/ftldomainunity/publicdata gs://multiverse-dev-blobs/infiniverse/public", shell=True)
