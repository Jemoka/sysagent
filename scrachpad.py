import json
import xapian
import binascii

from sysagent import db
db = db.DB("/Users/houjun/Documents/Projects/cs440lx-26spr/labs/2-remote-infra/index/")
db.index_dir("/Users/houjun/Documents/Projects/cs440lx-26spr/labs/2-remote-infra/docs/")
# db.search("majority NEAR \"hardware pipelines\"")

