
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='view', tags=['staging']) }}

with source as (
	select * from {{ source('postgres', 'premier_league_raw') }}
	union all
	select * from {{ source('postgres', 'laliga_raw') }}
	union all
	select * from {{ source('postgres', 'serie_a_raw') }}
	union all
	select * from {{ source('postgres', 'bundesliga_raw') }}
	union all
	select * from {{ source('postgres', 'ligue_1_raw')}}
),

first_clean as(
	select 
		trim(regexp_replace(headline_name, '[#0-9]', '', 'g')) as full_name,
		'#' || trim(regexp_replace(headline_name, '[^0-9]', '', 'g')) as shirt_num,
		club,
		league,
		to_date(left(dob_age, 10), 'dd/mm/yyyy') as dob,
		case 
			when place_of_birth = 'Korea, South' then 'Republic of Korea' 
			else place_of_birth end as place_of_birth,
		case 
			when citizenship = 'Korea, South' then 'Republic of Korea' 
			else citizenship end as citizenship,
		cast(trim(regexp_replace(height, '[,m]', '', 'g')) as numeric) as height,
		replace(trim(substring(position from 10)), '-', '') as position,
		regexp_replace(
			split_part(market_value_wrapper, E'\n', 1), '[€.]', '', 'g') as market_value_euro,
		trim(
			substring(
				split_part(market_value_wrapper, E'\n', 2) from 13)
				) as market_value_last_update,
		link
	from source
	where league in ('Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1') and league is not null
),

avg_height as (
	select avg(height) as avg_height from first_clean where height is not null
)

select 
	c.full_name,
	c.shirt_num,
	c.club,
	c.league,
	c.dob,
	c.place_of_birth,
	c.citizenship,
	round(coalesce(c.height, a.avg_height),0) as height,
	c.position,
	cast(
		(case
			when c.market_value_euro like '%m' then replace(c.market_value_euro, 'm', '0000')
			when c.market_value_euro like '%k' then replace(c.market_value_euro, 'k', '000')
			end)
			as numeric
			) as market_value_euro,
	to_date(c.market_value_last_update, 'dd/mm/yyyy') as market_value_last_update,
	link
from first_clean c
cross join avg_height a

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
