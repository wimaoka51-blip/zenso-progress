#!/bin/zsh
# 作品の本番 HTML を、このページの works/ の下に写す（撮影用の shots は除く）。検索よけを足す
set -e
cd "$(dirname "$0")"
SRC=../../LP/renovation-trial
DST=works/madobe
rm -rf $DST && mkdir -p $DST/hp
rsync -a --exclude shots --exclude '.DS_Store' $SRC/site/ $DST/site/
rsync -a --exclude shots --exclude '.DS_Store' $SRC/hp/site/ $DST/hp/site/
find $DST -name '*.html' -print0 | xargs -0 perl -0pi -e 's#<head>#<head>\n<meta name="robots" content="noindex,nofollow">#i unless /name="robots"/'
du -sh $DST
