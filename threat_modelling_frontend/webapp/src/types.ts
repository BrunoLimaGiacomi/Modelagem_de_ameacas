// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.]
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/

// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import { Threat } from "./API";

export type ThreatWithComponentId = Omit<Threat, "__typename"> & {
  componentId: string;
};

export type ComponentThreatAction = {
  componentId: string;
  threatId: string;
  action: string;
  reason: string;
};

export enum ThreatAction {
  Mitigate = "Mitigate",
  Avoid = "Avoid",
  Transfer = "Transfer",
  AcceptIgnore = "AcceptIgnore",
  NotApplicable = "NotApplicable",
}
