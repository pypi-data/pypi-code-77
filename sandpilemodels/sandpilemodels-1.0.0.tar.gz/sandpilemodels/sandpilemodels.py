from pylab import *
import matplotlib.pyplot as plt
import os
import sys

x=15000
sys.setrecursionlimit(x)

class Sandpile:
  """
                                Parameters

  N = Size of Grid
  critLevel = Critical Level
  iterations = Number of iterations
  mode = Random, SpecificCorners, SpecificMiddle
  initMode = RandomInt, RandomFloat, Static, NearCrit, OverCrit
  animated = Set to true if you want to see animation
  save = Set to true to save the file
  """

  def __init__(self, N, critLevel, iterations = 50, mode = "SpecificMiddle", initMode = "RandomInt", animated = False, save = False):
    if initMode == 'RandomFloat':
      self.grid = random(size=(N,N)) #Initialized with random floating point value
    elif initMode == 'RandomInt':
      self.grid = randint(critLevel, size=(N,N)) #With random integer values (not at the crit level)
    elif initMode == 'Static':
      self.grid = zeros((N,N))     #All zeros
    elif initMode == 'NearCrit':
      self.grid = ones((N,N)) * 3. #Near critical point
    elif initMode == 'OverCrit':
      self.grid = ones((N,N)) * 7. #Over critical point

    self.N = N
    self.critLevel = critLevel
    self.iterations = iterations
    self.mode = mode
    self.initMode = initMode
    self.animated = animated
    self.save = save
    self.breaks = []
    self.freq = {}
    self.numbreaks = 1
    self.time = 0
    self.set_of_area = set()
    self.freq_area_affected = {}
    self.time_taken = []

  def forward(self, x, y):
    grid = self.grid
    N = self.N
    critLevel = self.critLevel
    isBoundary = False

    #print(x,y)
    #If we reached a boundary:
    if x < 0 or x >= N:
        isBoundary = True
        pass
    if y < 0 or y >= N:
        isBoundary = True
        pass
    #If we're not on a boundary,
    if isBoundary == False:
        #Increment the current element
        grid[x][y] += 1
        self.numbreaks += 1
       # print('number of breaks: ' + str(self.numbreaks))
       # imshow(grid)
       # draw()
       # print(self.grid)
        #If we're past the critical number:
        if grid[x][y] >= critLevel:
            self.set_of_area.add((x,y))

            grid[x][y] -= 4
            self.forward(x+1,y)
            self.forward(x-1,y)
            self.forward(x,y+1)
            self.forward(x,y-1)

  def add_sand(self,x,y):
    self.forward(x,y)

  def saveFile(self, fileName, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    savefig(fileName)

  def linlaw(self, x,  b) :
      return -x * b

  def log_func(self, arr):
    for i in range(len(arr)):
      if arr[i] <= 0:
        arr[i] = 0
      else:
        arr[i] = np.log(x)
    return arr

  def plot_sandpile(self):
    grid = self.grid
    N = self.N
    critLevel = self.critLevel
    iterations = self.iterations
    initMode = self.initMode
    mode = self.mode
    animated = self.animated
    save = self.save

    #Plot variables:
    fontFamily = 'serif'
    fontSize = '25'

    #For plotting total activity vs. frequency of occurence:
    activity = []
    activity = sorted(self.freq.keys())
    freq = []
    print(activity)
    for x in activity:
      freq.append(self.freq[x])

    x = log10(array(activity))
    y = log10(array(freq))

    coefficients = polyfit(x, y, 1)
    polynomial = poly1d(coefficients)
    ys = polynomial(x)

    print('Total number of Avalanches' + str(activity))
    print('Frequency' + str(freq))

    clf()
    figure(0)
    plot(x,ys, color = "red")
    #loglog(activity, freq, 'go')
    scatter(x,y)
    title('Total Activity vs. Frequency($i = %d$ iterations)' %iterations, family=fontFamily, size=fontSize)
    xlabel('Total Number of Avalanches', family=fontFamily, size=int(fontSize)/1.5)
    ylabel('Frequency', family=fontFamily, size=int(fontSize)/1.5)
    #Text box:
    fig_text = figtext(0.75,0.75, 'Iterations: ' + str(iterations) + '\n'
                   'Init Mode: ' + str(initMode) + '\n'
                   'Dribble Mode: ' + str(mode) + '\n'+
                   'fit:' + 'y = {}x + {}'.format(coefficients[1], coefficients[0]), color='white' ,
                    backgroundcolor='black', size=int(fontSize)/1.5,
                    family=fontFamily)





    if save:
      fileName = 'images/' + str(initMode) + '_' + str(mode) + '/total_activity_plot' + '.png'
      directory = 'images/' + str(initMode) + '_' + str(mode) + '/'
      self.saveFile(fileName, directory)
    show()


    #plot area vs freq
    area = []
    area = sorted(self.freq_area_affected.keys())
    freq_a = []
    for x in area:
      freq_a.append(self.freq_area_affected[x])
    print(area, freq_a)
    x = log10(array(area))
    y = log10(array(freq_a))

    coefficients = polyfit(x, y, 1)
    polynomial = poly1d(coefficients)
    ys = polynomial(x)

    clf()
    figure(1)
    scatter(x,y)
    #loglog(area, freq_a, 'go')
    plot(x,ys)
    title('Area Affected vs. Frequency($i = %d$ iterations)' %iterations, family=fontFamily, size=fontSize)
    xlabel('Total Number of cells affected', family=fontFamily, size=int(fontSize)/1.5)
    ylabel('Frequency', family=fontFamily, size=int(fontSize)/1.5)
    #Text box:
    fig_text = figtext(0.75,0.75, 'Iterations: ' + str(iterations) + '\n'
                   'Init Mode: ' + str(initMode) + '\n'
                   'Dribble Mode: ' + str(mode) + '\n' +
                   'fit: ' +  'y = {}x + {}'.format(coefficients[1], coefficients[0]),
                   color='white', backgroundcolor='black', size=int(fontSize)/1.5,
                    family=fontFamily)

    if save:
      fileName = 'images/' + str(initMode) + '_' + str(mode) + '/area_affected_plot' + '.png'
      directory = 'images/' + str(initMode) + '_' + str(mode) + '/'
      self.saveFile(fileName, directory)
    show()


    #Area affected plot

  def run(self):
    grid = self.grid
    N = self.N
    critLevel = self.critLevel
    iterations = self.iterations
    initMode = self.initMode
    mode = self.mode
    animated = self.animated
    save = self.save

    if mode == 'Random':
      freq = {}
      for i in range(iterations):
        self.numbreaks = 1 #Reset the number of breaks
        self.set_of_area = set() #Reset the set of area affected
        x = randint(N-1)
        y = randint(N-1)
        self.add_sand(x, y)

        #Record the number of breaks and area affected:
        self.breaks.append(self.numbreaks)
        if self.numbreaks in self.freq:
            self.freq[self.numbreaks] += 1
        else:
            self.freq[self.numbreaks] = 1

        size = len(self.set_of_area) + 1
        if size in self.freq_area_affected:
            self.freq_area_affected[size] += 1
        else:
            self.freq_area_affected[size] = 1

        grid = array(grid)
        if animated:
            plt.imshow(grid)
            plt.draw()
            plt.pause(0.01)

    if mode == 'SpecificCorners':
      freqPlot = {}
      for i in range(iterations):
        self.numbreaks = 1 #Reset the number of breaks
        self.set_of_area = set() #Reset the set of area affected

        x = 0
        y = 0
        self.add_sand(x,y)
        #Record the number of breaks and area affected:
        self.breaks.append(self.numbreaks)
        if self.numbreaks in self.freq:
            self.freq[self.numbreaks] += 1
        else:
            self.freq[self.numbreaks] = 1

        size = len(self.set_of_area) + 1
        if size in self.freq_area_affected:
            self.freq_area_affected[size] += 1
        else:
            self.freq_area_affected[size] = 1


        x = len(grid) -1
        y = 0
        self.add_sand(x,y)

        x = 0
        y = len(grid)-1
        self.add_sand(x,y)

        x = len(grid)-1
        y = len(grid)-1
        self.add_sand(x,y)

        if animated:
            plt.imshow(grid)
            plt.draw()
            plt.pause(0.01)


    if mode == 'SpecificMiddle':
      freqPlot = {}
      for i in range(iterations):
        self.numbreaks = 1 #Reset the number of breaks
        self.set_of_area = set() #Reset the set of area affected

        x = int(floor(len(grid)/2))
        y = int(floor(len(grid)/2))
        self.add_sand(x,y)

        #Record the number of breaks and area affected:
        self.breaks.append(self.numbreaks)
        if self.numbreaks in self.freq:
            self.freq[self.numbreaks] += 1
        else:
            self.freq[self.numbreaks] = 1

        size = len(self.set_of_area) + 1
        if size in self.freq_area_affected:
            self.freq_area_affected[size] += 1
        else:
            self.freq_area_affected[size] = 1

        if animated:
            plt.imshow(grid)
            plt.draw()
            plt.pause(0.01)
    plt.imshow(grid)
    if save:
      fileName = 'images/' + str(initMode) + '_' + str(mode) + '/' + str(initMode) + '_' + str(mode) + '_' + str(iterations) + '.png'
      directory = 'images/' + str(initMode) + '_' + str(mode) + '/'
      self.saveFile(fileName, directory)
      show()

    breaks = array(self.breaks)
    self.plot_sandpile()
