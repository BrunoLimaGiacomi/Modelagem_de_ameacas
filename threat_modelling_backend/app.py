# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
#
# A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
# para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

#!/usr/bin/env python3

import aws_cdk as cdk

from backend.backend_stack import BackendStack

from cdk_nag import AwsSolutionsChecks


app = cdk.App()
BackendStack(app, "BackendStack")

cdk.Aspects.of(app).add(AwsSolutionsChecks())

app.synth()
