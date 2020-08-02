import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import numpy as np
import warnings

from Crawl import *
from Economic import Economic
from SIR import SIR
from Databook import Databook
from HeatMap import HeatMap

# Interactive System
class System:

    '''Public members'''

    # The commands and their meaning instructions
    commands = {'case':'View cases data from world wide','SIR': 'SIR model prediction','eco':'Economic impact calculator',\
                'data':'view GDP, GDP per capita data used for calculation',\
        'main':'Go to the main searching interface','back':'Go to previous menu','h':'Get global navigation instruction',\
                'p':'View the prologue','exit':'Close the system',}

    # Databook with URLs for crawling
    databook = Databook()

    # SIR model
    SIREngine = SIR()

    # Memory to temporarily store some crawled data
    memory = dict()

    ######################Constructor######################
    def __init__(self):
        print('System loading, please wait...')

        # Retrieve URL from databook
        # crawl and save
        try:
            url_pop = self.databook.ECO_DATA['population']
            self.memory['population'] = CrawlByKejin(url_pop).parse_eco()

            url_GDP = self.databook.ECO_DATA['GDP']
            self.memory['GDP'] = CrawlByKejin(url_GDP).parse_eco()

            url_GDP_pc = self.databook.ECO_DATA['GDP_pc']
            self.memory['GDP_pc'] = CrawlByKejin(url_GDP_pc).parse_eco()

        # exit if crawling fails
        except:
            self.ConnectException()

    ###################### System Util ######################
    #  Navigation
    # receive user input and function as navigation
    # if its navigation is triggered, return the [input,True], else return [input, False]
    def go(self):
        a = input().strip()
        # navigate to different interface according to the input
        if a.lower() == 'main':
            self.search()
            return [a, True]
        elif a.lower() == 'h':
            self.help()
            return [a, True]
        elif a.lower() == 'p':
            self.prologue()
            return [a, True]
        elif a.lower() == 'exit':
            self.exit()
            return [a, True]
        else:
            return [a, False]

    # System exit
    def exit(self):
        print("Thank you for using the system!")
        sys.exit()

    # stop system for failures in connection
    def ConnectException(self):
        print()
        print("ERROR: Problem arises in Internet connection!")
        self.exit()

    # Function to format input countries
    def standardizeCountry(self, inp):
        inp = inp.lower().capitalize()
        # correct some input
        if inp == 'Uk' or inp == 'England' or inp == 'Britain':
            inp = 'UK'
        if inp == 'Us' or inp == 'America' or inp == 'United states' or inp == 'Usa':
            inp = 'US'
        if inp == 'Southafrica' or inp == 'South_africa' or inp == 'South africa':
            inp = 'South_Africa'
        if inp == 'Mexica':
            inp = 'Mexico'
        if inp == 'Korean':
            inp ='Korea'
        if inp == 'German':
            inp ='Germany'
        return inp

    # check if the country is recorded
    def checkCountry(self, inp):
        return inp in Databook.COUNTRY_TS.keys()

    # function to print split line
    def splitLine(self, title=''):
        l = len(title)
        long = 80
        dash = (long - l) // 2
        print('-' * dash + title + '-' * (long - l - dash))

    # Nations introduction
    def nations(self):
        self.splitLine('Nation List')
        print("The followings countries are available:")
        count = 0
        # Print all the nations, 5 in a row
        for i in Databook.COUNTRY_TS.keys():
            print(i, end='\t')
            count += 1
            if count % 5 == 0:
                print('\n')
        print()
        self.splitLine('end')

    # display dataframe only for GDP and GDP per capital
    def displayData(self, data, title=''):
        # drop NA
        data[data == ''] = np.nan
        data = data.dropna()
        # change column names
        data.columns = ['Country', 'Continent', 'Year Recorded', title]
        # display all rows and columns
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        self.splitLine(title)
        print(data)
        self.splitLine('end')
        print('Directing back to data interface...')
        self.dataInterface()

        # since data in memory and case data have different countries
        # This function is to get the data for 18 countries in overlap
        # return a dictionary with key: 18 countries; values for 18 countries

    def filter18countries(self, dt,file = 'population'):
        # drop na
        dt[dt == ''] = np.nan
        dt = dt.dropna()

        data = []
        # search the data in dataframe
        for i in Databook.COUNTRY_TRANSLATE.keys():
            # get the data data we want

            if file == "population":
                pop = str(dt[dt['country'] == i]['value'].iloc[0])

            else:
                pop = str(dt[dt['country'] == i]['proportion'].iloc[0])

            # filter only numbers
            index_l = pop.find('(')
            index_r = pop.find(')')
            pop = pop[index_l + 1:index_r]
            # remove ',' in numbers
            res = pop.replace(',', '')
            # get the numeric result
            data.append(int(res))

        return dict(zip(Databook.COUNTRY_TS.keys(), data))

    ###################### System Interfaces ######################

    # System main program
    def main(self):
        # ignore warnings
        warnings.filterwarnings("ignore")
        # display prologue
        self.prologue()
        # loop main interface
        while True:
            self.search()

    # Display prologue
    def prologue(self):
        self.splitLine('Prologue') # split line
        print("Welcome to Covid-19 pandemic prediction system! (press enter to continue)")

        # The following block is used for many times
        if self.go()[-1]: # receive user input and check if it directs to other place
            return None # Stop the function

        print("This is an interactive system where you can retrieve information about the current situation of the pandemic, predictions of the spread of the corona virus and the prediction of the economical impact on different countries and areas.")
        if self.go()[-1]:
            return None
        print("All the data is based on the latest pandemic cases and socio-economic websites.")
        if self.go()[-1]:
            return None
        print('We hope you find this system helpful and wish you all the best during the pandemic!')
        if self.go()[-1]:
            return None

        print('To get the global navigation bar, input "h".')
        print('To see the prologue again, input "p".')
        print('To exit, input "exit".')
        print('To continue, press enter.')
        self.go() # Don't need to terminate the function because it has been at the end


    # Navigation introduction
    def help(self):
        self.splitLine('Navigation Bar')
        for k,v in self.commands.items():
            print(k,'->',v)
        self.splitLine('end')

    # search interface
    # The most fundamental interface
    def search(self):
        print('Please input what you would like to know. (You can input "h" to get some help)')
        inp,ind = self.go()

        if ind:
            return None

        # check input
        # sanity check
        if inp == None:
            return None
        elif inp.upper() == 'SIR':
            self.SIRInterface()
        elif inp.lower() == 'eco':
            self.ecoInterface()
        elif inp.lower() == 'case':
            self.caseInterface()
        elif inp.lower() == 'data':
            self.dataInterface()
        print('404: Result Not Found! Please input again')


    # Case interface division
    def caseInterface(self):
        self.splitLine('Case Interface')
        print("Welcome to the case interface!")
        print('Here you can view case data for different countries!')
        print('Please input the country you want inspect!')
        print('You can input "ls" to view the countries available!')
        inp, ind = self.go()  # get input

        if ind:
            return None

        # sanity check
        if inp == None:
            print('Wrong input! Please input again!')
            return self.caseInterface()

        # check input
        if inp.lower() == 'ls':
            self.nations()
            print("Direct Back to interface ...")
            return self.caseInterface()

        if inp.lower() == 'back':
            print('Go back to previous menu ...')
            return self.search()

        # correct country
        inp = self.standardizeCountry(inp)

        # check if the country is recorded
        if not self.checkCountry(inp):
            print('Wrong country or the country is not recorded! Please input again!')
            return self.caseInterface()

        try:
            temp = CrawlByYinjie(Databook.COUNTRY_TS[inp]).getData()
        except:
            self.ConnectException()

        # existing population
        temp['existing'] = temp['confirm'] - temp['heal']

        # use subplot
        fig, (ax1, ax2) = plt.subplots(2, 1)
        # plot1
        ax1.plot(temp['date'], temp['confirm'], color='orangered', linewidth=1, label='confirm')
        ax1.plot(temp['date'], temp['heal'], color='gold', linewidth=1, label='heal')
        ax1.plot(temp['date'], temp['existing'], color='lawngreen', linewidth=1, label='existing')
        # axis
        ax1.set_xlabel('Date')
        # title
        ax1.set_title(inp + ': Confirm / Heal / Existing Cases')
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(30))
        # legend
        ax1.legend(loc=0)

        # plot2
        ax2.plot(temp['date'], temp['confirm_add'], color='steelblue', linewidth=1, label='confirm_add')
        ax2.set_xlabel('Date')
        ax2.set_title(inp + ': Confirm Adding Cases')
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(30))
        ax2.legend(loc=0)
        plt.subplots_adjust(left=0.18, bottom=0.13, top=0.91, hspace=0.5)
        plt.show() # display
        print('Direct back to interface...')
        return self.caseInterface()


    # Data interface division
    def dataInterface(self):
        self.splitLine('Data Interface')
        print("Welcome to the data interface!")
        print("There is GDP, GDP per capita and country's Covid-19 case data available.")
        print('Input 1 to view GDP list.')
        print('Input 2 to view GDP per capita list.')
        print('Input country names to view case data.')
        print('input "ls" to check countries available.')
        inp,ind = self.go() # get input

        # if navigation triggered, terminate function
        if ind:
            return None

        # sanity check
        if inp == None:
            print('Wrong input! Please input again!')
            return self.dataInterface()

        # Back to search interface
        if inp.lower() == 'back':
            print('Go back to previous menu...')
            return self.search()
        # display GDP list
        elif inp == '1':
            data = self.memory['GDP'].iloc[:, 1:]
            self.displayData(data,'GDP($)')
        elif inp == '2':
            data = self.memory['GDP_pc'].iloc[:, 1:]
            self.displayData(data,'GDP per capita($)')

        elif inp.lower() == 'ls':
            self.nations()
            print("Direct Back to interface ...")
            return self.dataInterface()

        # correct country
        inp = self.standardizeCountry(inp)

        # check if the country is recorded
        if not self.checkCountry(inp):
            print('Wrong country or the country is not recorded! Please input again!')
            return self.dataInterface()

        try:
            temp = CrawlByYinjie(Databook.COUNTRY_TS[inp]).getData()
        except:
            print()
            print('ERROR: Problems arise in Internet connect')
            self.exit()

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.splitLine('Case data for %s in 2020'%inp)
        print(temp)
        self.splitLine('end')
        print('Directing back to interface')
        return self.dataInterface()


    # SIR interface
    def SIRInterface(self):
        print('---------------------------------------------------------')
        print("Welcome to the SIR model interface!")
        print('Please input the country you want to predict!')
        print('You can input "all" to view the map of predicted risks for all countries!')
        print('(You can input "ls" to view the countries available!)')
        inp,ind = self.go()

        # if navigation triggered, terminate function
        if ind:
            return None

        # sanity check
        if inp == None:
            print('Wrong input! Please input again!')
            return self.SIRInterface()

        # check input
        if inp.lower() == 'ls':
            self.nations()
            print("Direct Back to interface ...")
            return self.SIRInterface()

        if inp.lower() == 'back':
            print('Go back to previous menu ...')
            return self.search()

        if inp.lower() == 'all':
            HeatMap().visualRiskHeat()
            return self.SIRInterface()

        # correct country
        inp = self.standardizeCountry(inp)

        # check if the country is recorded
        if not self.checkCountry(inp):
            print('Wrong country or the country is not recorded! Please input again!')
            return self.SIRInterface()

        # Crawl data
        try:
            data_ts = CrawlByYinjie(Databook.COUNTRY_TS[inp]).getData()
            # load to SIR engine
            self.SIREngine.loadData(data_ts)
            return self.SIRSelection(inp) # go to next sub-interface
        except:
            print()
            print('ERROR: Problems arise in Internet Connection!')
            self.exit()

    # SIR interface
    def SIRSelection(self, inp):
        self.splitLine('Predictions for %s'%inp)
        print('What result would you like to get? (input numbers)')
        print('1. SIR prediction plot')
        print('2. R0 (basic reproduction rate of virus. If R0 > 1, it is an serious pandemic)')
        print('3. Current cases and prediction of maixmum cases')
        print('You can input "back" to get to previous menu')
        while True:
            res, ind = self.go()
            # terminate function and navigate
            if ind:
                return None
            # check input
            if res == 'back':
                print('Go back to previous menu...')
                return self.SIRInterface()

            if res == '1':
                self.SIREngine.predictCumPlot()
                break
            elif res == '2':
                self.SIREngine.predictR0()
                break
            elif res == '3':
                self.SIREngine.predictMaximum()
                break
            else:
                print('Wrong input!')
                # do again
                return self.SIRSelection(inp)
        # go to next interface
        return self.SIRSelection(inp)




    # economic impact calculator interface
    def ecoInterface(self):
        self.splitLine('Economic impact calculator')
        print("Welcome to the economical impact calculator!")
        print('Please input the country name you would like to calculate!')
        print('You can input multiple countries (separate by blank) to have a graphical comparison!')
        print('You can even input "all" to get the heatmap for all countries!')
        print('(You can input "ls" to view the countries available!)')
        inp,ind = self.go()
        if ind:
            return None
        # sanity check
        if inp == None:
            print('Wrong input! Please input again!')
            return self.EcoInterface()
        # check input
        if inp.lower() == 'ls':
            self.nations()
            print("Direct Back to interface...")
            return self.ecoInterface()

        if inp.lower() == 'back':
            print('Go back to previous menu...')
            return self.search()

        if inp.lower() == 'all':

            pop = self.memory['population']
            pop_18 = self.filter18countries(pop, file = 'population')
            wage = self.memory['GDP_pc']
            wage_18 = self.filter18countries(wage, file = 'GDP_pc' )

            print("The generated map will use:")
            print('1 -> Actual data')
            print('2 -> SIR Predicted data')
            print('It may some time. Thank you for your patience!')

            inp, ind = self.go()
            if ind:
                return None

            if inp == 'back':
                print('Directing back...')
                return self.ecoInterface()

            if inp == '1':
                try:
                    HeatMap().visualEcoHeat(pop_18=pop_18, wage_18=wage_18)
                except:
                    self.ConnectException()

            else:
                try:
                    HeatMap().visualEcoHeat(pop_18=pop_18, wage_18=wage_18, actual= 0)
                except:
                    self.ConnectException()

            return self.ecoInterface()

        if inp.lower() == 'south africa':
            inp = 'South_Africa'

        # split by blank
        regex = re.compile('\s+')
        inp_list = regex.split(inp)
        # standardize input
        inp_list = list(map(self.standardizeCountry,inp_list))

        # check if the input is right
        for i in inp_list:
            if not self.checkCountry(i):
                print()
                print('Wrong country or the country is not recorded! Please input again!')
                # go back to interface
                return self.ecoInterface()

        # crawl the data
        try:
            datalist = []
            for i in inp_list:
                datalist.append(CrawlByYinjie(Databook.COUNTRY_TS[i]).getData())
        except:
            self.ConnectException()

        # get wage and population data
        pop = self.memory['population']
        pop_18 = self.filter18countries(pop,file='population')
        wage = self.memory['GDP_pc']
        wage_18 = self.filter18countries(wage,file='GDP_pc')


        # containers of impact
        ImpactWithPredictedData = []
        ImpactWithActualData = []

        self.splitLine('Economic Impact')

        # calculate impact
        for j in range(len(inp_list)):
            # call economic class
            calculator = Economic(datalist[j], population=pop_18[inp_list[j]], wage=wage_18[inp_list[j]])

            # calculate and store the data
            c1 = calculator.cost_calculator(is_forecast=True)
            ImpactWithPredictedData.append(c1)
            c2 = calculator.cost_calculator(is_forecast=False)
            ImpactWithActualData.append(c2)
            
            # print result
            print("By SIR prediction, the estimated total economical impact on %s is $%f!" % (inp_list[j], c1))
            print("By actual SIR data, the estimated economical impact on %s is $%f!" % (inp_list[j], c2))
            print()
        self.splitLine('end')

        # if multiple countries are input
        # we add a graph
        if len(inp_list) > 1:
            # draw graph
            fig, (ax1, ax2) = plt.subplots(2, 1)
            ax1.bar(inp_list, ImpactWithPredictedData, color='#235389', linewidth=1)
            ax1.set_xlabel('Country Names')
            ax1.set_title('Predicted Total Economic Impact')

            ax2.bar(inp_list, ImpactWithActualData, color='#0FB5E8', linewidth=1)
            ax2.set_xlabel('Country Names')
            ax2.set_title('Current Economic Impact')

            plt.subplots_adjust(left=0.18, bottom=0.13, top=0.91, hspace=0.6)
            plt.show()

        # go back to interface
        print()
        print('Direct back to Economical cost calculator...')
        return self.ecoInterface()
