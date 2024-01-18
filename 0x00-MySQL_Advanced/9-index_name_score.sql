-- The script that creates an index 'idx_name_first_score' on table.
-- The table names and the first letter of name && the score.
CREATE INDEX idx_name_first_score on names(name(1), score)
