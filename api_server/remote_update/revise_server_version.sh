#!/bin/bashi
VERSION=1.42
PROGRAM=on-board-program-v$VERSION
sudo rm -r $PROGRAM
if [ -f $PROGRAM.tar.gz ] ; then
  tar -xzvf $PROGRAM.tar.gz > /dev/null 

  klb=$PROGRAM/config/KLB/confKLB.ini
  klb_v=$(cat $klb | grep VM)
  sed -i "s/$klb_v/VM=$VERSION/g" $klb

  ymt=$PROGRAM/config/YMT/confYMT.ini
  ymt_v=$(cat $ymt | grep VM)
  sed -i "s/$ymt_v/VM=$VERSION/g" $ymt

  ctl=$PROGRAM/config/CTL/confCTL.ini
  ctl_v=$(cat $ctl | grep VM)
  sed -i "s/$ctl_v/VM=$VERSION/g" $ctl

  cp -rf $PROGRAM/config ../

  rm $PROGRAM.tar.gz 
  tar -czvf $PROGRAM.tar.gz $PROGRAM > /dev/null

  echo '-found gz file'
  MD5=$(md5sum $PROGRAM.tar.gz | awk '{ print $1 }')
  echo "--new MD5: $MD5"
  OLD_MD5=$(cat ../vm | grep MD5)
  OLD_VM=$(cat ../vm | grep VM)
  echo "--old MD5: $OLD_MD5"
  sed -i "s/$OLD_MD5/MD5=$MD5/g" ../vm
  sed -i "s/$OLD_VM/VM=$VERSION/g" ../vm
  echo "-------- new vm --------"
  cat ../vm
  echo "-------- new vm --------"

fi
rm -r $PROGRAM
