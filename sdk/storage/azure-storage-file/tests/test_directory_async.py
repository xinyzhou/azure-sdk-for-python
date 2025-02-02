# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest
import asyncio
from datetime import timedelta

from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
from azure.core.pipeline.transport import AioHttpTransport
from multidict import CIMultiDict, CIMultiDictProxy
from azure.storage.file.aio import (
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

class AiohttpTestTransport(AioHttpTransport):
    """Workaround to vcrpy bug: https://github.com/kevin1024/vcrpy/pull/461
    """
    async def send(self, request, **config):
        response = await super(AiohttpTestTransport, self).send(request, **config)
        if not isinstance(response.headers, CIMultiDictProxy):
            response.headers = CIMultiDictProxy(CIMultiDict(response.internal_response.headers))
            response.content_type = response.headers.get("content-type")
        return response


class StorageDirectoryTest(FileTestCase):
    def setUp(self):
        super(StorageDirectoryTest, self).setUp()

        url = self.get_file_url()
        credential = self.get_shared_key_credential()
        self.fsc = FileServiceClient(url, credential=credential, transport=AiohttpTestTransport())
        self.share_name = self.get_resource_name('utshare')

    def tearDown(self):
        if not self.is_playback():
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(self.fsc.delete_share(self.share_name, delete_snapshots=True))
            except:
                pass

        return super(StorageDirectoryTest, self).tearDown()

    # --Helpers-----------------------------------------------------------------
    async def _setup(self):
        if not self.is_playback():
            try:
                await self.fsc.create_share(self.share_name)
            except:
                pass

    # --Test cases for directories ----------------------------------------------
    async def _test_create_directories_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)

        # Act
        created = await share_client.create_directory('dir1')

        # Assert
        self.assertTrue(created)

    @record
    def test_create_directories_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_directories_async())

    async def _test_create_directories_with_metadata_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {'hello': 'world', 'number': '42'}

        # Act
        directory = await share_client.create_directory('dir1', metadata=metadata)

        # Assert
        props = await directory.get_directory_properties()
        self.assertDictEqual(props.metadata, metadata)

    @record
    def test_create_directories_with_metadata_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_directories_with_metadata_async())

    async def _test_create_directories_fail_on_exist_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)

        # Act
        created = await share_client.create_directory('dir1')
        with self.assertRaises(ResourceExistsError):
            await share_client.create_directory('dir1')

        # Assert
        self.assertTrue(created)

    @record
    def test_create_directories_fail_on_exist_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_directories_fail_on_exist_async())

    async def _test_create_subdirectories_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        created = await directory.create_subdirectory('dir2')

        # Assert
        self.assertTrue(created)
        self.assertEqual(created.directory_path, 'dir1/dir2')

    @record
    def test_create_subdirectories_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_subdirectories_async())

    async def _test_create_subdirectories_with_metadata_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        metadata = {'hello': 'world', 'number': '42'}

        # Act
        created = await directory.create_subdirectory('dir2', metadata=metadata)

        # Assert
        self.assertTrue(created)
        self.assertEqual(created.directory_path, 'dir1/dir2')
        properties = await created.get_directory_properties()
        self.assertEqual(properties.metadata, metadata)

    @record
    def test_create_subdirectories_with_metadata_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_subdirectories_with_metadata_async())

    async def _test_create_file_in_directory_async(self):
        # Arrange
        await self._setup()
        file_data = b'12345678' * 1024
        file_name = self.get_resource_name('file')
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        new_file = await directory.upload_file(file_name, file_data)

        # Assert
        file_content = await new_file.download_file()
        file_content = await file_content.content_as_bytes()
        self.assertEqual(file_content, file_data)

    def test_create_file_in_directory_async(self):
        if TestMode.need_recording_file(self.test_mode):
            return
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_file_in_directory_async())

    async def _test_delete_file_in_directory_async(self):
        # Arrange
        await self._setup()
        file_name = self.get_resource_name('file')
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        new_file = await directory.upload_file(file_name, "hello world")

        # Act
        deleted = await directory.delete_file(file_name)

        # Assert
        self.assertIsNone(deleted)
        with self.assertRaises(ResourceNotFoundError):
            await new_file.get_file_properties()

    @record
    def test_delete_file_in_directory_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_file_in_directory_async())

    async def _test_delete_subdirectories_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        await directory.create_subdirectory('dir2')

        # Act
        deleted = await directory.delete_subdirectory('dir2')

        # Assert
        self.assertIsNone(deleted)
        subdir = directory.get_subdirectory_client('dir2')
        with self.assertRaises(ResourceNotFoundError):
            await subdir.get_directory_properties()

    @record
    def test_delete_subdirectories_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_subdirectories_async())

    async def _test_get_directory_properties_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        props = await directory.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)

    @record
    def test_get_directory_properties_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_directory_properties_async())

    async def _test_get_directory_properties_with_snapshot_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {"test1": "foo", "test2": "bar"}
        directory = await share_client.create_directory('dir1', metadata=metadata)
        snapshot1 = await share_client.create_snapshot()
        metadata2 = {"test100": "foo100", "test200": "bar200"}
        await directory.set_directory_metadata(metadata2)

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot1)
        snap_dir = share_client.get_directory_client('dir1')
        props = await snap_dir.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)
        self.assertDictEqual(metadata, props.metadata)

    @record
    def test_get_directory_properties_with_snapshot_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_directory_properties_with_snapshot_async())

    async def _test_get_directory_metadata_with_snapshot_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        metadata = {"test1": "foo", "test2": "bar"}
        directory = await share_client.create_directory('dir1', metadata=metadata)
        snapshot1 = await share_client.create_snapshot()
        metadata2 = {"test100": "foo100", "test200": "bar200"}
        await directory.set_directory_metadata(metadata2)

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot1)
        snap_dir = share_client.get_directory_client('dir1')
        snapshot_props = await snap_dir.get_directory_properties()

        # Assert
        self.assertIsNotNone(snapshot_props.metadata)
        self.assertDictEqual(metadata, snapshot_props.metadata)

    @record
    def test_get_directory_metadata_with_snapshot_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_directory_metadata_with_snapshot_async())

    async def _test_get_directory_properties_with_non_existing_directory_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            await directory.get_directory_properties()

            # Assert

    @record
    def test_get_directory_properties_with_non_existing_directory_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_directory_properties_with_non_existing_directory_async())

    async def _test_directory_exists_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        exists = await directory.get_directory_properties()

        # Assert
        self.assertTrue(exists)

    @record
    def test_directory_exists_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_directory_exists_async())

    async def _test_directory_not_exists_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            await directory.get_directory_properties()

        # Assert

    @record
    def test_directory_not_exists_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_directory_not_exists_async())

    async def _test_directory_parent_not_exists_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('missing1/missing2')

        # Act
        with self.assertRaises(ResourceNotFoundError) as e:
            await directory.get_directory_properties()

        # Assert
        self.assertEqual(e.exception.error_code, StorageErrorCode.parent_not_found)

    @record
    def test_directory_parent_not_exists_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_directory_parent_not_exists_async())

    async def _test_directory_exists_with_snapshot_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        snapshot = await share_client.create_snapshot()
        await directory.delete_directory()

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snap_dir = share_client.get_directory_client('dir1')
        exists = await snap_dir.get_directory_properties()

        # Assert
        self.assertTrue(exists)

    @record
    def test_directory_exists_with_snapshot_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_directory_exists_with_snapshot_async())

    async def _test_directory_not_exists_with_snapshot_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        snapshot = await share_client.create_snapshot()
        directory = await share_client.create_directory('dir1')

        # Act
        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snap_dir = share_client.get_directory_client('dir1')

        with self.assertRaises(ResourceNotFoundError):
            await snap_dir.get_directory_properties()

        # Assert

    @record
    def test_directory_not_exists_with_snapshot_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_directory_not_exists_with_snapshot_async())

    async def _test_get_set_directory_metadata_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        metadata = {'hello': 'world', 'number': '43'}

        # Act
        await directory.set_directory_metadata(metadata)
        props = await directory.get_directory_properties()

        # Assert
        self.assertDictEqual(props.metadata, metadata)

    @record
    def test_get_set_directory_metadata_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_set_directory_metadata_async())

    async def _test_set_directory_properties_with_empty_smb_properties(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory_client = await share_client.create_directory('dir1')
        directory_properties_on_creation = await directory_client.get_directory_properties()

        # Act
        await directory_client.set_http_headers()
        directory_properties = await directory_client.get_directory_properties()

        # Assert
        # Make sure set empty smb_properties doesn't change smb_properties
        self.assertEquals(directory_properties_on_creation.creation_time,
                          directory_properties.creation_time)
        self.assertEquals(directory_properties_on_creation.last_write_time,
                          directory_properties.last_write_time)
        self.assertEquals(directory_properties_on_creation.permission_key,
                          directory_properties.permission_key)

    @record
    def test_set_directory_properties_with_empty_smb_properties_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_directory_properties_with_empty_smb_properties())

    async def _test_set_directory_properties_with_file_permission_key(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory_client = await share_client.create_directory('dir1')

        directory_properties_on_creation = await directory_client.get_directory_properties()
        permission_key = directory_properties_on_creation.permission_key
        last_write_time = directory_properties_on_creation.last_write_time
        creation_time = directory_properties_on_creation.creation_time

        new_last_write_time = last_write_time + timedelta(hours=1)
        new_creation_time = creation_time + timedelta(hours=1)

        # Act
        await directory_client.set_http_headers(file_attributes='None', file_creation_time=new_creation_time,
                                                file_last_write_time=new_last_write_time,
                                                file_permission_key=permission_key)
        directory_properties = await directory_client.get_directory_properties()

        # Assert
        self.assertIsNotNone(directory_properties)
        self.assertEquals(directory_properties.creation_time, new_creation_time)
        self.assertEquals(directory_properties.last_write_time, new_last_write_time)

    @record
    def test_set_directory_properties_with_file_permission_key_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_directory_properties_with_file_permission_key())

    async def _test_list_subdirectories_and_files_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        await asyncio.gather(
            directory.create_subdirectory("subdir1"),
            directory.create_subdirectory("subdir2"),
            directory.create_subdirectory("subdir3"),
            directory.upload_file("file1", "data1"),
            directory.upload_file("file2", "data2"),
            directory.upload_file("file3", "data3"))

        # Act
        list_dir = []
        async for d in directory.list_directories_and_files():
            list_dir.append(d)

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
    def test_list_subdirectories_and_files_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_subdirectories_and_files_async())

    async def _test_list_subdirectories_and_files_with_prefix_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        await asyncio.gather(
            directory.create_subdirectory("subdir1"),
            directory.create_subdirectory("subdir2"),
            directory.create_subdirectory("subdir3"),
            directory.upload_file("file1", "data1"),
            directory.upload_file("file2", "data2"),
            directory.upload_file("file3", "data3"))

        # Act
        list_dir = []
        async for d in directory.list_directories_and_files(name_starts_with="sub"):
            list_dir.append(d)

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'subdir2', 'is_directory': True},
            {'name': 'subdir3', 'is_directory': True},
        ]
        self.assertEqual(len(list_dir), 3)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_subdirectories_and_files_with_prefix_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_subdirectories_and_files_with_prefix_async())

    async def _test_list_subdirectories_and_files_with_snapshot_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        await asyncio.gather(
            directory.create_subdirectory("subdir1"),
            directory.create_subdirectory("subdir2"),
            directory.upload_file("file1", "data1"))
        
        snapshot = await share_client.create_snapshot()
        await asyncio.gather(
            directory.create_subdirectory("subdir3"),
            directory.upload_file("file2", "data2"),
            directory.upload_file("file3", "data3"))

        share_client = self.fsc.get_share_client(self.share_name, snapshot=snapshot)
        snapshot_dir = share_client.get_directory_client('dir1')

        # Act
        list_dir = []
        async for d in snapshot_dir.list_directories_and_files():
            list_dir.append(d)

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'subdir2', 'is_directory': True},
            {'name': 'file1', 'is_directory': False, 'size': 5},
        ]
        self.assertEqual(len(list_dir), 3)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_subdirectories_and_files_with_snapshot_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_subdirectories_and_files_with_snapshot_async())

    async def _test_list_nested_subdirectories_and_files_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')
        subdir = await directory.create_subdirectory("subdir1")
        await subdir.create_subdirectory("subdir2")
        await subdir.create_subdirectory("subdir3")
        await asyncio.gather(
            directory.upload_file("file1", "data1"),
            subdir.upload_file("file2", "data2"),
            subdir.upload_file("file3", "data3"))

        # Act
        list_dir = []
        async for d in directory.list_directories_and_files():
            list_dir.append(d)

        # Assert
        expected = [
            {'name': 'subdir1', 'is_directory': True},
            {'name': 'file1', 'is_directory': False, 'size': 5},
        ]
        self.assertEqual(len(list_dir), 2)
        self.assertEqual(list_dir, expected)

    @record
    def test_list_nested_subdirectories_and_files_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_nested_subdirectories_and_files_async())

    async def _test_delete_directory_with_existing_share_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        deleted = await directory.delete_directory()

        # Assert
        self.assertIsNone(deleted)
        with self.assertRaises(ResourceNotFoundError):
            await directory.get_directory_properties()

    @record
    def test_delete_directory_with_existing_share_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_directory_with_existing_share_async())

    async def _test_delete_directory_with_non_existing_directory_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = share_client.get_directory_client('dir1')

        # Act
        with self.assertRaises(ResourceNotFoundError):
            await directory.delete_directory()

        # Assert

    @record
    def test_delete_directory_with_non_existing_directory_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_directory_with_non_existing_directory_async())

    async def _test_get_directory_properties_server_encryption_async(self):
        # Arrange
        await self._setup()
        share_client = self.fsc.get_share_client(self.share_name)
        directory = await share_client.create_directory('dir1')

        # Act
        props = await directory.get_directory_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertIsNotNone(props.etag)
        self.assertIsNotNone(props.last_modified)

        if self.is_file_encryption_enabled():
            self.assertTrue(props.server_encrypted)
        else:
            self.assertFalse(props.server_encrypted)

    @record
    def test_get_directory_properties_server_encryption_async(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_directory_properties_server_encryption_async())

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
