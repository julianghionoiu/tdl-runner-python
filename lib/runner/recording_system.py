import unirest

RECORDING_SYSTEM_ENDPOINT = "http://localhost:41375"


class RecordingSystem:
    def __init__(self):
        pass

    @staticmethod
    def is_running():
        try:
            response = unirest.get(RECORDING_SYSTEM_ENDPOINT + "/status")

            if response.code == 200 and response.body.startswith("OK"):
                return True
        except Exception as e:
            print("Could not reach recording system: " + str(e))

        return False

    @staticmethod
    def notify_event(last_fetched_round, short_name):
        try:
            response = unirest.post(RECORDING_SYSTEM_ENDPOINT + "/notify",
                                    params=last_fetched_round + "/" + short_name)

            if response.code != 200:
                print("Recording system returned code: " + response.code)
                return

            if not response.body.startswith("ACK"):
                print("Recording system returned body: " + response.body)

        except Exception as e:
            print("Could not reach recording system: " + str(e))
