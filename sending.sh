python /data/codes/stoker/updateDaily.py
python /data/codes/stoker/scoring.py
python /data/codes/stoker/mail.py

echo "今日打分，2017每日评分，每日排名" | mail -s "股票智能评分系统" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.xlsx -A /data/codes/stoker/resources/daily/score.txt -A /data/codes/stoker/resources/daily/alltoday.xlsx
