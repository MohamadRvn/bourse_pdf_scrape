import pandas as pd
from urllib import request,error
import re
def tse_amalkard(start,end):
    #download directory pdf and xls
    dir_xls = 'save xlsx files here'
    dir_pdf = 'save pdf files here'
    # create url
    url_list = [(lambda x: 'https://new.tse.ir/news/newsPages/news_S{}.html'.format(x))(x) for x in range(start,end+1)]
    dl_url1 = 'https://new.tse.ir/news/newsFiles/FILE/'
    dl_url2 = 'https://new.tse.ir/news/newsPages/CoDoc/'
    #download
    for urlx in url_list:
        pdf_code = ''
        xlsx_code = ''
        xls_code =''
        try:
            response = request.urlopen(urlx)
            p_c = response.read().decode('utf-8')
            pattern_check = 'خلاصه عملکرد'
            pattern_pdf = '(a href=\")(.*)(/)(?P<pcode>.+)(.pdf\">)'
            pattern_xlsx = '(a href=\")(.*)(/)(?P<xcode>.+)(.xlsx\">)'
            pattern_xls = '(a href=\")(.*)(/)(?P<xcode>.+)(.xls\">)'
            if len(re.findall(pattern_check,p_c)) != 0:
                for item in re.finditer(pattern_pdf, p_c):
                    pdf_code = item.groupdict()['pcode']
                    pdf_code = re.sub('\s+','%20', pdf_code)
                for item in re.finditer(pattern_xlsx, p_c):
                    xlsx_code = item.groupdict()['xcode']
                    xlsx_code = re.sub('\s+', '%20', xlsx_code)
                for item in re.finditer(pattern_xls, p_c):
                    xls_code = item.groupdict()['xcode']
                    xls_code = re.sub('\s+', '%20', xls_code)
                try:
                    request.urlretrieve(dl_url1+pdf_code+'.pdf',dir_pdf+pdf_code+'.pdf')
                    print(dl_url1+pdf_code+'.pdf')
                except error.URLError:
                    request.urlretrieve(dl_url2+pdf_code+'.pdf',dir_pdf+pdf_code+'.pdf')
                    print(dl_url2+pdf_code+'.pdf')
                except error.URLError:
                    pass
                try:
                    request.urlretrieve(dl_url1+xlsx_code+'.xlsx',dir_xls+xlsx_code+'.xlsx')
                    print(dl_url1+xlsx_code+'.xlsx')
                except error.URLError:
                    pass
                try:
                    request.urlretrieve(dl_url1+xls_code+'.xls',dir_xls+xls_code+'.xls')
                    print(dl_url1+xls_code+'.xls')
                except error.URLError:
                    pass

        except error.URLError:
            pass
