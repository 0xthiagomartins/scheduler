#!/bin/sh

echo Starting Nameko.
exec nameko run --config src/config.yaml src.service