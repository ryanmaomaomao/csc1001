import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros, linspace
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize

# SIR engine
class SIR():

    # Public members to initialize
    data = None      # case data
    dt = None        # Number of hours
    D = None         # Number of days simulated
    population = None # area population
    alpha = None    # alpha coefficient
    beta = None     # beta coefficient
    S = None        # Susceptable time series
    I = None        # Infected time series
    R = None        # Recovered time series
    R0 = None       # R0 coefficient

    # constructor with parameters
    def __init__(self, dt = 1,D = 180,population = 328200000):
        self.dt = dt
        self.D =  D
        self.population = population

    # add data to the engine
    def loadData(self,data):
        self.data = data

        # get optimal alpha and beta coefficients by optimization
        self.alpha, self.beta = self.__get_MSE_para()


        self.R0 = self.__get_MSE_para()[0]/self.__get_MSE_para()[1]
        self.S, self.I, self.R = self.__getSIR(self.alpha,self.beta)

    # check if Data is loaded
    # prevent Error
    def __checkData(self):
        return self.data is None

    # Return the parameters dictionary
    def getParameters(self):
        return {'dt':self.dt, 'D': self.D,'population': self.population,'alpha':self.alpha,'beta':self.beta,'S':self.S,'I':self.I,'R':self.R,'R0':self.Ro}

    # print parameter's meanings
    def parameterExplanations(self):
        print('dt -> Number of hours')
        print('D  -> Number of days simulated')
        print('population -> The population in that area')
        print('alpha -> alpha coefficient')
        print('beta -> beta coefficient')
        print('S -> Number of predicted susceptibles')
        print('I -> Number of predicted infected')
        print('R -> Number of predicted recovered ')
        print('R0 -> Virus basic reproduction rate ')

    # SIR stepwise equation calculator
    def __getSIR(self,alpha = 0.2, beta = 0.1,start = 1):
        # sanity check
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None

        else:
            N = self.data.shape[0] + 100
            t = linspace(0, N * self.dt, N + 1)
            S = zeros(N + 1)
            I = zeros(N + 1)
            R = zeros(N + 1)

            # Initial condition
            S[0] = self.population  # initial susceptible is number of population
            I[0] = start # initial infected people
            R[0] = 0 # initial recovered

            # Step equations forward in days
            for n in range(N):
                S[n + 1] = max(S[n] - self.dt * alpha * S[n] * I[n] / self.population, 0)
                I[n + 1] = max(I[n] + self.dt * alpha * S[n] * I[n] / self.population - self.dt * beta * I[n], 0)
                R[n + 1] = max(R[n] + self.dt * beta * I[n], 0)

            return (S, I, R)

    # MSE calculator
    def __MSE(self,params):
        alpha = params[0]
        beta = params[1]
        S, I, R = self.__getSIR(alpha, beta)
        length = self.data.shape[0]
        I = I[0:length]
        R = R[0:length]
        Y_true_I = self.data['confirm'] - self.data['heal'] - self.data['dead']
        Y_predict_I = I
        Y_true_R = self.data['heal'] + self.data['dead']
        Y_predict_R = R
        return (0.1 * mean_squared_error(Y_true_I, Y_predict_I) + 0.9 * mean_squared_error(Y_true_R, Y_predict_R))

    # MSE estimator
    # return the best alpha and beta coefficient by minimizing MSE
    def __get_MSE_para(self):
        guess = np.array([0.8380207226432153,0.027889393118167467])

        # utilize minimize function to find MSE estimator
        results = minimize(self.__MSE, guess, method = 'nelder-mead', options={'disp': False})

        return(results.x)

    # R0 is the basic reproduction ratio of virus. If it's above 1, it's a pandemic.
    def predictR0(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        print(self.R0)

    # plot infected the pandemic
    def predictInfectedPlot(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        length = len(self.data)

        # Since most investigated countries' pandemic is moving to the end, by default we only
        # predict 60 days after newest data
        t = np.linspace(1, length + 60, length + 60)

        # plot predicted infected and actual infected
        plt.plot(t, self.I[0:len(t)], label="Predicted infected")
        plt.plot(np.linspace(1, length, length), self.data['confirm'] - self.data['heal'] - self.data['dead'],
                 'o',label="Actual infected")
        plt.title("Predicted infected population plot")
        plt.legend()
        plt.show()

    # plot susceptable predicted
    def predictSusceptablePlot(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        length = len(self.data)
        t = np.linspace(1, length + 60, length + 60)
        plt.plot(t, self.S[0:len(t)], label="Predicted Susceptable")
        plt.title("Predicted susceptable population plot")
        plt.legend()
        plt.show()

    # plot Recovered predicted
    def predictRecoverPlot(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        length = len(self.data)
        t = np.linspace(1, length + 60, length + 60)
        plt.plot(t, self.R[0:len(t)], label="Predicted Recovered")
        plt.title("Predicted recovered population plot")
        plt.legend()
        plt.show()

    # plot cumulative case predicted
    def predictCumPlot(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        length = len(self.data)
        t = np.linspace(1, length + 60, length + 60)
        plt.plot(t, self.I[0:len(t)] + self.R[0:len(t)], label="Predicted Cumulative Cases")
        plt.plot(np.linspace(1, length, length), self.data['confirm'],
                 'o', label="Actual infected")
        plt.title("Predicted cumulative case plot")
        plt.legend()
        plt.show()

    # predict maximum cases
    def predictMaximum(self):
        if self.__checkData():
            print("You have NOT uploaded data!")
            return None
        print("By SIR prediction, maximum cases are ",end = "")
        alist = self.I[-1] + self.R[-1]
        print(int(alist)+1)
        print("Current cases are ",end = "")
        print(max(self.data['confirm']))
