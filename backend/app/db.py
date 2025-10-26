import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("doc-db")

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://docsearch-mongodb:27017')
DB_NAME = os.getenv('MONGO_DB', 'docsearch')

logger.info(f"MongoDB URI: {MONGO_URI}, Database: {DB_NAME}")

client: AsyncIOMotorClient = None

def get_db():
    return client[DB_NAME]

async def init_db():
    global client
    logger.info("Initializing MongoDB connection...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = get_db()
    # ensure text index on title and body
    result = await db.documents.create_index([('title', 'text'), ('body', 'text')], name='title_body_text')
    logger.info(f"Ensured text index on documents: {result}")

async def add_document(title: str, body: str) -> str:
    db = get_db()
    logger.info(f"Inserting document: title='{title}', body='{body[:30]}...'")
    res = await db.documents.insert_one({'title': title, 'body': body})
    logger.info(f"Document inserted with ID: {res.inserted_id}")
    return str(res.inserted_id)

async def get_document(doc_id: str):
    db = get_db()
    logger.info(f"Fetching document by ID: {doc_id}")
    r = await db.documents.find_one({'_id': ObjectId(doc_id)})
    if not r:
        logger.warning(f"Document ID {doc_id} not found")
        return None
    r['id'] = str(r['_id'])
    r.pop('_id', None)
    logger.info(f"Fetched document: {r}")
    return r

async def search(q: str, limit: int = 20):
    db = get_db()
    logger.info(f"Searching documents for query: '{q}', limit={limit}")
    cursor = db.documents.find(
        {'$text': {'$search': q}},
        {'score': {'$meta': 'textScore'}}
    ).sort([('score', {'$meta': 'textScore'})]).limit(limit)

    results = []
    async for doc in cursor:
        doc['id'] = str(doc['_id'])
        doc.pop('_id', None)
        results.append(doc)
    logger.info(f"Search returned {len(results)} results")
    return results