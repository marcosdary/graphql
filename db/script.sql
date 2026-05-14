create type papers as enum (
	'SESSION',
	'API_KEY'
);

create table users (
    "user_id" varchar(255) primary key,
    "name" varchar(255) not null,
    "email" varchar(255) not null unique,
    "password" varchar(255) not null,
    "is_deleted" boolean default false,
    "created_at" timestamp default current_timestamp,
    "updated_at" timestamp default current_timestamp
);

create table token (
	"token" varchar(600) primary key,
	"paper" papers not null,
	"disabled" boolean default false,
	"created_at" timestamp default current_timestamp,
	"updated_at" timestamp default current_timestamp
);

create table role_permissions (
    role_id varchar(255) not null,
    permission_id varchar(255) not null,

    primary key (role_id, permission_id),

    constraint fk_role_permissions_role
        foreign key (role_id)
        references role(role_id)
        on delete cascade,

    constraint fk_role_permissions_permission
        foreign key (permission_id)
        references permission(permission_id)
        on delete cascade
);

create table permission (
	permission_id varchar(255) primary key,
	name varchar(255) not null unique,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp
);

create table role (
	role_id varchar(255) primary key,
	name varchar(255) not null unique,
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp
);



create index "idx_tokens_token" on token("token");

create index "idx_tokens_get_by_paper" on token("paper");

create index "idx_tokens_get_by_disabled" on token("disabled");

create index "idx_users_userId" on users("userId");

create index "idx_users_email" on users(email);

create index "idx_users_get_by_email" on users("isDeleted", email);

create index "idx_users_get_by_id" on users("isDeleted", "userId");

create index "idx_users_isDeleted" on users("isDeleted");

drop table users;
drop type roles;

select * from users;
select * from token;
select * from role;
select * from permission;


