#!/bin/bash

#echo {time}
scanimage >testPFAS;
if [ -s testPFAS ]; then
	cp testPFAS scannedPFAS
fi
