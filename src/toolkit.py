import beer_db
import argparse
import argparse


"""

"""
# TODO add ability to pass in the location of the database to edit



def yes_or_no(question):
    """
    :param question: string to present to the user
    :return:
    """
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

parser = argparse.ArgumentParser(description='Example with long option names')
parser.add_argument('--reset-tap', action="store", dest="reset_tap_id")
results = parser.parse_args()


# TODO Resetting a tap volume amount
if results.reset_tap_id:
    db = beer_db.BeerDB(db_filepath="../db/db.sqlite")
    print "current [Tap %s ] %s remaining" % (str(results.reset_tap_id), str(db.get_percentage(results.reset_tap_id)))
    msg = "Are you sure that you reset tapid: "+ str(results.reset_tap_id)
    if yes_or_no( msg ):
        db.reset_tap_val(results.reset_tap_id)
        print "updated! [Tap %s ] %s remaining" % (str(results.reset_tap_id), str(db.get_percentage(results.reset_tap_id)))
    else:
        print "bailing"

# TODO print out all the tap volume amounts

# TODO calibrate flow per pint

# TODO print out temperature value

# TODO update mqtt

