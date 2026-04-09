# Copyright 2024 Google LLC
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

from google.cloud import storage

import pytest

import create_anywhere_cache
import create_folder
import delete_folder
import disable_anywhere_cache
import get_anywhere_cache
import get_folder
import list_anywhere_cache
import list_folders
import managed_folder_create
import managed_folder_delete
import managed_folder_get
import managed_folder_list
import pause_anywhere_cache
import rename_folder
import resume_anywhere_cache
import update_anywhere_cache

# === Folders === #


def test_folder_create_get_list_rename_delete(
    capsys: pytest.LogCaptureFixture, hns_enabled_bucket: storage.Bucket, uuid_name: str
) -> None:
    bucket_name = hns_enabled_bucket.name
    folder_name = uuid_name

    # Test create folder
    create_folder.create_folder(bucket_name=bucket_name, folder_name=folder_name)
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test get folder
    get_folder.get_folder(bucket_name=bucket_name, folder_name=folder_name)
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test list folders
    list_folders.list_folders(bucket_name=bucket_name)
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test rename folder
    new_name = f"new-name-{uuid_name}"
    rename_folder.rename_folder(
        bucket_name=bucket_name,
        source_folder_name=folder_name,
        destination_folder_name=new_name,
    )
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test delete folder
    delete_folder.delete_folder(bucket_name=bucket_name, folder_name=new_name)
    out, _ = capsys.readouterr()
    assert new_name in out


# === Anywhere Cache === #


def test_anywhere_cache_create_get_list_update_pause_resume_disable(
    capsys: pytest.LogCaptureFixture,
    ubla_enabled_bucket: storage.Bucket,
) -> None:
    bucket_name = ubla_enabled_bucket.name
    zone = "us-central1-a"

    # Test create anywhere cache
    create_anywhere_cache.create_anywhere_cache(
        bucket_name=bucket_name, zone=zone, admission_policy="ADMIT_ON_FIRST_MISS"
    )
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out

    # Test get anywhere cache
    get_anywhere_cache.get_anywhere_cache(bucket_name=bucket_name, zone=zone)
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out
    assert "ADMIT_ON_FIRST_MISS" in out

    # Test list anywhere caches
    list_anywhere_cache.list_anywhere_caches(bucket_name=bucket_name)
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out

    # Test update anywhere cache
    update_anywhere_cache.update_anywhere_cache(
        bucket_name=bucket_name, zone=zone, admission_policy="ADMIT_ON_FIRST_MISS"
    )
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out
    assert "ADMIT_ON_FIRST_MISS" in out

    # Test pause anywhere cache
    pause_anywhere_cache.pause_anywhere_cache(bucket_name=bucket_name, zone=zone)
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out

    # Test resume anywhere cache
    resume_anywhere_cache.resume_anywhere_cache(bucket_name=bucket_name, zone=zone)
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out

    # Test disable anywhere cache
    disable_anywhere_cache.disable_anywhere_cache(bucket_name=bucket_name, zone=zone)
    out, _ = capsys.readouterr()
    assert f"buckets/{bucket_name}/anywhereCaches/{zone}" in out


# === Managed Folders === #


def test_managed_folder_create_get_list_delete(
    capsys: pytest.LogCaptureFixture,
    ubla_enabled_bucket: storage.Bucket,
    uuid_name: str,
) -> None:
    bucket_name = ubla_enabled_bucket.name
    folder_name = uuid_name

    # Test create managed folder
    managed_folder_create.create_managed_folder(
        bucket_name=bucket_name, managed_folder_id=folder_name
    )
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test get managed folder
    managed_folder_get.get_managed_folder(
        bucket_name=bucket_name, managed_folder_id=folder_name
    )
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test list managed folders
    managed_folder_list.list_managed_folders(bucket_name=bucket_name)
    out, _ = capsys.readouterr()
    assert folder_name in out

    # Test delete managed folder
    managed_folder_delete.delete_managed_folder(
        bucket_name=bucket_name, managed_folder_id=folder_name
    )
    out, _ = capsys.readouterr()
    assert folder_name in out
