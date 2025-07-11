param name string
param location string = resourceGroup().location
param tags object = {}
param kind string = 'OpenAI'
param sku object = { name: 'S0' }
param deployments array = []

resource account 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  kind: kind
  properties: {
    customSubDomainName: name
    networkAcls: {
      defaultAction: 'Allow'
    }
    publicNetworkAccess: 'Enabled'
  }
  sku: sku
}

@batchSize(1)
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = [for deployment in deployments: {
  parent: account
  name: deployment.name
  properties: {
    model: deployment.model
    raiPolicyName: deployment.?raiPolicyName
  }
  sku: deployment.?sku ?? {
    name: 'GlobalStandard'
    capacity: 250
  }
}]

output endpoint string = account.properties.endpoint
output id string = account.id
output name string = account.name
