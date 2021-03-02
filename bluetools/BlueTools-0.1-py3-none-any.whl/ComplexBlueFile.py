import os
import struct
import sys
import cmath
import statistics

class ComplexBlueFile:

    def __init__(self, rotation ="f", file = "",  elevation= 0, res = 1, mode='d'):

        """ A set of methods for working with Blue Files

        :param rotation: The rotation of the aperture
        :param fileLength: The length of the file
        :param elevation: The elevation of the aperture
        :param res: Resolution of the processing
        :param mode: Detached or not Detached
        """
        self.rotation = rotation
        self.fileLength = fileLength
        self.elevation = elevation
        self.res = res
        self.mode = mode
        #Signal Statistics
        self.mean = [0] * (360 * res)
        self.median = [0] * (360 * res)
        self.sd = [0] * (360 * res)
        self.variance = [0] * (360 * res)

        #Verify that the file exists
        if (os.path.exists(file)):
            self.file = file
            if (mode == "d"):
                self.fileLength = int(os.stat(file).st_size / 2)
            elif (mode == "f"):
                self.fileLength = int((os.stat(file).st_size - 513) / 2)  # if not detached
            self.partitionWidth = int(fileLength / (360 * res))
        else:
            self.file = None
            self.fileLength = 0
            self.partitionWidth = 0
            print("Error File Not Found")

    def process_complex_blue_file(self, write_csv = True):
        """
        Processes the Midas Blue File and optionally writes a CSV summary at each azimuth
        :return: None
        """
        headers = "azimuth,elevation,meanAmp,medianAmp,sdAmp,VarAmp"
        with open(self.file, "rb") as binaryFile:
            if (self.mode == "n"):
                binaryFile.read(512)
            dataStep = 0  # Current part of the azimuth data is working on
            processingStep = 0  # A sample counter used to keep track of when it is time to process the data
            cpData = []
            x = 0
            while x < self.fileLength:
                # Convolution for filtering here

                # Process Complex Numbers
                cpNum = complex(struct.unpack("b", binaryFile.read(1))[0],
                                struct.unpack("b", binaryFile.read(1))[0])
                cpMod = cmath.polar(cpNum)[0]
                cpData.append(cpMod)
                processingStep = processingStep + 1

                # Crunch numbers in bucket
                if (processingStep == partitionWidth):
                    # print("Averaging....")
                    processingStep = 0
                    self.mean[dataStep] = statistics.mean(cpData)
                    self.median[dataStep] = statistics.median(cpData)
                    self.sd[dataStep] = statistics.pstdev(cpData, mean[dataStep])
                    self.variance[dataStep] = statistics.pvariance(cpData, mean[dataStep])
                    cpData = []
                    dataStep = dataStep + 1
                x = x + 1
            # leftovers
            self.mean[-1] = statistics.mean(cpData)
            self.median[-1] = statistics.mean(cpData)
            self.sd[-1] = statistics.mean(cpData)
            self.variance[-1] = statistics.mean(cpData)
            if(write_csv):
                outputCSV = open(self.file + ".csv", "w+")
                string = headers
                for x in range(len(self.mean)):
                    if (self.rotation == "f"):
                        string += "\n" + str(x / self.res)
                        string += "," + str(self.elevation) + "," + str(self.mean[x])
                        string += "," + str(median[x]) + "," + str(self.sd[x]) + "," + str(self.variance[x])
                    else:
                        string += "\n" + str(360 - (x / self.res))
                        string += "," + str(self.elevation) + "," + str(self.mean[x])
                        string += "," + str(self.median[x]) + "," + str(self.sd[x]) + "," + str(self.variance[x])
                outputCSV.write(string[0:-1])
                print("Output to: " + self.file + ".csv")
                print("Reduced " + str(self.fileLength) + " values to " + str(len(self.mean)))

    def get_raw_complex_values(self, write_csv = True):
        """
        Gets the magnitude of the reading from the complex file and stores in object
        :param write_csv: a boolean indicator that the values would be written to a file
        :return: None
        """
        with open(self.file, "rb") as binaryFile:
            if (self.mode == "n"):
                binaryFile.read(512)
            self.cpData = []
            x = 0
            while x < self.fileLength:
                # Convolution for filtering here

                # Process Complex Numbers
                cpNum = complex(struct.unpack("b", binaryFile.read(1))[0],
                                struct.unpack("b", binaryFile.read(1))[0])
                cpMod = cmath.polar(cpNum)[0]
                self.cpData.append(cpMod)
                # Crunch numbers in bucket
                x = x + 1
            if (write_csv):
                outputCSV = open(self.file + ".csv", "w+")
                string = "Magnitude"
                x = 0
                while x < self.fileLength:
                    string += "\n" + str(self.cpNum[x])
                    x = x + 1
                outputCSV.write(string[0:-1])
                print("Output to: " + self.file + "_raw.csv")