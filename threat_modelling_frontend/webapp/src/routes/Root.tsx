// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/
//
// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import { Outlet } from "react-router-dom";
import { NavBar } from "@/components/ui/navbar";
import { TooltipProvider } from "@/components/ui/tooltip";

export const HeaderGradient: React.FC = () => {
  /**
   * Constant definition que provides configuration values para application settings e constants.
   */
  return (
    <div className="absolute inset-0 -z-10 mx-0 max-w-none overflow-hidden">
      <div className="absolute left-1/2 top-0 ml-[-38rem] h-[25rem] w-[81.25rem]">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 via-purple-600/30 to-indigo-500/20 [mask-image:radial-gradient(farthest-side_at_top,white,transparent)] blur-3xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-purple-400/10 to-transparent [mask-image:radial-gradient(circle_at_center,white,transparent)]"></div>
      </div>
    </div>
  );
};

export default function Root() {
  return (
    <>
      <TooltipProvider>
        <NavBar />
        <HeaderGradient />
        <main className="container mx-auto mt-4">
          <Outlet />
        </main>
      </TooltipProvider>
    </>
  );
}
