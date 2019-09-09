'''
Scraping Boilerplate/Example Script
Tucker Craig
09-09-2019
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup as bs
import os,time,smtplib,json
# from selenium import webdriver # uncomment for JavaScript

def ESPNExample(team_id='2166',year='2016', debug=False):
    team_id = str(team_id)
    year = str(year)
#BASIC FORMULA
#-------------------------------------------------------------------------#
    with requests.Session() as session:
        url = 'http://www.espn.com/mens-college-basketball/team/schedule/_/id/{}/season/{}'.format(team_id, year)
        sauce = session.get(url).content
        soup = bs(sauce, 'lxml')
#-------------------------------------------------------------------------#
        if debug:
            print soup
        
        num_games_played = len(soup.find_all('span', {'class':'ml4'}))
        #print num_games_played
        for game_number in range(num_games_played):
            try:
                output = []
                latest_game_id = soup.find_all('span', {'class':'ml4'})[-1 + game_number].find('a').get('href').split('/')[-1].split('=')[-1]

                game_url = 'http://www.espn.com/mens-college-basketball/game?gameId=' + latest_game_id
                pbp_url = 'http://www.espn.com/mens-college-basketball/playbyplay?gameId=' + latest_game_id
                box_url = 'http://www.espn.com/mens-college-basketball/boxscore?gameId=' + latest_game_id
                stats_url = 'http://www.espn.com/mens-college-basketball/matchup?gameId=' + latest_game_id

                print game_url, pbp_url, box_url, stats_url
                # http://www.espn.com/mens-college-basketball/game?gameId=game?gameId=400871137

                game_sauce = session.get(game_url).content
                game_soup = bs(game_sauce, 'lxml')
                try:
                    game_date = game_soup.find('span',{'class':'date'}).text
                except:
                    print "game {} {} has no data".format(team_id,game_number)
                    continue
                
#STATS
#-------------------------------------------------------------------------#
                stats_sauce = session.get(stats_url).content
                stats_soup = bs(stats_sauce, 'lxml')
                
                stats_table = stats_soup.find('table', {'class':'mod-data'})

                opp_index = -1
                team_index = -1

                home_team = stats_soup.find('div',{'class':'team home'}).find('a',{'class':'team-name'})
                home_id = home_team.get('href').split('/')[5]
                
                away_team = stats_soup.find('div',{'class':'team away'}).find('a',{'class':'team-name'})
                away_id = away_team.get('href').split('/')[5]

                if (home_id) != team_id:
                    team_index = 1
                    opp_index = 2
                    opp_id = away_id
                else:
                    opp_index = 1
                    team_index = 2
                    opp_id = home_id
                team_name = str(stats_soup.find_all('td',{'class','team-name'})[team_index - 1].text)
                opp_name = str(stats_soup.find_all('td',{'class','team-name'})[opp_index - 1].text)

                #print stats_soup.find_all('span',{'class':'abbrev'})

                stats = stats_table.find('tbody')

                #print stats
		print str(stats_soup.find_all('td',{'class','team-name'})[1].text)
		#print ("header, %s, %s" % (str(stats_soup.find_all('td',{'class','team-name'})[1].text),
		#			  str(stats_soup.find_all('td',{'class','team-name'})[2].text)))
                for row in stats.find_all('tr'):
                    print list(str(i.text.strip()) for i in row.find_all('td'))
#PlayByPlay
#-------------------------------------------------------------------------#
                pbp_sauce = session.get(pbp_url).content
                pbp_soup = bs(pbp_sauce, 'lxml')

                opp_index -= 1
                team_index -= 1
                
                try:
                    pbp_half1 = pbp_soup.find('div',{'id':'gp-quarter-1'}).find('table')
                except:
                    print "no 1st half play by play for {}".format(game_soup.find('span',{'class':'date'}).text)
                try:
                    pbp_half2 = pbp_soup.find('div',{'id':'gp-quarter-2'}).find('table')
                except:
                    print "no 2nd half play by play for {}".format(game_soup.find('span',{'class':'date'}).text)

                #'NoneType has no .get'
                last_score = "0 - 0"
                for row in pbp_half1.find_all('tr')[1:]:
                    score = row.find('td',{'class','combined-score'}).text
                    if score == last_score:
                        continue #not a scoring play
                    last_score = score
                    try:
                        scorer_id = row.find('td',{'class','logo'}).find('img').get('src').split('/')[-1].split('.')[0]
                    except:
                        scorer_id = opp_id
                        pass
                    time = '1' + row.find('td',{'class','time-stamp'}).text.split(':')[0]
                    print [int(score.split('-')[team_index].strip()),int(score.split('-')[opp_index].strip()),int(score.split('-')[team_index].strip()) - margins[r - 2][0], int(score.split('-')[opp_index].strip()) - margins[r - 2][1]]
                #to find scoring plays take 'td' "combined-score"
                last_score = "0 - 0"
                for row in pbp_half2.find_all('tr')[1:]:
                    score = row.find('td',{'class','combined-score'}).text
                    if score == last_score:
                        continue #not a scoring play
                    last_score = score
                    try:
                        scorer_id = row.find('td',{'class','logo'}).find('img').get('src').split('/')[-1].split('.')[0]
                    except:
                        scorer_id = opp_id
                        pass
                    time = '2' + row.find('td',{'class','time-stamp'}).text.split(':')[0]
                    r = rounds(time)
                    if r == 6 and bg15 == None:
                        bg15 = (scorer_id == team_id)
                    #print margins
                    margins[r - 1] = [int(score.split('-')[team_index].strip()),int(score.split('-')[opp_index].strip()),int(score.split('-')[team_index].strip()) - margins[r - 2][0], int(score.split('-')[opp_index].strip()) - margins[r - 2][1]]
                margins = list(i[2:] for i in margins)
                rounds_won = list(i[0] - i[1] > 0 for i in margins)
                bg11 = sum(rounds_won)
                bg12 = rounds_won[4]
                bg13 = rounds_won[9]

                output += ['BEAUTIFUL GAME SCORE:']
                header = ['DFG%','D3FG%','#F','OFG%','O3FG%','OFT%','#TO','RB%','ORB','DRB','#RWON','WR5','WR10','FTSR1','FTSR6']
                #bg = [40, 35, 17, 45, 36, 75, 15, 58, 11, 14, 7, True, True, True, True] #'\t'.join(str(i) for i in bg)
                bg_stats = [bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8, bg9, bg10, bg11, bg12, bg13, bg14, bg15]
                bg_bools = [bg1<40, bg2<35, bg3<17, bg4>45, bg5>36, bg6>75, bg7<15, bg8>58, bg9<=11, bg10>14, bg11>=7, bg12, bg13, bg14, bg15]
                output += ['\t'.join(str(i) for i in header),'\t'.join(str(i) for i in bg_stats),'\t'.join(str(i) for i in bg_bools)]
                score = sum(bg_bools)
                output.append('Total: {}/15'.format(score))
#Output
#-------------------------------------------------------------------------#
                try:
                    os.mkdir('bg') #try to create directory
                except OSError as e: #bg already exists
                    pass
                os.chdir('bg')
                try:
                    os.mkdir(team_name) #try to create directory
                except OSError as e: #team_name already exists
                    pass
                os.chdir(team_name)
                try:
                    os.mkdir(year) #try to create directory
                except OSError as e: #year already exists
                    pass
                os.chdir(year)

                game_sauce = session.get(game_url).content
                game_soup = bs(game_sauce, 'lxml')
                date = game_soup.find('span',{'data-behavior':'date_time'}).get('data-date').split('T')[0]
                
                with open("{}_{}.tsv".format(date,opp_name),"w") as file:
                    for row in output:
                        file.write(row + '\n')
                os.chdir('..')
                os.chdir('..')
                os.chdir('..') #return to original directory
            except Exception as e:
                print "[{}]{}\nNo data could be found for {} {} {}.".format(sys.exc_traceback.tb_lineno,str(e), team_id, game_number, game_soup.find('span',{'class':'date'}).text)
        #return (date,output[-4:-2])
        return 'DONE'

def twitterExample(username="timchartier", debug=False):
    with requests.Session() as session:
        url = "https://twitter.com/timchartier"
        sauce = session.get(url).content
        soup = bs(sauce, 'lxml')

        next_pointer = soup.find("div", {"class": "stream-container"})["data-min-position"]

        while True:
            next_url = "https://twitter.com/i/profiles/show/" + username + \
                    "/timeline/tweets?include_available_features=1&" \
                    "include_entities=1&max_position=" + next_pointer + "&reset_error_state=false"

            next_response = None
            try:
                next_response = requests.get(next_url)
            except Exception as e:
                # in case there is some issue with request. None encountered so far.
                print(e)
                return tweets_list

            tweets_data = next_response.text
            tweets_obj = json.loads(tweets_data)
            if not tweets_obj["has_more_items"] and not tweets_obj["min_position"]:
                # using two checks here bcz in one case has_more_items was false but there were more items
                print("\nNo more tweets returned")
                break
            next_pointer = tweets_obj["min_position"]
            html = tweets_obj["items_html"]
            soup = bs(html, 'lxml')
            print soup, next_url
            #tweets_list.extend(get_this_page_tweets(soup))

        num_tweets = len(soup.find_all('div', {'class':'content'}))
        print num_tweets
        return 'DONE'

def davidsonExample(debug=False):
    with requests.Session() as session:
        url = "https://www.davidson.edu/offices/registrar/schedules-and-courses/fall-2018-courses/" + sub + "-fall-2018-courses"
        sauce = session.get(url).content
        soup = bs(sauce, 'lxml')

        rows = soup.find_all('tr')
        foundClass = 0
        space = False
        for index,row in enumerate(rows):
            cells = row.find_all('td')
            foundSubject = False
            foundCourse = False
            thisIsClass = False
            for i,e in enumerate(cells):
                if(e.get('class')[0] == 'subject'):
                    if(e.text.strip() == sub):
                        foundSubject = True
                elif(foundSubject and e.get('class')[0] == 'course'):
                    if(e.text.strip() == lvl):
                        foundCourse = True
                elif(foundCourse and e.get('class')[0] == 'section'):
                    if(e.text.strip() == sec):
                        thisIsClass = True
                if (not foundClass and thisIsClass and e.get('class')[0] == 'remaining'):
                    foundClass += 1
                    remaining = int(e.text.strip())
                    if (remaining > 0):
                        with open("output.csv", "w") as f:
                            f.write("%s,%s" %(e.text.strip(), "2"))
        return foundClass # returns number of classes with space


if __name__ == '__main__':
	print ESPNExample(debug=False)
