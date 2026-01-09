// Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/
//
// A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
// para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import { useLoaderData, Await } from "react-router-dom";
import { Suspense } from "react";

import { Skeleton } from "@/components/ui/skeleton";

type ItemsData = {
  /**
   * Items data type que defines structure for API response data 
   * para home page content rendering.
   */
  items: Record<string, string>[];
};

export default function Home() {
  /**
   * Home page component que displays sample API data rendering 
   * with suspense loading e error handling para demonstration purposes.
   */
  const loaderData = useLoaderData() as ItemsData;

  return (
    <Suspense fallback={<Skeleton />}>
      <Await resolve={loaderData.items} errorElement={<p>Error</p>}>
        {(loadedData) => (
          <div>
            <p>This is a sample rendering with items fetched from an API:</p>
            <pre className="whitespace-pre-wrap rounded-md border border-orange-400 bg-orange-100 p-2 text-xs text-orange-950">
              {JSON.stringify(loadedData, null, 2)}
            </pre>
          </div>
        )}
      </Await>
    </Suspense>
  );
}
