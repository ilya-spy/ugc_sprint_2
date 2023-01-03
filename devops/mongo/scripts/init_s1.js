sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

const dbname = "default";
const conn = new Mongo();
const database = conn.getDB(dbname);

sh.enableSharding(dbname);

rating_collection = "rating";
database.createCollection(rating_collection);
sh.shardCollection(`${dbname}.${rating_collection}`, {["user_id"]: "hashed"});
database[rating_collection].createIndex({["film_id"]: -1});
database[rating_collection].createIndex({["rating"]: -1});

bookmark_db = "bookmark";
database.createCollection(bookmark_db);
sh.shardCollection(`${dbname}.${bookmark_db}`, {["user_id"]: "hashed"});
database[bookmark_db].createIndex({["film_id"]: -1});
