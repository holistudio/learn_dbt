SELECT * FROM {{ ref('stg_pluto') }}
WHERE landuse = '11';