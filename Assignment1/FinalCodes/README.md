This Repository contains simple client server models that serialise and deserialise data over HTTP and TCP protocols.

Ser/Dser is done in JSON and Binary.

Json ser/Dser is done over HTTP server, which is hosted locally and on AWS using FLASK.
Server and client use json and request libraries to parse data and get responses.

Binary ser/Dser is done using protobuf
.proto file has message for Request, Data and Datalog.
Server client Connection is made using sockets and data is communicated as string of bytes.
