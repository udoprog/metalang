LIBJSON=/usr/local/lib/libjson.a

all:
	metalang -p jsoncpp -M cpp messages.txt
	metalang -M python messages.txt
	g++ -g -Wall -I out out/generated.cpp example.cpp ${LIBJSON} -o example
	./example | python example.py
