-- this mysql script creates an index on a database called names.
CREATE INDEX idx_name_first ON names (SUBSTRING(name, 1, 1))
