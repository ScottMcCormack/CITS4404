from eLCS.DataManagement import DataManagement
from eLCS.Constants import cons


class OfflineEnvironment:
    """
    In the context of data mining and classification tasks,
    the environment is a data set with a limited number of instances with X attributes
    and some endpoint (typically a discrete phenotype or class) of interest.

    This module loads the data set, automatically detects features of the data by executing
    the DataManagement module
    """

    def __init__(self):
        """Initialize global variables"""
        self.dataRef = 0
        self.storeDataRef = 0
        self.formatData = DataManagement(cons.trainFile, cons.testFile)

        # Initialize the first dataset instance to be passed to eLCS
        self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
        self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        if cons.testFile == 'None':
            pass
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]

    def getTrainInstance(self):
        """Returns the current training instance"""
        return [self.currentTrainState, self.currentTrainPhenotype]

    def getTestInstance(self):
        """ Returns the current training instance. """
        return [self.currentTestState, self.currentTestPhenotype]

    def newInstance(self, isTraining):
        """  Shifts the environment to the next instance in the data. """
        # -------------------------------------------------------
        # Training Data
        # -------------------------------------------------------
        if isTraining:
            if self.dataRef < (self.formatData.numTrainInstances - 1):
                self.dataRef += 1
                self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
                self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
            else:  # Once learning has completed an epoch (i.e. a cycle of iterations though the entire training dataset) it starts back at the first instance in the data)
                self.resetDataRef(isTraining)

        # -------------------------------------------------------
        # Testing Data
        # -------------------------------------------------------
        else:
            if self.dataRef < (self.formatData.numTestInstances - 1):
                self.dataRef += 1
                self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
                self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]

    def resetDataRef(self, isTraining):
        """ Resets the environment back to the first instance in the current data set. """
        self.dataRef = 0
        if isTraining:
            self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
            self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]

    def startEvaluationMode(self):
        """ Turns on evaluation mode.  Saves the instance we left off in the training data. """
        self.storeDataRef = self.dataRef

    def stopEvaluationMode(self):
        """ Turns off evaluation mode.  Re-establishes place in dataset."""
        self.dataRef = self.storeDataRef
