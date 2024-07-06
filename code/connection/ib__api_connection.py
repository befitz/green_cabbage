import datetime
import queue
import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ib_insync import IB



class IBAPIWrapper(EWrapper):
    """
    A derived subclass of the IB API EWrapper interface
    that allows more straightforward response processing
    from the IB Gateway or an instance of TWS.
    """

    def init_error(self):
        """
        Place all of the error messages from IB into a
        Python queue, which can be accessed elsewhere.
        """
        error_queue = queue.Queue()
        self._errors = error_queue

    def is_error(self):
        """
        Check the error queue for the presence
        of errors.

        Returns
        -------
        `boolean`
            Whether the error queue is not empty
        """
        return not self._errors.empty()

    def get_error(self, timeout=5):
        """
        Attempts to retrieve an error from the error queue,
        otherwise returns None.

        Parameters
        ----------
        timeout : `float`
            Time-out after this many seconds.

        Returns
        -------
        `str` or None
            A potential error message from the error queue.
        """
        if self.is_error():
            try:
                return self._errors.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(self, id, errorCode, errorString):
        """
        Format the error message with appropriate codes and
        place the error string onto the error queue.
        """
        error_message = (
            "IB Error ID (%d), Error Code (%d) with "
            "response '%s'" % (id, errorCode, errorString)
        )
        self._errors.put(error_message)

    def init_time(self):
        """
        Instantiates a new queue to store the server
        time, assigning it to a 'private' instance
        variable and also returning it.

        Returns
        -------
        `Queue`
            The time queue instance.
        """
        time_queue = queue.Queue()
        self._time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):
        """
        Takes the time received by the server and
        appends it to the class instance time queue.

        Parameters
        ----------
        server_time : `str`
            The server time message.
        """
        self._time_queue.put(server_time)
        

        
        
        
# ib_api_connection.py

class IBAPIClient(EClient):
    """
    Used to send messages to the IB servers via the API. In this
    simple derived subclass of EClient we provide a method called
    obtain_server_time to carry out a 'sanity check' for connection
    testing.

    Parameters
    ----------
    wrapper : `EWrapper` derived subclass
        Used to handle the responses sent from IB servers
    """

    MAX_WAIT_TIME_SECONDS = 10

    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def obtain_server_time(self):
        """
        Requests the current server time from IB then
        returns it if available.

        Returns
        -------
        `int`
            The server unix timestamp.
        """
        # Instantiate a queue to store the server time
        time_queue = self.wrapper.init_time()

        # Ask IB for the server time using the EClient method
        self.reqCurrentTime()

        # Try to obtain the latest server time if it exists
        # in the queue, otherwise issue a warning
        try:
            server_time = time_queue.get(
                timeout=IBAPIClient.MAX_WAIT_TIME_SECONDS
            )
        except queue.Empty:
            print(
                "Time queue was empty or exceeded maximum timeout of "
                "%d seconds" % IBAPIClient.MAX_WAIT_TIME_SECONDS
            )
            server_time = None

        # Output all additional errors, if they exist
        while self.wrapper.is_error():
            print(self.get_error())

        return server_time
    
    
    
    
    
    

    
# ib_api_connection.py

class IBAPIApp(IBAPIWrapper, IBAPIClient):
    """
    The IB API application class creates the instances
    of IBAPIWrapper and IBAPIClient, through a multiple
    inheritance mechanism.

    When the class is initialised it connects to the IB
    server. At this stage multiple threads of execution
    are generated for the client and wrapper.

    Parameters
    ----------
    ipaddress : `str`
        The IP address of the TWS client/IB Gateway
    portid : `int`
        The port to connect to TWS/IB Gateway with
    clientid : `int`
        An (arbitrary) client ID, that must be a positive integer
    """

    def __init__(self, ipaddress, portid, clientid):
        IBAPIWrapper.__init__(self)
        IBAPIClient.__init__(self, wrapper=self)

        # Connects to the IB server with the
        # appropriate connection parameters
        self.connect(ipaddress, portid, clientid)

        # Initialise the threads for various components
        thread = threading.Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

        # Listen for the IB responses
        self.init_error()



        self.data = []

    def historicalData(self, reqId, bar):
        self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

        
        



def ibapi__connect(
    dict__proc,
    dict__conn,
    dict__log,
):
    
    dict__proc['I__flag'] = False

    # Application parameters
    host = dict__conn['cfg']['host']
    port = dict__conn['cfg']['port']
    client_id = dict__conn['cfg']['client_id']

    print("Launching IB API application...")

    try:
        # Instantiate the IB API application
        # dict__conn['app'] = IBAPIApp(host, port, client_id)
        dict__conn['app'] = IB()

        dict__conn['app'].connect(
            host=host,
            port=port,
            clientId=client_id
            )

        if dict__conn['app'].isConnected() == True:
            print("Successfully launched IB API application...")

            dict__conn['status'] = 'connected'
        else:
            dict__conn['status'] = 'disconnected'

        time.sleep(3)

    except Exception as e:
        dict__proc['I__flag'] = True
        print(str(e))
        print("Unable to initiate the IB API application")
        dict__conn['status'] = 'disconnected'


    # Obtain the server time via the IB API app
    # server_time = app.obtain_server_time()
    # server_time_readable = datetime.datetime.utcfromtimestamp(
    #     server_time
    # ).strftime('%Y-%m-%d %H:%M:%S')

    # print("Current IB server time: %s" % server_time_readable)


    return dict__proc, dict__conn, dict__log
 


def ibapi__disconnect(
    dict__proc,
    dict__conn,
    dict__log
):

    if 'app' in dict__conn.keys():
        if dict__conn['status'] == 'connected':
            try:
                dict__conn['app'].disconnect()
                print("Disconnected from the IB API application. Finished.")
                dict__conn['status'] = 'disconnected'
            except Exception as e:
                print(str(e))
                print("Unable to disconnect from application")

    return dict__proc, dict__conn, dict__log