import pytest
from utils import dashboard_validation as df

def test_is_afk():
    assert callable(df.is_afk), "Is afk doasn't seem like a function"
    assert df.is_afk() in (True, False)



#def test_stat_chain(query):
def test_stat_chain():
   stat_chaing.handle(query) 
