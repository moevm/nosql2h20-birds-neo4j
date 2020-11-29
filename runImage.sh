# This runs the application without database
sudo docker run -it                   \
    -v /tmp/.X11-unix:/tmp/.X11-unix  \
    -e DISPLAY=$DISPLAY               \
    -u qtuser                         \
    --rm \
    birdwatcher python3 src/main.py