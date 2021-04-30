# soroban-csv-convert
CSV convert built with FastAPI.

This project is made for [Soroban Academy](https://akademiasorobanu.pl/) . The goal is to achieve the following points:

* FastAPI with one page with button to upload CSV file and process it
* FastAPI endpoint `/get_file` with code to process CSV file
* rewite rules hardcoded in Python:
  * delete 1st row
  * change coding for UTF-8
  * remove all `"` signs
  * change dates, from `22012/03/23` to `2012年03月23`

Example CSV input is:

```
"TEN pierwszy wiersz jest do usunecia"
"ÝĐÔ","m","Žłş","óąłş","śk","wN","śNú","ęčú","čú","ŞĚ","JĂń","","Ć","óąÔ","iÔ","ćZ","Z","ŠćZ","`[Z"
"		9999999999","AkademiaSorobanu","AkademiaSorobanu","AkademiaSorobanu","XXX Blanka","-2","2012/03/23","2021/03/28","2021/03/28","ş21-3","454","9","","1","1339","100","0","90","0"
"		9999999999","AkademiaSorobanu","AkademiaSorobanu","AkademiaSorobanu","XXX Wiktoria","-2","2012/02/14","2021/03/28","2021/03/28","ş21-3","454","9","","2","1340","100","0","80","0"
```

Example CVS output is:

```
ÝĐÔ,m,Žłş,óąłş,śk,wN,śNú,ęčú,čú,ŞĚ,JĂń,,Ć,óąÔ,iÔ,ćZ,Z,ŠćZ,`[Z
		9999999999,AkademiaSorobanu,AkademiaSorobanu,AkademiaSorobanu,XXX Blanka,-2,2012年0323,2021年03月28,2021年03月28,ş21-3,454,9,,1,1339,100,0,90,0
		9999999999,AkademiaSorobanu,AkademiaSorobanu,AkademiaSorobanu,XXX Wiktoria,-2,2012年02月14,2021年03月28,2021年03月28,ş21-3,454,9,,2,1340,100,0,80,0
```

