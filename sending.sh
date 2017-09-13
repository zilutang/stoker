python /data/codes/stoker/updateDaily.py
python /data/codes/stoker/scoring.py
python /data/codes/stoker/mail.py

echo "scoring for stocks" | mail -s "subject" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt
