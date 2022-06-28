# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server_proto.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12server_proto.proto\"<\n\nClientInfo\x12\x1b\n\x06status\x18\x01 \x01(\x0e\x32\x0b.CodeResult\x12\x11\n\tjson_info\x18\x02 \x01(\t\"4\n\x0fRequestSelfInfo\x12\x13\n\x0b\x63redentials\x18\x01 \x01(\t\x12\x0c\n\x04time\x18\x02 \x01(\x05\"\'\n\x08Response\x12\x1b\n\x06status\x18\x01 \x01(\x0e\x32\x0b.CodeResult\"B\n\x07Message\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x11\n\taddressee\x18\x02 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x03 \x01(\t\"7\n\x10\x41\x64\x64\x46riendRequest\x12\x0e\n\x06\x66riend\x18\x01 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x02 \x01(\t\":\n\x13RemoveFriendRequest\x12\x0e\n\x06\x66riend\x18\x01 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x02 \x01(\t\"6\n\x11\x43reateRoomRequest\x12\x0c\n\x04room\x18\x01 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x02 \x01(\t\"4\n\x0fJoinRoomRequest\x12\x0c\n\x04room\x18\x01 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x02 \x01(\t\"6\n\x11\x45scapeRoomRequest\x12\x0c\n\x04room\x18\x01 \x01(\t\x12\x13\n\x0b\x63redentials\x18\x02 \x01(\t*1\n\nCodeResult\x12\x12\n\x0eunknown_format\x10\x00\x12\x06\n\x02ok\x10\x01\x12\x07\n\x03\x62\x61\x64\x10\x02\x32\xcf\x02\n\x07Greeter\x12\x35\n\x12InformationRequest\x12\x10.RequestSelfInfo\x1a\x0b.ClientInfo\"\x00\x12$\n\x0bSendMessage\x12\x08.Message\x1a\t.Response\"\x00\x12+\n\tAddFriend\x12\x11.AddFriendRequest\x1a\t.Response\"\x00\x12\x31\n\x0cRemoveFriend\x12\x14.RemoveFriendRequest\x1a\t.Response\"\x00\x12-\n\nCreateRoom\x12\x12.CreateRoomRequest\x1a\t.Response\"\x00\x12)\n\x08JoinRoom\x12\x10.JoinRoomRequest\x1a\t.Response\"\x00\x12-\n\nRoomEscape\x12\x12.EscapeRoomRequest\x1a\t.Response\"\x00\x62\x06proto3')

_CODERESULT = DESCRIPTOR.enum_types_by_name['CodeResult']
CodeResult = enum_type_wrapper.EnumTypeWrapper(_CODERESULT)
unknown_format = 0
ok = 1
bad = 2


_CLIENTINFO = DESCRIPTOR.message_types_by_name['ClientInfo']
_REQUESTSELFINFO = DESCRIPTOR.message_types_by_name['RequestSelfInfo']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_ADDFRIENDREQUEST = DESCRIPTOR.message_types_by_name['AddFriendRequest']
_REMOVEFRIENDREQUEST = DESCRIPTOR.message_types_by_name['RemoveFriendRequest']
_CREATEROOMREQUEST = DESCRIPTOR.message_types_by_name['CreateRoomRequest']
_JOINROOMREQUEST = DESCRIPTOR.message_types_by_name['JoinRoomRequest']
_ESCAPEROOMREQUEST = DESCRIPTOR.message_types_by_name['EscapeRoomRequest']
ClientInfo = _reflection.GeneratedProtocolMessageType('ClientInfo', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTINFO,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:ClientInfo)
  })
_sym_db.RegisterMessage(ClientInfo)

RequestSelfInfo = _reflection.GeneratedProtocolMessageType('RequestSelfInfo', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTSELFINFO,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:RequestSelfInfo)
  })
_sym_db.RegisterMessage(RequestSelfInfo)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:Response)
  })
_sym_db.RegisterMessage(Response)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

AddFriendRequest = _reflection.GeneratedProtocolMessageType('AddFriendRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDFRIENDREQUEST,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:AddFriendRequest)
  })
_sym_db.RegisterMessage(AddFriendRequest)

RemoveFriendRequest = _reflection.GeneratedProtocolMessageType('RemoveFriendRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEFRIENDREQUEST,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:RemoveFriendRequest)
  })
_sym_db.RegisterMessage(RemoveFriendRequest)

CreateRoomRequest = _reflection.GeneratedProtocolMessageType('CreateRoomRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEROOMREQUEST,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:CreateRoomRequest)
  })
_sym_db.RegisterMessage(CreateRoomRequest)

JoinRoomRequest = _reflection.GeneratedProtocolMessageType('JoinRoomRequest', (_message.Message,), {
  'DESCRIPTOR' : _JOINROOMREQUEST,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:JoinRoomRequest)
  })
_sym_db.RegisterMessage(JoinRoomRequest)

EscapeRoomRequest = _reflection.GeneratedProtocolMessageType('EscapeRoomRequest', (_message.Message,), {
  'DESCRIPTOR' : _ESCAPEROOMREQUEST,
  '__module__' : 'server_proto_pb2'
  # @@protoc_insertion_point(class_scope:EscapeRoomRequest)
  })
_sym_db.RegisterMessage(EscapeRoomRequest)

_GREETER = DESCRIPTOR.services_by_name['Greeter']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CODERESULT._serialized_start=530
  _CODERESULT._serialized_end=579
  _CLIENTINFO._serialized_start=22
  _CLIENTINFO._serialized_end=82
  _REQUESTSELFINFO._serialized_start=84
  _REQUESTSELFINFO._serialized_end=136
  _RESPONSE._serialized_start=138
  _RESPONSE._serialized_end=177
  _MESSAGE._serialized_start=179
  _MESSAGE._serialized_end=245
  _ADDFRIENDREQUEST._serialized_start=247
  _ADDFRIENDREQUEST._serialized_end=302
  _REMOVEFRIENDREQUEST._serialized_start=304
  _REMOVEFRIENDREQUEST._serialized_end=362
  _CREATEROOMREQUEST._serialized_start=364
  _CREATEROOMREQUEST._serialized_end=418
  _JOINROOMREQUEST._serialized_start=420
  _JOINROOMREQUEST._serialized_end=472
  _ESCAPEROOMREQUEST._serialized_start=474
  _ESCAPEROOMREQUEST._serialized_end=528
  _GREETER._serialized_start=582
  _GREETER._serialized_end=917
# @@protoc_insertion_point(module_scope)
