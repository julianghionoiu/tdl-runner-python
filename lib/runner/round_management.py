import os

CHALLENGES_FOLDER = "challenges"
LAST_FETCHED_ROUND_PATH = "{}/XR.txt".format(CHALLENGES_FOLDER)


class RoundManagement:
    def __init__(self):
        pass

    @staticmethod
    def display_and_save_description(label, description):

        # Save description
        current_path = os.path.dirname(os.path.abspath(__file__))
        challenges_folder = os.path.normpath(os.path.join(current_path, "../..", CHALLENGES_FOLDER))
        challenge_file = os.path.join(challenges_folder, "{}.txt".format(label))
        with open(challenge_file, "w+") as output:
            output.write(description)
            print "Challenge description saved to file: {}.".format(output.name)

        # Save round label
        with open(os.path.join(challenges_folder, "XR.txt"), "w+") as output:
            output.write(label)

        return 'OK'

    @staticmethod
    def save_description(raw_description, callback):
        if "\n" not in raw_description:
            return

        newline_index = raw_description.find("\n")
        round_id = raw_description[:newline_index]
        last_fetched_round = RoundManagement.get_last_fetched_round()
        if not round_id == last_fetched_round:
            callback(round_id)

        RoundManagement.display_and_save_description(round_id, raw_description)

    @staticmethod
    def get_last_fetched_round():
        # noinspection PyUnusedLocal
        try:
            with open(LAST_FETCHED_ROUND_PATH, 'r') as round_file:
                return round_file.read().replace('\n', '')
        except Exception as e:
            return "noRound"
