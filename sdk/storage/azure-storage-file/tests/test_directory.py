# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest
from datetime import timedelta

from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError

from azure.storage.file import (
    FileServiceClient,
    StorageErrorCode,
)
from filetestcase import (
    FileTestCase,
    record,
    LogCaptured,
    TestMode
)


# ------------------------------------------------------------------------------


class StorageDirectoryTest(FileTestCase):
    def setUp(self):
        super(StorageDirectoryTest, self).setUp()

        url = self.get_file_url()
        credential = self.get_shared_key_credential()
        self.fsc = FileServiceClient(url, credential=credential)
        self.share_name = self.get_resource_name('utshare')

        if not self.is_playback():
            self.fsc.create_share(self.share_name)

    def tearDown(self):
        if not self.is_playback():
            try:
                self.fsc.delete_share(self.share_name, delete_snapshots='include')
            except:
                pass

        return super(StorageDirectoryTest, self).tearDown()

    # --Helpers-----------------------------------------------------------------

    # --Test cases for directories ----------------------------------------------
    @record
    def test_create_directories(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)

        # Act
        created = share_client.create_directory('dir1')

        # Assert
        self.assertTrue(created)

    @record
    def test_create_directories_with_metadata(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {'hello': 'world', 'number': '42'}

        # Act
        directory = share_client.create_directory('dir1', metadata=metadata)

        # Assert
        md = directory.get_directory_properties().metadata
        self.assertDictEqual(md, metadata)

    @record
    def test_create_directories_fail_on_exist(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)

        # Act
        created = share_client.create_directory('dir1')
        with self.assertRaises(ResourceExistsError):
            share_client.create_directory('dir1')

        # Assert
        self.assertTrue(created)

    @record
    def test_create_subdirectories(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        created = directory.create_subdirectory('dir2')

        # Assert
        self.assertTrue(created)
        self.assertEqual(created.directory_path, 'dir1/dir2')

    @record
    def test_create_subdirectories_with_metadata(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        metadata = {'hello': 'world', 'number': '42'}

        # Act
        created = directory.create_subdirectory('dir2', metadata=metadata)

        # Assert
        self.assertTrue(created)
        self.assertEqual(created.directory_path, 'dir1/dir2')
        sub_metadata = created.get_directory_properties().metadata
        self.assertEqual(sub_metadata, metadata)

    @record
    def test_create_file_in_directory(self):
        # Arrange
        file_data = b'12345678' * 1024
        file_name = self.get_resource_name('file')
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        new_file = directory.upload_file(file_name, file_data)

        # Assert
        file_content = new_file.download_file().content_as_bytes()
        self.assertEqual(file_content, file_data)

    @record
    def test_delete_file_in_directory(self):
        # Arrange
        file_name = self.get_resource_name('file')
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        new_file = directory.upload_file(file_name, "hello world")

        # Act
        deleted = directory.delete_file(file_name)

        # Assert
        self.assertIsNone(deleted)
        with self.assertRaises(ResourceNotFoundError):
            new_file.get_file_properties()

    @record
    def test_delete_subdirectories(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        directory.create_subdirectory('dir2')

        # Act
        deleted = directory.delete_subdirectory('dir2')

        # Assert
        self.assertIsNone(deleted)
        subdir = directory.get_subdirectory_client('dir2')
        with self.assertRaises(ResourceNotFoundError):
            subdir.get_directory_properties()

    @record
    def test_get_directory_properties(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        props = directory.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)

    @record
    def test_get_directory_properties_with_snapshot(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {"test1": "foo", "test2": "bar"}
        directory = share_client.create_directory('dir1', metadata=metadata)
        snapshot1 = share_client.create_snapshot()
        metadata2 = {"test100": "foo100", "test200": "bar200"}
        directory.set_directory_metadata(metadata2)

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot1)
        snap_dir = share_client.get_directory_client('dir1')
        props = snap_dir.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)
        self.assertDictEqual(metadata, props.metadata)

    @record
    def test_get_directory_metadata_with_snapshot(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {"test1": "foo", "test2": "bar"}
        directory = share_client.create_directory('dir1', metadata=metadata)
        snapshot1 = share_client.create_snapshot()
        metadata2 = {"test100": "foo100", "test200": "bar200"}
        directory.set_directory_metadata(metadata2)

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot1)
        snap_dir = share_client.get_directory_client('dir1')
        snapshot_metadata = snap_dir.get_directory_properties().metadata

        # Assert
        self.assertIsNotNone(snapshot_metadata)
        self.assertDictEqual(metadata, snapshot_metadata)

    @record
    def test_get_directory_properties_with_non_existing_directory(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            directory.get_directory_properties()

            # Assert

    @record
    def test_directory_exists(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        exists = directory.get_directory_properties()

        # Assert
        self.assertTrue(exists)

    @record
    def test_directory_not_exists(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            directory.get_directory_properties()

        # Assert

    @record
    def test_directory_parent_not_exists(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('missing1/missing2')

        # Act
        with self.assertRaises(ResourceNotFoundError) as e:
            directory.get_directory_properties()

        # Assert
        self.assertEqual(e.exception.error_code, StorageErrorCode.parent_not_found)

    @record
    def test_directory_exists_with_snapshot(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        snapshot = share_client.create_snapshot()
        directory.delete_directory()

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snap_dir = share_client.get_directory_client('dir1')
        exists = snap_dir.get_directory_properties()

        # Assert
        self.assertTrue(exists)

    @record
    def test_directory_not_exists_with_snapshot(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        snapshot = share_client.create_snapshot()
        directory = share_client.create_directory('dir1')

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snap_dir = share_client.get_directory_client('dir1')

        with self.assertRaises(ResourceNotFoundError):
            snap_dir.get_directory_properties()

        # Assert

    @record
    def test_get_set_directory_metadata(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        metadata = {'hello': 'world', 'number': '43'}

        # Act
        directory.set_directory_metadata(metadata)
        md = directory.get_directory_properties().metadata

        # Assert
        self.assertDictEqual(md, metadata)

    @record
    def test_set_directory_properties_with_empty_smb_properties(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory_client = share_client.create_directory('dir1')
        directory_properties_on_creation = directory_client.get_directory_properties()

        # Act
        directory_client.set_http_headers()
        directory_properties = directory_client.get_directory_properties()

        # Assert
        # Make sure set empty smb_properties doesn't change smb_properties
        self.assertEquals(directory_properties_on_creation.creation_time,
                          directory_properties.creation_time)
        self.assertEquals(directory_properties_on_creation.last_write_time,
                          directory_properties.last_write_time)
        self.assertEquals(directory_properties_on_creation.permission_key,
                          directory_properties.permission_key)

    @record
    def test_set_directory_properties_with_file_permission_key(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory_client = share_client.create_directory('dir1')

        directory_properties_on_creation = directory_client.get_directory_properties()
        permission_key = directory_properties_on_creation.permission_key
        last_write_time = directory_properties_on_creation.last_write_time
        creation_time = directory_properties_on_creation.creation_time

        new_last_write_time = last_write_time + timedelta(hours=1)
        new_creation_time = creation_time + timedelta(hours=1)

        # Act
        directory_client.set_http_headers(file_attributes='None', file_creation_time=new_creation_time,
                                          file_last_write_time=new_last_write_time,
                                          file_permission_key=permission_key)
        directory_properties = directory_client.get_directory_properties()

        # Assert
        self.assertIsNotNone(directory_properties)
        self.assertEquals(directory_properties.creation_time, new_creation_time)
        self.assertEquals(directory_properties.last_write_time, new_last_write_time)

    @record
    def test_list_subdirectories_and_files(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        directory.create_subdirectory("subdir1")
        directory.create_subdirectory("subdir2")
        directory.create_subdirectory("subdir3")
        directory.upload_file("file1", "data1")
        directory.upload_file("file2", "data2")
        directory.upload_file("file3", "data3")

        # Act
        list_dir = list(directory.list_directories_and_files())

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'subdir2', 'is_directory': True},
            {'name': 'subdir3', 'is_directory': True},
            {'name': 'file1', 'is_directory': False, 'size': 5},
            {'name': 'file2', 'is_directory': False, 'size': 5},
            {'name': 'file3', 'is_directory': False, 'size': 5},
        ]
        self.assertEqual(len(list_dir), 6)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_subdirectories_and_files_with_prefix(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        directory.create_subdirectory("subdir1")
        directory.create_subdirectory("subdir2")
        directory.create_subdirectory("subdir3")
        directory.upload_file("file1", "data1")
        directory.upload_file("file2", "data2")
        directory.upload_file("file3", "data3")

        # Act
        list_dir = list(directory.list_directories_and_files(name_starts_with="sub"))

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'subdir2', 'is_directory': True},
            {'name': 'subdir3', 'is_directory': True},
        ]
        self.assertEqual(len(list_dir), 3)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_subdirectories_and_files_with_snapshot(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        directory.create_subdirectory("subdir1")
        directory.create_subdirectory("subdir2")
        directory.upload_file("file1", "data1")
        
        snapshot = share_client.create_snapshot()
        directory.create_subdirectory("subdir3")
        directory.upload_file("file2", "data2")
        directory.upload_file("file3", "data3")

        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snapshot_dir = share_client.get_directory_client('dir1')

        # Act
        list_dir = list(snapshot_dir.list_directories_and_files())

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'subdir2', 'is_directory': True},
            {'name': 'file1', 'is_directory': False, 'size': 5},
        ]
        self.assertEqual(len(list_dir), 3)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_nested_subdirectories_and_files(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')
        subdir = directory.create_subdirectory("subdir1")
        subdir.create_subdirectory("subdir2")
        subdir.create_subdirectory("subdir3")
        directory.upload_file("file1", "data1")
        subdir.upload_file("file2", "data2")
        subdir.upload_file("file3", "data3")

        # Act
        list_dir = list(directory.list_directories_and_files())

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'file1', 'is_directory': False, 'size': 5},
        ]
        self.assertEqual(len(list_dir), 2)
        self.assertEqual(list_dir, expected)

    @record
    def test_delete_directory_with_existing_share(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        deleted = directory.delete_directory()

        # Assert
        self.assertIsNone(deleted)
        with self.assertRaises(ResourceNotFoundError):
            directory.get_directory_properties()

    @record
    def test_delete_directory_with_non_existing_directory(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            directory.delete_directory()

        # Assert

    @record
    def test_get_directory_properties_server_encryption(self):
        # Arrange
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.create_directory('dir1')

        # Act
        props = directory.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)

        if self.is_file_encryption_enabled():
            self.assertTrue(props.server_encrypted)
        else:
            self.assertFalse(props.server_encrypted)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
