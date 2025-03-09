docker run -it \
	--network=host \
    -v=/dev:/dev \
    --privileged \
    --device-cgroup-rule="a *:* rmw" \
    --cap-add=SYS_PTRACE \
    --security-opt=seccomp:unconfined \
    --security-opt=apparmor:unconfined \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    -e ROBOT_NAME="814" \
    hicsail/limo
