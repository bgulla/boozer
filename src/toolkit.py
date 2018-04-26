import beer_db
import argparse
import argparse
import ConfigParser
import requests

"""

"""


# Setup the argparser
parser = argparse.ArgumentParser(description='Example with long option names')
parser.add_argument('--reset-tap', '-t', action="store", help='Reset the database value for a tap', dest="reset_tap_id")
parser.add_argument('--printval', '-p',  action='store_true', help='print all tap volumes')
parser.add_argument('--temp',  action='store_true', help='print the temperature values')

# Read in config
CONFIG_FILE = "../config/config.ini"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)


results = parser.parse_args()


# TODO add ability to pass in the location of the database to edit

DB_FILEPATH="../db/db.sqlite"

def display_config():
    print "Loaded config..."
    print "\tDatabase file:\t", DB_FILEPATH
    print "\tTemperature Endpoint:\t", config.get("Temperature", "endpoint")
    print "----------------------------------------------------"

def print_temperature():
    """

    :return:
    """
    t = get_temperature()
    print "\t Temperature: %s" % t
    return

def get_temperature():
    """

    :return:
    """
    try:
        temperature_url = config.get("Temperature", "endpoint")
        if not temperature_url:
            return "No Temperature endpoint provided"
        r = requests.get(temperature_url)
        if r.status_code == 200:
            return r.text
        else:
            return "error_http"
    except:
        return "error"

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

def print_taps():
    """

    :return:
    """
    db = beer_db.BeerDB(db_filepath=DB_FILEPATH)
    for i in range(1,5):
        print "\tTap %s | %s remaining" % (i, db.get_percentage100(i))

def reset_tap(tap_id):
    """

    :param tap_id:
    :return:
    """
    db = beer_db.BeerDB(db_filepath="../db/db.sqlite")
    print "current [Tap %s ] %s remaining" % (str(tap_id), str(db.get_percentage(tap_id)))
    msg = "Are you sure that you reset tapid: " + str(tap_id)
    if yes_or_no(msg):
        db.reset_tap_val(tap_id)
        print "updated! [Tap %s ] %s remaining" % (
        str(results.reset_tap_id), str(db.get_percentage(tap_id)))
    else:
        print "bailing"




def main():

    # Sanity check
    display_config()

    # TODO Resetting a tap volume amount
    if results.reset_tap_id:
        reset_tap(results.reset_tap_id)

    # TODO print out all the tap volume amounts
    if results.printval:
        print_taps()

    if results.temp:
        print_temperature()

    # TODO calibrate flow per pint


    # TODO update mqtt

if __name__ == "__main__":
    main()
