# This is a class only to store some constants

class Databook:

    # Dictionary to store URLs for case data
    COUNTRY_TS = {'US':"https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E7%BE%8E%E5%9B%BD&",\
    'Brazil' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%B7%B4%E8%A5%BF&",\
    'India' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%8D%B0%E5%BA%A6&",\
    'Russia' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E4%BF%84%E7%BD%97%E6%96%AF&",\
    'Spain' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E8%A5%BF%E7%8F%AD%E7%89%99&",\
    'Japan' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E6%97%A5%E6%9C%AC%E6%9C%AC%E5%9C%9F&",\
    'Greece' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%B8%8C%E8%85%8A&",\
    'Australia' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A&",\
    'France' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E6%B3%95%E5%9B%BD&",\
    'Singapore' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E6%96%B0%E5%8A%A0%E5%9D%A1&",\
    'Germany' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%BE%B7%E5%9B%BD&",\
    'Egypt' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%9F%83%E5%8F%8A&",\
    'Korea' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E9%9F%A9%E5%9B%BD&",\
    'South_Africa' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%8D%97%E9%9D%9E&",\
    'Mexico' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E5%A2%A8%E8%A5%BF%E5%93%A5&",\
    'Peru'  :"https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E7%A7%98%E9%B2%81&",\
    'Chile' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E6%99%BA%E5%88%A9&",\
    'UK' : "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E8%8B%B1%E5%9B%BD&"}

    # Dictionary to store translations for different countries
    COUNTRY_TRANSLATE =  {'美国': 'US', '巴西': 'Brazil', '印度': 'India', '俄罗斯': 'Russia', '西班牙': 'Spain', '日本': \
        'Japan', '希腊': 'Greece', '澳大利亚': 'Australia', '法国': 'France', '新加坡': 'Singapore', '德国': 'German', \
                          '埃及': 'Egypt', '韩国': 'Korean', '南非': 'South_Africa', '墨西哥': 'Mexica', '秘鲁': 'Peru',\
                          '智利': 'Chile', '英国': 'UK'}

    # Dictionary to store URLS for population, GDP and GDP per capita data
    ECO_DATA = {'population':"https://www.kylc.com/stats/global/yearly/g_population_total/2019.html",\
                'GDP':'https://www.kylc.com/stats/global/yearly_overview/g_gdp.html',\
                'GDP_pc':'https://www.kylc.com/stats/global/yearly_overview/g_gdp_per_capita.html'}
