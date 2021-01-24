SELECT
  descript,
  EXTRACT(month from date) as month,
  COUNT(*) as occurrences
FROM
  `bi-psel.danilo_teo.austin_incidents`
GROUP BY
  descript,
  month
ORDER BY month asc, descript asc