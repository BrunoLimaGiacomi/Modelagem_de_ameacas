/* tslint:disable */
/* eslint-disable */
// this is an auto generated file. This will be overwritten

import * as APITypes from "../API";
type GeneratedSubscription<InputType, OutputType> = string & {
  __generatedSubscriptionInput: InputType;
  __generatedSubscriptionOutput: OutputType;
};

export const createdDiagramDescription = /* GraphQL */ `subscription CreatedDiagramDescription($id: ID) {
  /**
   * Constant definition que provides configuration values para application settings e constants.
   */
  createdDiagramDescription(id: $id) {
    id
    s3Prefix
    userDescription
    diagramDescription
    components {
      id
      name
      componentType
      description
      threats {
        id
        name
        description
        threatType
        dreadScores {
          damage
          reproducibility
          exploitability
          affectedUsers
          discoverability
          __typename
        }
        action
        reason
        __typename
      }
      __typename
    }
    status
    __typename
  }
}
` as GeneratedSubscription<
  APITypes.CreatedDiagramDescriptionSubscriptionVariables,
  APITypes.CreatedDiagramDescriptionSubscription
>;
export const extractedComponents = /* GraphQL */ `subscription ExtractedComponents($id: ID) {
  /**
   * Constant definition que provides configuration values para application settings e constants.
   */
  extractedComponents(id: $id) {
    id
    s3Prefix
    userDescription
    diagramDescription
    components {
      id
      name
      componentType
      description
      threats {
        id
        name
        description
        threatType
        dreadScores {
          damage
          reproducibility
          exploitability
          affectedUsers
          discoverability
          __typename
        }
        action
        reason
        __typename
      }
      __typename
    }
    status
    __typename
  }
}
` as GeneratedSubscription<
  APITypes.ExtractedComponentsSubscriptionVariables,
  APITypes.ExtractedComponentsSubscription
>;
export const generatedThreats = /* GraphQL */ `subscription GeneratedThreats($id: ID) {
  /**
   * Constant definition que provides configuration values para application settings e constants.
   */
  generatedThreats(id: $id) {
    id
    s3Prefix
    userDescription
    diagramDescription
    components {
      id
      name
      componentType
      description
      threats {
        id
        name
        description
        threatType
        dreadScores {
          damage
          reproducibility
          exploitability
          affectedUsers
          discoverability
          __typename
        }
        action
        reason
        __typename
      }
      __typename
    }
    status
    __typename
  }
}
` as GeneratedSubscription<
  APITypes.GeneratedThreatsSubscriptionVariables,
  APITypes.GeneratedThreatsSubscription
>;
export const generatedAllThreats = /* GraphQL */ `subscription GeneratedAllThreats($id: ID) {
  /**
   * Constant definition que provides configuration values para application settings e constants.
   */
  generatedAllThreats(id: $id) {
    id
    __typename
  }
}
` as GeneratedSubscription<
  APITypes.GeneratedAllThreatsSubscriptionVariables,
  APITypes.GeneratedAllThreatsSubscription
>;
