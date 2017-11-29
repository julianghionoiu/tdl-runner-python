import logging
import sys
import os

from tdl.client import Client
from tdl.processing_rules import ProcessingRules

from runner_action import RunnerActions
from credentials_config_file import read_from_config_file_with_default
from recording_system import RecordingSystem
from round_management import RoundManagement

from challenge_server_client import ChallengeServerClient, ClientErrorException, ServerErrorException, \
    OtherCommunicationException
from credentials_config_file import read_from_config_file


def configure_logging():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    client_logger = logging.getLogger('tdl.client')
    client_logger.setLevel(logging.INFO)
    client_logger.addHandler(ch)
    stomp_logger = logging.getLogger('stomp')
    stomp_logger.setLevel(logging.WARN)
    stomp_logger.addHandler(ch)


# ~~~~~~~~ Runner ~~~~~~~~~~

def start_client(args, username, hostname, action_if_no_args, solutions):
    configure_logging()

    if not is_recording_system_ok():
        print("Please run `record_screen_and_upload` before continuing.")
        return

    enable_colour_support_for_windows()

    print("Connecting to " + hostname)

    if use_experimental_feature():
        execute_server_action_from_user_input(args, username, hostname, solutions)
    else:
        execute_runner_action_from_args(args, username, hostname, action_if_no_args, solutions)


def execute_server_action_from_user_input(args, username, hostname, solutions):
    try:
        journey_id = read_from_config_file("tdl_journey_id")
        use_colours = is_true(read_from_config_file_with_default("tdl_use_coloured_output", "true"))
        challenge_server_client = ChallengeServerClient(hostname, journey_id, use_colours)
        journey_progress = challenge_server_client.get_journey_progress()
        print(journey_progress)
        available_actions = challenge_server_client.get_available_actions()
        print(available_actions)

        if "No actions available." in available_actions:
            return

        user_input = get_user_input(args)
        if user_input == "deploy":
            runner_action = RunnerActions.deploy_to_production
            execute_runner_action(hostname, runner_action, solutions, username)

        action_feedback = challenge_server_client.send_action(user_input)
        print(action_feedback)

        response_string = challenge_server_client.get_round_description()
        RoundManagement.save_description(
            response_string,
            lambda x: RecordingSystem.notify_event(x, RunnerActions.get_new_round_description.short_name)
        )
    except ClientErrorException as e:
        print "The client sent something the server didn't expect."
        print e.get_response_message()
    except ServerErrorException as e:
        print "Server experienced an error. Try again."
        print e.get_response_message()
    except OtherCommunicationException as e:
        print "Client threw an unexpected error."
        print e.get_response_message()


def get_user_input(args):
    return args[0] if len(args) > 0 else raw_input()


def execute_runner_action_from_args(args, username, hostname, action_if_no_args, solutions):
    value_from_args = extract_action_from(args)
    runner_action = value_from_args if value_from_args is not None else action_if_no_args
    execute_runner_action(hostname, runner_action, solutions, username)


def execute_runner_action(hostname, runner_action, solutions, username):
    print("Chosen action is: {}".format(runner_action.name))
    client = Client(hostname, unique_id=username)
    rules = ProcessingRules()
    rules.on("display_description").call(RoundManagement.display_and_save_description).then("publish")
    for key, value in solutions.iteritems():
        rules.on(key).call(value).then(runner_action.client_action)
    client.go_live_with(rules)
    RecordingSystem.notify_event(RoundManagement.get_last_fetched_round(), runner_action.short_name)


def use_experimental_feature():
    return is_true(read_from_config_file_with_default("tdl_enable_experimental", "false"))


def extract_action_from(args):
    if len(args) > 0:
        first_arg = args[0]
    else:
        first_arg = ""

    return get_first([action for action in RunnerActions.all if action.name.lower() == first_arg.lower()])


def is_recording_system_ok():
    require_recording = is_true(read_from_config_file_with_default("tdl_require_rec", "true"))

    if require_recording:
        return RecordingSystem.is_running()
    else:
        return True


def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def is_true(s):
    return s in ['true', '1']


def enable_colour_support_for_windows():
    os.system('')
