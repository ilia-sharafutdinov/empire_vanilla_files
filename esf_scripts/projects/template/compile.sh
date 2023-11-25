#!/bin/bash

SCRIPT_DIR=$(dirname "$0")

export $(grep -v '^#' $SCRIPT_DIR/.env | xargs)

if [ -z "$OUTPUT_DIR" ]
then
    eval "OUTPUT_DIR=$SCRIPT_DIR/$STARTPOS_DIR"
else
    eval "OUTPUT_DIR=$SCRIPT_DIR/${OUTPUT_DIR//[\{\}]/}"
fi

eval "TEMP_DIR=$SCRIPT_DIR/$TEMP_DIR"

echo "Compiling..."

xml2esf $OUTPUT_DIR $TEMP_DIR/startpos.esf && echo "Compilation succeeded." || echo "Compilation failed."
