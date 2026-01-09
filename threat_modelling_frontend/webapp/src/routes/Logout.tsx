// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/
//
// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import { useAuthenticator } from "@aws-amplify/ui-react";
import { Navigate } from "react-router";

export function Logout() {
  /**
   * Utility function que provides helper functionality para application components e services.
   */
  const { signOut } = useAuthenticator((context) => [context.route]);
  signOut();

  return <Navigate to={"/login"} replace />;
}
