import requests

registry = 'harbor.dev.afsmtddso.com'
projectName = 'devsecops-lab'

# projectSha = 'sha256:909adc24a5bdae62298897e17db0ecf63de8b13c03bbc331f55d75fc84d8492a'
projectSha = 'sha256:5e95e5eb8be4322e3b3652d737371705e56809ed8b307ad68ec59ddebaaf60e4'
imageName = 'nginx'
url = 'https://' + registry + '/api/v2.0/projects//' + projectName + '/repositories/' + imageName +'/artifacts/' + projectSha + '/scan'
userPass = ('', '')

scanInitResp = requests.post(url, data={}, auth=userPass)

urlScanOverview = 'https://harbor.dev.afsmtddso.com/api/v2.0/projects/devsecops-lab/repositories/nginx/artifacts/sha256:5e95e5eb8be4322e3b3652d737371705e56809ed8b307ad68ec59ddebaaf60e4?with_scan_overview=true'
scanResultResp = requests.get(urlScanOverview, auth=userPass)
scanOverview = scanResultResp.json()['scan_overview']['application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0']

print(scanOverview)