import sys

from runner.client_runner import start_client
from runner.runner_action import RunnerActions
from runner.credentials_config_file import read_from_config_file

"""
  ~~~~~~~~~~ Running the system: ~~~~~~~~~~~~~
 
    From command line:
       PYTHONPATH=lib python lib/befaster_app.py $ACTION
 
    From IDE:
       Set the value of the `action_if_no_args`
       Run this file from the IDE.
 
    Available actions:
         * get_new_round_description - Get the round description (call once per round).
         * test_connectivity         - Test you can connect to the server (call any number of time)
         * deploy_to_production      - Release your code. Real requests will be used to test your solution.
                                       If your solution is wrong you get a penalty of 10 minutes.
                                       After you fix the problem, you should deploy a new version into production.
 
    To run your unit tests locally:
       PYTHONPATH=lib python -m unittest discover -s test
 
  ~~~~~~~~~~ The workflow ~~~~~~~~~~~~~
 
    +------+-----------------------------------------+-----------------------------------------------+
    | Step |          IDE                            |         Web console                           |
    +------+-----------------------------------------+-----------------------------------------------+
    |  1.  |                                         | Start a challenge, should display "Started"   |
    |  2.  | Run "get_new_round_description"         |                                               |
    |  3.  | Read description from ./challenges      |                                               |
    |  4.  | Implement the required method in        |                                               |
    |      |   ./lib/solutions                       |                                               |
    |  5.  | Run "test_connectivity", observe output |                                               |
    |  6.  | If ready, run "deploy_to_production"    |                                               |
    |  7.  |                                         | Type "done"                                   |
    |  8.  |                                         | Check failed requests                         |
    |  9.  |                                         | Go to step 2.                                 |
    +------+-----------------------------------------+-----------------------------------------------+
 
"""
start_client(sys.argv[1:],
             username=read_from_config_file("tdl_username"),
             hostname="run.befaster.io",
             action_if_no_args=RunnerActions.test_connectivity)
