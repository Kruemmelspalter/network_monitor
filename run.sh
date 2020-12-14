if
	[ "$EUID" -ne 0 ]
then
	printf "Running as root\n\n"
	sudo ./run.sh $@
	exit
fi
python3 $@
