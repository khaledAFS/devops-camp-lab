import requests, time, sys, json

## Arguments needed from user ##
userPass = ('', '')
registry = 'harbor.dev.afsmtddso.com'
projectName = 'devsecops-lab'
imageName = 'nginx'

## Grab sha256 digest from Harbor project repository ##
urlBase = 'https://' + registry + '/api/v2.0/projects/' + projectName + '/repositories/' + imageName + '/artifacts/'
digestResp = requests.get(urlBase, auth=userPass)
projectSha = digestResp.json()[0]['digest']

## Initialize image scanner ##
urlScanInit = urlBase + projectSha + '/scan'
scanInitResp = requests.post(urlScanInit, data={}, auth=userPass)

## Checks scanner status ##
urlScanOverview = urlBase + projectSha + '?with_scan_overview=true'
scanStatus = 'Pending'
maxApiCall = 5

while scanStatus != 'Success':
    scanOverviewResp = requests.get(urlScanOverview, auth=userPass)
    scanOverviewResult = scanOverviewResp.json()['scan_overview']['application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0']
    scanStatus = scanOverviewResult['scan_status']
    print(scanStatus)
    if scanStatus == 'Success':
        break
    elif maxApiCall <= 0:
        print('Reached maximum API calls')
        sys.exit(-1)
    else:
        maxApiCall -= 1
        time.sleep(4)

print(json.dumps(scanOverviewResult['summary'], indent=4))