import os

from eLCS.Timer import Timer
from eLCS.OfflineEnvironment import OfflineEnvironment
from eLCS.Algorithm import Algorithm
from eLCS.Constants import cons

"""To run e-LCS, run this module.  

A properly formatted configuration file, including all run parameters must be included with the path to that
file given below.  In this example, the configuration file has been included locally, so only the file name is required.
"""

if __name__ == "__main__":
    helpstr = """Failed attempt to run e-LCS.  Please ensure that a configuration file giving all run parameters has been specified."""

    # Specify the name and file path for the configuration file.
    config_txt = os.path.join('config', 'eLCS_config.yaml')

    # Obtain all run parameters from the configuration file and store them in the 'Constants' module.
    dataset_path = os.path.join('data', 'eLCS')
    cons.setConstants(config_txt, dataset_path=dataset_path)

    # Initialize the 'Timer' module which tracks the run time of algorithm and it's different components.
    timer = Timer()
    cons.referenceTimer(timer)

    # Initialize the 'Environment' module which manages the data presented to the algorithm.  While e-LCS learns iteratively (one inistance at a time
    env = OfflineEnvironment()
    cons.referenceEnv(
        env)  # Passes the environment to 'Constants' (cons) so that it can be easily accessed from anywhere within the code.
    cons.parseIterations()  # Identify the maximum number of learning iterations as well as evaluation checkpoints.

    # Run the e-LCS algorithm.
    eLCS = Algorithm()
