import sqlite3
import logging

log = logging.getLogger(__name__)

class BeerDB():
  DB_FILEPATH = "db.sqlite"
  TABLE_NAME = "beer"
  ROW_ID = "id"
  TAP_ID = "tap_id"

  def __init__(self,db_filepath="./db.sqlite"):
    self.DB_FILEPATH = db_filepath

  def create_table(self):
    conn = sqlite3.connect(self.DB_FILEPATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE beer 
        (tap_id INT PRIMARY KEY NOT NULL,
         volume_poured REAL);''')
    conn.commit()
    conn.close()
    self.set_tap(1,0) #TODO, make this dynamic based on how many taps are loaded in config file
    self.set_tap(2,0)
    self.set_tap(3,0)
    self.set_tap(4,0)
    log.info("Table created: " + self.DB_FILEPATH)

  def get_percentage(self, tap_id):
    PINTS_PER_GALLON=8
    GALLONS=5
    TOTAL_VOLUME= PINTS_PER_GALLON * GALLONS
    volume_expelled = self.get_tap(tap_id)
    n = volume_expelled / TOTAL_VOLUME
    return 1 - n

  def get_percentage100(self, tap_id):
    return self.get_percentage(tap_id) * 100

  def set_tap_name(self, tap_id, name):
    conn = sqlite3.connect(self.DB_FILEPATH)
    c = conn.cursor()
    sql = "UPDATE beer SET volume_poured = %s WHERE tap_id=%s; " % (volume, tap_id)
    c.execute(sql)


  def set_tap(self, tap_id, volume):
    conn = sqlite3.connect(self.DB_FILEPATH)
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

  def get_tap(self, tap_id):
    conn = sqlite3.connect(self.DB_FILEPATH)
    c = conn.cursor()
    sql = "SELECT volume_poured FROM beer WHERE tap_id=%s" % tap_id
    results = c.execute(sql)
    for row in results:
      volume = row[0]
    conn.close()
    return volume

  def print_all_taps(self):
    for x in range(1,5):
      print "Tap: ", x, self.get_tap(x)

  def update_tap(self, tap_id,volume):
    old_volume = self.get_tap(tap_id)
    new_volume = old_volume + volume
    self.set_tap(tap_id, new_volume)

  def reset_tap_val(self, tap_id):
    self.set_tap(self.tap_id, 0)
    print "Reset Tap ", self.tap_id

"""if __name__ == '__main__':
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
    """
#print "Tap 1", get_tap(1)
#update_tap(1,2.5)
#print "percentage: ", get_percentage(1) 


#create_table()

