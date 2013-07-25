#!/usr/bin/python
import ospi, urllib, json, web, time, datetime, thread
import xml.etree.ElementTree as etree

### Weather Forecast addon for OSPi ###

# Load json file to memory
def jload(fname):
    """Load data from a json file."""
    sfile = open('./data/'+fname+'.json', 'r')
    sdict = json.load(sfile)
    sfile.close()
    return sdict

# Get forecast from wunderground
def GetForecast(): 
	global High
	global Precip
	global srHour
	global srMin
	global API
	global state
	global zip
	try:
		print('Getting Forecast')
		# Get wunderground settings from json file
		settingsDict = jload('fcSettings')
		API = settingsDict['WundergroundAPIKey']
		state = settingsDict['State']
		zip = settingsDict['Zip']

		# Set wunderground urls
		urlForecast = 'http://api.wunderground.com/api/' + API + '/forecast/q/' + state + '/' + zip + '.xml'
		urlAstronomy = 'http://api.wunderground.com/api/' + API + '/astronomy/q/' + state + '/' + zip + '.xml'
		
		#Get high temp and precip from xml
		xmlForecast = urllib.urlopen(urlForecast)    
		treeTempSource = etree.parse(xmlForecast)
		rootTempSource = treeTempSource.getroot()
		elemSourceHigh = rootTempSource.find('forecast/simpleforecast/forecastdays/forecastday[1]/high/fahrenheit')
		High = elemSourceHigh.text
		elemSourcePrecip = rootTempSource.find('forecast/simpleforecast/forecastdays/forecastday[1]/qpf_allday/in')
		Precip = elemSourcePrecip.text

		#Get sunrise hour and minute from xml
		xmlAstronomy = urllib.urlopen(urlAstronomy)
		treeSunSource = etree.parse(xmlAstronomy)
		rootSunSource = treeSunSource.getroot()
		elemHourSource = rootSunSource.find('moon_phase/sunrise/hour')
		srHour = elemHourSource.text
		elemMinSource = rootSunSource.find('moon_phase/sunrise/minute')
		srMin = elemMinSource.text
	except urllib.HTTPError, e:
		print('HTTPError = ' + str(e.code))
	except urllib.URLError, e:
		print('URLError = ' + str(e.reason))
	except httplib.HTTPException, e:
		print('HTTPException')
	except Exception:
		import traceback
		print('generic exception: ' + traceback.format_exc())

def load_rules():
    #Load rules data from json file into memory."""
    global rdict
    try:
	with open('./data/fcRules.json'):
	    pass
    except IOError:
		data = { "rules": [] }
		ospi.jsave(data, 'fcRules')

    rfile = open('./data/fcRules.json', 'r')
    rdict = json.load(rfile)
    rfile.close()
    return rdict

def load_rule(rid):
    #Load specified rule from json file into memory
    rdict = load_rules()
    iIndex = 0
    for rule in rdict['rules']:
		if int(rule['rid']) == int(rid):
			outRule = rule
    return str(convert(outRule)).replace("'", '"')

# Convert dictionaries from unicode to string
def convert(input):
    if isinstance(input, dict):
	return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
	return [convert(element) for element in input]
    elif isinstance(input, unicode):
	return input.encode('utf-8')
    else:
	return input

