WITH phase as (SELECT
  descript,
  date,
  EXTRACT(month from date) as month,
  EXTRACT(year from date) as year,
  REGEXP_EXTRACT(safe_cast(time as STRING), "^([0-9]{2}):") as hour,
  COUNT(*) as occurrences
FROM
  `bi-psel.danilo_teo.austin_incidents`
GROUP BY
    date, 
  descript,
  month,
  year,
  hour
 ORDER BY descript asc, date asc)
 
 SELECT 
  Descript,
  COUNT(*) as occurrences
 FROM 
  phase
 WHERE 
  year >= 2016
 GROUP BY
  Descript
 ORDER BY occurrences desc