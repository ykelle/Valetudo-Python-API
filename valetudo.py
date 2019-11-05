import requests

# BASE
BASE_API = 'http://{ip}/api/{endpoint}'

# GET-COMMANDS
STATUS = 'current_status'
WEAR = 'consumable_status'
TOKEN = 'token'
GET_VOLUME = 'get_sound_volume'

# PUT-COMMANDS
SET_VOLUME = 'set_sound_volume'
TEST_VOLUME = 'test_sound_volume'
START = 'start_cleaning'
PAUSE = 'pause_cleaning'
STOP = 'stop_cleaning'
HOME = 'drive_home'
GOTO = 'go_to'
FIND = 'find_robot'
SPEED = 'fanspeed'
SPOT = 'spot_clean'


class ValetudoError(Exception):
    # Base error
    pass


class ValetudoConnectionError(ValetudoError):
    # Error when no connection could be established e.g. wrong ip
    def __init__(self, value):
        super(Exception, self).__init__(value)


class ValetudoRequestError(ValetudoError):
    # Error when there was an error in the request e.g. wrong value was send
    def __init__(self, status_code):
        if status_code >= 500:
            msg = 'Valetudo internal error (you may re-try)'
        else:
            msg = 'Valetudo request failed'
        super(Exception, self).__init__(msg)
        self.status_code = status_code

    def __str__(self):
        return '%s (%d)' % (self.args[0], self.status_code)


class Valetudo:

    def __init__(self, ip):
        self.ip = ip

    def get_request(self, endpoint):
        response = None
        try:
            url = BASE_API.format(ip=self.ip, endpoint=endpoint)
            response = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            raise ValetudoConnectionError(e)

        if response.status_code != 200:
            raise ValetudoRequestError(response.status_code)

        return response.json()

    def put_request(self, endpoint, msg=None):
        response = None
        try:
            url = BASE_API.format(ip=self.ip, endpoint=endpoint)
            response = requests.put(url, json=msg)
        except requests.exceptions.RequestException as e:
            raise ValetudoConnectionError(e)

        if response.status_code != 200:
            raise ValetudoRequestError(response.status_code)

        return response.json()

    def get_token(self):
        '''
        Get the token for using the normal API of the vacuum cleaner.
        Not necessary for communication over this REST API
        :return: token
        '''
        return self.get_request(TOKEN)['token']

    def get_status(self):
        '''
        Get the status of the vacuum cleaner e.g. battery charge status, clean time, ...
        :return: JSON object
        '''
        return self.get_request(STATUS)

    def get_consumable(self):
        '''
        Displays the elapsed time since the last cleaning or replacement of sensors and brushes.
        :return: JSON object
        '''
        return self.get_request(WEAR)

    def get_volume(self):
        '''
        Return the current volume setting.
        :return: volume between 0 and 100
        '''
        return self.get_request(GET_VOLUME)

    def set_volume(self, value):
        '''
        Set the volume setting.
        :param value: The volume to set. Value must be between 0 and 100
        :return: ok when successful
        '''
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        data = {"volume": str(value)}
        return self.put_request(SET_VOLUME, data)

    def find(self):
        '''
        The robot draws attention to itself with a tone at maximum volume.
        :return:
        '''
        return self.put_request(FIND)

    def test_volume(self):
        '''
        The robot plays a sound at the currently set volume.
        :return: ok when successful
        '''
        return self.put_request(TEST_VOLUME)

    def start_cleaning(self):
        '''
        The robot starts the cleaning process
        :return: ok when successful
        '''
        return self.put_request(START)

    def stop_cleaning(self):
        '''
        The robot stops the cleaning process
        :return: ok when successful
        '''
        return self.put_request(STOP)

    def pause_cleaning(self):
        '''
        The robot pauses the cleaning process
        :return: ok when successful
        '''
        return self.put_request(PAUSE)

    def send_home(self):
        '''
        Sending the vacuum back to his dock
        :return: ok when successful
        '''
        self.stop_cleaning()
        return self.put_request(HOME)

    def go_to(self, x_coord=0, y_coord=0):
        '''
        Send the roboter to a specific position
        :param x_coord:
        :param y_coord:
        :return:
        '''
        data = {"x": str(x_coord), "y": str(y_coord)}
        return self.put_request(GOTO, msg=data)

    def set_fanspeed(self, speed):
        '''
        Set the fanspeed of the vacuum.
        :param speed: speed between 0 and 100
        :return: ok when successful
        '''
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        data = {"speed": str(speed)}
        return self.put_request(SPEED, msg=data)

    def start_spot_cleaning(self):
        '''
        The robot starts a spot cleaning at his position
        :return: ok when successful
        '''
        self.put_request(SPOT)
