create table if not exists public.tour_package (
    id uuid primary key default gen_random_uuid(),
    tour_package_id serial not null,
    place_id int not null,
    created_at timestamp with time zone default timezone('utc' :: text, now()),
    updated_at timestamp with time zone default timezone('utc' :: text, now()),
    deleted_at timestamp with time zone null
);
