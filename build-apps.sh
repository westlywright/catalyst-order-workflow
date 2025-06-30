cd ./services/inventory
pip3 install -r requirements.txt

cd ../notifications
pip3 install -r requirements.txt

cd ../notifications
npm install

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
