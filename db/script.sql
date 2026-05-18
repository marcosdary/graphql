create type papers as enum (
	'SESSION',
	'API_KEY'
);

create table users (
    user_id varchar(255) primary key,
    name varchar(255) not null,
    email varchar(255) not null unique,
    role_id varchar(255) not null,
    password varchar(255) not null,
    is_deleted boolean default false,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,
    
    constraint fk_users_role
        foreign key (role_id)
        references role(role_id)
        on delete restrict
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
    created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,

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
drop table role_permissions;

select * from users;
select * from token;
select * from role where role_id = 'f20dcb79-e960-41ce-8055-80b5b3fb87b0';
select * from permission;

delete from users where user_id = '3396441b-b0cd-48cb-96ac-b13ae55115f4';

update permission as p 
set 
	name=v.name
from (
	values
	('db4d790b-5e36-4f27-b9da-e75a621deb8e', 'auth:verifyTwoFactor'),
	('7acf8f02-687c-46d4-863f-de41f03a210d', 'auth:resetPassword'),
	('15263b82-03d6-4299-9353-debee13417c9', 'auth:forgotPassword'),
	('681de4a5-426b-4f96-97d7-1c5a866a5090', 'user:deleteAccount'),
	('7b0c22c5-e394-424a-b9b6-f89c9f727680', 'user:updateProfile'),
	('62614608-f9f9-4919-9c5b-1f7fa9656c86', 'admin:users:getById')
) as v(permission_id, name)
where p.permission_id = v.permission_id ;




select p.permission_id , p.name, r.role_id, r.name from role_permissions as rp
inner join role as r on rp.role_id = r.role_id 
inner join permission as p on rp.permission_id = p.permission_id;


