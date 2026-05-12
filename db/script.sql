create type roles as enum (
    'ADMIN', 
    'USER', 
    'SUPER_ADMIN'
);

create type papers as enum (
	'SESSION',
	'API_KEY'
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

create table token (
	"token" varchar(600) primary key,
	"paper" papers not null,
	"disabled" boolean default false,
	"createdAt" timestamp default current_timestamp
);


create index "idx_tokens_token" on token("token");

create index "idx_tokens_get_by_paper" on token("paper");

create index "idx_tokens_get_by_disabled" on token("disabled");

create index "idx_users_userId" on users("userId");

create index "idx_users_email" on users(email);

create index "idx_users_get_by_email" on users("isDeleted", email);

create index "idx_users_get_by_id" on users("isDeleted", "userId");

create index "idx_users_isDeleted" on users("isDeleted");


