import json
import urllib.request
import datetime

def ret_delay():
	dt = datetime.datetime.now()
	ret = '<head> <title>白陵遅延情報</title> <style> table td {	background: #eee;} table tr:nth-child(odd) td {	background: #fff;}  </style> <meta http-equiv="refresh" content="60" > <meta name="keyword" content="白陵, 遅延, 登校情報, JR"> <meta name="description" content="白陵関係路線遅延情報を自動で取得します。"> </head>'
	ret += f'<h1>JR山陽神戸線 白陵関係路線遅延情報</h1> <h3>データ取得時刻: <br>{dt.year}年{dt.month}月{dt.day}日 / {dt.hour} : {dt.minute} : {dt.second} </h3> <table border="1"> <tr> <th>種別</th> <th>終点</th> <th>遅れ</th> <th>場所</th> </tr>'
	
	is_delay = False
	try:
		url = 'https://www.train-guide.westjr.co.jp/api/v3/kobesanyo.json'
		url_st = url.replace('.json','_st.json')
		res = urllib.request.urlopen(url)
		res_st = urllib.request.urlopen(url_st)
		data = json.loads(res.read().decode('utf-8'))
		data_st = json.loads(res_st.read().decode('utf-8'))

		dictst = {}

		for station in data_st['stations']:
			dictst[station['info']['code']] = station['info']['name']

		for item in data['trains']:
			if item['delayMinutes'] > 0:
				stn = item['pos'].split('_')
				try:
					position = dictst[stn[0]] + '駅'
				except KeyError:
					position = "特定失敗"
				#print(item['displayType'], item['dest']['text'],'行き:',item['delayMinutes'],'分遅れ',position,'辺り')
				if(item["displayType"] == "普通" or item["displayType"] == "新快速"):
					if(item["dest"]["text"] == "西明石" or item["dest"]["text"] == "野洲" or item["dest"]["text"] == "米原" or item["dest"]["text"] == "網干" or item["dest"]["text"] == "姫路"):
						ret += "<tr> <td>" + item["displayType"] + "</td> <td>" + item["dest"]["text"] + "行き" + "</td> <td>" + str(item["delayMinutes"]) + "分" + "</td> <td>" + position + "</td> </tr>" + " <br>"
						is_delay = True

	except urllib.error.HTTPError as err:
		print('HTTPError: ', err)
	except json.JSONDecodeError as err:
		print('JSONDecodeError: ', err)

	if(is_delay == False):
		ret += "<tr> <td>遅延は</td> <td>発生して</td> <td>いま</td> <td>せん</td> </tr> <br>"
	ret += "</table>"
	ret += ' <img src=\"data:image/png;base64,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\"> '
	ret += r'<p>※このページは1分ごとにリロードされます。</p> <a href="https://twitter.com/BOT43858908">Twitter(@BOT43858908)</a>'
	return ret