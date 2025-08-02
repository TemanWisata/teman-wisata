create table if not exists public.user_place_rating (
    id uuid primary key default gen_random_uuid(),
    user_id int not null,
    place_id int not null,
    rating numeric(2, 1) not null check (
        rating >= 0
        and rating <= 5
    ),
    created_at timestamp with time zone default timezone('utc' :: text, now()),
    updated_at timestamp with time zone default timezone('utc' :: text, now()),
    deleted_at timestamp with time zone null
);
