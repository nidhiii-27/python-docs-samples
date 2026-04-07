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

# [START storage_control_update_anywhere_cache]
from google.cloud import storage_control_v2
from google.protobuf import field_mask_pb2


def update_anywhere_cache(
    bucket_name: str, zone_name: str, admission_policy: str
) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The zone of the anywhere cache to be updated
    # zone_name = "us-central1-a"

    # The admission policy to set for the anywhere cache
    # admission_policy = "admit-on-second-miss"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = storage_control_client.common_project_path("_")
    cache_path = f"{project_path}/buckets/{bucket_name}/anywhereCaches/{zone_name}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        name=cache_path,
        admission_policy=admission_policy,
    )

    update_mask = field_mask_pb2.FieldMask(paths=["admission_policy"])

    request = storage_control_v2.UpdateAnywhereCacheRequest(
        anywhere_cache=anywhere_cache,
        update_mask=update_mask,
    )

    # Start an update operation and block until it completes. Real applications
    # may want to setup a callback, wait on a coroutine, or poll until it
    # completes.
    operation = storage_control_client.update_anywhere_cache(request=request)
    response = operation.result()

    print(f"Updated anywhere cache: {response.name}")


# [END storage_control_update_anywhere_cache]


if __name__ == "__main__":
    update_anywhere_cache(
        bucket_name=sys.argv[1], zone_name=sys.argv[2], admission_policy=sys.argv[3]
    )
