import os
import yaml


class Constants(object):
    """Stores and manages all algorithm run parameters

    Parameters are accessible anywhere in the rest of the algorithm code by importing `cons`
    """

    def setConstants(self, config_file, dataset_path):
        """Parse the configuration file and save them as global constants

        :param str config_file: Path to the configuration yaml file
        :param str dataset_path: Directory to the datasets
        """

        # Static Run Parameters
        par = self.loadParameters(config_file)  # Load in the parameters from the yaml file
        self.datasetPath = dataset_path
        self.outputFolder = 'output'
        self.outputSource = 'eLCS_out'
        self.outputPath = os.path.join(self.outputFolder, self.outputSource)

        # Major Run Parameters -----------------------------------------------------------------------------------------
        self.trainFile = os.path.join(self.datasetPath, par['trainFile'])  # Saved as text
        self.testFile = par['testFile']  # Saved as text
        self.originalOutFileName = os.path.join(self.outputPath, str(par['outFileName']))  # Saved as text
        self.outFileName = os.path.join(self.outputPath, str(par['outFileName']) + '_eLCS')  # Saved as text
        self.learningIterations = par['learningIterations']  # Saved as text
        self.N = int(par['N'])  # Saved as integer
        self.p_spec = float(par['p_spec'])  # Saved as float

        # Logistical Run Parameters ------------------------------------------------------------------------------------
        if par['randomSeed'] == 'False' or par['randomSeed'] == 'false':
            self.useSeed = False  # Saved as Boolean
        else:
            self.useSeed = True  # Saved as Boolean
            self.randomSeed = int(par['randomSeed'])  # Saved as integer

        self.labelInstanceID = par['labelInstanceID']  # Saved as text
        self.labelPhenotype = par['labelPhenotype']  # Saved as text
        self.labelMissingData = par['labelMissingData']  # Saved as text
        self.discreteAttributeLimit = int(par['discreteAttributeLimit'])  # Saved as integer
        self.trackingFrequency = int(par['trackingFrequency'])  # Saved as integer

        # Supervised Learning Parameters -------------------------------------------------------------------------------
        self.nu = int(par['nu'])  # Saved as integer
        self.chi = float(par['chi'])  # Saved as float
        self.upsilon = float(par['upsilon'])  # Saved as float
        self.theta_GA = int(par['theta_GA'])  # Saved as integer
        self.theta_del = int(par['theta_del'])  # Saved as integer
        self.theta_sub = int(par['theta_sub'])  # Saved as integer
        self.acc_sub = float(par['acc_sub'])  # Saved as float
        self.beta = float(par['beta'])  # Saved as float
        self.delta = float(par['delta'])  # Saved as float
        self.init_fit = float(par['init_fit'])  # Saved as float
        self.fitnessReduction = float(par['fitnessReduction'])  # Saved as float

        # Algorithm Heuristic Options -------------------------------------------------------------------------------
        self.doSubsumption = bool(int(par['doSubsumption']))  # Saved as Boolean
        self.selectionMethod = par['selectionMethod']  # Saved as text
        self.theta_sel = float(par['theta_sel'])  # Saved as float

        # PopulationReboot -------------------------------------------------------------------------------
        self.doPopulationReboot = bool(int(par['doPopulationReboot']))  # Saved as Boolean
        self.popRebootPath = os.path.join(self.outputPath, par['popRebootPath'])  # Saved as text

    def loadParameters(self, config_file):
        """Load the environment parameters from yaml configuration file

        :param str config_file: Path to the configuration yaml file
        :return: Parameters read from yaml file
        :rtype: dict
        """

        parameters = {}

        with open(config_file, 'r') as stream:
            try:
                # Read parameters from yaml file
                parameters = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        stream.close()

        return parameters

    def referenceTimer(self, timer):
        """Store reference to the Timer object

        :param timer: A timer object
        """
        self.timer = timer

    def referenceEnv(self, env):
        """ Store reference to `OfflineEnvironment` object

        :param Environment env: An `OfflineEnvironment` file
        """
        self.env = env

    def parseIterations(self):
        """ Parse the 'learningIterations' string

        Identify the maximum number of learning iterations as well as evaluation checkpoints
        """

        self.learningCheckpoints = self.learningIterations
        self.maxLearningIterations = self.learningCheckpoints[(len(self.learningCheckpoints) - 1)]

        if self.trackingFrequency == 0:
            self.trackingFrequency = self.env.formatData.numTrainInstances  # Adjust tracking frequency to match the training data size - learning tracking occurs once every epoch


# To access one of the above constant values from another module, import GHCS_Constants * and use "cons.something"
cons = Constants()
