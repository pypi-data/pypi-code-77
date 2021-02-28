class Distribution:

    def __init__(self, mu, sigma=1):
        """
        Distribution class used for calculating and visualizing a probability
        distribution

        Attributes:
            mean (float):  representing the mean value of the distribution
            stdev (float):  representing the standard deviation of the
            distribution
            data_list (list of floats): data points extracted from the data
            file
        """

        self.mean = mu
        self.stdev = sigma
        self.data = []

    def read_data_file(self, file_name):
        """
        Function that reads in data from a txt file. txt file must contain
        one number (float) per line. The numbers are stored in the data
        attribute.

        :param file_name: string representing the name of the txt file
        containing the data points
        :return: None
        """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()
        self.data = data_list