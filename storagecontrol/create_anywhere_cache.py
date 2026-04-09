# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_control_create_anywhere_cache]
from google.cloud import storage_control_v2


def create_anywhere_cache(
    bucket_name: str, zone: str, admission_policy: str = "ADMIT_ON_FIRST_MISS"
) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The zone where the Anywhere Cache will be created
    # zone = "us-central1-a"

    # The admission policy for the Anywhere Cache
    # admission_policy = "ADMIT_ON_FIRST_MISS"

    client = storage_control_v2.StorageControlClient()

    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = client.common_project_path("_")
    bucket_path = f"{project_path}/buckets/{bucket_name}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        admission_policy=admission_policy,
    )

    request = storage_control_v2.CreateAnywhereCacheRequest(
        parent=bucket_path,
        anywhere_cache=anywhere_cache,
        anywhere_cache_id=zone,
    )

    # create_anywhere_cache is a long-running operation.
    # Real applications may want to setup a callback or poll for the operation to complete.
    operation = client.create_anywhere_cache(request=request)
    response = operation.result()

    print(f"Created Anywhere Cache: {response.name}")


# [END storage_control_create_anywhere_cache]


if __name__ == "__main__":
    create_anywhere_cache(
        bucket_name=sys.argv[1], zone=sys.argv[2], admission_policy=sys.argv[3]
    )
