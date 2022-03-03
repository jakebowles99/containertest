import requests
from bs4 import BeautifulSoup


def get_results(meeting_id):

    url = f'https://www.thepowerof10.info/results/results.aspx?meetingid={meeting_id}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # if 'Could not find meeting' in soup.find('div', {'id': 'main'}).text.replace('\n','') or 'No results found' in soup.find('div', {'id': 'main'}).text.replace('\n',''):
    #     raise QueryError('Meeting not found. Please input a valid meeting id')

    try:
        'www.runbritain.com' in str(soup.find('div', {'id': 'header'}).find_all('a')[0])

        meeting_dets = soup.find('div', {'id': 'main'}).find_all('table')[0].find('span')
        meeting_res = soup.find('table', {'id': 'cphBody_gvP'}).find_all('tr')[1:]

        results = []
        count = -1
        for i in meeting_res:
            dets = i.find_all('td')
            if len(dets) == 1 and '\xa0' not in str(dets[0]):
                vals = str(dets[0].text).split(" ")
                results.append({
                    # 'event': vals[0],
                    # 'age_group': vals[1],
                    # 'race': vals[2] if len(vals)>2 else 1,
                    'results': []
                })
                count += 1
                
            else:
                if '\xa0' not in str(dets[0]) and 'Pos' not in str(dets[1].text) and 'Gun' not in str(dets[3].text) :
                    try :
                        int(dets[3].text)
                        try:
                            results[count]['results'].append({
                                'pos': dets[1].text,
                                'perf': dets[2].text,
                                'name': dets[3].text,
                                'athlete_id': str(dets[3]).split('"')[1].split('=')[1] if len(str(dets[3]).split('"')) > 1 else '',
                                'age_group': dets[5].text,
                                'gender': dets[6].text,
                                #'year': dets[6].text,
                                #'coach': dets[7].text if dets[7].text != '\xa0' else '',
                                'club': dets[7].text,
                                'sb': dets[8].text,
                                'pb': dets[9].text
                            })
                        except:
                            results[count]['results'].append({
                                'pos': dets[1].text,
                                'perf': dets[2].text,
                                'name': dets[3].text,
                                'athlete_id': 'n/a',
                                'age_group': dets[5].text,
                                'gender': dets[6].text,
                                #'year': dets[6].text,
                                #'coach': dets[7].text if dets[7].text != '\xa0' else '',
                                'club': dets[7].text,
                                'sb': dets[8].text,
                                'pb': dets[9].text
                            })
                    except:
                        try:
                            results[count]['results'].append({
                                'pos': dets[1].text,
                                'perf': dets[2].text,
                                'name': dets[4].text,
                                'athlete_id': str(dets[4]).split('"')[1].split('=')[1] if len(str(dets[4]).split('"')) > 1 else '',
                                'age_group': dets[6].text,
                                'gender': dets[7].text,
                                #'year': dets[6].text,
                                #'coach': dets[7].text if dets[7].text != '\xa0' else '',
                                'club': dets[8].text,
                                'sb': dets[9].text,
                                'pb': dets[10].text
                            })
                        except:
                            results[count]['results'].append({
                                'pos': dets[1].text,
                                'perf': dets[2].text,
                                'name': dets[4].text,
                                'athlete_id': 'n/a',
                                'age_group': dets[6].text,
                                'gender': dets[7].text,
                                #'year': dets[6].text,
                                #'coach': dets[7].text if dets[7].text != '\xa0' else '',
                                'club': dets[8].text,
                                'sb': dets[9].text,
                                'pb': dets[10].text
                            })

        meeting = {
            'title': str(meeting_dets).split('<b>')[1].split('</b')[0],
            'location': str(meeting_dets).split('<br/>')[1],
            'date': str(meeting_dets).split('<br/>')[2].split('</span>')[0],
            'results': results
        }
        
    except:
        meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span')
        meeting_res = soup.find('table', {'id': 'cphBody_dgP'}).find_all('tr')[1:]

        results = []
        count = -1
        for i in meeting_res:
            dets = i.find_all('td')
            if len(dets) == 1 and '\xa0' not in str(dets[0]):
                vals = str(dets[0].text).split(" ")
                results.append({
                    # 'event': vals[0],
                    # 'age_group': vals[1],
                    # 'race': vals[2] if len(vals)>2 else 1,
                    'results': []
                })
                count += 1
                
            else:
                if '\xa0' not in str(dets[0]) and 'Pos' not in str(dets[0].text) :
                    try:

                        results[count]['results'].append({
                            'pos': dets[0].text,
                            'perf': dets[2].text,
                            'name': dets[3].text,
                            'athlete_id': str(dets[3]).split('"')[1].split('=')[1] if len(str(dets[3]).split('"')) > 1 else '',
                            'age_group': dets[5].text,
                            'gender': dets[6].text,
                            #'year': dets[7].text,
                            #'coach': dets[8].text if dets[7].text != '\xa0' else '',
                            #'club': dets[9].text
                        })
                    except:
                        results[count]['results'].append({
                            'pos': dets[0].text,
                            'perf': dets[2].text,
                            'name': dets[3].text,
                            'athlete_id': 'n/a',
                            'age_group': dets[5].text,
                            'gender': dets[6].text,
                            #'year': dets[7].text,
                            #'coach': dets[8].text if dets[7].text != '\xa0' else '',
                            #'club': dets[9].text
                        })

        meeting = {
            'title': str(meeting_dets).split('<b>')[1].split('</b')[0],
            'location': str(meeting_dets).split('<br/>')[1],
            'date': str(meeting_dets).split('<br/>')[2].split('</span>')[0],
            'results': results
        }
    return meeting