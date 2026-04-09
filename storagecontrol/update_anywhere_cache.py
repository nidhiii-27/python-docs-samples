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

from google.cloud import storage_control_v2
from google.protobuf import field_mask_pb2

# [START storage_control_update_anywhere_cache]


def update_anywhere_cache(
    bucket_name: str, zone: str, admission_policy: str = "ADMIT_ON_FIRST_MISS"
) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The zone of the Anywhere Cache
    # zone = "us-central1-a"

    # The new admission policy for the Anywhere Cache
    # admission_policy = "ADMIT_ON_FIRST_MISS"

    client = storage_control_v2.StorageControlClient()

    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = client.common_project_path("_")
    name = f"{project_path}/buckets/{bucket_name}/anywhereCaches/{zone}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        name=name,
        admission_policy=admission_policy,
    )

    update_mask = field_mask_pb2.FieldMask(paths=["admission_policy"])

    request = storage_control_v2.UpdateAnywhereCacheRequest(
        anywhere_cache=anywhere_cache,
        update_mask=update_mask,
    )

    # update_anywhere_cache is a long-running operation.
    # Real applications may want to setup a callback or poll for the operation to complete.
    operation = client.update_anywhere_cache(request=request)
    response = operation.result()

    print(f"Updated Anywhere Cache: {response.name}")
    print(f"New Admission Policy: {response.admission_policy}")


# [END storage_control_update_anywhere_cache]


if __name__ == "__main__":
    update_anywhere_cache(
        bucket_name=sys.argv[1], zone=sys.argv[2], admission_policy=sys.argv[3]
    )
