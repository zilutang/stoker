python /data/codes/stoker/updateDaily.py
python /data/codes/stoker/scoring.py
python /data/codes/stoker/mail.py

echo "score.txt" | mail -s "score.txt" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt
echo "alltoday.xlsx" | mail -s "alltoday" 184083376@qq.com -A /data/codes/stoker/resources/daily/alltoday.xlsx
