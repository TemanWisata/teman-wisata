create table if not exists public.place (
    id uuid primary key default gen_random_uuid(),
    place_id int unique not null,
    place_name text not null,
    description text not null,
    category text not null,
    province text not null,
    price float null,
    rating float null,
    time_minutes float null,
    latitude float not null,
    longitude float not null,
    created_at timestamp with time zone default timezone('utc' :: text, now()),
    updated_at timestamp with time zone default timezone('utc' :: text, now()),
    deleted_at timestamp with time zone null
);
