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

import backoff
from google.api_core import exceptions

import create_anywhere_cache
import disable_anywhere_cache
import get_anywhere_cache
import list_anywhere_caches
import pause_anywhere_cache
import resume_anywhere_cache
import update_anywhere_cache


# Anywhere Cache requires a bucket with UBLA enabled.
# The zone should be a valid zone where Anywhere Cache is supported.
ZONE = "us-central1-f"


@backoff.on_exception(
    backoff.expo, exceptions.InternalServerError, max_tries=3
)
def test_anywhere_cache_operations(ubla_enabled_bucket, capsys):
    bucket_name = ubla_enabled_bucket.name

    # Create
    create_anywhere_cache.create_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache created: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # Get
    get_anywhere_cache.get_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # List
    list_anywhere_caches.list_anywhere_caches(bucket_name)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # Update
    update_anywhere_cache.update_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache updated: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # Pause
    pause_anywhere_cache.pause_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache paused: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # Resume
    resume_anywhere_cache.resume_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache resumed: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out

    # Disable
    disable_anywhere_cache.disable_anywhere_cache(bucket_name, ZONE)
    out, _ = capsys.readouterr()
    expected = (
        f"Anywhere Cache disabled: "
        f"projects/_/buckets/{bucket_name}/anywhereCaches/{ZONE}"
    )
    assert expected in out
