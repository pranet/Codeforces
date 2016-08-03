# Will print the list of problems (by name) which a user solved in group but not in regular mode
import urllib
import json
import time
import hashlib

# http://codeforces.com/settings/api
username = "pranet"
key = ""
secret = ""

# Get all AC submissions with contest ID in specified range
def getACs(data, lo, high):
	unique = set()
	for x in data:
		if x['verdict'] == 'OK':
			contestId = int(x['author']['contestId'])
			problemName = x['problem']['name']
			if lo <= contestId and contestId <= high:
				unique.add(problemName)
	return unique

# http://codeforces.com/api/help
def generateURL():
	tim = str(int(time.time()))
	rand = str(123456)
	baseURL = "http://codeforces.com/api/"
	methodName = "user.status"

	hashString = rand + "/" + methodName + "?"
	hashString += "apiKey=" + key
	hashString += "&handle=" + username 
	hashString += "&time=" + tim
	hashString += "#" + secret

	apiSig = rand + hashlib.sha512(hashString).hexdigest()
	url = baseURL + methodName + "?handle=" + username + "&apiKey=" + key + "&time=" + tim + "&apiSig=" + apiSig
	return url

def run():
	response = urllib.urlopen(generateURL())
	data = json.loads(response.read())
	data =  data['result']
	regularSolved = getACs(data, 0, 1000)
	gymSolved = getACs(data, 200000, 200000000)
	for problem in gymSolved:
		if problem not in regularSolved:
			print problem

if __name__ == '__main__':
	run()