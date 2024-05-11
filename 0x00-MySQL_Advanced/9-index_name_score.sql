-- this mysql script creates an index on a database called names.
CREATE INDEX idx_name_first_score ON names(name(1), score)
