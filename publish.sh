#!/bin/zsh
# 非公開リポジトリのカードから data.json を作り直し、変わっていれば公開する
set -e
cd "$(dirname "$0")"
python3 build.py
if git diff --quiet -- data.json; then echo "変更なし"; exit 0; fi
git add data.json
git commit -qm "進み具合を更新"
git push -q
echo "公開しました: https://wimaoka51-blip.github.io/zenso-progress/"
