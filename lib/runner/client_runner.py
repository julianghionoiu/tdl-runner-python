import logging
import sys

from tdl.client import Client
from tdl.processing_rules import ProcessingRules

from runner.runner_action import RunnerActions
from runner.credentials_config_file import read_from_config_file_with_default
from runner.recording_system import RecordingSystem
from runner.round_management import RoundManagement

from solutions.sum import sum
from solutions.hello import hello
from solutions.fizz_buzz import fizz_buzz
from solutions.checkout import checkout


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

def start_client(args, username, hostname, action_if_no_args):
    configure_logging()

    if not is_recording_system_ok():
        print("Please run `record_screen_and_upload` before continuing.")
        return

    value_from_args = extract_action_from(args)
    runner_action = value_from_args if value_from_args is not None else action_if_no_args
    print("Chosen action is: {}".format(runner_action.name))

    client = Client(hostname, unique_id=username)

    rules = ProcessingRules()
    rules.on("display_description").call(RoundManagement.display_and_save_description).then("publish")
    rules.on("sum").call(sum).then(runner_action.client_action)
    rules.on("hello").call(hello).then(runner_action.client_action)
    rules.on("fizz_buzz").call(fizz_buzz).then(runner_action.client_action)
    rules.on("checkout").call(checkout).then(runner_action.client_action)

    client.go_live_with(rules)

    RecordingSystem.notify_event(RoundManagement.get_last_fetched_round(), runner_action.short_name)


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

