param name string
param location string = resourceGroup().location
param tags object = {}

param appServicePlanId string
param runtimeName string
param runtimeVersion string
param appSettings object = {}

var linuxFxVersion = '${toUpper(runtimeName)}|${runtimeVersion}'

resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: name
  location: location
  tags: tags
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlanId
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      alwaysOn: true
      ftpsState: 'FtpsOnly'
      minTlsVersion: '1.2'
      pythonVersion: ''
      appCommandLine: 'python -m uvicorn main:app --host 0.0.0.0 --port 8000'
      appSettings: [for item in items(appSettings): {
        name: item.key
        value: item.value
      }]
    }
    httpsOnly: true
  }
}

output id string = appService.id
output name string = appService.name
output uri string = 'https://${appService.properties.defaultHostName}'
output identityPrincipalId string = appService.identity.principalId
