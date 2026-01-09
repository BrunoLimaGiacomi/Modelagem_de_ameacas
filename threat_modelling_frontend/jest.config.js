// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/
//
// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

/**
 * Jest testing configuration que defines test environment e TypeScript transform 
 * para frontend CDK infrastructure testing.
 */
module.exports = {
  testEnvironment: "node",
  roots: ["<rootDir>/test"],
  testMatch: ["**/*.test.ts"],
  transform: {
    "^.+\\.tsx?$": "ts-jest",
  },
};
