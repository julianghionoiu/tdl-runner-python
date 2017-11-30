import unirest

from credentials_config_file import read_from_config_file_with_default

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
        print("Notify round \"" + last_fetched_round + "\", event \"" + short_name + "\"")

        require_recording = is_true(read_from_config_file_with_default("tdl_require_rec", "true"))

        if not require_recording:
            return

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


def is_true(s):
    return s in ['true', '1']
