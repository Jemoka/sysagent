import json
import xapian
import binascii

from sysagent import db
db = db.DB("/Users/houjun/Downloads/aaaa")
# db.index_dir("/Users/houjun/Downloads/tmp43")
db.search("majority NEAR \"hardware pipelines\"")


# db = xapian.WritableDatabase("/Users/houjun/Downloads/aaaa", xapian.DB_CREATE_OR_OPEN)
# c
# title = "Heartache on the Dancefloor"
# text = "I'd just hum around this little west-coast town."
# hash = "0xdeadbeef1"
# metadata = {}

# def index_file_raw(db, title, text, metadata={}):
#     hash = binascii.crc32((title+text).encode()) % (1<<32)
#     id = "Q" + str(hash) # for some reason for idempotency xapian requires "Q" prefix
#     doc = xapian.Document()
#     termgen = xapian.TermGenerator()
#     termgen.set_stemmer(xapian.Stem("en"))
#     termgen.set_document(doc)

#     termgen.index_text(title, 1, "S")  # S = subject/title
#     termgen.index_text(text)

#     doc.add_boolean_term(id)

#     doc.set_data(json.dumps({
#         "title": title,
#         "hash": hash,
#         "metadata": metadata or {},
#         "text": text,
#     }))

#     return db.replace_document(id, dok)

# index_file_raw(db, title, text, metadata)



# qp = xapian.QueryParser()
# qp.set_stemmer(xapian.Stem("en"))
# qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
# qp.set_database(db)  # needed for wildcard expansion

# # Register field prefixes so "title:foo" and "author:bar" work
# qp.add_prefix("title", "S")
# qp.add_prefix("author", "A")

# flags = (
#     xapian.QueryParser.FLAG_BOOLEAN |        # AND, OR, NOT
#     xapian.QueryParser.FLAG_PHRASE |          # "exact phrase"
#     xapian.QueryParser.FLAG_LOVEHATE |        # +required -excluded
#     xapian.QueryParser.FLAG_WILDCARD |        # prefix*
#     xapian.QueryParser.FLAG_PARTIAL            # partial matching
# )
# query = qp.parse_query("west-coast", flags)
# enquire = xapian.Enquire(db)
# enquire.set_query(query)

# for match in enquire.get_mset(0, 10000):
#     data = match.document.get_data()
#     print(json.loads(data))


