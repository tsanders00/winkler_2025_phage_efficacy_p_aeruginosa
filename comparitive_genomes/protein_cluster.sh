#!/usr/bin/bash

function run_mmseq_lincluster(){
    input=$1
    outputPrefix=$2
    threads=$3
    otherPara=$4
    mmseq="/home/viro/xue.peng/software_home/mmseq2/mmseqs/bin/mmseqs"
    tmp=`md5sum $input|cut -d " " -f 1`    
    echo "Run command: $mmseq easy-linclust $input $outputPrefix $tmp $otherPara --thread $threads"
    $mmseq easy-linclust $input $outputPrefix $tmp $otherPara --threads $threads && rm -rf $tmp
}

function help(){
    echo "Usage: $0 <input> <output Dir> [thread] [other Para]"
    echo -e "\toutput Dir: dir name and output prefix is mmseq2_linclust"
    echo -e "\tthread: default 2"
    echo -e "\tother Para: default --cov-mode 0 -c 0.70"
}

if [ $# -lt 2 ];then
    help
    exit 1
fi

input=$1
outputDir=$2
threads=${3:-2}
otherPara=${4:-"--cov-mode 0 -c 0.70"}

mkdir -p $outputDir
outputPrefix="$outputDir/mmseq2_linclust"
run_mmseq_lincluster $input $outputPrefix $threads "$otherPara"
