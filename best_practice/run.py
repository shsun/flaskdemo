# encoding: utf-8
import cx_Oracle
import os, sys

def main():
    os.system('echo "--------.."')
    print 'aaaaaaaaaaaa'

    file_path = 'a.html'
    with open(file_path) as f:
        contents = f.read()
    # print contents
    print '------------'
    # print contents.rstrip()

    print "****************************** start\n"

    # db = cx_Oracle.connect('saluser/saluser@192.2.71.96:1521/ageb')
    db = cx_Oracle.connect('saluser/saluser@192.2.71.96:1521/ageb')

    # select BLOCK_CONTENT_PUBLISH from G_BLOCK where id='f1cf53c4-a1a5-4680-bca5-fbd611b9fb26'
    # sql = "update G_BLOCK set BLOCK_CONTENT_PUBLISH=\'aa\' where alias like '%我的订单%'"
    sql = "update G_BLOCK set BLOCK_CONTENT_PUBLISH='www' where id='f1cf53c4-a1a5-4680-bca5-fbd611b9fb26'"

    sqlDML(sql, db)
    print "******************************done\n"

    sys.exit(0)


def sqlDML(sql, db):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "execute sql failed -sql= %s" % sql
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    sys.exit(main())
