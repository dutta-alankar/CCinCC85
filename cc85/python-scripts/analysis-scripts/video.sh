#!/bin/bash
cd $1
ffmpeg -pattern_type glob -i 'cold-mass.*.svg' -framerate 0.5 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" cold-mass.mp4
ffmpeg -pattern_type glob -i 'flux.*.svg' -framerate 0.5 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" flux.mp4
ffmpeg -pattern_type glob -i 'profiles.*.svg' -framerate 0.5 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" profiles.mp4
ffmpeg -pattern_type glob -i 'Rclprp.*.svg' -framerate 0.5 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" Rclprp.mp4
ffmpeg -pattern_type glob -i 'timescales.*.svg' -framerate 0.5 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" timescales.mp4
ffmpeg -itsscale 10 -i cold-mass.mp4 -c copy cold-mass-slow.mp4
ffmpeg -itsscale 10 -i flux.mp4 -c copy flux-slow.mp4
ffmpeg -itsscale 10 -i profiles.mp4 -c copy profiles-slow.mp4
ffmpeg -itsscale 10 -i Rclprp.mp4 -c copy Rclprp-slow.mp4
ffmpeg -itsscale 10 -i timescales.mp4 -c copy timescales-slow.mp4
