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


def create_anywhere_cache(bucket_name: str, zone: str) -> None:
    """Creates an Anywhere Cache."""
    # bucket_name = "your-unique-bucket-name"
    # zone = "us-central1-a"

    client = storage_control_v2.StorageControlClient()

    # The resource name of the bucket
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    parent = f"projects/_/buckets/{bucket_name}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        admission_policy=storage_control_v2.AnywhereCache.AdmissionPolicy.ADMIT_ON_FIRST_MISS,  # noqa: E501
    )

    request = storage_control_v2.CreateAnywhereCacheRequest(
        parent=parent,
        anywhere_cache=anywhere_cache,
        anywhere_cache_id=zone,
    )

    # Start an operation and block until it completes.
    # Real applications may want to setup a callback, wait on a coroutine, or
    # poll until it completes.
    operation = client.create_anywhere_cache(request=request)
    response = operation.result()

    print(f"Anywhere Cache created: {response.name}")


# [END storage_control_create_anywhere_cache]

if __name__ == "__main__":
    create_anywhere_cache(bucket_name=sys.argv[1], zone=sys.argv[2])
