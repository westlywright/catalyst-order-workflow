cd ./services/inventory
pip3 install -r requirements.txt

cd ../notifications
pip3 install -r requirements.txt

cd ../notifications
npm install
npm run build

cd ../order-processor
pip3 install -r requirements.txt

cd ../payments
pip3 install -r requirements.txt

cd ../shipping
pip3 install -r requirements.txt

cd ../batch-processor
pip3 install -r requirements.txt

cd ../returns
pip3 install -r requirements.txt

cd ../chaos-engineer
pip3 install -r requirements.txt

cd ../saga-demo
pip3 install -r requirements.txt

cd ../agent-coordinator
pip3 install -r requirements.txt

cd ../agent-worker
pip3 install -r requirements.txt
