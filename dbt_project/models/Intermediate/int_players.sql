
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='view', tags=['intermediate']) }}

with stg_ref as (
	select * from {{ ref('stg_players') }}
)

select
	*,
	extract(year from current_date) - extract(year from dob) as age,
	case
		when position in ('Right Midfield', 'Attacking Midfield', 'Central Midfield', 'Left Midfield', 'Defensive Midfield') then 'Midfielder'
		when position in ('Second Striker', 'CentreForward', 'Left Winger', 'Right Winger') then 'Forwarder'
		when position in ('RightBack', 'LeftBack', 'CentreBack') then 'Defender'
		when position = 'Goalkeeper' then 'Goalkeeper'
	else position
	end as general_position,
	case
		when place_of_birth = citizenship then 'Native player'
		else 'Heritage player'
		end as national_type
from stg_ref

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
