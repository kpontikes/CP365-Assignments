import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42) # Get the same random numbers every time

class LinearRegression:
# Ugly code for thinking about linear regression with gradient descent

################################################################
### Load the dataset
  def __init__(self):
    self.weight = np.random.rand(1)
    self.bias = np.random.rand(1)

  def loadData(self, file_name):
    my_data = np.genfromtxt(file_name, delimiter=';', skip_header=1)[:10]
    self.date = my_data[:, 0]
    self.djia_close = my_data[:, 1]
    self.rec_high_temp = my_data[:,2]
    self.hist_avg = my_data[:,3]

    #print self.rec_high_temp

   # print self.djia_close

  def regressData(self):
    self.loadData("djia_temp.csv")
    self.chooseVariables()
    self.setLearningRate(.01)
    self.gradientDescent()


  def setLearningRate(self, learning_rate):
    self.learning_rate = learning_rate


################################################################
### How do we change the weight and the bias to make the line's fit better?
  def chooseVariables(self):
    #self.temp_abnormality = []

    #for day in range(len(self.rec_high_temp)):
      #temp_delta = self.rec_high_temp[day] - self.hist_avg[day]
      #self.temp_abnormality.append(temp_delta)

    self.x_variable = self.rec_high_temp
    self.y_variable = self.djia_close



  def calculateError(self):
    error = (self.x_variable*self.weight+self.bias) - self.y_variable
    return error

  def calculateCost(self):
  #  cost = np.sum(np.power((self.x_variable*self.weight+self.bias) - self.y_variable, 2))
    cost = np.sum(np.power(self.calculateError()*2))
    return cost

  def calculateRegression(self):
    init_cost = self.calculateCost()
    error = self.calculateError()
    self.weight = self.weight - np.sum(self.learning_rate * error *  self.x_variable / len(self.x_variable))
    self.bias = self.bias - np.sum(self.learning_rate * error * 1.0 / len(self.x_variable))
    end_cost = self.calculateCost()
    print init_cost
    print end_cost
    return end_cost


  def gradientDescent(self):
   # init_cost = self.calculateCost()
    #init_error = self.calculateError()
    val = self.calculateRegression()
    old_val = 0
    while np.absolute(val-old_val) > 1:
      old_val = val
      val = self.calculateRegression()
   # error = self.calculateError()
  #  print init_error
 #   print error


  #  for i in range(0, epochs):
  #    hypothesis = np.dot(x, theta)
   #   loss = hypothesis - y
  #  end_cost = self.calculateCost()
    ##if((init_cost - end_cost) > 0.001):
    #  self.gradientDescent()
   # else:
  #  print end_cost

   # self.weight = self.weight - alpha * error


    #error = ( self.x_variable*self.weight+self.bias) - self.y_variable

    #self.weight = self.weight - np.sum(learning_rate * error *  self.x_variable / len( self.x_variable))
    #self.bias = self.bias - np.sum(learning_rate * error * 1.0 / len( self.x_variable))

    #end_end_cost = np.sum(np.power((self.x_variable*self.weight+b) - self.y_variable, 2))




################################################################
### Graph the dataset along with the line defined by the model
  def graphFunction(self):
    xs = np.arange(0, 5)
    ys = xs * self.weight + self.bias

    plt.plot(self.x_variable, self.y_variable, 'r+', xs, ys, 'g-')
    plt.xlabel('Temperature (degrees C)')
    plt.ylabel('DJIA Close')
    plt.show()

LR = LinearRegression()
LR.regressData()
LR.graphFunction()
