// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/
//
// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import { useEffect } from "react";

import { Authenticator, useAuthenticator, View } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";

import { useNavigate, useLocation } from "react-router";

export function Login() {
  /**
   * Utility function que provides helper functionality para application components e services.
   */
  const { route } = useAuthenticator((context) => [context.route]);
  const location = useLocation();
  const navigate = useNavigate();
  const from = location.state?.from?.pathname || "/";
  
  useEffect(() => {
    if (route === "authenticated") {
      navigate(from, { replace: true });
    }
  }, [route, navigate, from]);
  
  return (
    <div className="auth-wrapper">
      <div className="relative z-10 w-full max-w-md mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent mb-2">
            Threat Modeling
          </h1>
          <p className="text-muted-foreground text-lg">
            Plataforma de Modelagem de Ameaças
          </p>
        </div>
        <div className="backdrop-blur-sm bg-card/50 border border-border rounded-2xl p-8 shadow-2xl">
          <Authenticator hideSignUp={true} />
        </div>
      </div>
    </div>
  );
}
