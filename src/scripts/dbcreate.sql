drop table if exists grouptab cascade;
drop table if exists student cascade;
drop table if exists theme cascade;
drop table if exists "source" cascade;
drop table if exists project cascade;
drop table if exists source_project cascade;


CREATE TABLE grouptab
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
    group_num int not null,
    faculty text not null,
    qualification text not null,
    creation int default date_part('year', CURRENT_DATE),
    unique (group_num,faculty,qualification,creation)
);

CREATE TABLE student
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
    FIO text not null,
    group_id int references grouptab(id),
    book_num int not null,
    birth date not null,
    enrollment int default date_part('year', CURRENT_DATE),
    unique (enrollment, book_num)
);

CREATE TABLE theme
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
    name text unique not null,
	complexity int not null CHECK (complexity > 0) check (complexity < 11),
    first_time int default date_part('year', CURRENT_DATE)
);

CREATE TABLE source
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
    name text not null,
	type text default '',
	authors text not null,
    creation int default date_part('year', CURRENT_DATE),
    unique(name, type, authors, creation)
);

CREATE TABLE project
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
    theme_id int references theme(id),
    author_id int references student(id),
    mark int not null CHECK (mark > 1) check (mark < 6),
  	passed date not null default CURRENT_DATE,
  	unique(theme_id, author_id, mark, passed)
);

create table source_project
(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY key,
	source_id int references source(id),
	project_id int references project(id)
)