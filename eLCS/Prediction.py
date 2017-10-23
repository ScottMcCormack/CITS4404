from eLCS.Constants import cons
import random


class Prediction(object):
    """Given a match set, this module uses a voting scheme to select the phenotype prediction.

    Set up to handle both discrete and continuous phenotypes.
    Also set up to try and handle prediction ties if possible.
    """

    def __init__(self, population):
        """Constructs the voting array and determines the prediction decision.

        :param population:
        """
        self.decision = None
        # -------------------------------------------------------
        # DISCRETE PHENOTYPES (CLASSES)
        # -------------------------------------------------------
        if cons.env.formatData.discretePhenotype:
            self.vote = {}
            self.tieBreak_Numerosity = {}
            self.tieBreak_TimeStamp = {}

            for eachClass in cons.env.formatData.phenotypeList:
                self.vote[eachClass] = 0.0
                self.tieBreak_Numerosity[eachClass] = 0.0
                self.tieBreak_TimeStamp[eachClass] = 0.0

            for ref in population.matchSet:
                cl = population.popSet[ref]
                self.vote[cl.phenotype] += cl.fitness * cl.numerosity
                self.tieBreak_Numerosity[cl.phenotype] += cl.numerosity
                self.tieBreak_TimeStamp[cl.phenotype] += cl.initTimeStamp

            highVal = 0.0
            bestClass = []  # Prediction is set up to handle best class ties for problems with more than 2 classes
            for thisClass in cons.env.formatData.phenotypeList:
                if self.vote[thisClass] >= highVal:
                    highVal = self.vote[thisClass]

            for thisClass in cons.env.formatData.phenotypeList:
                if self.vote[thisClass] == highVal:  # Tie for best class
                    bestClass.append(thisClass)
            # ---------------------------
            if highVal == 0.0:
                self.decision = None
            # -----------------------------------------------------------------------
            elif len(bestClass) > 1:  # Randomly choose between the best tied classes
                bestNum = 0
                newBestClass = []
                for thisClass in bestClass:
                    if self.tieBreak_Numerosity[thisClass] >= bestNum:
                        bestNum = self.tieBreak_Numerosity[thisClass]

                for thisClass in bestClass:
                    if self.tieBreak_Numerosity[thisClass] == bestNum:
                        newBestClass.append(thisClass)
                # -----------------------------------------------------------------------
                if len(newBestClass) > 1:  # still a tie
                    bestStamp = 0
                    newestBestClass = []
                    for thisClass in newBestClass:
                        if self.tieBreak_TimeStamp[thisClass] >= bestStamp:
                            bestStamp = self.tieBreak_TimeStamp[thisClass]

                    for thisClass in newBestClass:
                        if self.tieBreak_TimeStamp[thisClass] == bestStamp:
                            newestBestClass.append(thisClass)
                    # -----------------------------------------------------------------------
                    if len(
                            newestBestClass) > 1:  # Prediction is completely tied - eLCS has no useful information for making a prediction
                        self.decision = 'Tie'
                else:
                    self.decision = newBestClass[0]
            # ----------------------------------------------------------------------
            else:  # One best class determined by fitness vote
                self.decision = bestClass[0]

        # -------------------------------------------------------
        # CONTINUOUS PHENOTYPES
        # -------------------------------------------------------
        else:
            if len(population.matchSet) < 1:
                print("empty matchSet")
                self.decision = None
            else:
                # IDEA - outputs a single continuous prediction value(closeness to this prediction accuracy will dictate accuracy). In determining this value we examine all ranges
                phenotypeRange = cons.env.formatData.phenotypeList[1] - cons.env.formatData.phenotypeList[
                    0]  # Difference between max and min phenotype values observed in data.
                predictionValue = 0
                valueWeightSum = 0
                for ref in population.matchSet:
                    cl = population.popSet[ref]
                    localRange = cl.phenotype[1] - cl.phenotype[0]
                    valueWeight = (phenotypeRange / float(localRange))
                    localAverage = cl.phenotype[1] + cl.phenotype[0] / 2.0

                    valueWeightSum += valueWeight
                    predictionValue += valueWeight * localAverage
                if valueWeightSum == 0.0:
                    self.decision = None
                else:
                    self.decision = predictionValue / float(valueWeightSum)

    def getFitnessSum(self, population, low, high):
        """Get the fitness sum of rules in the rule-set. For continuous phenotype prediction.

        :param population:
        :param low:
        :param high:
        :return:
        """
        fitSum = 0
        for ref in population.matchSet:
            cl = population.popSet[ref]
            if cl.phenotype[0] <= low and cl.phenotype[1] >= high:  # if classifier range subsumes segment range.
                fitSum += cl.fitness
        return fitSum

    def getDecision(self):
        """Returns prediction decision.

        :return:
        """
        return self.decision
