copy grouptab (group_num, faculty, qualification, creation) from '/var/lib/postgresql/data/csv_sources/group.csv' delimiter ',' CSV;

copy theme (name, complexity, first_time) from '/var/lib/postgresql/data/csv_sources/theme.csv' delimiter ',' CSV;

copy source (name, type, authors, creation) from '/var/lib/postgresql/data/csv_sources/source.csv' delimiter ',' CSV;

copy student (FIO, group_id, book_num, birth, enrollment) from '/var/lib/postgresql/data/csv_sources/student.csv' delimiter ',' CSV;

copy project (theme_id, author_id, mark, passed) from '/var/lib/postgresql/data/csv_sources/project.csv' delimiter ',' CSV;

copy source_project (source_id, project_id) from '/var/lib/postgresql/data/csv_sources/source_project.csv' delimiter ',' CSV;
