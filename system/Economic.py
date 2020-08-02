from SIR import SIR

# Economic impact calculator
class Economic:
    # Public members we will use
    data = None # case data
    population = None # area population
    wage = None # area wage data -> use by GDP per capita
    SIR = None # SIR engine

    # constructor with parameters
    def __init__(self, data,population, wage):
        self.data = data
        self.population = population
        self.wage = wage
        self.SIR = SIR(population = population) # SIR class
        self.SIR.loadData(data)


    # Economic impact calculator
    # input: is_forecast: True if using SIR prediction data; False if using actual data
    # input: is_total: True if all the data is included; False if not
    # output: impact amount
    def cost_calculator(self,is_forecast=False, is_total=True):

        if is_forecast:
            R = self.SIR.R
        else:
            R = self.data['dead'] + self.data['heal']

        R = max(R)
        # max(R) records the predicted maximum cumulative cases (healed or dead) in the SIR model.
        # These are the infected people and the orgin of ecnomic cost.
        
        C_direct = (0.19 * 12 * 58.75 + 0.05 * 28 * 1212) * R
        # Direct cost to the economy is: 
        # cost per day in ICU of infected (1212 dollar) + average days in ICU (28 days) + Prob
        # of going to ICU after COVID-19 infection (0.05) + cost per day after hospitalization *
        # average days in hospitalization * Prob of hospitalization after COVID-19 infection.
        
        C_indirect = (0.19 * 12 + 0.05 * 28) * self.wage * (1 / 365) * R
        # Indirect cost to the economy is:
        # local wage per day * (Prob of hospitalization * average days in hospitalization
        # + Prob of ICU * average days in ICU.

        if is_total:
            return (int(C_indirect + C_direct)+1)
        else:
            return (int(C_direct)+1)
