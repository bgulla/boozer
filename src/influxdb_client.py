from influxdb import InfluxDBClient
import random

logger = logging.getLogger(__name__)

class InfluxdbBoozerClient():
    """
    """
    
    username = None
    password = None
    database = "boozer"
    port = 8086
    host = None
    client = None
    measurement_field = "boozer"
    DEFAULT_METRIC_NAME = "temperature"

    def __init__(self, host, database="boozer", username=None, password=None, port=8086):
        """ 
        """
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port

        try:
            self.client = InfluxDBClient(host, port, user, password, database)
        except: 
            logger.error("Unable to create InfluxDBClient or connect to influxdb instance.")
            self.client = None
            return
        
        # Try to create the database
        client.create_database(database)
    
    def write_metric(metric_value, metric_name=self.DEFAULT_METRIC_NAME):
        """
        Writes a metric to the influxdb instance.

        Parameters
        ----------
        metric_value : float
            value of the metric
        metric_name : str
            the 'key' or column of the metric you want to write.

        Returns
        -------
        None
        """
        json_body = [
            {
                'measurement': self.measurement_field,
                'fields': {
                    metric_name: metric_value,
                },
                'tags': {
                    'host': os.getenv('HOSTNAME', "boozer_host"),
                }
            }
        ]
        logger.debug("Attempting to write influxdb metric.")
        logger.debug(json_body)
        self.client.write_points(json_body)
        logger.info("Influx update pushed. %s = %s" % (str(metric_name), str(metric_value)))

        return None
    
    def get_metrics():
        self.client.query("select * from demo")

def main():
    """
    """
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    influx_client = InfluxdbBoozerClient('texas.lol', database="boozer", username="", password="", port=8086)
    random_metric = random.random() * 100
    influx_client.write_metric(metric_name='test_metric', random_metric) # Write a random metric to influx

if __name__ == "__main__":
    main()