CHALLENGES_FOLDER = "challenges"
LAST_FETCHED_ROUND_PATH = "{}/XR.txt".format(CHALLENGES_FOLDER)


class RoundManagement:
    def __init__(self):
        pass

    @staticmethod
    def display_and_save_description(label, description):
        print('Starting round: {}'.format(label))
        print(description)

        # Save description
        output = open("{}/{}.txt".format(CHALLENGES_FOLDER, label), "w")
        output.write(description)
        output.close()
        print "Challenge description saved to file: {}.".format(output.name)

        # Save round label
        output = open(LAST_FETCHED_ROUND_PATH, "w")
        output.write(label)
        output.close()

        return 'OK'

    @staticmethod
    def get_last_fetched_round():
        with open(LAST_FETCHED_ROUND_PATH, 'r') as round_file:
            data=round_file.read().replace('\n', '')
        return data
