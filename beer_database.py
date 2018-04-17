import sqlite3

DB_FILE="db.sqlite"
TABLE_NAME="beer"
ROW_ID="id"
TAP_ID="tap_id"


def create_table():
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute('''CREATE TABLE beer 
      (tap_id INT PRIMARY KEY NOT NULL,
       volume_poured REAL);''')
  conn.commit()
  conn.close()
  set_tap(1,0)
  set_tap(2,0)
  set_tap(3,0)
  set_tap(4,0)
  print "Table created: ", DB_FILE 

def get_percentage(tap_id):
  PINTS_PER_GALLON=8
  GALLONS=5
  TOTAL_VOLUME= PINTS_PER_GALLON * GALLONS
  volume_expelled = get_tap(tap_id)
  n = volume_expelled / TOTAL_VOLUME
  return 1 - n

def get_percentage100(tap_id):
  return get_percentage(tap_id) * 100  

def set_tap_name(tap_id, name):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql = "UPDATE beer SET volume_poured = %s WHERE tap_id=%s; " % (volume, tap_id)
  c.execute(sql)


def set_tap(tap_id, volume):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql = "INSERT INTO beer (tap_id,volume_poured) VALUES (%s,%s)" %( tap_id, volume)
  #c.execute('INSERT INTO beer (tap_id,volume_poured) VALUES (0,0)')
  try:
    c.execute(sql)
  except:
    sql = "UPDATE beer SET volume_poured = %s WHERE tap_id=%s; " % (volume, tap_id)
    c.execute(sql)
  conn.commit()
  conn.close()
  print "Record: Tap %s Volume %s " % (tap_id,volume)

def get_tap(tap_id):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  sql = "SELECT volume_poured FROM beer WHERE tap_id=%s" % tap_id
  results = c.execute(sql)
  for row in results:
    volume = row[0]
  conn.close()
  return volume

def print_all_taps():
  for x in range(1,5):
    print "Tap: ", x, get_tap(x)

def update_tap(tap_id,volume):
  old_volume = get_tap(tap_id)
  new_volume = old_volume + volume
  set_tap(tap_id, new_volume)


def reset_tap_val(tap_id):
  set_tap(tap_id, 0)
  print "Reset Tap ", tap_id
if __name__ == '__main__':
  try:
#    reset_tap_val(4)
    print_all_taps()
    reset_tap_val(1)
    reset_tap_val(2)
    reset_tap_val(3)
    reset_tap_val(4)
    print "[Tap 1]\t",get_percentage100(1),"%"
    print "[Tap 2]\t",get_percentage100(2),"%"
    print "[Tap 3]\t",get_percentage100(3),"%"
    print "[Tap 4]\t",get_percentage100(4),"%"
    #create_table()
  except:
    pass
#print "Tap 1", get_tap(1)
#update_tap(1,2.5)
#print "percentage: ", get_percentage(1) 


#create_table()

