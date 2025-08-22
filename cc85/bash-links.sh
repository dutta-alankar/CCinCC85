#!/bin/bash

src_dir="$(pwd)/output-res-16"
dest_dir="$(pwd)/output-c100,m1.496,T4e4,t0.80,r282.684-r16"

src_start=7
dest_start=53
count=$((53 - 7))  # 46 links in total

for ((i=0; i<count; i++)); do
  src_idx=$(printf "%04d" $((src_start + i)))
  dest_idx=$(printf "%04d" $((dest_start + i)))
  rm "${dest_dir}/data.${dest_idx}.flt.h5"
  rm "${dest_dir}/data.${dest_idx}.flt.xmf"
  ln -s "${src_dir}/data.${src_idx}.flt.h5" "${dest_dir}/data.${dest_idx}.flt.h5"
  cp "${src_dir}/data.${src_idx}.flt.xmf" "${dest_dir}/data.${dest_idx}.flt.xmf"
  ex -sc "%s/${src_idx}.flt/${dest_idx}.flt/g|x" "${dest_dir}/data.${dest_idx}.flt.xmf"
done
