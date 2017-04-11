drop table if exists imagens;
create table imagens(
	id integer primary key autoincrement,
	nome varchar(20) not null,
	metadados varchar(100),
	imagem blob not null
);
