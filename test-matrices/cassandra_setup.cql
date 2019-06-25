CREATE KEYSPACE IF NOT EXISTS performo WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 3 };

DESCRIBE keyspaces;

USE performo;

CREATE TABLE IF NOT EXISTS test_matrices (log_stamp timestamp PRIMARY KEY, matrix text);

INSERT INTO test_matrices (log_stamp, matrix) VALUES ( toTimestamp( now() ), '[ { "testUnitName":"ApplicationCreation", "duration":23194 }, { "testUnitName":"ApplicationDeletion", "duration": 5297 } ]');