import os

CHALLENGES_FOLDER = "challenges"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ABSOLUTE_CHALLENGES_FOLDER = os.path.normpath(os.path.join(CURRENT_PATH, "../..", CHALLENGES_FOLDER))
LAST_FETCHED_ROUND_PATH = "{}/XR.txt".format(CHALLENGES_FOLDER)


class RoundManagement:
    def __init__(self):
        pass

    @staticmethod
    def display_and_save_description(label, description):

        # Save description
        description_filename = "{}.txt".format(label)
        abs_challenge_file = os.path.join(ABSOLUTE_CHALLENGES_FOLDER, description_filename)
        with open(abs_challenge_file, "w+") as output:
            output.write(description)
            # hide username from output
            rel_challenge_file = os.path.join(CHALLENGES_FOLDER, description_filename)
            print "Challenge description saved to file: {}.".format(rel_challenge_file)

        # Save round label
        with open(os.path.join(ABSOLUTE_CHALLENGES_FOLDER, "XR.txt"), "w+") as output:
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
