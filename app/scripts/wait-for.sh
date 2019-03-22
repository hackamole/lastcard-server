#!/bin/bash -eu
#
# wait_for.sh - Waits until get a successful connection with host.
#
# Copyright (c) 2018, Bright Pixel
#

open_conn() {
	local host=$1
	local port=$2
	local timeout=$3

	echo "Connecting to ${host}..."
	if ! timeout "$timeout" bash -c "</dev/tcp/${host}/${port}" >/dev/null 2>&1; then
		return 1;
	else
		return 0;
	fi
}

wait_for(){
	local host=$1
	local port=$2
	local retries=$3
	local timeout=$4

	local i=0
	local return_code
	for i in `seq $retries` ; do
		if open_conn "${host}" "${port}" "${timeout}" ; then
			exit 0;
		fi

		echo "Retrying in $timeout seconds..."
		sleep $timeout;
	done

	exit 1;
}


main(){
	local host=$1
	local port=$2
	local retries=${3:-1}
	local timeout=${4:-1}
	wait_for "$host" "$port" "$retries" "$timeout"
}

main "$@"

