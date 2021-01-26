SELECT
  descript,
  date,
  EXTRACT(month from date) as month,
  SAFE_CAST(EXTRACT(year from date) AS STRING) as year,
  REGEXP_EXTRACT(safe_cast(time as STRING), "^([0-9]{2}):") as hour,
  CONCAT(address, ', Austin, TX') as address,
  location,
  COUNT(*) as occurrences
FROM
  `bi-psel.danilo_teo.austin_incidents`
GROUP BY
    date, 
  descript,
  month,
  year,
  hour,
  address,
  location
 ORDER BY descript asc, date asc