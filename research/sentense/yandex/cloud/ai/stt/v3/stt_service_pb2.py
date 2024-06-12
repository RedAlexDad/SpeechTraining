# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/stt/v3/stt_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.ai.stt.v3 import stt_pb2 as yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(yandex/cloud/ai/stt/v3/stt_service.proto\x12\x10speechkit.stt.v3\x1a yandex/cloud/ai/stt/v3/stt.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1dyandex/cloud/validation.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/operation/operation.proto\";\n\x15GetRecognitionRequest\x12\"\n\x0coperation_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=502q\n\nRecognizer\x12\x63\n\x12RecognizeStreaming\x12\".speechkit.stt.v3.StreamingRequest\x1a#.speechkit.stt.v3.StreamingResponse\"\x00(\x01\x30\x01\x32\xb3\x02\n\x0f\x41syncRecognizer\x12\x9c\x01\n\rRecognizeFile\x12&.speechkit.stt.v3.RecognizeFileRequest\x1a!.yandex.cloud.operation.Operation\"@\xb2\xd2*\x17\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x1f\"\x1a/stt/v3/recognizeFileAsync:\x01*\x12\x80\x01\n\x0eGetRecognition\x12\'.speechkit.stt.v3.GetRecognitionRequest\x1a#.speechkit.stt.v3.StreamingResponse\"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/stt/v3/getRecognition0\x01\x42\\\n\x1ayandex.cloud.api.ai.stt.v3Z>github.com/yandex-cloud/go-genproto/yandex/cloud/ai/stt/v3;sttb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.ai.stt.v3.stt_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\032yandex.cloud.api.ai.stt.v3Z>github.com/yandex-cloud/go-genproto/yandex/cloud/ai/stt/v3;stt'
  _globals['_GETRECOGNITIONREQUEST'].fields_by_name['operation_id']._loaded_options = None
  _globals['_GETRECOGNITIONREQUEST'].fields_by_name['operation_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_ASYNCRECOGNIZER'].methods_by_name['RecognizeFile']._loaded_options = None
  _globals['_ASYNCRECOGNIZER'].methods_by_name['RecognizeFile']._serialized_options = b'\262\322*\027\022\025google.protobuf.Empty\202\323\344\223\002\037\"\032/stt/v3/recognizeFileAsync:\001*'
  _globals['_ASYNCRECOGNIZER'].methods_by_name['GetRecognition']._loaded_options = None
  _globals['_ASYNCRECOGNIZER'].methods_by_name['GetRecognition']._serialized_options = b'\202\323\344\223\002\030\022\026/stt/v3/getRecognition'
  _globals['_GETRECOGNITIONREQUEST']._serialized_start=231
  _globals['_GETRECOGNITIONREQUEST']._serialized_end=290
  _globals['_RECOGNIZER']._serialized_start=292
  _globals['_RECOGNIZER']._serialized_end=405
  _globals['_ASYNCRECOGNIZER']._serialized_start=408
  _globals['_ASYNCRECOGNIZER']._serialized_end=715
# @@protoc_insertion_point(module_scope)
