#!/bin/zsh
# 作品の本番 HTML を、このページの works/ の下に写す（撮影用の shots は除く）。検索よけを足す
# 使い方：./sync-works.sh（全部）／ ./sync-works.sh madobe ／ ./sync-works.sh hitotsugama
set -e
cd "$(dirname "$0")"
sync_one() {
  local SRC=$1 DST=$2
  rm -rf $DST && mkdir -p $DST/hp
  rsync -a --exclude shots --exclude '.DS_Store' $SRC/site/ $DST/site/
  rsync -a --exclude shots --exclude '.DS_Store' $SRC/hp/site/ $DST/hp/site/
  find $DST -name '*.html' -print0 | xargs -0 perl -0pi -e 's#<head>#<head>\n<meta name="robots" content="noindex,nofollow">#i unless /name="robots"/'
  du -sh $DST
}
[[ -z $1 || $1 == madobe ]] && sync_one ../../LP/renovation-trial works/madobe
[[ -z $1 || $1 == hitotsugama ]] && sync_one ../../LP/bakery-trial works/hitotsugama
true
