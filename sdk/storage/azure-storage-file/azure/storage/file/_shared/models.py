# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from enum import Enum


def get_enum_value(value):
    if value is None or value in ["None", ""]:
        return None
    try:
        return value.value
    except AttributeError:
        return value


class StorageErrorCode(str, Enum):

    account_already_exists = "AccountAlreadyExists"
    account_being_created = "AccountBeingCreated"
    account_is_disabled = "AccountIsDisabled"
    authentication_failed = "AuthenticationFailed"
    authorization_failure = "AuthorizationFailure"
    condition_headers_not_supported = "ConditionHeadersNotSupported"
    condition_not_met = "ConditionNotMet"
    empty_metadata_key = "EmptyMetadataKey"
    insufficient_account_permissions = "InsufficientAccountPermissions"
    internal_error = "InternalError"
    invalid_authentication_info = "InvalidAuthenticationInfo"
    invalid_header_value = "InvalidHeaderValue"
    invalid_http_verb = "InvalidHttpVerb"
    invalid_input = "InvalidInput"
    invalid_md5 = "InvalidMd5"
    invalid_metadata = "InvalidMetadata"
    invalid_query_parameter_value = "InvalidQueryParameterValue"
    invalid_range = "InvalidRange"
    invalid_resource_name = "InvalidResourceName"
    invalid_uri = "InvalidUri"
    invalid_xml_document = "InvalidXmlDocument"
    invalid_xml_node_value = "InvalidXmlNodeValue"
    md5_mismatch = "Md5Mismatch"
    metadata_too_large = "MetadataTooLarge"
    missing_content_length_header = "MissingContentLengthHeader"
    missing_required_query_parameter = "MissingRequiredQueryParameter"
    missing_required_header = "MissingRequiredHeader"
    missing_required_xml_node = "MissingRequiredXmlNode"
    multiple_condition_headers_not_supported = "MultipleConditionHeadersNotSupported"
    operation_timed_out = "OperationTimedOut"
    out_of_range_input = "OutOfRangeInput"
    out_of_range_query_parameter_value = "OutOfRangeQueryParameterValue"
    request_body_too_large = "RequestBodyTooLarge"
    resource_type_mismatch = "ResourceTypeMismatch"
    request_url_failed_to_parse = "RequestUrlFailedToParse"
    resource_already_exists = "ResourceAlreadyExists"
    resource_not_found = "ResourceNotFound"
    server_busy = "ServerBusy"
    unsupported_header = "UnsupportedHeader"
    unsupported_xml_node = "UnsupportedXmlNode"
    unsupported_query_parameter = "UnsupportedQueryParameter"
    unsupported_http_verb = "UnsupportedHttpVerb"
    append_position_condition_not_met = "AppendPositionConditionNotMet"
    blob_already_exists = "BlobAlreadyExists"
    blob_not_found = "BlobNotFound"
    blob_overwritten = "BlobOverwritten"
    blob_tier_inadequate_for_content_length = "BlobTierInadequateForContentLength"
    block_count_exceeds_limit = "BlockCountExceedsLimit"
    block_list_too_long = "BlockListTooLong"
    cannot_change_to_lower_tier = "CannotChangeToLowerTier"
    cannot_verify_copy_source = "CannotVerifyCopySource"
    container_already_exists = "ContainerAlreadyExists"
    container_being_deleted = "ContainerBeingDeleted"
    container_disabled = "ContainerDisabled"
    container_not_found = "ContainerNotFound"
    content_length_larger_than_tier_limit = "ContentLengthLargerThanTierLimit"
    copy_across_accounts_not_supported = "CopyAcrossAccountsNotSupported"
    copy_id_mismatch = "CopyIdMismatch"
    feature_version_mismatch = "FeatureVersionMismatch"
    incremental_copy_blob_mismatch = "IncrementalCopyBlobMismatch"
    incremental_copy_of_eralier_version_snapshot_not_allowed = "IncrementalCopyOfEralierVersionSnapshotNotAllowed"
    incremental_copy_source_must_be_snapshot = "IncrementalCopySourceMustBeSnapshot"
    infinite_lease_duration_required = "InfiniteLeaseDurationRequired"
    invalid_blob_or_block = "InvalidBlobOrBlock"
    invalid_blob_tier = "InvalidBlobTier"
    invalid_blob_type = "InvalidBlobType"
    invalid_block_id = "InvalidBlockId"
    invalid_block_list = "InvalidBlockList"
    invalid_operation = "InvalidOperation"
    invalid_page_range = "InvalidPageRange"
    invalid_source_blob_type = "InvalidSourceBlobType"
    invalid_source_blob_url = "InvalidSourceBlobUrl"
    invalid_version_for_page_blob_operation = "InvalidVersionForPageBlobOperation"
    lease_already_present = "LeaseAlreadyPresent"
    lease_already_broken = "LeaseAlreadyBroken"
    lease_id_mismatch_with_blob_operation = "LeaseIdMismatchWithBlobOperation"
    lease_id_mismatch_with_container_operation = "LeaseIdMismatchWithContainerOperation"
    lease_id_mismatch_with_lease_operation = "LeaseIdMismatchWithLeaseOperation"
    lease_id_missing = "LeaseIdMissing"
    lease_is_breaking_and_cannot_be_acquired = "LeaseIsBreakingAndCannotBeAcquired"
    lease_is_breaking_and_cannot_be_changed = "LeaseIsBreakingAndCannotBeChanged"
    lease_is_broken_and_cannot_be_renewed = "LeaseIsBrokenAndCannotBeRenewed"
    lease_lost = "LeaseLost"
    lease_not_present_with_blob_operation = "LeaseNotPresentWithBlobOperation"
    lease_not_present_with_container_operation = "LeaseNotPresentWithContainerOperation"
    lease_not_present_with_lease_operation = "LeaseNotPresentWithLeaseOperation"
    max_blob_size_condition_not_met = "MaxBlobSizeConditionNotMet"
    no_pending_copy_operation = "NoPendingCopyOperation"
    operation_not_allowed_on_incremental_copy_blob = "OperationNotAllowedOnIncrementalCopyBlob"
    pending_copy_operation = "PendingCopyOperation"
    previous_snapshot_cannot_be_newer = "PreviousSnapshotCannotBeNewer"
    previous_snapshot_not_found = "PreviousSnapshotNotFound"
    previous_snapshot_operation_not_supported = "PreviousSnapshotOperationNotSupported"
    sequence_number_condition_not_met = "SequenceNumberConditionNotMet"
    sequence_number_increment_too_large = "SequenceNumberIncrementTooLarge"
    snapshot_count_exceeded = "SnapshotCountExceeded"
    snaphot_operation_rate_exceeded = "SnaphotOperationRateExceeded"
    snapshots_present = "SnapshotsPresent"
    source_condition_not_met = "SourceConditionNotMet"
    system_in_use = "SystemInUse"
    target_condition_not_met = "TargetConditionNotMet"
    unauthorized_blob_overwrite = "UnauthorizedBlobOverwrite"
    blob_being_rehydrated = "BlobBeingRehydrated"
    blob_archived = "BlobArchived"
    blob_not_archived = "BlobNotArchived"
    cannot_delete_file_or_directory = "CannotDeleteFileOrDirectory"
    file_lock_conflict = "FileLockConflict"
    invalid_file_or_directory_path_name = "InvalidFileOrDirectoryPathName"

class DictMixin(object):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.keys())

    def __delitem__(self, key):
        self.__dict__[key] = None

    def __eq__(self, other):
        """Compare objects by comparing all attributes."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Compare objects by comparing all attributes."""
        return not self.__eq__(other)

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith('_')})

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return [k for k in self.__dict__ if not k.startswith('_')]

    def values(self):
        return [v for k, v in self.__dict__.items() if not k.startswith('_')]

    def items(self):
        return [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]

    def get(self, key, default=None):
        if key in self.__dict__:
            return self.__dict__[key]
        return default
