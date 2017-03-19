import json
import sqlite3
import sys

class Databaser:
    def __init__(self):
        self.conn = sqlite3.connect('gallerydata.sqlite')
        self.c = self.conn.cursor()

    def createDatabase(self):

        self.c.execute("DROP TABLE gallery")
        self.c.execute("DROP TABLE tag")
        self.c.execute("DROP TABLE gallery_tags")

        """This is really just here for posterity in case the DB needs to be rebuilt."""
        self.c.execute("CREATE TABLE gallery ("
					"gid INTEGER PRIMARY KEY,"
					"token TEXT,"
					"title TEXT,"
					"category TEXT,"
					"uploader TEXT,"
					"posted TEXT,"
					"filecount TEXT,"
					"rating DECIMAL(3,2)"
					")")
        self.c.execute("CREATE TABLE tag ("
                    "tag_id INTEGER PRIMARY KEY AUTOINCREMENT,"
					"tag_name TEXT"
					")")
        self.c.execute("CREATE TABLE gallery_tags("
					"gallery_id INTEGER REFERENCES gallery(gid),"
					"gallery_tag_id INTEGER REFERENCES tag(tag_id)"
					")")

    def getJsonFromFile(self, jsonFileName):
        with open(jsonFileName) as fo:
            json_obj = json.load(fo)
        return json_obj

    def jsonToDatabase(self, jsonData):
        try:
            for entry in jsonData:
                gid = entry.get('gid', 'NULL')
                token = entry.get('token', 'NULL')
                title = entry.get('title', 'NULL')
                category = entry.get('category', 'NULL')
                uploader = entry.get('uploader', 'NULL')
                posted = entry.get('posted', 'NULL')
                filecount = entry.get('filecount', 'NULL')
                rating = entry.get('rating', 'NULL')
                tags = entry.get('tags', 'NULL')

                found_gallery_id = self.c.execute("SELECT gid FROM gallery WHERE gid = ?", [gid]).fetchone()
                if found_gallery_id:
                    continue

                gallery_tuple = (gid, token, title, category, uploader, posted, filecount, rating)
                self.c.execute("INSERT INTO gallery VALUES (?,?,?,?,?,?,?,?)", gallery_tuple)
                print 'created gallery ' + title

                for tag in tags:
                    found_tag_id = self.c.execute("SELECT tag_id FROM tag WHERE tag_name = ?", [tag]).fetchone()
                    if not found_tag_id:
                        self.c.execute("INSERT INTO tag (tag_name) VALUES (?)", [tag])
                        print 'created tag ' + tag
                        found_tag_id = self.c.execute("SELECT tag_id FROM tag WHERE tag_name = ?", [tag]).fetchone()
                    self.c.execute("INSERT INTO gallery_tags VALUES (?,?)", (gid, found_tag_id[0]))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        # only commits the changes if all went through correctly
        self.conn.commit()

    def addJsonInput(self, content):
        json_obj = json.loads(content)
        for response in json_obj:
            self.jsonToDatabase(json_obj.get(response))

    def addJsonInputFromFile(self, jsonLocation):
        content = self.getJsonFromFile(jsonLocation)
        for response in content:
            self.jsonToDatabase(content.get(response))
