pip install -r requirements.txt
python -m unittest src/test/test_remover.py > test_remover.log 2>&1

out=$(grep -c "^OK" test_remover.log)

if [ "$out" -eq "0" ]; 
  then echo $(tail test_remover.log);
  else python -m PyInstaller -F -D -n "remover" src/remover.py;
fi