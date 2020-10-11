import json, os, shutil, time, requests, re
import urllib
from bs4 import BeautifulSoup


def PageCrawler(recipeUrl):
    url = 'https://www.10000recipe.com' + recipeUrl
    print(url)

    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
     
    recipe_title = [] #레시피 제목
    recipe_source = {} #레시피 재료
     
    res = soup.find('div','view2_summary')
    res = res.find('h3')
    recipe_title.append(res.get_text())
    res = soup.find('div','view2_summary_info')
    recipe_title.append(res.get_text().replace('\n',''))
 
    res = soup.find('div','ready_ingre3')
    
    #재료 찾는 for문 가끔 형식에 맞지 않는 레시피들이 있어 try / except 해준다.
    try :
        for n in res.find_all('ul'):
            source = []
            title = n.find('b').get_text()
            recipe_source[title] = ''
            for tmp in n.find_all('li'):
                print(tmp.get_text().replace('\n','').replace('                                                        ',':'))
                source.append(tmp.get_text().replace('\n','').replace('                                                        ',':'))
                
            recipe_source[title] = source
    except (AttributeError):
            return


def PagePharsing(pageUrl):
    url = 'https://www.10000recipe.com/recipe/list.html?reco&page=' + pageUrl
    print(url)
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    res = soup.find('ul','common_sp_list_ul ea4')
    try :
        for n in res.findAll('li'):
            for m in n.findAll("a", href = re.compile("^(/recipe/)((?!:).)")):
                if 'href' in m.attrs:
                    recipe_url = m.attrs['href']
                    #print(recipe_url)
                    PageCrawler(recipe_url)
                    print("=========================")
            # m = n.find('a').get_text
            # print(n)
            


    except (AttributeError):
            return
 

if __name__ == '__main__':
    #ppt = (PageCrawler("6864674"))
    page = 1
    for n in range(1, 2):
        PagePharsing(str(page))
        page += 1
