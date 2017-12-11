import sys

from runner.client_runner import start_client
from runner.credentials_config_file import read_from_config_file
from runner.runner_action import RunnerActions
from solutions.checkout import checkout
from solutions.fizz_buzz import fizz_buzz
from solutions.hello import hello
from solutions.sum import sum

"""
  ~~~~~~~~~~ Running the system: ~~~~~~~~~~~~~
 
    From IDE:
       Run this file from the IDE.
 
    From command line:
       PYTHONPATH=lib python lib/send_command_to_server.py
 
    To run your unit tests locally:
       PYTHONPATH=lib python -m unittest discover -s test
 
  ~~~~~~~~~~ The workflow ~~~~~~~~~~~~~
 
    By running this file you interact with a challenge server.
    The interaction follows a request-response pattern:
         * You are presented with your current progress and a list of actions.
         * You trigger one of the actions by typing it on the console.
         * After the action feedback is presented, the execution will stop.
 
    +------+-------------------------------------------------------------+
    | Step | The usual workflow                                          |
    +------+-------------------------------------------------------------+
    |  1.  | Run this file.                                              |
    |  2.  | Start a challenge by typing "start".                        |
    |  3.  | Read description from the "challenges" folder               |
    |  4.  | Implement the required method in                            |
    |      |   ./lib/solutions                                           |
    |  5.  | Deploy to production by typing "deploy".                    |
    |  6.  | Observe output, check for failed requests.                  |
    |  7.  | If passed, go to step 3.                                    |
    +------+-------------------------------------------------------------+
 
    You are encouraged to change this project as you please:
         * You can use your preferred libraries.
         * You can use your own test framework.
         * You can change the file structure.
         * Anything really, provided that this file stays runnable.
 
"""
start_client(sys.argv[1:],
             username=read_from_config_file("tdl_username"),
             hostname=read_from_config_file("tdl_hostname"),
             action_if_no_args=RunnerActions.test_connectivity,
             solutions={
                 "sum": sum,
                 "hello": hello,
                 "fizz_buzz": fizz_buzz,
                 "checkout": checkout,
             })
