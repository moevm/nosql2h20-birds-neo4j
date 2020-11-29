for a in `docker ps -a -q`
do
  docker stop $a
done