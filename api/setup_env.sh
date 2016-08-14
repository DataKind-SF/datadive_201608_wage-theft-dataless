conda create --name wage_theft_api python=2 flask sqlalchemy -yf
source activate wage_theft_api
pip install flask_restful
FLASK_APP="sql-server.py"

# requirments.txt
# python==2.7
# flask==0.11.1
# flask_restful==0.3.5
# sqlalchemy==1.0.14`