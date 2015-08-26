#!/bin/sh

C_S_IN=10000
C_S_OUT=10001
C_R_IN=10002
C_R_OUT=10003
S_IN=10004
S_OUT=10005
R_IN=10006
R_OUT=10007

if [ $# -ne 3 ]
then
    printf 'Usage: %s INPUT_FILE OUTPUT_FILE P_RATE\n' "$0"
    exit 1
else
    INPUT_FILE="$1"
    OUTPUT_FILE="$2"
    P_RATE="$3"
fi

# Terminate channel/receiver automatically on exit
trap '( kill $channel_pid; kill $receiver_pid ) >/dev/null 2>&1' 0

./channel.py $C_S_IN $C_S_OUT $C_R_IN $C_R_OUT $S_IN $R_IN $P_RATE &
channel_pid=$!
sleep 1

./receiver.py $R_IN $R_OUT $C_R_IN "$OUTPUT_FILE" &
receiver_pid=$!
sleep 1

# Set a small block size so that it takes multiple packets to send the file
# Set a small timeout so that the test runs faster
SENDER_BLOCK_SIZE=32 SENDER_TIMEOUT=0.05 \
    ./sender.py $S_IN $S_OUT $C_S_IN "$INPUT_FILE"
