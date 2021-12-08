import sqlite3
import config
import filters
import generic

TABLE_NAME      = "content"
COL_CONTENTID   = "ContentID"
COL_GROUPID     = "GroupID"
COL_CONTENTTYPE = "ContentType"
COL_CONTENTHELD = "ContentHeld"
COL_PAGEID      = "PageID"

def drop_content_table(db=config.DB_NAME):
    generic.drop_table(TABLE_NAME,db)

def create_content_table(db=config.DB_NAME):
    print("create_collector_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME} (
        {COL_CONTENTID} integer primary key,
        {COL_GROUPID}  integer not null,
        {COL_CONTENTTYPE} text not null,
        {COL_CONTENTHELD} text not null,
        {COL_PAGEID} integer not null
    )
    """
    print("sql=" + sql)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_content(values,db=config.DB_NAME):
    print(f"insert_content(values={values},db={db})")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_CONTENTID},{COL_GROUPID}, {COL_CONTENTTYPE},{COL_CONTENTHELD},{COL_PAGEID} )
      values (:{COL_CONTENTID}, :{COL_GROUPID}, :{COL_CONTENTTYPE}, :{COL_CONTENTHELD}, :{COL_PAGEID})
      """
    params = {
        COL_CONTENTID: filters.dbInteger(values[COL_CONTENTID]), 
        COL_GROUPID: filters.dbInteger(values[COL_GROUPID]), 
        COL_CONTENTTYPE: filters.dbString(values[COL_CONTENTTYPE]),
        COL_CONTENTHELD: filters.dbString(values[COL_CONTENTHELD]),
        COL_PAGEID: filters.dbInteger(values[COL_PAGEID])
        }
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def fetch_row_length(db=config.DB_NAME):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    SELECT COUNT({COL_CONTENTID}) FROM {TABLE_NAME}
      """
    cursor.execute(sql)
    response=cursor.fetchone()
    connection.commit()
    connection.close()
    if response != None:
        return response[0]
    else:
        return None
def select_content_by_id(id,db=config.DB_NAME):
    print("select_content_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_CONTENTTYPE}, {COL_GROUPID}, {COL_CONTENTHELD}, {COL_PAGEID}  from {TABLE_NAME}
      where ({COL_CONTENTID} = :{COL_CONTENTID})
      """

    print('sql='+sql)
    params = {COL_CONTENTID: filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_CONTENTID : filters.dbInteger(id),
            COL_CONTENTTYPE: response[0],
            COL_GROUPID: response[1],
            COL_CONTENTHELD: response[2],
            COL_PAGEID: response[3]
        }
    else:
        return None
def update_content_by_id(id,values,db=config.DB_NAME):
    print("Update_content_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      Update {TABLE_NAME} SET {COL_GROUPID} = :{COL_GROUPID}, {COL_CONTENTTYPE} = :{COL_CONTENTTYPE}, {COL_CONTENTHELD} = :{COL_CONTENTHELD}, {COL_PAGEID} = :{COL_PAGEID}
      where ({COL_CONTENTID} = :{COL_CONTENTID})
      """

    print('sql='+sql)
    params = {
        COL_CONTENTID: filters.dbInteger(id), 
        COL_GROUPID: filters.dbInteger(values[COL_GROUPID]), 
        COL_CONTENTTYPE: filters.dbString(values[COL_CONTENTTYPE]),
        COL_CONTENTHELD: filters.dbString(values[COL_CONTENTHELD]),
        COL_PAGEID: filters.dbInteger(values[COL_PAGEID])
        }
    cursor.execute(sql,params)
    connection.commit()
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_CONTENTID : filters.dbInteger(id),
            COL_CONTENTTYPE: response[0],
            COL_GROUPID: response[1],
            COL_CONTENTHELD: response[2],
            COL_PAGEID: response[3]
        }
    else:
        return None


def select_content_by_pageID(id,db=config.DB_NAME):
    print("select_content_by_PageID()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_CONTENTID}, {COL_GROUPID}, {COL_CONTENTTYPE}, {COL_CONTENTHELD} from {TABLE_NAME}
      where ({COL_PAGEID} = :{COL_PAGEID})
      """

    print('sql='+sql)
    params = {COL_PAGEID: filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_CONTENTID : response[0],
            COL_GROUPID: response[1],
            COL_CONTENTTYPE: response[2],
            COL_CONTENTHELD: response[3]
        }
    else:
        return None
def select_content_by_groupID(id,db=config.DB_NAME):
    print("select_content_by_groupID()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_CONTENTID}, {COL_PAGEID}, {COL_CONTENTTYPE}, {COL_CONTENTHELD} from {TABLE_NAME}
      where ({COL_GROUPID} = :{COL_GROUPID})
      """

    print('sql='+sql)
    params = {COL_GROUPID: filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_CONTENTID : response[0],
            COL_PAGEID: response[1],
            COL_CONTENTTYPE: response[2],
            COL_CONTENTHELD: response[3]
        }
    else:
        return None

def test_content():
    db=config.DB_TEST_NAME
    drop_content_table(db)
    create_content_table(db)
    id1=insert_content({
        'ContentID': 1,
        'GroupID': 1,
        'ContentType': 'header',
        'ContentHeld': 'a lovely egg salad recipe.',
        'PageID': 1
        },db) 

    id2=insert_content({
        'ContentID': 2,
        'GroupID': 1,
        'ContentType': 'text',
        'ContentHeld': 'This is a lovely egg salad recipe.',
        'PageID': 1
        },db) 
    id3=insert_content({
        'ContentID': 3,
        'GroupID': 2,
        'ContentType': 'header',
        'ContentHeld': 'Cheesey Pizza',
        'PageID': 1
        },db) 
    id4=insert_content({
        'ContentID': 4,
        'GroupID': 2,
        'ContentType': 'text',
        'ContentHeld': 'the cheesyiest Cheesey Pizza',
        'PageID': 1
        },db) 


    row1=select_content_by_id(id1,db)
    row2=select_content_by_id(id2,db)
    row3=select_content_by_id(id3,db)
    row4=select_content_by_id(id4,db)
    rowNone=select_content_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['ContentID'] != 1:
        raise ValueError('id1 id wrong:' + str(row1['ContentID']))
    if row1['GroupID'] != 1:
        raise ValueError('id1 GroupID wrong.')
    if row2['ContentType'] != 'text':
        raise ValueError('id2 ContentType wrong.')
    if row2['ContentHeld'] != 'This is a lovely egg salad recipe.':
        raise ValueError('id2 ContentHeld wrong.')
    
    page1 = select_content_by_pageID(1,db)
    if page1['ContentID'] != 1:
        raise ValueError('wrong record for PageID')
    print(row3)
    print(row4)
