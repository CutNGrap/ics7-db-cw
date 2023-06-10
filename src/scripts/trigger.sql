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


create or replace function more_than_avg_sources(gr_id int) returns table(id int, fio text, project int, source_counter bigint) 
as $$
begin
	return query(
		select s.id as student_id, s.fio, p.id as project_id, count(sp.source_id) as cnt
		from (student s join project p on s.id = p.author_id) 
				join source_project sp on p.id = sp.project_id
		where s.group_id = gr_id
		group by s.id, p.id
		having count(sp.source_id) > (select avg(cnt)
										from (select project_id, count(source_id) as cnt
												from source_project sp2
												group by project_id) as avg_cnt)
		order by cnt desc
	);
end;
$$ LANGUAGE 'plpgsql';


create  or replace function st_per_group(gr_id int) returns table(proj_id int) 
as $$
begin
	return query(
		select p.id 
		from (student s join project p on s.id = p.author_id) 
		where s.group_id = gr_id 
	);
end;
$$ LANGUAGE 'plpgsql';

create or replace function avg_per_group(gr_id int) returns int
as $$
begin
	return (
		select avg(p.mark)
		from (student s join project p on s.id = p.author_id) 
		where s.group_id = gr_id );
end;
$$ LANGUAGE 'plpgsql';


explain select count(group_num)
		from grouptab g  
		where group_num = 3
		
explain select id
		from grouptab  
		where group_num = 3
		
		Aggregate  (cost=2.29..2.30 rows=1 width=8)
		Seq Scan on grouptab  (cost=0.00..2.25 rows=17 width=4)
		

create index st_ii on grouptab using BTREE(group_num)		
		
		
		
drop function avg_per_group

select * from st_per_group(1)

select avg_per_group(1)

select s.id, count(sp.id)
		from (student s join project p on s.id = p.author_id) 
				join source_project sp on p.id = sp.project_id
group by s.id

select * from more_than_avg_sources(2)

select * from source_project sp 

select * from project


explain select s.id as student_id, s.fio, p.id as project_id, count(sp.source_id) as cnt
		from (student s join project p on s.id = p.author_id) 
				join source_project sp on p.id = sp.project_id
		where s.group_id = 2
		group by s.id, p.id
		having count(sp.source_id) > (select avg(cnt)
										from (select project_id, count(source_id) as cnt
												from source_project sp2
												group by project_id) as avg_cnt)
		order by cnt desc;
	

	Sort  (cost=173084.01..173099.97 rows=6384 width=21)
	Sort  (cost=173084.01..173099.97 rows=6384 width=21)
	Sort  (cost=173084.01..173099.97 rows=6384 width=21)
	
create index student_group on student using BTREE(group_id)

create index st_id on student using BTREE(id)

create index st_ii on source_project using BTREE(source_id)

create index st_i2 on project using BTREE(mark)

explain select * from student s where group_id = 2

drop index st_id

drop index st_ii

create index st_ii on source_project using BTREE(project_id)

explain analyze select count(id)  as cnt
		from source_project sp 
		
explain analyze select id  as cnt
		from source_project sp 
		where project_id  = 2

Aggregate  (cost=8.65..8.66 rows=1 width=8) (actual time=0.018..0.019 rows=1 loops=1)
Finalize Aggregate  (cost=22231.49..22231.50 rows=1 width=8) (actual time=83.879..86.877 rows=1 loops=1)
		
Hash Join  (cost=1194.00..5493.06 rows=200000 width=4)
Index Scan using st_ii on source_project sp  (cost=0.43..8.62 rows=11 width=4) (actual time=0.773..0.775 rows=9 loops=1)

Aggregate  (cost=4602.63..4602.64 rows=1 width=32)
Finalize Aggregate  (cost=4088.82..4088.83 rows=1 width=32)

Hash Join  (cost=798.79..4597.84 rows=1915 width=4)
Hash Join  (cost=326.56..4125.62 rows=1915 width=4)



explain analyze select count(group_id) from student s 

create index st_ii on student using BTREE(group_id)

drop index st_ii

Execution Time: 4.769 ms
4.880 
Execution Time: 15.880 ms

Finalize Aggregate  (cost=63805.88..63805.89 rows=1 width=8) (actual time=2478.654..2481.535 rows=1 loops=1)

Execution Time: 266.323 ms

create  or replace function test1() returns int
as $$
begin
	return (
		select count(group_id) from student s where group_id = 50
	);
end;
$$ LANGUAGE 'plpgsql';

create  or replace function test2() returns int
as $$
begin
	return (
		select count(group_id) from student s 
	);
end;
$$ LANGUAGE 'plpgsql';

explain analyze select count(group_id) from student s where group_id = 50


SET enable_seqscan = on;

Execution Time: 2.598 ms
Execution Time: 0.131 ms
