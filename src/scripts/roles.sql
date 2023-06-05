CREATE ROLE StUser LOGIN PASSWORD 'postgres';
GRANT SELECT ON TABLE "theme", "grouptab"  TO StUser;

CREATE ROLE TeUser LOGIN PASSWORD 'postgres';
GRANT SELECT ON TABLE "theme", "grouptab", "student", "source", "project", "source_project"  TO TeUser;
 
CREATE ROLE AdmUser LOGIN PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO AdmUser;
