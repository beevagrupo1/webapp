mysql -uroot -proot druzi -e \
  "CREATE FULLTEXT INDEX descripcion_texto ON Druzi_activity (description);"
