create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null,
  user_id int not null,
  password text not null,
  dob date not null,
  full_name text not null,
  province text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()),
  updated_at timestamp with time zone default timezone('utc'::text, now()),
  deleted_at timestamp with time zone null
);
