#!/usr/bin/env bash
# restroles.sh <port> : single-user routes in every spelling, over HTTP, as a visitor and logged in (cookie + REST nonce)
P=$1
B=http://127.0.0.1:$P
T=$(mktemp -d)
paths=(/wp-json/wp/v2/users /wp-json/WP/V2/users '/wp-json/wp/v2/users?who=authors'
  /wp-json/wp/v2/users/2 /wp-json/wp/v2/users/2/ /wp-json/WP/V2/users/2 /wp-json/WP/V2/users/2/ /wp-json/wp/v2/USERS/2
  /wp-json/Wp/v2/users/4 /wp-json/wp/v2/Users/4/ '/?rest_route=/wp/v2/users/4' '/?rest_route=/WP/v2/users/4' '/?rest_route=/WP/V2/USERS/2/'
  '/wp-json/wp/v2/users/1?id=2' '/wp-json/WP/V2/users/1?id=4' '/?rest_route=/wp/v2/users/1&id=2'
  /wp-json/wp/v2/users/3 /wp-json/wp/v2/users/5 /wp-json/WP/V2/Users/5 /wp-json/wp/v2/users/1 /wp-json/wp/v2/users/me)
probe() { # label curlargs...
  local label=$1; shift
  echo "== $label"
  for p in "${paths[@]}"; do
    out=$(curl -s "$@" -w '\n%{http_code}' "$B$p"); code=$(echo "$out" | tail -1); body=$(echo "$out" | head -n -1)
    summ=$(echo "$body" | python3 -c 'import sys,json
try: d=json.load(sys.stdin)
except Exception: print("nonjson"); sys.exit()
if isinstance(d,list): print(",".join(str(x.get("slug")) for x in d))
elif "code" in d: print(d["code"])
else: print("id", d.get("id"), d.get("slug"))')
    printf '  %-40s %s %s\n' "$p" "$code" "$summ"
  done
  for p in /wp-json/wp/v2/users/2 /wp-json/WP/V2/users/2 /wp-json/wp/v2/users/5; do
    printf '  HEAD %-35s %s\n' "$p" "$(curl -s -o /dev/null -I "$@" -w '%{http_code}' "$B$p")"
    printf '  POST?_method=GET %-22s %s\n' "$p" "$(curl -s -o /dev/null -X POST "$@" -w '%{http_code}' "$B$p?_method=GET")"
  done
}
probe visitor
for u in author1 editor1 contrib1; do
  J=$T/$u.jar
  curl -s -c "$J" -b "$J" -o /dev/null "$B/wp-login.php"
  curl -s -c "$J" -b "$J" -o /dev/null -d "log=$u&pwd=$(case $u in author1) echo authorpass;; editor1) echo editorpass;; contrib1) echo contribpass;; esac)&wp-submit=Log+In&testcookie=1" "$B/wp-login.php"
  N=$(curl -s -b "$J" "$B/wp-admin/admin-ajax.php?action=rest-nonce")
  probe "$u (nonce $N)" -b "$J" -H "X-WP-Nonce: $N"
done
rm -rf "$T"
