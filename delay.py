import json
import urllib.request
import datetime

def ret_delay():
	dt = datetime.datetime.now()
	ret = '''<head> <title>白陵遅延情報</title> <link rel="icon" href="https://raw.githubusercontent.com/matcha1024/mc-note-functioner/master/favicon.ico"> <style> table td {	background: #eee;} table tr:nth-child(odd) td {	background: #fff;} 
p {
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  margin: 60px auto 40px;
}
th {
  background: #e9727e;
  border: solid 1px #ccc;
  color: #fff;
  padding: 10px;
}
td {
  border: solid 1px #ccc;
  padding: 10px;
}
@media screen and (max-width: 640px) {
  .tbl-r03 {
    width: 90%;
  }
  .tbl-r03 tr {
    display: block;
    float: left;
  }
  .tbl-r03 tr td, 
  .tbl-r03 tr th {
    border-left: none;
    display: block;
    height: 50px;
  }
  .tbl-r03 thead {
    display: block;
    float: left;
    width: 30%;
  }
  .tbl-r03 thead tr {
    width: 100%;
  }
  .tbl-r03 tbody {
    display: block;
    float: left;
    width: 70%;
  }
  .tbl-r03 tbody tr {
    width: 50%;
  }
  .tbl-r03 tr td + td {
    border-left: none;
  }
  .tbl-r03 tbody td:last-child {
    border-bottom: solid 1px #ccc;
  }
}

html {
  height:100%;
}

body {
  margin:0;
}

.bg {
  animation:slide 3s ease-in-out infinite alternate;
  background-image: linear-gradient(-60deg, #6c3 50%, #09f 50%);

  bottom:0;
  left:-50%;
  opacity:.5;
  position:fixed;
  right:-50%;
  top:0;
  z-index:-1;
}

.bg2 {
  animation-direction:alternate-reverse;
  animation-duration:4s;
}

.bg3 {
  animation-duration:5s;
}

.content {
  background-color:rgba(255,255,255,.8);
  border-radius:.25em;
  box-shadow:0 0 .25em rgba(0,0,0,.25);
  box-sizing:border-box;
  left:50%;
  padding:10vmin;
  position:fixed;
  text-align:center;
  top:50%;
  transform:translate(-50%, -50%);
}

h1 {
  font-family:monospace;
}

@keyframes slide {
  0% {
    transform:translateX(-25%);
  }
  100% {
    transform:translateX(25%);
  }
}
  </style> <meta http-equiv="refresh" content="60" > <meta name="keyword" content="白陵, 遅延, 登校情報, JR"> <meta name="description" content="白陵関係路線遅延情報を自動で取得します。"> </head>

<div class="bg"></div>
<div class="bg bg2"></div>
<div class="bg bg3"></div>
<div class="content">
	'''
	ret += f'<h1>JR山陽神戸線 白陵関係路線遅延情報</h1> <h3>データ取得時刻: <br>{dt.year}年{dt.month}月{dt.day}日 / {dt.hour} : {dt.minute} : {dt.second} </h3> <table border="1" class="tbl-r03" align="center"> <tr> <th>種別</th> <th>終点</th> <th>遅れ</th> <th>場所</th> </tr>'
	
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
	ret += '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAApQAAABFCAMAAADD7IatAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEyUExURf////Hx8aurq2ZmZpqamgN6wFVVVQBzvaHL5//+/nh4eImJiSkpKfv7+7y8vH5+fgEBATAwMEhISMbGxpCQkM3NzUJCQoWFhd/f3z4+PmFhYbOzs+fn54q/4TCQywF2vxISEiMjI+Li4huGxnV1dcDAwAoKCr/d7xkZGQt+wpycnD2WzjQ0NNHR0Wpqak+g0qmpqdXV1bfY7f+aVDg4OCWKyE5OTrPV7KCgoK3S6x4eHhOCxG9vb1tbW9zc3Pn5+WKp15WVldnq91JSUi0tLUWb0Ovr6+/v7/f392uv2dnZ2ZDC44O736jP6fPz81ml1XWz3K+vr5vI5vD3/Li4uHy33tDm9JbG5srKyqWlpSWA///07bnV/1ic/+bx+8ni8SQkJAsLC3at/7jV/4/C4//BlxHdeHAAAC2HSURBVHja7Jtrj6pKFoaXQEi4Q3ET4AMQMMQA0RxCjFE7ThshfiAx6WRkLsnMJOf//4UB+7JnT+NRtD1H9tnLbjodqVKqnnrXqlVVAP9nXFIAALtyMmRPGYZx699VQJJp/SItkHE7oCMmpxYl/LSf9tl0D1Y8H/F8DCsjHBNMRsjgZdvpmiU8EPJr6lSmcITyGWZ6HhAESxBBUxGqXwC2NNbpGWbuwNP/JI08tCy6NuInbhdZUNW/Ry2bAHBZodAaE5fGBF8TvMBD7l9T6WuhBkpmDcES22DmCwAinfoVAbVAPK0Qz7v3GzsYOe1hG+dCdMiHPjO0+04LRd04OAeNZK3O8kPBFsNqbDBspWYOjWgti0GXXtYCgfMA+uCKr06/QekYqIDAoOe01kAJ2lEr5Q0KdV/DPQC9qxALa/Ce+taV26q0KoOmU6zfSCp4OANeuaGGjG+ERT53Gw2wxWamsJlgK8DYHCWpFg+11KXNdHkAqK6RJh9AiBulzA2AIDIdM22gtBbA4g4UAZIX64i2AIROgO2fNXY0j/onljtj/SNAySjzAqz0hhrcrazoLCIn5z3tTmMCpDBQpC5Om5k5LHh0YJSUIACI1TVQcqBjeVq7bzKGwfQ5REEJgJIBqIEGA4TI4SJMAKhFp2rLoZ2jHnbswAi4HwFKSDCAgzi8vgIH+HVFCuqZOEa3oZAOmY24VLaUbMjQpKJCjU25lDIKYHFNFBErsNWiYGjCi7CloxhtM0OGlGmMhd0CqUjFcQXGQfeoJIx72JtTSTF5ftlzKAcuBRA7y1ugBAChOhuELwBUfQEIvJLiMmKxsBfZgETTpYULNBXMroqHq29u2a44WADEKyDUxhSAwtzy+xk1pbpWPpYMwxHVvnVmoWymHrn2myi6z8abABCYUXV1Q4SXQQn8EBSFkkkAAA6fDp+zKofSLCe8Dgf4qiRGIcu3V+JtBgBPL72b6Ez1stL0fOBnVK+htBqNHAtT4WoKHPCM1CG7BQB//c9f4Ndf/34H5SfGXzCLdbd97c/XVYJ+Mwm2M4Rc4m+oYQSVDqbpdNK6f/7tH/DLL48KJcycCJE9TPbtVPUgHlS15+4bJiN3JNxSwfIp1yJU5tMfCErgPJnn+teZxlgRMMzE1J5DCZz3B7T+A0BJFa92slnOF8IejVuD0KKJIJryI32p6VVpjLK4neyyd1BaoZGKhjE6sdaTkOcLsSUe4vXP4GGgZBAiSNZ/mLVvmWGYLKsv3bR7QsGavi0AWAPIHed7jwAlDYUEkLZDqUStw8wSqPKjkDznuRTH08cRJYNQhPHaxIJH+UJTDMNws1la7lQsLe3sui0676YrAGoPodzg5gjHndZnJ6T8fCFl5D9pGKY9DpSsWjkCwyiPk/dXN3ia4lLHeAI30EjY3LL4TVcAU9Q/KM344Mbxpo0+Ih2cLCSzccy+uW8ODIIw7Edx37YkoGbHywNptyw17jvqBuV2vrA1KIwbQmN/b1NDo39QLgPeDQK2DUq0vqTQLkyWG4Qc/PAgBPCzKcXSNI0eB8pDpgq++twNr+V4o1cA1Q1ZIUFnV32EMvJ9x/fnbVDaLHOy0KIpdNTGbJQrGJcnPjyQFfBQJofkSMzYTlCWLvhhATC5oWFr6QDL7B2UT+VxotOeLsqjhDpRqPxWiOV2eDBTrvfe+fTNvia3xCUBtbGGw+EdFqQ84sO6rCpw28Q10m4xbp7C0lGhNPjbWiPtWP4xkucnoQQoT1AJ30Pp+YzyfH3oo4hv9kVLMHKia81xiOrrG1bVNE3chE79p8MyiS2EBKHEbmp1+Sxzg3vlxL1pTQdy0oReQmn8xjPpp6D8mG3PRmVaUZRlXC1M5fbNvmax2iMCB5Fk59641ByLJruVCAQbCAWeZp2ghKZB5Rv3WNMC10sobw3figfb+bDFX6zF1gD2HpUL87nojMT5XOjeTP2wB4CyPO66VFsDwvI3zhzlH2KRNwM6OjUe40vEwSeP1k1HQKMAqEOLjy5fIhY55Ii8Q5cliB8xpMGj5H0uwVzkir8LVy5Uv3wIIJ8I1fNT6UuMAYi+qYTt9xBKG6/NFFsP3w6UqDVVZEmSxIr15ZhbD+besgZAawd4fEmjCPjRXro8oq6JWkKnpvJ5zUnRlbFq3kcpE9wWVzTpZe9QVsklxVgAD8Ow18mReQCq/udsCs0iKZlAn6m0SZJEDkmSn1N2uhQ6klT3zeBtqhqnasAXPYMSALjAaI8cVwW0TzG3w6Ea1dPbVx7sAMNCLFM+7SWNm2ShVF+sO9CRa7mx8ls4puzQS1KNfR7d45h7YmYpCGEkNizazQNuzj9gVWPCTjTG2AOAJ41cN3CY5GyqxlpSttmiqtzQwtYShsltUTymjL23ZQPuX1KUOiZO5/2DshBPTJxPHmRcaqxEjpB77As8OAVlow1Hu8d6n5IKIeMLLZWra9jnsEX4XZTSCYfgCcLRfecEQaCQIAj5vFKyEwGE/atSqr61gcMlUJ54x2VolyHbAgebICSB2H/rg85LCH88lCuGYXSxOWHWIvFhOeD5tlG2VGW0SgfCEcodDSfdN0XmhXlu+mc57zbv8Ih7LMQwf4GS33eDWkLGw8bId69NihckLLnvoESrW6GcN+47aoOSN2oolehteBoSO2Ld/Q8EJTWiU4F2W054LAPcdHD9FUrIPYZxGKZtTw4fAaBz59W86t26HD+km5jSfxFaPOeO4PhKMe9yYj0RR0cT36DMHeWC1FOM/hfKeXkrlCxfpTzdAuWKIFVjL7PqMbLi8rKPSnl036MTqRVRoQCUlmnecs8Ic0Z5BSJ3t437bvPRT6wFEP97dQ/JKglxNljKbVCWgoyqaX4XpZTfxl7wJtA4/rQ539aCAu4HlGoKycslUL6QzR37lttMghVJveXRFRzHRba+vLb5GKVzLP+9oczt+0HJ7Zo3yX2bUqq8pMavQOg0eZzvSZ92sHLL7NhQN5wdfyKaJvVadnVam9Ak5mUblLMtoGXdMTzc23LcHcDK8c9s7s6dbTGfpHR6bEtUATo4tHkWymk4gDxxW6DykGmQ5q4VAd003qd/O6OUDWGenPsgz/tSKJURdSuUA9M56XX+S8u5traKhHHcqgjqRMe7mgBOMCLFSAISgsSUkBBDAKEQoL7r+f5fYudmmrTptsvueqDl9DbjzO/5P5e5rKrk0fUIzVw4RsKUFhZf8gkreTyo2vCtb/qvqiYPDfqJXhDxSIvMM3jydeERlONUsJctav+PcvXS87xW1nWdlGOcP3tqM9EP+2glfZloY8kwibyOq5fK6g5G7/7YWJqBZPO1JNTta3G6UncZvaegz1Va15NI8DPXD/HpaEcuJbUFbtUL3Y/GKUnqWRyKVP8BlPm/V8rvC2Yn7/H1VuupcJoJS5O+Oa1LPBzgbkhxfrPis4UPNsrNx1D2RDEvHx0CM0c9nuIHKqz25+Li1Z73P6w0AZjBBSqUiljycf53BnVjb6r6oaWjVvj1qZnR5GGWeBkJE1MVOho0B/ZoDlNU0brUa0C/5qRM+47jX8TVbag0oZn5fh7/eygDRVEAVPBD45unfwBlO4R5asufn/f4TFtSuPxGPz7GDg/49+no5ftmTPgAr9SyMgQBzDPpA7BvOtFe06Rd3Aemngb61xk9dcLL+I7Vpzf+U9u79r+rPIK1gBZoIVy4ewlv2zj+TSVgcgtudxtmj24aHmHjez0+diQ3KN/8hJbBTIKjvcnf6nO+qc7Ubyznch15/CAfj/YDKN/+4bEzEtQCGOOPVEaQ4JNFFku9gdKx2PO5P4shY+wyRdlXirKi9dZY4U/IRJ08+zkvf0WpjPRrBWxa35fhrqOad0/1sPSXHgqACost93nY52Wmrj9Oxkf1sMPjTaMPl+/pHwOeD+uSQnkyg8aCEefgnb4am5+Gr3GQs2KTZHqpXME8sL7OFcM6IItVSXY7obeJB6azodgRQj4jaVtLdEca/Q7J3BzTsuixLQf35kSaIu2CUkwWqLZqDuVhHc6vkG8i3bypIFi3mN8V2J3bGuqkvv6BqZEtvfrMCh6lJCkYHOrzhZnfVuRE+5lXmKZkbsg4L99TJMFDllgiHWSki2tFoVeZTS3rLZ2tFozXtjqlNp5tOvXEW+eiKLKWDqXqfqOUya2FOPtfgenD15v6LP10C6WR0v74d9ol63pjYUKIwnfFklR3pJZCGYYhCtE2DKkYgScioRvjK5TzozAlC2d0hGb8/VhHjNgxnm3DoJIYv5ErGo5sF9LO9FLPC2bnxxYGuYmrE4M+rMunKu3orjYK5SgZe5NrQPFO2OXmDlTznI51jwzhUhZc0shyQUJeE72p7bhpmcXv5JbkphLFZRtOrrWFlwN4LXYxX7UkNS4R/w41J9f0wBN+3QNpGeQWXKBUNBmUITbqoeeCU3iz/EYDrcF3uthcUMVtxsGfo5rsYiKvBHz6VKxyU2uaHWlaRs3OOgnuWjckAuX8fWtaYFGYZFl75ERzR9kCumG0gx5K4UIUEQl/jrPC2ZchvcJZ2G5cQy9Xm35C84N+Vc52s92eQVkEYmkzKB2Yv7lIlv3PUBZ8NXnQi9nqV3WRzK+YmXUWbJ6lJInWd1AmVE2yz1DqejBA+axtck1j1yCGspzgfzIbZdBL2UcOK/Zr2dzs6bdsh0Lp0p0yY1ku4V6WmQLasq7FQNNoTBNv3MZ2gwHKKNtoEDzc5TjJHl4u1kYQbqCB9Ia574SKGXeS74RdzgDYrIp9WopfXLu665wptjqbakePkEKYpH0NrRzkOUgsMjPOKl8lPgCRRhoK9sAWG3fHoJSF4gm3nL9c3fe6FRmUpSmECRc6J/OlCkhscVPF/cxNWaYmGGJtjl2P3dnR4s/rFf4w/7D89sy8Sa4oFlAUDuVOVtbpmEI5daL1ORWKCYGyLUAdECjp1gPYwWdyHwigqVc0VrTSVuiQbyPFMAsbaaSlpyhyyrkpeXumMbEtFyl1DB1IEFSiti2/KqXeYKG6+tlZ5P0iUDez9rrCC4TT7k84fxPulPJEsuftfXC1w55kzE5uEKXET7CkUIo2hVJjzh2MtrncbziUmFxdl8fHL1CS/2fDtUM9SVfmA2BxsNgoi+cBylVuSih9tOdrCq6Fj7VlIQCQZRGdAzbsA6hkEbpCaVpXKInEcKVDYuP4jaLzSr84EdyBT9maX6E8uW4n9+2WRy/l7Nk9c5f0tJ/ahmleTqwOKGryFUosjh9QumG9yCGEFErnTysEw62fvlu2tnc8sHAEq3gSX6OQb933U+pH2HPyI+rvnmduPK+m89WU5s7hUApm0NioYVAK5qJ5RpLkBzQibKAHMwhponjxJEVqYpYzhpFi+kkBfWpovSZJjV3F5H1b45ma99rAjiFFcdmnxB19gTLMVopSXWdshnvq/xRkrnFHRMh3UwAh1lcrdmLuA8ouE86mfQ+ljMXdLDmUo9owepu5b9GcVJjFywBlGvSrK5Qk1tyz/eafoJRjsC5YCqMFu7lsFjz0jC+TnTZZcii1PhalWJs8WmjMbytlkbfmhah5C8MukzLbZ3FRLQhLviHN1TIWfDLBGUmXRtyxhQzBS6ZCw3FtqnZShWG/4e5bMIbtNa6fWAgVGQPbrA7YOtFq9gHl4L6JUl7dN5l9eGFKOapfscYPc6YaSEns/eGr+xbGyMqRVTNZP9UWyC1wvSqhra7is9PZw74QlPIApQgXvRNPOJTRNrpg578gUIpuAvck0ZnRvz4piBtkbha774tppg51BXKeF7kW7wNmhImWZtqGKpMXSqXqPlLKZY19m7b6gPJn971saKTlwoKaI2hnkQ6Xd9m3qHWwtsz5HZTqBI6EiBluV6iLKjEPEw5lgydgAzmUTr0P5GEjTk2d/iMoRdACIS0YbPIdlNHKQiubQakvdpoE5Nev5ZMdjO5IRdMByqFOSd2tqihQUXxsHeQlHSM39poYs+ATCBY2fIX1dfp+6XC6w97QGc0MrPLKAGX3kcndKWX3Xim9BhoKpbYq/L45HBiUQXg4QsuCBEplLJz26IVn362grsrrQqyRCnY4egQlSywtFk53fyhxfJFwYx2gZQ0rhrRzA6RNkGocSm8jSjOrZ1C+wGfgJT4CBEo1gM823NplOP0C5Z9EqjeJ5hP22ou9KMeRx5MV7DwyKeYHHQmUB8PYf4LynLxGooHdx++hVPOEkXep8ZyFG9i8XkDCTicNUKZyl3Vkdfr+V5Vpm71wKNeFjlbKnEGpYMpD45V2TkWL6TN60XdvrDVSXe2bL1CeNiCwoJUG2ZJBeeO+tx1JdNSWExD8Rdr19SbqdGEKhAQYAAFFhAsgQEyDRBJDCFEaoxHjhQmJF/Vuf9//S7wzZwZqa7e7m9ds3dQqzpx5zt/nzKAIkaLYT0GJ9vk0orSRMSjt/gmUuu7X5B9rEkFcHKG9Ro0NRzbVKnBW8aVZE527RLRmb0f2CEp9g14tJ7WM6deYcv4LuUIqSEDKAW96szRmKSeS5EvMUnJc3zQl9y7RmPIs5ef1gMoUIJX8GyjJ4F/HJju0JmkjSxOQ7Luj+8ag3Ja5TUD5UleZsdCOwOVUmc+tIBeEjz2CcpU4fvw6e63OUEOwJGs+EVcUlNG8jebTB1CaTZN9tZQB56HJpPkXS7ka8tA3vDDx/hRs0TS3w9UHKE9hcM1OXbd/zCLmBF3Jhud1yI/sODY63maghE4zFwaHoeljMfpLkHL92MZthc2STIKMVjOutCSUgusUnfncrz52Et4HeWtHXxCkBrvIn7uGAhVL+T7jK1i0s0Au5NIoUvPRjktDl6kYCvT1MgEl5IXrDmNyW5APva241VHuy3MJw2tKef9a7sCg2lgjRlACOTxm3ys1TKtZ45EmiIBk34YnU1C2c24VrUZQ6gaOVKYCCXnlHnkYxG62pgHYJW/RCcEvIospabSyJtUONWSghAaYGQVl13Xz/CINJzk8gFIWRK7GPp6B0okmlpPfwPzf0Mqp3iNIlYinCJRR0TsrEnYZndV97+ja7jWFeFzsLd+al3pLQZkTSyk4DixG33M2BsylfEp0yMar3mC0j2AtSQLyT5QEX59nGy54yL7jPSdD8TL9FGSzh0vTd3h4Fu0AgIgmgfLcbm6TlZS3ZKjYgT32A6SQMt7r5zqlyLY21F9BeSKC8n67s2Wkt+8VtsynrZA8u3knIqWFdrEk723zZeW2nbIka6asjuVWuCnVmvFmPjdtALtvxss7Kk5cHVEot5OwicKGHGVyx4KJGvxEZNVNPBKTCfY4IyvlFiwh6smO7eL4tBrBcg+v3QEqO+XNPFu9vexoTUL8qHuuLVIpmLTMUpJfBAqcHZX/jNlXdMCyo9QxjhoNYhQi+JRxJ2kvPdpplbfc9BdewY/Tr4Yatz/Ja64zjhuiQEWL7FnSmjR61SyuwCZdHXIsucE5wnhQwan7lvvGoLz8ommTPjx+Tr2lKlEBAWOtstP+kWaU/3b38s+HTH+EBy9fOJu3v2QEsm+JyvdBgYAf0OQH1vLTIYUy90JOvJPpa/HWPFSSNwj8CkP6U1cndcGn8zgjfL0X9iHtN8bh882XNI2O7P8hN+PfXZy6nkAeBDAe8Kdj4fSBqeqgGMPRgR19W/xIAwXcCc/n+s3w5iVXLL4FZaAN0ddfPjypiqoZMW2Deo/NEyMoicOon3hjN+CS3zGG2xGmdP/dmcrp8lVN5Lb/qBPfH6FY30eXiL/qokn0q2psNnybr20Kkb50uT0UsFbDtm/zCEwsfgwIsgeKSRpKK863ikpqf9ORP9FsslFD1j+YlrFgX9JZjJ5jev9W9+Y0sf9mH0EzDha+zp2SeIdd7uJz6WNLaB88sJsfesRWOQaxvJIDAkV1SMUXwLXwZORkSx/OULs7fXuAXc6eJZ09zwerghLLTiROFNVsMnpvk3OxIheg36Szzv9nvoL85T3VdRr1Khu5EL4DpfwAEyLj8oyffgalY7mHT/4QPYHSkm9S5H3aJ9iqaqSooavCizGVvjMyDybZMg2gcF3OrjmblvO3CTgjGt7zlYeyfPGxAMth9VKyQUASaf09aFJHOhQbFWSpHsXGt9QZGbHs3a0i6o9Ayq3Md7j2XSWgdPNoE44Zwpw5QUCyP5OkCf6RyBIHzO/ByG1k7ZaFTM2hNvD5NMjF80H4h2Y9CwMuN7ax+Ab7EJdCFGPSORlYJM0gFuc/2tebpZD069kWgE2uLv9aHUXRYYyH6nDtL/0bRoerBa50uDmNck5YiFuNQ6DTaDo1nGgdjVGDusBSJkMiG4AMY1PRqFkQTEkwdwLgv+EPfYJmUGpxPFkqMtO2aI0vPRiFKFZU1457UYwUUYQr9Hl+DPN8w2LXpSMZCoKOTQ5lkyzDcUz/FZT6EsQFOGzFpRhdjk72o+/zVHN+iCTJAmBa+KKEEzo8gLK8W69lG0XTR7MY8Pxxzy/XtDnIjmr8cCiTLd1gv+0FnRko6y1nUwJsa4EX3bC+ku48hpH9GkA5V55Aya361VSs2OHj7UaPrlZ8jGn7T1FtfBQZ2CvFws3EgECNTeJP9674EsJTgXSZNwF5WUGzElvnJV2Hgbeoe7HKl5pqeHKLLauZLMliXHA4vssFQZJohrA++PbCod5kcYBpAIpedL3mJTnNB+mc22EHnZcIe88VXGsodDxEObb5YXhs62J13YWCUj7qkpRXNP1ORQBlR6GC5Xg7yAMosUqYGAlg2RDWMyeSEVQZHdJNL6kqgJK78bw9ltxjkVTaRLox8cgZ+6a6HSg/m5lN5JvsNChhbdy7jt2m5PhWk3aDUU/Kce8tEkNDijeQl3O6WfOz2cCEP4DybeKKi4qBUlSXarg/6D+3gXpuph9mprsZEuNk3CnLQGm7luIe/RR9PtP2JdGcUqYGghrCgILSP4WkycOvtWdQStSk+kOoRxjIjr2NgHJKq5ErXd8J5B69zJOGOJqm42uRurxaKVxOdrXXRhXyww3U7kZCf4OOwVUk1ysHo8+b8L/HQMmLLhJpEbTF77Dm3J2BcmNZ00LeEehdDlNlESluyUCZhHc7ZG0XiwWdxo2aokw072h0++/Z4NZbV+EtURnu/6Y/nCqo5RG4RHD0M+GSeZk3Y1TGaT7frel9Sl8TmYAyjv4EyrLf7i25QcTqXS9Npya6ThkdpCYHpWD87QvPq5thW+5iM3N9l55ycyrR/jpfmCbkXHPz3UANagZQopbwBvIzKPXlq8TpLh3PlnR/PLtvTVpMp27B4qL43ZtH9mGb/sF9u7PKyFLEMt02b4ZzvR5AiTzC938yuYbLeZ3flE+gxOjC4q6Ydn4GpaNbRo96sBJX6Nxgod9nUNZ00WFIqVJr2GotGCi9Kbpaqw0stJBKG/e4RLSkjS2lGSEGSis/RA+g/GQpHc8KJep729AwmsKoPizl20ZGVwBlIiwqQaAkoSFIuVttDOqoFnt95q6PPkVbMPEjRpCSUM5F+Akmf1ddd1o4rMmk+4VIWAtro+3MDLa9E4Wsw+IUtxva+BdHS41UY1mt6W9B6aFQvU11m9EIvephhaegxDNRisSroViHcoitwU6tDV++owQOYRWPSDLCPOb/i7A2eKEdnNx9RxucMShxNu8BKOOqqmYZfgJDjpJsIeWTSYS1syuKCbjv/7F3pk2pM1kcb0ERICEAYQvIvsmqlAAB8YKgKAoqisobfb7/p3i6z+mkg3jv3JqnaubW1ORFYtR/r7+cPr2kM/kCpatXyNjDfjsf753Qm/nkX+wZFVPj5dqY2ko03DN/UAqVQ1+hLNhsoUDdanKffHESm/KvJn+B0mFLVyLcdEQ8Fijt+47iRDs7S8BQogdeFfOou1ByJxAKPLoJyH6bbcOhzLjTtPmuh7FjqGY8ifAQnvxlT934FN5fgObbhHLjg+D8eQ6lw953Z/hSsxdvbeN1C0tJOhtI63wSPdvfd+e5pVSCSmijvmBZDiuOokOrhWc8h3H3FCl6oYa/w9oJGPLL2mNRLaAhh1F/xkOfQI21grNaMcxizEKhJ2zDcNhPnxtW7fJ8Knf8xQx6Zr8LZaagBrL9PHjaJFEuByIRKZgHKDN+aZJ/KfCp9fOG5vGco+8/VaadsxOvwraK2PdLfq1TZqPGMpvly4fD6XQ4HMfJVyni8WgA5Y9EIlGYZhMJeAiz1KhcE+0FNy0I2qD5ftnp6AQbOJeJ3aFxNDufZP2/HIiJxYppXzDuw1Rnpw1v2aumN1YotZqjcKYoHesbid7MkEJpjD1sQzmm/jStGOxLn+9boOyETqONp1lQhuW01tVq21DaagyiMxwvjAZk2tqOOZSTGz+FkoDDFFLtZfvLX+g4Zn0dZgQkCCGi2isBE8pI2vI4qWOrpdxuvl+oXxD0vSCU14okaeE6xNvweGoaf32BkPB8Hh16ZzirFO3vxZX3vjkM827s9LV0dPph91DrONjf3KrKSjPPoHQ1LhoCSkKJ2av5jHdgpj+1lB7FAuVcskBZDNTKqrrBeVZHRHJ5evlA4Bot5bI+fOdQuiRPgPKFSxGn1FIqblttDutNpB6pSNGCD2ptWCcFn7GY7i+iFM4jY68xbsaab0xrh03CEU07MfL+XfM9s3fAUqKpjPsC7v58Qn69s3AsP+7XguWyj33GO5vexN1Fd/ydGXETypg7VshMtqFczqhjGJuRRI+vpWMHhzJQZ73Ws2sshncBpaufDYfL07C2u643onm96SfvmEMJ7QvP7EVA+JRyphwr0uYb0RsqHV8sUpu8I5T4SgVCSZuptAGlS5pYoGxUbLbx9AR3P7nov7+fxd8jUJheqTwJECUNdTafqAGl1tEKDsxSxEfbMCmLS5AvqCHxh88R6xfW+66kg1+hJFn/0LFx+yPoXBNVpaXS4HXbYF2CsQFlaKrGGoH5LpQTrzfT854glIEnC5RjTUCZrcXj9utlGs3RuywRT499aQxXbZNl/4ZDqVIbv79/bkCp7Ctx4gAopUxYUqVZiEMZUqV8RIosIfAfsbGnN3TIOz4lqz8XwY+6XLPO7WQS4qM9Fp+S/Yr6lOBUXkv5HpHmk00m9OvmO1Y+9zmWvSJMjfEhIdliKRM00iXtjIW3392mUAYUD05X1LUlPRK8jQhEmJ1DN2uf5mAe5FCeTGhNBBTuctFQTwSUNVyhzqGEOWicavNKAY267d5NkI/n1pilRMu8bJzXNtPABmrGR1sf2v5ACGzvu4QcRwtZsW7esZcOWaEsNtgBjSmpB+VsoNFZavDp6trYNh7aFI8DYsqrHSoJQ8SVIc1GLIJTrMoTmXkUl7l/czZvLGZNxOL5vZndW3cbU0nUry0bUAqfkhTs/fh1zDXGyZ7pids9HeLMYgXWEtuHAGW8/4NkvXxIKJGmtdrjUI4jtXp+7Bhm8H0nIs0607NemRXf6RlZdiIEoTydXldo/zECUJ4WY0pIOXOUGZQxn5Qv7PuKRQ6lO5ZVe4mhAp6LXZs1ektz21QTypl94otpHMpe0TxcOyvPRfP9Q43Zy/OJ7eTXr0MUgrMoi2/PYE7bGadEf2m4PbT0VGc7qnyzXIfWExuBUyB7CSymLIzcXcz5oirej5fdZtr4t0n38AF6V1gIEbipn5JChDFqdP4LcpB/NTE49rj2orRBqkMRnbIR8xfLQHYPnae93ta6DZYq412Um/n2jNFM9crExUoikcchYxjEv/Gy5Yc2mwq5PTWywcPNWjdqvxb7Kciep5DmTXC/m9RZXEE+LPTEnJaZGyf8xksyyxvTRXk+NM/+VMewbvB5xH7VDNeVcEtTmcEUBKUnYiMzfOGLOG7Ylmx1eKujQPY81C6c8FH9OM2WCkW0ZEYjlCV1FpE3C50H+nyBr+c5lQl75FiKLhIJV5SaU/P9vYQBmOvk9Ia1DN+9DfQFyqA5XUiDrWT/wRau/8n9Kf9//G8d/+RtRteHUxzys+Xm2YDy0vJLU/cqftclW2G4LDcfpCtuXsmnuGltiVzyvyGSf2yJ9J+IStsZ2M7ilqj0E9Hii2grRb8rWoiby23R55F5vJEPcXP0TCw3r2QhblpW0WqrVH78IkW/W2n/bShJ95Ae7SN2Pny+ZOfUIsUurwaUC3aXe4P/MD3cR3ZXhXOStNjl2IlhPMPFeczOXZJkl8cqnMktu1zdokhnl8EK/ltG0eKAnVukzS5rkK5R1IRzFVPL0/L8YRGVSI5d7kF0T0YgGqEIEpa7g7wRaxY/yUCIjsgDuzzA+YqsRLkckO1y2Qq8KURNAnG076E4yKtFdEkglXeQyDcUjVBKII4qSAfkEyIscRFcFlAcTnIFhQgxjQjEUQVpjpRABPV0+PFNipI8RWtRaW0U8Ur7kC2Vpv8hUN61BgLKZqm5C+V9KbcL5aKVElA+lpICymTpVkCZ6i4sUBoigHJdagsoqyhCKA9aTguUetcCJU8LQlktjQSUB62VBUpDBAEdgYhDeVV6EFAet94sUKKIQ4nlwqE0y2Ur8Ka44Qi8tY4FlA+lKwHloHRkgRJFHEpn91hAeas3BZRt/UhAmUIRhxJFHMpRqWqB8tsUAZROKH8O5S1WGkLZLj3+QVCm9OpaQLkY6LtQtpJHO1AOVqMHAWWr/SagfMu1BJQPD4uBCeXg7bYpoGy17wSUKxQhlKOmfmxCmbt7vBJQ8rQglM5cV0B529QPTCjbR+uqCWWqW70XUC4GXQHl7VX3wISyfX9fNaHk5XJAtstlZE0RZOb+KGkikNKvHgWU+mAhoFwnAQiEsrq+S5pQHixAxKFsHS8ElEdtECGUzVsQIZTHTmhAOJTdnFNAmVx/l6I1iKDS2oZoJaC8a7f+ICibn/qnCeXgUr/MfYXy6lN/TX2F8rEEzyNCmXzVL1MGlAeX+mvShLKrwyOIUK5bum5CWeUimYsukyaULR3sJkJ539IXJpRGWgDKYypqm1CWUIRQHrW6CxPKJooQymOeRYSSikYmlHfdrtOEkpcLQinKBQPnKWIIrLrdlYnAQwlECGWOigYmlDS4pgmls9u6M6G87a5KJpTtz9XrwIAy9blqPZhQ6ivnmwnlow4ihLJNYzowoaQpettN0RorrWVCySrtwIAyRSut+udASVsBsA8A5frq8Or+K5TU1D02v0JJPZ9FzoBy1T68fTCgHI0O2ysDSvoEp0omlPQnFOlg5lAkG6K/2zXfVslpKIwXltAuoIIggNAEDFBDwEKx1BKFMFKktqWlS6cici+o3/8z+Jxz0rt311eLKyzsDszczrRPcnLy6/lT7nlBCTmLGEo66sMF5WULQwm5ni4oIWcRQ0lHlN4ESsixsAQl5FyOMZSQq+aC0uCoUReUyS8C5Wu/pMF7l6AkeaUuBCAv/QUl5MNxQYlY7boLShaZC0ockUigRDBMIpyvNxExlBSraSaBEiKKmwIljtbxgvLfFukLSoiK9oLybMnrCUrIOdh+IFD62pXllqC0Y+53/xaUus5XrOA5lKachnwsnUA5TmNuDiVQDlNpahqDoGzLstVnFChZZMYgUJKonGqBsp6wO7UVKCGy+EEzlAoiM5dKoNymKLYwlB4TnEOCMqy0lgvKMQ/TbBKU0Zl5cglKiHK9JijtyvYmKLGvIV5QRsd+ESgHffmFBzfmwNoJSltO0RyYiREopzlXR4JynEobdy1QDmXph70WKFuIcJ1hKM2+767YB4Hy2Om2cwJlvRfDuAMjglLv+xjOSTGUat/PfEYsYCg1BvanTlBuU8jbmKCsd81rZyjj2TpaLUOJM7mJrUBpsRlx2j4UKEM1G1cnKM3e4G6q3oTSNZNd6PZ7DuXijJ8RZxjKxal8ujuBsmyBqroLlDV4CAZ3K0GpCod9uLcCJYl6vBnKybrcLilSkki5xTGUbndmmFE/MZQQiS0EpUK91SgEBYayt7nv5gTlAVxcWQuUCIwmIPwwlK4zuer3BCVi6AR7Bcp5kG6XoRwgIr8wlAGi5JfITfA6YlCC0rhxjXHdBAEHjxT3BKXCVDpUAqVxRQg0wimiOt9uJkVKPdvyKX2jj66fIiW1xKa/0vfmxxXFrERKfQwHqk+GslKVgSMESn362RZ9gvJRNc6uB0OpmrAohUzRiqhBBTUIlKcuAm3IBwLlST1AbwTKTTeo++Y3oZz05Kr6LSirXY8DnCxQnithKlAe5yyphqAc+tPlUyGRUkEUEDoFyh6iiqIPQTlDVCwxQblARE8yGMpqb1X1aAXK7qzFFoLyaDbT5X+3DKW/z87oBKV6mAAXQgxDWSGQDOj0Gcq525DPEpTDfVY0NUPpHhDVb4iADOUjhWD4haEsu/Hyiww+FKNAiSYKdxQ6BkmWe+AiQNI3Pfah8oLTN5o6tZcpfUOkt/6CcnGhK3SCcvOYOiYoaT00CkOp+jzc7ypB2au22QqBMlanPSlRE5SmetTGXFCeVGfjFuVIuVQ1rnUC5V5FtY8JSv/Y5AVN+0FA2d77e+A2k6C87Q++Cag8nkFpb8vdBoT3N2tK1Yw1lp66byoW3dV9l9p04Wp0EGxC36aaUnVzdz+v7ruSMk66b+r+ELek0UFgpOGk0XFLvSHOpe67ytkWgrIzs2/Q6zOUh8c1F5T+QBiIW6opEf1zVZ8CZZOXw21Bf0RQzppyBCoygtJvrhsHRECCEthUOflFiejUyS8Rk2DwtmoFyjUiN9hJEOCy7AlKOqDenqHcEcwtojpDiR64KG6bQMnPIEIhUMIhPLVASU6g9puhRJA8BkzHUNIzCLV4gbIPHcpwRHOOlKU+8wtKbEST0y1IUIbF9rnaRoZSdaGL1WMnUO4tZX8s8L1A+fI/15TYSH5oI4+EsIFr81ZNCa9R/nojUo7HYbt5FSjXuLyGclgbdRbRSE0ZCz+sVZCacpw3Su8CZYRo3GaBkkRFpHRMNeW6aM7lXFOO8zgUc0rfMRZiC0E5b10oaGqCctjP+gnK0Ixle4taoOxih1FS+i7HJvBje4KyPveBpmYoQ7PNvphWiZRN7NgvDOU0Ni75JaKcGSfK7gIlxL5AeSY1pX8GJfUrTRkFSupX1hW7zlDy8/ErUqJEdgeCOUNJ/Uq/LQIlOYG7HoYS9K07OGQoqV/xZ2p0OgzcxTOl7347XkNZrb26IR4SlK6JBTZE0reqyHNXpDzHzq5Y8XuB8uWfv/9+fwcof0n/TJC+NkopZ5XGH/XqRp+tct4p9QRlL1fYgL9PoxxKaWgs3prGaD0rMcYrpcIQlPb4pck0BrPKDVapI9tEpKxT4EtEmoSfJZHzmKRKogCNmrNRRPQerpnYllcP+KDBydoqa+UaWKpKElmvgsfpOluUomt46iyJ2NjHJKKp1d9ZZJFqcV2dFUmEK0N2ezbTPQ3Op4ZslYMWI63ZKT6gD5vdxU7tcf6WBbaMZ9qzWkR0Xcx2a7XFGx8+u+OgxTeP90PW2lanH/osvr5uy870pSVRpdhzjlz5QBZdu8EWBe+c9y0smsVwz5tW8Rmx8dVnskA74Ifu/TD5R/YOUP760+c/fPXFb99/pP+Q8TL79PrfX2Dyr+ydoPzxmx+/+fmXLz9SKD+9/v/7PjH5LlB+/eLFty+++/IfEObHIixTfNYAAAAASUVORK5CYII=">'
	ret += r'<p>※このページは1分ごとにリロードされます。</p> <a href="https://twitter.com/hakuryo_BOT">Twitter( @hakuryo_BOT )</a> </div>'
	return ret