# Enable/Disable programs based on rules and forecast
def EditProgram():
    global pdict
    global High
    global Precip
    try:
		pdict = ospi.load_programs() #load program file to memory
		rdict = load_rules() #load rules file to memory
		
		#Loop through each rule, and enable/disable programs as configured
		for rule in rdict['rules']:
			#Enable/Disable programs based on Temperature rules
			if str(rule['type']) == 'Temperature' and rule['enabled'] == 'true':
				if rule['eval'] == '>' and int(High) >= int(rule['thresh']):
					if rule['action'] == 'Enable':
						print('Enable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 1
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
					elif rule['action'] == 'Disable':
						print('Disable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 0
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
				elif rule['eval'] == '<' and int(High) <= int(rule['thresh']):
					if rule['action'] == 'Enable':
						print('Enable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 1
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
					elif rule['action'] == 'Disable':
						print('Disable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 0
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
			#Enable/Disable programs based on Precip rules
			elif str(rule['type']) == 'Precip' and rule['enabled'] == 'true':
				if rule['eval'] == '>' and float(Precip) >= float(rule['thresh']):
					print('Precip > ', str(rule['thresh']))
					if rule['action'] == 'Enable':
						print('Enable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 1
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
					elif rule['action'] == 'Disable':
						print('Disable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 0
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
				if rule['eval'] == '<' and float(Precip) <= float(rule['thresh']):
					if rule['action'] == 'Enable':
						print('Enable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 1
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
					elif rule['action'] == 'Disable':
						print('Disable Program ', str(rule['prog']))
						mp = pdict[int(rule['prog'])]
						mp[0] = 0
						pdict[int(rule['prog'])] = mp
						ospi.jsave(pdict, 'programs')
    except:
		pass
#Loop for getting new forecast data and applying rules
# loops every 60 seconds, but only gets forecast and applies rules at configured time
def ForecastLoop():
    while True:
        try:
			global RunHour
			global RunMinute
			now = datetime.datetime.now()
			midnight = now.replace(hour=0,minute=0,second=0,microsecond=0)
			stripTimeNow = now.replace(second=0,microsecond=0)

			#Get Forecast at set time, and edit programs accordingly
			getForecastTime = midnight + datetime.timedelta(hours=int(RunHour), minutes=int(RunMinute))
			if stripTimeNow == getForecastTime:
				GetForecast() #Run GetForecast function to get current forecast data
				EditProgram() 
				print('editting programs according to rules')
				print(now)
        except:
            pass
	now = datetime.datetime.now()
	nowSecond = int(now.second)
	if nowSecond != 0:
	    time.sleep(60-nowSecond)
	else:
		time.sleep(60)

#start a new thread for looping
thread.start_new_thread(ForecastLoop, ())

# Get Forecast when ospi starts
GetForecast()

#run Edit program (testing only)
EditProgram()

### Custom Classes ####
class view_forecastSettings:
## View forecast settings
    def GET(self):
		# Get wunderground settings from json file
		settingsDict = jload('fcSettings')
		runtimeHr = settingsDict['RuntimeHr']
		runtimeMin = settingsDict['RuntimeMin']
		wgKey = settingsDict['WundergroundAPIKey']
		state = settingsDict['State']
		zip = settingsDict['Zip']
		custpg = '<!DOCTYPE html>\n'
		custpg += '<script >var baseurl=\"'+ ospi.baseurl()+'\"</script>\n'
		custpg += '<script >var api="' + wgKey + '",state="' + state + '",zip=' + str(zip) + ',runtimehr=' + str(runtimeHr) + ',runtimemin=' + str(runtimeMin) + ';</script>\n'
		custpg += '<script type="text/javascript" src="/static/scripts/java/svc1.8/forecastSettings.js"></script>\n'
		return custpg

class change_forecastSettings:
## Commit changes to forecast settings (no display)
    def GET(self):
	# Declare global variables
        global rdict
        global RunHour
        global RunMinute

	# load dictionaries
	qdict = web.input()

	# Save new runtime to global variables
	RunHour = qdict['RuntimeHr']
	RunMinute = qdict['RuntimeMin']
	
	# Save query dictionary to fcSettings.json file
	ospi.jsave(qdict, 'fcSettings')

	# re-direct
	raise web.seeother('/vfc')
	return   

class view_forecastRules:
## view forecast rules
    def GET(self):
	global High
	global Precip
        custpg = '<!DOCTYPE html>\n'
        custpg += '<script >var baseurl=\"'+ ospi.baseurl()+'\"</script>\n'
        custpg += '<script >var hi=' + High + ',pre=' + Precip +';</script>\n'
        custpg += '<script type="text/javascript" src="/static/scripts/java/svc1.8/viewForecastRules.js"></script>'
        rdict = load_rules()
        for rule in rdict['rules']:
		if rule['enabled'] == 'true':
			custpg += '<p><b>Rule ' + str(int(rule['rid'])) +'</b><br />'
		else:
			custpg += '<b><strike>Rule ' + str(int(rule['rid'])) + '</strike> (Disabled)</b><br />'
		custpg += 'If ' + rule['type'] + ' ' + rule['eval'] + ' ' + str(rule['thresh']) + '<br />'
		custpg += 'Then ' + rule['action'] + ' Program ' + str((int(rule['prog'])+1)) + '<br />'
		custpg += '<button style=\"height:20\" onclick=\"mod(mfc, ' + str(rule['rid']) + ')\"><b>Edit</b></button>'
		custpg += '<button style=\"height:20\" onclick=\"mod(dfc, ' + str(rule['rid']) + ')\"><b>Delete</b></button><hr></p>'
	return custpg
		

class modify_forecastRule:
## Modify selected rule or add new rule
    def GET(self):
		qdict = web.input()
		rdict = load_rules()
		global High
		global Precip
		global srHour
		global srMin
        
		custpg = '<!DOCTYPE html>\n'
		custpg += '<script >function id(s){return document.getElementById(s);}</script>\n'
		custpg += '<script >var baseurl=\"'+ ospi.baseurl()+'\"</script>\n'
		custpg += '<script >'+ospi.output_prog()+'</script>\n'
		custpg += '<script >var rid=' + qdict['rid']
		if int(qdict['rid']) > -1:
			custpg += ',rule=' + str(load_rule(qdict['rid'])) +';</script>\n'
		else:
			custpg += ',rule=[];</script>\n'
		custpg += '<script >var hi=' + High + ',pre=' + Precip +',srh=' + srHour + ',srm=' + srMin + ',rid=' + qdict['rid'] + ';</script>\n'
		custpg += '<script src=\"' + ospi.baseurl() + '/static/scripts/java/svc1.8/modForecastRules.js\"></script>'
		return custpg

class change_forecastRule:
## Commit changes to forecast rule (no display)
    def GET(self):
		global rdict
		rdict = load_rules()
		qdict = web.input()
		if str(qdict['enabled']) == 'on':
			qdict['enabled'] = 'true'
		#add new rule
		if str(qdict['rid']) == '-1':
			iRid = 0
			for rule in rdict['rules']:
				if int(rule['rid']) > iRid:
					iRid = int(rule['rid'])
			qdict['rid'] = iRid + 1
			rdict['rules'].append(qdict)
		#replace existing rule
		else:
			iIndex = 0
			for rule in rdict['rules']:
				if int(rule['rid']) == int(qdict['rid']):
					rdict['rules'][iIndex] = qdict
				iIndex += 1
		ospi.jsave(rdict, 'fcRules')
		raise web.seeother('/vfc')
		return   
        
class delete_forecastRules:
## delete selected rule (no display)
    def GET(self):
		rdict = load_rules()
		qdict = web.input()
		
		#delete all rules
		if str(qdict['rid']) == '-1':
			del rdict['rules'][:]
			ospi.jsave(rdict, 'fcRules')
		#delete selected rule
		else:
			iIndex = 0
			for rule in rdict['rules']:
				if int(rule['rid']) == int(qdict['rid']):
					del rdict['rules'][iIndex]
				iIndex += 1
		ospi.jsave(rdict, 'fcRules')
		raise web.seeother('/vfc')
		return 

