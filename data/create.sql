create table links(
    movie_id int not null,
    imdb_id varchar(255) null,
    tmdb_id varchar(255) null,
    primary key ( movie_id )
);

create table movies(
    movie_id int not null,
    title varchar(255) null,
    genres varchar(255) null,
    primary key ( movie_id )
);

create table ratings(
    user_id int not null,
    movie_id int not null,
    rating int,
    time_stamp varchar(10) null
);

create table tags(
    user_id int not null,
    movie_id int not null,
    tag varchar(255) null,
    time_stamp varchar(10) null
);
