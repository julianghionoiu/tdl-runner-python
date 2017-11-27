import unirest


class ChallengeServerClient:

    __port = 8222

    def __init__(self, url, journey_id, use_colours):
        self.__url = url
        self.__journey_id = journey_id
        if use_colours:
            self.__accept_header = "text/coloured"
        else:
            self.__accept_header = "text/not-coloured"

    def get_journey_progress(self):
        return self.__get("journeyProgress")

    def get_available_actions(self):
        return self.__get("availableActions")

    def get_round_description(self):
        return self.__get("roundDescription")

    def send_action(self, action):
        encoded_path = unicode(self.__journey_id, "UTF-8")
        url = "http://{}:{}/action/{}/{}".format(self.__url, self.__port, action, encoded_path)
        response = unirest.post(url, headers={"Accept": self.__accept_header, "Accept-Charset": "UTF-8"})
        self.__ensure_status_ok(response)
        return response.body

    def __get(self, name):
        journey_id_utf8 = unicode(self.__journey_id, "UTF-8")

        url = "http://{}:{}/{}/{}".format(self.__url, self.__port, name, journey_id_utf8)

        response = unirest.get(url, headers={"Accept": self.__accept_header, "Accept-Charset": "UTF-8"})
        self.__ensure_status_ok(response)
        return response.body

    def __ensure_status_ok(self, response):
        if self.__is_client_error(response.code):
            raise ClientErrorException(response.body)
        elif self.__is_server_error(response.code):
            raise ServerErrorException(response.body)
        elif self.__is_other_error_response(response.code):
            raise OtherCommunicationException(response.body)

    @staticmethod
    def __is_client_error(response_status):
        return 400 <= response_status < 500

    @staticmethod
    def __is_server_error(response_status):
        return 500 <= response_status < 600

    @staticmethod
    def __is_other_error_response(response_status):
        return response_status < 200 or response_status > 300


class ClientErrorException(Exception):

    def __init__(self, message):
        self.__responseMessage = message

    def get_response_message(self):
        return self.__responseMessage


class ServerErrorException(Exception):
    def __init__(self, message):
        self.__responseMessage = message

    def get_response_message(self):
        return self.__responseMessage


class OtherCommunicationException(Exception):
    def __init__(self, message):
        self.__responseMessage = message

    def get_response_message(self):
        return self.__responseMessage

