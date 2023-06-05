CREATE FUNCTION check_first_date() RETURNS TRIGGER AS $$
declare first_t int;
begin
  select  first_time
		from theme
		where id = new.theme_id
		into first_t;
  IF first_t > extract('Year' from new.passed) then
    RAISE NOTICE 'Previous first_time: %', first_t;
    RAISE NOTICE 'New first_time: %', extract('year' from new.passed);
    RAISE NOTICE 'Updating table theme with new value: %', extract('year' from new.passed);
    update theme set first_time = extract('year' from new.passed) where id = new.theme_id;
    Return NEW;
  ELSE
    RETURN NULL;
  END IF;
END;
$$ LANGUAGE plpgsql;

select first_time from theme
		where name = '101'

create TRIGGER check_first_date_trigger
AFTER INSERT or UPDATE  ON "project"
FOR EACH ROW
EXECUTE FUNCTION check_first_date();


create or replace function cnt_sources() returns table(id int, fio text, cnt bigint) 
as $$
begin
	return query(
		select s.id, s.fio, count(project_id)
		from (student s join project p on s.id = p.author_id) 
				join source_project sp on p.id = sp.project_id
		group by s.id);
end;
$$ LANGUAGE 'plpgsql';

drop function cnt_sources(int4) 


select * from cnt_sources()

