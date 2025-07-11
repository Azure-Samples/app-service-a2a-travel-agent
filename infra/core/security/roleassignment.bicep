param principalId string
param roleDefinitionId string
param openAiAccountName string

resource openAiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAiAccountName
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: openAiAccount
  name: guid(openAiAccount.id, principalId, roleDefinitionId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
