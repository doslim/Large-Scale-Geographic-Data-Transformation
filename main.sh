# conda activate deeplearning

nohup python -u main.py --config='./config.yaml' >> ./output_log/$(date +%m-%d-%R)_1.log 2>&1 &
# nohup python -u main.py --config='./config_2.yaml' >> ./output_log/$(date +%m-%d-%R)_2.log 2>&1 &
# nohup python -u main.py --config='./config_3.yaml' >> ./output_log/$(date +%m-%d-%R)_3.log 2>&1 &
# nohup python -u main.py --config='./config_4.yaml' >> ./output_log/$(date +%m-%d-%R)_4.log 2>&1 &
# nohup python -u main.py --config='./config_5.yaml' >> ./output_log/$(date +%m-%d-%R)_5.log 2>&1 &