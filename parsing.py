import calendar

def parse_s1(filename):
    matches = {
        "singles":[],
        "teams":[],
        "innergeekdom":[],
        "starwars":[],
        "exhibition":[]
    }
    with open(filename) as f:
        lines = f.readlines()
        index = 0
        while index < len(lines):
            if lines[index].startswith('|') and lines[index].count('/') == 2:
                # Line with the date
                date = lines[index][1:].strip()
                # Player lines
                p1 = lines[index + 1][1:].strip().split('(')[0].replace('[','').replace(']','').strip()
                p2 = lines[index + 2][1:].strip().split('(')[0].replace('[','').replace(']','').strip()

                # score
                score = lines[index + 3][1:].strip()
                # winner
                winner = lines[index + 4][1:].split(' by ')[0].split(' in ')[0].strip()
                # update dict
                matches['singles'].append((date, p1, p2, score, winner))
                index += 5
            else:
                index += 1
    
    return matches

def parse_s2(filename):
    matches = {
        "singles":[],
        "teams":[],
        "innergeekdom":[],
        "starwars":[],
        "exhibition":[]
    }
    with open(filename) as f:
        lines = f.readlines()
        index = 0
        while index < len(lines):
            if lines[index].startswith('|') and lines[index].count('/') == 2:
                # Line with the date
                date = lines[index][1:].strip()
                # Player lines
                t1 = lines[index + 1][1:].strip().split('(')[0].split('|')[1].replace('[','').replace(']','') if '|' in lines[index+1][1:] else lines[index + 1][1:].strip().split('(')[0].replace('[','').replace(']','').strip()
                t2 = lines[index + 2][1:].strip().split('(')[0].split('|')[1].replace('[','').replace(']','') if '|' in lines[index+2][1:] else lines[index + 2][1:].strip().split('(')[0].replace('[','').replace(']','').strip()

                # score
                score = lines[index + 3][1:].strip()
                # winner
                winner = lines[index + 4][1:].split(' by ')[0].split(' in ')[0].strip()
                # update dict
                matches['teams'].append((date, t1, t2, score, winner))
                index += 5
            else:
                index += 1

    return matches

def parse_s3_to_8(filename):
    matches = {
        "singles":[],
        "teams":[],
        "innergeekdom":[],
        "starwars":[],
        "exhibition":[]
    }
    with open(filename) as f:
        lines = f.readlines()
        index = 0
        while index < len(lines):
            if lines[index].startswith('|') and ',' in lines[index] and ('202' in lines[index] or '201' in lines[index]) and 'colspan' not in lines[index] and 'rowspan' not in lines[index]:
                # Line with the date
                date = lines[index][1:].strip()
                month = list(calendar.month_name).index(date.split(' ')[0])
                date = f"{month}/{date.split(' ')[1].replace(',','')}/{date.split(' ')[2][2:]}"
                print(date)

                # division
                div = lines[index + 1][1:].strip().replace(' ','').lower().split('(')[0]
                # Player lines
                t1 = lines[index + 2][1:].strip().split('(')[0].split('|')[-1].replace('[','').replace(']','') if '|' in lines[index+2][1:] else lines[index + 2][1:].strip().split('(')[0].replace('[','').replace(']','').strip().replace('\u00c2','')
                t2 = lines[index + 3][1:].strip().split('(')[0].split('|')[-1].replace('[','').replace(']','') if '|' in lines[index+3][1:] else lines[index + 3][1:].strip().split('(')[0].replace('[','').replace(']','').strip().replace('\u00c2','')

                # score
                score = lines[index + 4][1:].strip()
                # winner
                winner = lines[index + 5][1:].split(' by ')[0].split(' in ')[0].strip()
                # update dict
                if 'celebrity' not in div:  
                    matches[div].append((date, t1, t2, score, winner))
                index += 4
            else:
                index += 1

    return matches