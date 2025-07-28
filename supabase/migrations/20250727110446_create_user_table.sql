create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null,
  password text not null,
  full_name text,
  province text,
  created_at timestamp with time zone default timezone('utc'::text, now())
);
