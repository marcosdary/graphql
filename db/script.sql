create type roles as enum (
    'ADMIN', 
    'USER', 
    'SUPER_ADMIN'
);

create table users (
    "userId" varchar(255) primary key,
    "name" varchar(255) not null,
    "email" varchar(255) not null unique,
    "role" roles not null default 'USER',
    "password" varchar(255) not null,
    "isDeleted" boolean default false,
    "createdAt" timestamp default current_timestamp,
    "updatedAt" timestamp default current_timestamp
);

