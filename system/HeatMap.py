from Crawl import *
from Economic import Economic
from Databook import Databook
from SIR import SIR
from pyecharts import Map

import webbrowser
import os


import numpy as np

### Must install the following package

#pip install wheel
#pip install pyecharts==0.1.9.4
#pip install echarts-countries-pypkg



class HeatMap:

    ### generate heat map of eco costs input 1 to get map with actual data
    ### 0 to get map with predicted data
    ### automatically pop up a website
    def visualEcoHeat(self, pop_18, wage_18, actual = 1):
    
        print('Map is processing...') # print for long waiting time


        ImpactWithActualData = []
        ImpactWithPredictedData = []

        Countries = []
    
        for i in Databook.COUNTRY_TS.keys():
    
            data_ts = CrawlByYinjie(Databook.COUNTRY_TS[i]).getData()
    
            calculator = Economic(data_ts, population=pop_18[i], wage=wage_18[i])
    
            # 把名字改为包可识别的
            if i == 'South_Africa':
                i = 'South Africa'
            elif i == 'US':
                i = 'United States'
            elif i == 'UK':
                i = 'United Kingdom'
            elif i == 'German':
                i = 'Germany'
            elif i == 'Korean':
                i ='Korea'
            elif i == 'Mexica':
                i ='Mexico'
    
            Countries.append(i)

            # separate to reduce calculation
            if actual == 1:
                ImpactWithActualData.append(calculator.cost_calculator(is_forecast=False))
                mapEco = Map('World Economic Costs with Actual Data', width=1000, height=800)
                mapEco.add('World Map', Countries, ImpactWithActualData,
                                 visual_range=[min(ImpactWithActualData), max(ImpactWithActualData)],
                                 maptype="world", is_visualmap=True, visual_text_color='#000')
                mapEco.render(path="World_Economic_Costs.html")
    
    
            else:
                ImpactWithPredictedData.append(calculator.cost_calculator(is_forecast=True))
                mapEco = Map('World Economic Costs with Predicted Data', width=1000, height=800)
                mapEco.add('World Map', Countries, ImpactWithPredictedData,
                                    visual_range=[min(ImpactWithPredictedData), max(ImpactWithPredictedData)],
                                    maptype="world", is_visualmap=True, visual_text_color='#000')
                mapEco.render(path="World_Economic_Costs.html")
    
        webbrowser.open('file://' + os.getcwd() + '/World_Economic_Costs.html')



### generate a heatmap of onging risk
    def visualRiskHeat(self):
    
        print('It may take some time. Thank you for your patience.') # print for long waiting time
    
        Countries = ['United States','Brazil','India','Russia','Spain','Japan','Greece','Australia','France',
                     'Singapore','Germany','Egypt','Korea','South Africa','Mexico','Peru','Chile','United Kingdom']

        SIRengine = SIR()

        risks = []

        try:
            for i in Databook.COUNTRY_TS.keys():

                SIRengine.loadData(CrawlByYinjie(Databook.COUNTRY_TS[i]).getData())
                risks.append(SIRengine.R0)
        except:
                self.ConnectException()

        mapEco = Map('World Future Risks of COVID-19 based on R0', width=1000, height=800)
        mapEco.add('World Map', Countries, risks,
                         visual_range=[min(risks), max(risks)],
                         maptype="world", is_visualmap=True, geo_normal_color='808080',visual_text_color='#000')
        mapEco.render(path="World_Risk.html")
    
    
        webbrowser.open('file://' + os.getcwd() + '/World_Risk.html')
