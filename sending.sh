/opt/anaconda2/anaconda/bin/python /data/codes/stoker/updateDaily.py
/opt/anaconda2/anaconda/bin/python /data/codes/stoker/scoring.py
/opt/anaconda2/anaconda/bin/python /data/codes/stoker/mail.py

echo "scoring" | mail -s "score system" 184083376@qq.com -A /data/codes/stoker/resources/daily/score1-today.xls -A /data/codes/stoker/resources/daily/score.txt -A /data/codes/stoker/resources/daily/all-today.xls
