import tinify
import sqlite3 as db
import os


tinify.key = "YOUR_API_KEY"
dbname='/data/memos/memos_prod.db' 


def compressImage(dbName):
    dbConnect=db.connect(dbName)
    cursor = dbConnect.cursor()
    querySQL="SELECT id,filename,blob,size \
        FROM resource where type like 'image%%' and filename not like '%%CMP.%%' "
    records=cursor.execute(querySQL).fetchall()
    cursor.close()
    for r in records:
        id=r[0]
        sourceImageName=r[1]
        fileHead=os.path.splitext(sourceImageName)[0]
        fileEx=os.path.splitext(sourceImageName)[-1]
        destImageName=fileHead + '_CMP' + fileEx
        sourceImage=r[2]
        size=r[3]
        resultImage = tinify.from_buffer(sourceImage).preserve("location").to_buffer()
        new_size=len(resultImage)
        print(destImageName,size,new_size)
        try:
            cursor = dbConnect.cursor()
            updateSQL="update resource set filename=? , blob =?, size= ? where id=?"
            data_tuple=(destImageName,resultImage,new_size,id)
            cursor.execute(updateSQL,data_tuple)
            dbConnect.commit()
        except db.Error as error:
            print("Failed to insert blob data into sqlite table", error)
    dbConnect.execute('vacuum')
        

if __name__=="__main__":
    compressImage(dbname)


